from datetime import date
today = date.today()
formatted_date = today.strftime('%Y-%m-%d')

opml_file = "rss_feeds.opml"
db_name = "articles.db"
about_file = "../src/content/blog/about/index.md"
readings_file = "../src/content/blog/readings/index.md"
interests_section = "What"
model_name = "gemini-1.5-flash"
num_days_to_fetch = 2
num_days_to_summarize = 7
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

readings_file_start = f"""---
title: Current Readings
description: Relevant articles from my RSS feeds summarized by AI.
date: {formatted_date}
tags:
  - about
---

This is a weekly newsletter based on my RSS feeds. I have an LLM pipeline select the most relevant articles from my feeds (based on the about page of this website) and summarize them. \n\n
"""