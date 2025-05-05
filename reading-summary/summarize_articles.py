from db.db_operations import get_most_relevant_articles
from summarize.summarize_web_pages import load_web_pages, summarize_web_pages
import sqlite3
from dotenv import load_dotenv
import consts

load_dotenv()


def main():
    connection = sqlite3.connect(consts.db_name)
    # fetch web page of most relevant articles and summarize
    try:
        most_relevant_articles = get_most_relevant_articles(connection, consts.relevancy_threshold, consts.num_days_to_summarize)   
        print(f"fetching {len(most_relevant_articles)} relevant articles from the web")
 
        documents = load_web_pages(most_relevant_articles, connection)

        # summarize web pages
        print("summarizing content")
        summary = summarize_web_pages(documents, consts.model_name)
        output = consts.readings_file_start + summary
        with open(consts.readings_file, "w") as f:
            f.write(output)
    except Exception as e:
        print(e)
    
    connection.close()
    
if __name__ == "__main__":
    main()