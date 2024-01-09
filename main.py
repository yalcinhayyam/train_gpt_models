from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from utilities.query import Prompt,query

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
    return {'model': prompt.model, 'result': query(prompt)}
