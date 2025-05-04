from fetch.fetch_feeds import get_feeds_from_opml
from fetch.fetch_interests import extract_section_from_markdown
from filter.filter_articles import filter_articles_by_date
from filter.filter_articles import rate_relevance
from db.db_operations import insert_articles, create_table, get_articles_to_rate, update_relevance, get_most_relevant_articles
from summarize.summarize_web_pages import load_web_pages, summarize_web_pages
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
max_article_len = 500
relevancy_threshold  = 0.7
article_rating_chunk_size = 10

rating_prompt = """
    Based on my interests: {interests}
    rate the relevance of each article in the list below on a scale from 0 to 1, 
    with 0 being irrelevant and 1 being very relevant. 
    The list of articles will be in the format: [(title1, summary1), (title2, summary2), ...]

    {format_instructions}

    {articles}
"""
question_prompt = """
    Please provide a summary of the following text.
    TEXT: {text}
    SUMMARY:
"""
refine_prompt = """
    Write a concise summary of the following text. 
    Separate each summary by the title of the article and include a link to the source.
    Output in markdown format.
    TEXT: {text}
"""

def main():
    connection = sqlite3.connect(db_name)
    try:
        print("fetching articles from feeds")
        # get feeds from opml file
        result = get_feeds_from_opml(opml_file)
        feeds = result.feeds
        create_table(connection)

        # get recent articles from feeds and insert them into database
        recent_articles = filter_articles_by_date(feeds, num_days)
        insert_articles(connection, recent_articles, max_article_len)
    except Exception as e:
        print(e)

    # get articles to rate from database
    articles_to_rate = []
    try:
        articles_to_rate = get_articles_to_rate(connection, num_days)
    except Exception as e:
        print(e)

    # prompt llm to rate relevance of articles
    if len(articles_to_rate) > 0:
        print(f'ranking {len(articles_to_rate)} new articles')
        # chunk articles for the llm
        articles_to_rate_chunks = [articles_to_rate[i:i + article_rating_chunk_size] for i in range(0, len(articles_to_rate), article_rating_chunk_size)]
        for chunk in articles_to_rate_chunks:
            llm_input_articles = ",".join([f"({title}, {summary})" for link, title, summary, relevance in chunk])
            llm_input_articles = f"[{llm_input_articles}]"

            try:
                print("getting relevancy score from llm")
                interests = extract_section_from_markdown(about_file, interests_section)
                relevance_list = rate_relevance(interests, llm_input_articles, model_name, rating_prompt)

                insert_data = [(score, data[0]) for data, score in zip(chunk, relevance_list)]
                update_relevance(connection, insert_data)
            except Exception as e:
                print(e)

    # fetch web page of most relevant articles
    try:
        most_relevant_articles = get_most_relevant_articles(connection, relevancy_threshold)   
        print(f"fetching {len(most_relevant_articles)} relevant articles from the web")
 
        documents = load_web_pages(most_relevant_articles)

        # summarize web pages
        print("summarizing content")
        summary = summarize_web_pages(documents, model_name, question_prompt, refine_prompt)
        with open("summary.txt", "w") as f:
            f.write(summary)
    except Exception as e:
        print(e)
    
    connection.close()
    
if __name__ == "__main__":
    main()