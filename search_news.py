
'''
make_report.py 를 만들 뉴스를 수집하는 파일
'''


import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Constants
NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def search_news_about_query(query, from_date='2024-07-05', sort_by='popularity'):
    """Fetch news articles based on the query."""
    params = {
        'q': query,
        'from': from_date,
        'sortBy': sort_by,
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

def process_articles(articles, limit=6):
    """Process a list of articles, extracting relevant information."""
    processed_articles = []
    for article in articles[:limit]:
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        urlToImage = article.get('urlToImage','')

        processed_articles.append({
            'title': title,
            'description': description,
            'url': url,
            'urlToImage' : urlToImage
        })
    return processed_articles

def fetch_and_process_articles(query):
    """Fetch and process articles based on a query."""
    articles = search_news_about_query(query)
    if articles:
        processed_articles = process_articles(articles)
        # make_report.py 로 간다.
        return processed_articles
    else:
        return []

