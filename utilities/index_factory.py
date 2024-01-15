import os

from langchain.document_loaders.base import BaseLoader
from utilities.bard_llm import BardLLM
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
# from langchain.document_loaders import DirectoryLoader, TextLoader,JSONLoader
from langchain_experimental.llms import ChatLlamaAPI
from llamaapi import LlamaAPI
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores.chroma import Chroma
import dotenv
# from langchain.chat_models.openai import ChatOpenAI
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.base_language import BaseLanguageModel
from langchain_openai import ChatOpenAI
dotenv.load_dotenv()


class IndexFactory():
    def __init__(self, loaders: [BaseLoader]) -> None:
        self.index =  VectorstoreIndexCreator(embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")).from_loaders(loaders)

    def query(self, question: str, model: BaseLanguageModel):
        return self.index.query(question, llm=self.create(model))

    def create(self, model: BaseLanguageModel):
        match model:
            case "gpt-3.5-turbo":
                return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
            case "gpt-4":
                return ChatOpenAI(model="gpt-4", temperature=0.3)
            case "gemini-pro":
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                return ChatGoogleGenerativeAI(convert_system_message_to_human=True,model="gemini-pro", temperature=0.3)
            case "llama-default":
                token = os.getenv('LLAMA_API_TOKEN')
                return ChatLlamaAPI(client=LlamaAPI(api_token=token))
            case "bard":
                return BardLLM()
