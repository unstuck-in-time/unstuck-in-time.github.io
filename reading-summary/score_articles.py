from fetch.fetch_feeds import get_feeds_from_opml
from fetch.fetch_interests import extract_section_from_markdown
from filter.filter_articles import filter_articles_by_date
from filter.filter_articles import rate_relevance
from db.db_operations import insert_articles, create_table, get_articles_to_rate, update_relevance
import sqlite3
from dotenv import load_dotenv
import consts

load_dotenv()

def main():
    connection = sqlite3.connect(consts.db_name)
    try:
        print("fetching articles from feeds")
        # get feeds from opml file
        result = get_feeds_from_opml(consts.opml_file)
        feeds = result.feeds
        create_table(connection)

        # get recent articles from feeds and insert them into database
        recent_articles = filter_articles_by_date(feeds, consts.num_days_to_fetch)
        insert_articles(connection, recent_articles, consts.max_article_len)
    except Exception as e:
        print(e)

    # get articles to rate from database
    articles_to_rate = []
    try:
        articles_to_rate = get_articles_to_rate(connection, consts.num_days_to_fetch)
    except Exception as e:
        print(e)

    # prompt llm to rate relevance of articles
    if len(articles_to_rate) > 0:
        print(f'ranking {len(articles_to_rate)} new articles')
        # chunk articles for the llm
        articles_to_rate_chunks = [articles_to_rate[i:i + consts.article_rating_chunk_size] for i in range(0, len(articles_to_rate), consts.article_rating_chunk_size)]
        for chunk in articles_to_rate_chunks:
            llm_input_articles = ",".join([f"({title}, {summary})" for link, title, summary, relevance in chunk])
            llm_input_articles = f"[{llm_input_articles}]"

            try:
                print("getting relevancy score from llm")
                interests = extract_section_from_markdown(consts.about_file, consts.interests_section)
                relevance_list = rate_relevance(interests, llm_input_articles, consts.model_name, consts.rating_prompt)

                insert_data = [(score, data[0]) for data, score in zip(chunk, relevance_list)]
                update_relevance(connection, insert_data)
            except Exception as e:
                print(e)
    
    connection.close()
    
if __name__ == "__main__":
    main()