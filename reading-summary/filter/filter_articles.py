from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from models.open_router import ChatOpenRouter
from datetime import datetime, timedelta
from fetch.fetch_feeds import fetch_feed

class RatingResponse(BaseModel):
    value: float = Field(..., ge=0.0, le=1.0)

def rate_relevance(interests, article_title, article_summary, model_name, rating_prompt):
    llm = ChatOpenRouter(model_name=model_name)
    parser = PydanticOutputParser(pydantic_object=RatingResponse)
    prompt = PromptTemplate.from_template(rating_prompt).partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    res = chain.invoke({'interests': interests, 'article_title': article_title, 'article_summary': article_summary})
    return res.value

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

def filter_articles_by_date(feeds, days=7):
    all_articles = []
    for feed in feeds:
        url = feed.url
        print(url)
    
        parsed_feed = fetch_feed(url)
        articles = parsed_feed.entries

        cut_off = datetime.now() - timedelta(days=days)

        recent_articles = [article for article in articles if get_article_date(article) >= cut_off]
        all_articles.extend(recent_articles)

    all_articles.sort(key=lambda article: get_article_date(article), reverse=True)
    return all_articles