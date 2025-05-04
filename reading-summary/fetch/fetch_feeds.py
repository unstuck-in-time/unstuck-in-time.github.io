import listparser
import feedparser
from datetime import datetime, timedelta

def get_feeds_from_opml(opml_file):
    with open(opml_file) as f:
        return listparser.parse(f.read())

def fetch_feed(feed_url):
    return feedparser.parse(feed_url)

def time_struct_to_dt(t_struct):
    if isinstance(t_struct, datetime):
        return t_struct
    
    dt_from_struct = datetime(
            year=t_struct.tm_year,
            month=t_struct.tm_mon,
            day=t_struct.tm_mday,
            hour=t_struct.tm_hour
        )
    return dt_from_struct

def get_article_date(article):
    if 'published_parsed' in article:
        return time_struct_to_dt(article['published_parsed'])
    elif 'updated_parsed' in article:
        return time_struct_to_dt(article['updated_parsed'])
    elif 'created_parsed' in article:
        return time_struct_to_dt(article['created_parsed'])
    else:
        return datetime.now()

def get_filtered_articles(opml_file, days=7):
    result = get_feeds_from_opml(opml_file)
    feeds = result.feeds
    all_articles = []
    for feed in feeds:
        url = feed.url
        print(url)
        parsed_feed = fetch_feed(url)
        articles = parsed_feed.entries

        cut_off = datetime.now() - timedelta(days=days)

        recent_articles = [article for article in articles if get_article_date(article) >= cut_off]
        all_articles.extend(recent_articles)

    all_articles.sort(key=lambda article: get_article_date(article), reverse=False)
    return all_articles