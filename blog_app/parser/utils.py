import logging
from typing import List

import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from .models import News
from env_config.config import PARSER_URL

# Configure logging to write errors to a file named news_parser.log
logging.basicConfig(filename='news_parser.log', level=logging.ERROR)


def fetch_news(page=1):
    """
    Fetch news from the specified page of the news source.

    Args:
        page (int): The page number to fetch. Default is 1.

    Returns:
        str: The HTML content of the fetched page, or None if an error occurred.
    """
    try:
        url = f'{PARSER_URL}?p={page}'
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch news from {url}: {e}")
        return None


def parse_news(html) -> List:
    """
    Parse the HTML content to extract news items.

    Args:
        html (str): The HTML content to parse.

    Returns:
        list: A list of dictionaries containing news item details, or an empty list if an error occurred or no news items were found.
    """
    if not html:
        return []  # Return an empty list if HTML content is None

    try:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = []

        # Find elements containing titles and time information
        titles = soup.find_all('span', class_='titleline')
        ages = soup.find_all('span', class_='age')

        for title, age in zip(titles, ages):
            title_tag = title.find('a')
            age_tag = age.find('a')
            if title_tag and age_tag:
                title_text = title_tag.text
                link = title_tag['href']
                time_ago = age_tag.text

                # Check the publication time of the news
                if 'day' in time_ago or 'hour' in time_ago or 'minute' in time_ago:
                    days = int(time_ago.split()[0]) if 'day' in time_ago else 0
                    hours = int(time_ago.split()[0]) if 'hour' in time_ago else 0
                    minutes = int(time_ago.split()[0]) if 'minute' in time_ago else 0

                    # Calculate the elapsed time since publication
                    time_passed = timedelta(days=days, hours=hours, minutes=minutes)
                    if time_passed < timedelta(days=1):  # Filter news within the last 24 hours
                        news_items.append({
                            'title': title_text,
                            'link': link,
                            'time_ago': time_ago
                        })
        return news_items  # Return the list of news items
    except Exception as e:
        logging.error(f"Failed to parse news: {e}")
        return []  # Return an empty list if there is an error


def fetch_and_save_news():
    """
    Fetch and parse news from the source, and save or update the news items in the database.
    """
    all_news = []
    page = 1
    while True:
        html = fetch_news(page)
        if not html:
            break  # Exit the loop if no HTML content is returned

        news = parse_news(html)
        if not news:
            break  # Exit the loop if no news items are parsed

        all_news.extend(news)

        soup = BeautifulSoup(html, 'html.parser')
        more_link = soup.find('a', class_='morelink')
        if not more_link:
            break  # Exit the loop if there is no 'more' link to the next page

        page += 1

    # Save or update news items in the database
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
