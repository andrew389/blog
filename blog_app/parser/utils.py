import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from .models import News
from env_config.config import PARSER_URL


def fetch_news(page=1):
    url = f'{PARSER_URL}?p={page}'
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    titles = soup.find_all('span', class_='titleline')
    ages = soup.find_all('span', class_='age')

    for title, age in zip(titles, ages):
        title_tag = title.find('a')
        age_tag = age.find('a')
        if title_tag and age_tag:
            title_text = title_tag.text
            link = title_tag['href']
            time_ago = age_tag.text

            if 'day' in time_ago or 'hour' in time_ago or 'minute' in time_ago:
                if 'day' in time_ago:
                    days = int(time_ago.split()[0])
                else:
                    days = 0

                if 'hour' in time_ago:
                    hours = int(time_ago.split()[0])
                else:
                    hours = 0

                if 'minute' in time_ago:
                    minutes = int(time_ago.split()[0])
                else:
                    minutes = 0

                time_passed = timedelta(days=days, hours=hours, minutes=minutes)
                if time_passed < timedelta(days=1):
                    news_items.append({
                        'title': title_text,
                        'link': link,
                        'time_ago': time_ago
                    })
    return news_items


def fetch_and_save_news():
    all_news = []
    page = 1
    while True:
        html = fetch_news(page)
        news = parse_news(html)
        if not news:
            break
        all_news.extend(news)

        soup = BeautifulSoup(html, 'html.parser')
        more_link = soup.find('a', class_='morelink')
        if not more_link:
            break

        page += 1

    for item in all_news:
        existing_news = News.objects.filter(link=item['link']).first()
        if existing_news:
            existing_news.time_ago = item['time_ago']
            existing_news.save()
        else:
            News.objects.create(
                title=item['title'],
                link=item['link'],
                time_ago=item['time_ago']
            )
