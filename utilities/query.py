from langchain_experimental.llms import ChatLlamaAPI
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import GooglePalmEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
import google.generativeai as genai
from llamaapi import LlamaAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
load_dotenv()


from utilities.bard_llm import BardLLM

prompt_loader = TextLoader(file_path = "./data.txt",encoding='utf-8')
# loader = PyPDFLoader("emirdag.pdf")
index = VectorstoreIndexCreator(embedding=GooglePalmEmbeddings()).from_loaders([ prompt_loader ])


class Prompt(BaseModel):
    model:str
    message: str

def query(prompt: Prompt):

    match prompt.model:
        case 'llama-default':
            return index.query(prompt.message, llm=BardLLM())
        
        case 'bard':
            return index.query(prompt.message, llm=ChatLlamaAPI(client=LlamaAPI(api_token=os.getenv('LLAMA_API_TOKEN'))))
        
        case 'gemini-pro':
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            return index.query(prompt.message,llm=GoogleGenerativeAI( model="gemini-pro", temperature=0.3))
        
        case 'gpt-3.5-turbo':
            return index.query(prompt.message,llm= ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3))