from fetch.fetch_feeds import get_feeds_from_opml
from fetch.fetch_interests import extract_section_from_markdown
import json
from bs4 import BeautifulSoup
from filter.filter_articles import filter_articles_by_date
from filter.filter_articles import rate_relevance

opml_file = "rss_feeds.opml"
num_days = 2
about_file = "../src/content/blog/about/index.md"
interests_section = "What"
model_name = 'mistralai/mistral-small-3.1-24b-instruct:free'
rating_prompt = "Based on my interests {interests}, rate the relevance of this article on a scale from 0 to 1, with 0 being irrelevant and 1 being very relevant.\n{format_instructions}\nTitle:{article_title} Summary:{article_summary}"
max_article_len = 500
relevancy_threshold  = 0.5

def main():
    result = get_feeds_from_opml(opml_file)
    feeds = result.feeds

    recent_articles = filter_articles_by_date(feeds, num_days)
    
    interests = extract_section_from_markdown(about_file, interests_section)
    print("number of articles in the last", num_days, "days:", len(recent_articles))
    print("rankning relevance based on:", interests)
    data = []
    for article in recent_articles:
        article_title = article.get('title', '')[:max_article_len]
        article_summary = BeautifulSoup(article.get('summary', 'No summary'), 'html.parser').get_text(separator=' ', strip=True)[:max_article_len]

        try:
            relevance = rate_relevance(interests, article_title, article_summary, model_name, rating_prompt)
            print("title:", article_title, "relevance:", relevance)
            data.append({
                'title': article_title,
                'summary': article_summary,
                'relevance': relevance,
                'link': article.get('link', ''),
                'published': article.get('published', ''),
                'updated': article.get('updated', ''),
                'created': article.get('created', '')
            })
        except Exception as e:
            print(e)
            break

    with open('articles.json', 'w') as f:
        json.dump(data, f, indent=4)
    
if __name__ == "__main__":
    main()