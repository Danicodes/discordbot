import re
import asyncio
import discord
from discord.ext import commands

# A rudimentary database
orders_database = {
    "12345": {"order_number": "12345", 
               "items": ["keychain", "screwdriver"],
               "order_date": "2023-02-15",
               "customer": "Dani",
               "status": "PROCESSING",
               "estimated_ship_date": "2023-02-23", 
               "order_total": "$58.36 USD"
               }
    , 
    "202302": {"order_number": "202302",
                "items": ["sweater", "hot cocoa"],
                "order_date": "2023-02-19",
                "customer": "Daisy",
                "status": "SHIPPED",
                "estimated_ship_date": None, 
                "ship_date": "2023-02-20",
                "estimated_delivery_date": "2023-03-01",
                "order_total": "$73.19 CAD"
                }
    }


class DecisionCog(commands.Cog):
    current_order_number = None

    def __init__(self, bot) -> None:
       self.bot = bot

       # order information 
       self.current_order_number = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.channel.name == "help_thread":
            thread = message.channel
            await self.on_help_thread_update(thread)
            return    

        if message.channel.name != "customer-help":
            # This cog will only listen on the customer channel
            return
            
        if message.mentions and 'chatbot' in map(lambda x: x.name, message.mentions):
            if "help" in message.content:
                try:
                    reply_thread = await message.create_thread(name="help_thread")
                    await reply_thread.send(f"Hello, {message.author.mention}, how can I help you today?")
                except Exception as e:
                    print(e)
                    await message.channel.send("Error creating help thread")
                    return

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        print("New thread created")
        return

    async def on_help_thread_update(self, thread: discord.Thread) -> None:
        last_message = thread.last_message
        if not last_message.content:
            return
        last_five = [message async for message in thread.history(limit=5, oldest_first=False)]

        if last_message.author.name != "chatbot": # i.e. There is a response
            # Getting context of response
            if len(last_five) > 1 and last_five[1].author.name == "chatbot":
                last_prompts = list(filter(lambda message: message.content.endswith('?') and message.author.name == 'chatbot', last_five))
                last_prompt = last_prompts[0].content if len(last_prompts) > 0 else ""
                response = last_message.content
               
                # Responding to found order request
                if "right order?" in last_prompt and response.lower() == "yes":
                    await thread.send("How can I help with this order?") 
                    return
                elif "right order?" in last_prompt and response.lower() == "no":
                    DecisionCog.current_order_number = None
                    await thread.send("Sorry about the confusion, please repeat your order number")
                    return
                elif "right order?" in last_prompt:
                    await thread.send("Please respond yes or no.")
                    return

                # Responding to 'how can I help with your order' 
                if ("How can I help" in last_prompt and "order" in last_prompt) or "anything else" in last_prompt:
                    match response.lower():
                        case "cancel":
                            await thread.send("Cancelling this order")
                            cancelled = DecisionCog.cancel(DecisionCog.current_order_number)
                            await thread.send("Successfully cancelled" if cancelled else "An error occurred") 
                            await thread.send("Is there anything else?") 
                            return
                        
                        case "expected":
                            await thread.send("Finding expected ship date")
                            ship_date = DecisionCog.expected_ship(DecisionCog.current_order_number)
                            await thread.send(f"Order expected to ship on {ship_date}")
                            await thread.send("Is there anything else?") 
                            return

                        case "items" | "get items":
                            await thread.send("Getting order items")
                            items = self.get_order_items(DecisionCog.current_order_number)
                            await thread.send("Your order includes: " + ", ".join(items))
                            await thread.send("Is there anything else?") 
                            return

                        
                        case "finished":
                            await thread.send("Have a good day!")
                            await asyncio.sleep(2)
                            await thread.delete()
                            return

                        case _:
                            await thread.send("Options: cancel, expected, items, finished")
                            return



            if "help" in last_message.content and "order" in last_message.content:
                await thread.send("What is your order id?")
                return

            if orders:= re.findall(r"\d{4,6}", last_message.content):
                order_number = orders[0]
                if not order_number:
                    await thread.send(f"Order number must be a 4 to 6 digit number")
                    return

                async with thread.typing():
                    await thread.send(f"Looking for order {order_number}")
                    order = DecisionCog.find(order_number)
                    if not order:
                        await thread.send(f"Sorry, I could not find an order with that id ({order_number})")
                        return
                    else:
                        DecisionCog.current_order_number = order_number
                        await thread.send(f"Found an order for {len(order.get('items'))} items, totalling {order.get('order_total')} placed on {order.get('order_date')}")
                        await thread.send("Is this the right order?") 
                        return
        return

    def included_order_number():
        async def pred(ctx):
            content = ctx.message.clean_content.split(' ')
            order_number = content[-1] if len(content) > 1 else None
            if not order_number:
                await ctx.send(f"Must include an order number to use command: {ctx.invoked_with}")
                return False
            return True
        return commands.check(pred)

    ### Class Methods ### 
    
    @classmethod
    def find(cls, order_number) -> dict | None:
        if match:= orders_database.get(order_number.strip(), None):
            return match
        else:
            return None
    
    @classmethod
    def get_order_items(cls, order_number) -> list | None:
        order = DecisionCog.find(order_number)
        return order.get("items") if order else None
    
    @classmethod
    def cancel(cls, order_number) -> bool:
        order = DecisionCog.find(order_number)

        try:
            # No reason this should fail, but this is the pattern you'd likely want with a real db
            order.add("cancelled", "true")
            orders_database[order_number] = order
        except Exception as e:
            print(e)
            return False # Order cannot be cancelled at the moment
    
        return True

    @classmethod
    def expected_ship(cls, order_number) -> bool:
        order = DecisionCog.find(order_number)
        return order.get("estimated_ship_date")

    ### Commands ###
        
    @commands.command(name="order_items")
    async def order_items_command(self, ctx, order_number=None):
        if not order_number:
            await ctx.send("Please include an order number")

        items = DecisionCog.get_order_items(order_number) 
        items_str = ", ".join(items)
        await ctx.send(f"Items ordered: {items_str}")

    @included_order_number()
    @commands.command(name="find_order")
    async def find_order(self, ctx, order_number=None):
        found = DecisionCog.find(order_number)
        if found:
            await ctx.send("Found your order!")
        elif not found:
            await ctx.send("Couldn't find your order")
        return



async def setup(bot):
    await bot.add_cog(DecisionCog(bot))
        
async def teardown(bot):
    await bot.remove_cog(DecisionCog(bot))
