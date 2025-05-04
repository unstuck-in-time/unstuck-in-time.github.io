from fetch.fetch_feeds import get_feeds_from_opml, fetch_feed, get_filtered_articles
import json
from bs4 import BeautifulSoup


opml_file = "rss_feeds.opml"

def main():
    articles = get_filtered_articles(opml_file, 2)
    output_data = []
    for article in articles:
        output_data.append({
            'title': article.get('title', 'No title'),
            'summary': BeautifulSoup(article.get('summary', 'No summary'), 'html.parser').get_text(separator=' ', strip=True),
            'link': article.get('link', 'No link'),
            'published': article.get('published', 'No date'),
            'updated': article.get('updated', 'No date'),
            'created': article.get('created', 'No date')
        })
    with open('articles.json', 'w') as f:
        json.dump(output_data, f, indent=4)
    # print(test_article.keys())
    # print(test_article['title'])
    # print(test_article['summary'])
    # print(test_article['link'])
    # print(test_article['description'])
    # print(type(test_article['published']))
    # print(type(test_article['published_parsed']))


if __name__ == "__main__":
    main()