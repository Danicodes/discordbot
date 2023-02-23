import asyncio
import aiohttp
from discord import Webhook, Embed
import requests
from bs4 import BeautifulSoup

async def monitor_event(url: str, event_name:str =None):
    """Command to return send some important data via a webhook

       A more realistic use-case may have had us create an event listener for an action on another api,
       collect some data from that and funnel it to webhook
    """
    # Get data based on event_name
    data = None
    if not event_name:
        data = get_any_data() 

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = Embed(title=data.get('title'), description=data.get('description'), 
                      url=data.get('url'))
        await webhook.send(embed=embed, username='MonitorBot')
        await session.close()
    return

def get_any_data():
    """Retrieve data from a static wikipedia page and format it for our webhook. 
    """
    
    data = {'url': 'https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors'}
    res = requests.get(data.get('url'))
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        data['title'] = soup.find_all('title')[0].get_text()
        data['description'] = soup.find_all('p')[1].get_text()
    
    return data





