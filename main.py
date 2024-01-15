from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from utilities.chain_factory import ChainFactory
from utilities.index_factory import IndexFactory
from utilities.prompt import Prompt
from langchain.document_loaders.text import TextLoader 
# from langchain.document_loaders.json_loader import JSONLoader

loader = TextLoader(file_path = "./data/hastaliklar.json")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "localhost:3000",
    "localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/ask')
def ask(prompt:  Prompt):
    return {'model': prompt.model, 'result': IndexFactory([loader]).query(prompt.message,prompt.model)}

@app.post('/rag')
def with_rag(prompt:  Prompt):
    return {'model': prompt.model, 'result': ChainFactory(prompt.model).create_retrieval_QA_chain(False,[loader]).run(prompt.message)}
