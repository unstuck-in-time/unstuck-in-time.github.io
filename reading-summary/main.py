from fetch.fetch_feeds import get_feeds_from_opml
from fetch.fetch_interests import extract_section_from_markdown
from filter.filter_articles import filter_articles_by_date
from filter.filter_articles import rate_relevance
from db.db_operations import insert_articles, create_table, get_articles_to_rate, update_relevance
import sqlite3
from dotenv import load_dotenv

load_dotenv()

opml_file = "rss_feeds.opml"
db_name = "articles.db"
num_days = 2
about_file = "../src/content/blog/about/index.md"
interests_section = "What"
# model_name = 'mistralai/mistral-small-3.1-24b-instruct:free'
model_name = "gemini-1.5-flash"
rating_prompt = """
Based on my interests: {interests}
rate the relevance of each article in the list below on a scale from 0 to 1, 
with 0 being irrelevant and 1 being very relevant. 
The list of articles will be in the format: [(title1, summary1), (title2, summary2), ...]

{format_instructions}

{articles}
"""
max_article_len = 500
relevancy_threshold  = 0.5

def main():
    connection = sqlite3.connect(db_name)

    # get feeds from opml file
    result = get_feeds_from_opml(opml_file)
    feeds = result.feeds

    # get recent articles from feeds and insert them into database
    # create_table(connection)
    # recent_articles = filter_articles_by_date(feeds, num_days)
    # insert_articles(connection, recent_articles, max_article_len)

    # get articles to rate from database
    articles_to_rate = get_articles_to_rate(connection, num_days)
    articles_to_rate = articles_to_rate
    if len(articles_to_rate) > 0:
        llm_input_articles = ",".join([f"({title}, {summary})" for link, title, summary, relevance in articles_to_rate])
        llm_input_articles = f"[{llm_input_articles}]"

        # rate relevance of articles
        interests = extract_section_from_markdown(about_file, interests_section)
        relevance_list = rate_relevance(interests, llm_input_articles, model_name, rating_prompt)
        insert_data = [(score, data[0]) for data, score in zip(articles_to_rate, relevance_list)]
        update_relevance(connection, insert_data)
    
    connection.close()
    
if __name__ == "__main__":
    main()