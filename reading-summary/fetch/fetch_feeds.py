import listparser
import feedparser
def get_feeds_from_opml(opml_file):
    with open(opml_file) as f:
        return listparser.parse(f.read())

def fetch_feed(feed_url):
    return feedparser.parse(feed_url)