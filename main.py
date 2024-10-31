from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def fetch_quotes(path = None):
    url = f'https://quotes.toscrape.com{path}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def fetch_author(path):
    url = f'https://quotes.toscrape.com{path}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def collect_write_author_data(data):
    ...
        
async def collect_quotes_data(data):
    quotes = {}
    soup = BeautifulSoup(data, 'lxml')
    raw_quotes = soup.find_all('div','quote') # Поиск всех цитат на странице
    
    new_link = soup.find('li','next') # Получение ссылки для новой страницы
    quotes_list = []
    for raw_quote in raw_quotes:
        raw_author = raw_quote.find('small', 'author')
        author_data = await fetch_author() 
        
        quote = {'quote':raw_quote.find('span', 'text').text,
                 'author':raw_author.text,
                 'tags':[tag.text for tag in raw_quote.find_all('a', 'tag')]}
        
        quotes_list.append(quote)
        
    
    
async def main():
    quotes = {}
    html = await fetch_quotes()
    
    await collect_quotes_data(html)

if __name__ == '__main__':
    asyncio.run(main())