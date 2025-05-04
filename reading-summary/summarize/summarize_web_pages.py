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


def add_url_to_content(content, url):
    return f"Source: {url}\n{content}"

def load_web_pages(articles):
    documents = []
    for article in articles:
        url = article[0]
        title = article[1]
        summary = article[2]
        print(url)
        try:
            loader = ScrapingAntLoader([url], api_key= os.getenv('SCRAPINGANT_TOKEN'))
            for doc in loader.lazy_load():
                doc = Document(page_content=add_url_to_content(doc.page_content, url), metadata={'url': url, 'title': title})
                documents.append(doc)
        except Exception as e:
            print(e)
            doc = Document(page_content=add_url_to_content(title + summary, url), metadata={'url': url, 'title': title})
            documents.append(doc)

    return documents

def summarize_web_pages(documents, model_name, input_prompt, refine_prompt):
    llm = get_llm(model_name)
    
    markdown_output = "# Summarized Articles\n\n"
    summary_chain = load_summarize_chain(llm, chain_type="stuff")
    for doc in documents:
        summary = summary_chain.invoke( [doc])['output_text']
        markdown_output += f"## {doc.metadata['title']}\n\n"
        markdown_output += f"[Source]({doc.metadata['url']})\n\n"
        markdown_output += f'{summary}\n\n'
       
    return markdown_output