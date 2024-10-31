# Verba-group test-task

## Библиотеки

Для работы парсера использовались библиотеки aiohttp и beautifulsoup, lxml

## Установки

Для работы скрипта необходимо развернуть виртуальное окружение: __python -m venv .venv__ и активировать его __.venv/scripts/activate__

Установить необходимые библиотеки из файла requirements.txt: __pip install -r requirements.txt__

Запустить скрипт 

## Работа скрипта

Парсер собирает информацию с сайта [__Quotes to scrape__](https://quotes.toscrape.com)

Скрипт получает html разметку сайта в функции __fetch_quotes__, после чего информация передается в функцию __collect_quotes_data__, в которой информация собирается при помощи beautifulsoup

Информация собирается в виде 

    quote = {
        'quote':'str',
        'author':{
            'author':'str',
            'born':'str',
            'location':'str',
            'description':'str',
        },
        'tags':['str']
    }

Информация о авторе собирается со страницы с подробным описанием автора, к примеру [__отсюда__](https://quotes.toscrape.com/author/J-K-Rowling/)

Получение Html разметки страницы автора происходит в функции __fetch_author__ после чего данные передаются в функцию __collect_author_data__



## Доп.информация
По каким-то причинам на моем оборудовании при парсинге выдает ошибку "__OSError: [WinError 121] Превышен таймаут семафора__", смог проблему решить только при использовании VPN 😒, при наличии прокси - можно было бы дописать использование с ним

Скрипт можно доработать и сначала собрать все следующие ссылки, а потом уже переходить к парсингу данных, но написание займет время на внедрение данной идеи

[Связаться](https://t.me/ocherednoy_p)