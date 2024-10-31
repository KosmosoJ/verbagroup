from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json
import random


headers = {
    "Accepts": "application/json",
}

quotes = {"quotes": []}


async def fetch_quotes(path=None):
    """Получение информации о цитатах

    Args:
        path (str, optional): Относительный путь до определнной страницы с цитатами. Defaults to None.

    Returns:
        str: Тело ответа после запроса к сайту
    """
    url = f'https://quotes.toscrape.com{path if path else ""}'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_author(path):
    """Получение страницы автора

    Args:
        path (str): Относительный путь к странице автора

    Returns:
        str: Тело ответа после запроса к сайту
    """
    url = f"https://quotes.toscrape.com{path}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()


async def collect_author_data(data):
    """Сбор информации о авторе

    Args:
        data (str): HTML файл с /author/author-name

    Returns:
        dict: Словарь с полученной информацией о авторе
    """
    soup = BeautifulSoup(data, "lxml")
    author_info = {
        "author": soup.find("h3", "author-title").text,
        "born": soup.find("span", "author-born-date").text,
        "location": soup.find("span", "author-born-location").text[2:].strip(),
        "description": soup.find("div", "author-description").text,
    }
    return author_info


async def save_to_json(data):
    """Сохранение информации в JSON

    Args:
        data (dict): Информация о полученных цитатах
    """
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


async def get_next_link(data):
    """Получение ссылки на следующую страницу цитат

    Args:
        data (str): HTML файл

    Returns:
        str: Возвращает относительную ссылку на следующие цитаты
    """
    soup = BeautifulSoup(data, "lxml")

    try:
        new_link = soup.find("li", "next").find("a", href=True)[
            "href"
        ]  # Получение ссылки для новой страницы
    except AttributeError:
        new_link = None

    return new_link


async def collect_quotes_data(data):
    """Сбор информации об цитатах

    Args:
        data (str): Html файл
    """
    soup = BeautifulSoup(data, "lxml")

    raw_quotes = soup.find_all("div", "quote")  # Поиск всех цитат на странице

    try:
        new_link = soup.find("li", "next").find("a", href=True)[
            "href"
        ]  # Получение ссылки для новой страницы
    except AttributeError:
        new_link = None

    quotes_list = []
    for raw_quote in raw_quotes:
        raw_author_data = await fetch_author(
            raw_quote.find("a", href=True)["href"]
        )  # Получение ссылки на автора
        author_data = await collect_author_data(
            raw_author_data
        )  # Получение информации о авторе с /author/author-name

        quote = {
            "quote": raw_quote.find("span", "text").text,
            "author": author_data,
            "tags": [tag.text for tag in raw_quote.find_all("a", "tag")],
        }  # Создание словаря для цитаты
        quotes_list.append(quote)

    quotes["quotes"].append(
        quotes_list
    )  # Сохранение полученных цитат в словарь для дальнейшей записи в JSON


async def main():
    path_link = ""
    count = 1

    while True:
        if path_link is None:
            break

        html = await fetch_quotes(path_link)  # Получение HTML с сайта
        path_link = await get_next_link(html)  # Получение ссылки на следующую страницу
        await collect_quotes_data(html)  # Получение информации о цитатах
        print(f"Страница {count} пройдена")
        count += 1

    await save_to_json(quotes)


if __name__ == "__main__":
    asyncio.run(main())
