# from langchain_community.document_loaders import UnstructuredURLLoader
# from unstructured.cleaners.core import remove_punctuation,clean,clean_extra_whitespace
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.document_loaders import SeleniumURLLoader
# from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.document_loaders import ScrapingAntLoader
from langchain_core.documents import Document
import os
from models.google import get_llm
from langchain.chains.summarize import load_summarize_chain
from db.db_operations import insert_full_text

def add_url_to_content(content, url):
    return f"Source: {url}\n{content}"

def load_web_pages(articles, connection):
    documents = []
    for article in articles:
        url = article[0]
        title = article[1]
        summary = article[2]
        full_text = article[3]

        if full_text is None or full_text.strip() == '':
            try:
                print(f"scraping {url}")
                loader = ScrapingAntLoader([url], api_key= os.getenv('SCRAPINGANT_TOKEN'))
                docs = [doc.page_content for doc in loader.lazy_load()]
                full_text = '\n'.join(docs)
            except Exception as e:
                print(e)
                print("falling back to title and summary")
                full_text = title + " "  + summary
                print(full_text)
        try:
            insert_full_text(connection, full_text, url)
        except Exception as e:
            print(e)

        metadata={'url': url, 'title': title, 'summary': summary}
        doc = Document(page_content=full_text, metadata=metadata)
        documents.append(doc)

    return documents

def summarize_web_pages(documents, model_name):
    llm = get_llm(model_name)
    
    markdown_output = ""
    summary_chain = load_summarize_chain(llm, chain_type="stuff")
    for doc in documents:
        summary = doc.metadata['summary']
        try:
            summary = summary_chain.invoke( [doc])['output_text']
        except Exception as e:
            print(e)

        markdown_output += f"## {doc.metadata['title']}\n\n"
        markdown_output += f"[Source]({doc.metadata['url']})\n\n"
        markdown_output += f'{summary}\n\n'
       
    return markdown_output