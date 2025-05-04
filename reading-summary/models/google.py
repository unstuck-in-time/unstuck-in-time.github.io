from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(model_name):
    return ChatGoogleGenerativeAI(
        model=model_name
    )