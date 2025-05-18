from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from filter.filter_articles import get_article_date

create_table_query = '''
    CREATE TABLE IF NOT EXISTS Articles (
        link TEXT PRIMARY KEY,
        relevance REAL,
        title TEXT NOT NULL,
        summary TEXT,
        full_text TEXT,
        date INTEGER
    );
    '''
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()

def clean_text(text):
    parsed_html = BeautifulSoup(text, 'html.parser').get_text(separator=' ', strip=True)
    sanitized_text = parsed_html.encode('ascii', errors='ignore').decode('ascii')
    return sanitized_text

def insert_articles(connection, articles):
    data = []
    for article in articles:
        article_title = clean_text(article.get('title', ''))
        article_link = article.get('link', '')

        if article_title == '' or article_link == '':
            continue
        
        article_summary = clean_text(article.get('summary', ''))
        article_date = get_article_date(article)
        data.append((article_link, article_title, article_summary, int(article_date.timestamp())))
    
    cursor = connection.cursor()
    cursor.executemany("INSERT OR IGNORE INTO Articles (link, title, summary, date) VALUES (?, ?, ?, ?)", data)
    connection.commit()

def get_articles_to_rate(connection, days, max_article_len):
    cut_off = datetime.now() - timedelta(days=days)
    cut_off_timestamp = int(cut_off.timestamp())
    cursor = connection.cursor()
    cursor.execute(f"SELECT link, SUBSTR(title, 1, {max_article_len}), SUBSTR(summary, 1, {max_article_len}), relevance FROM Articles WHERE relevance IS NULL AND date > ?", (cut_off_timestamp,))
    return cursor.fetchall()

def update_relevance(connection, data):
    cursor = connection.cursor()
    cursor.executemany("UPDATE Articles SET relevance = ? WHERE link = ?", data)
    connection.commit()

def get_most_relevant_articles(connection, threshold, days):
    cut_off = datetime.now() - timedelta(days=days)
    cut_off_timestamp = int(cut_off.timestamp())
    cursor = connection.cursor()
    cursor.execute(f"SELECT link, title, summary, full_text relevance FROM Articles WHERE relevance >= ? AND date > ?", (threshold,cut_off_timestamp))
    return cursor.fetchall()

def insert_full_text(connection, full_text, link):
    cursor = connection.cursor()
    cursor.execute("UPDATE Articles SET full_text = ? WHERE link = ?", (full_text, link))
    connection.commit()