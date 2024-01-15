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


class Chain():  
  def __init__(self, loaders:[BaseLoader]):
     self.loaders=loaders

  def get_retrieval_QA_chain(self,llm: BaseLanguageModel,persist:bool):
    index: VectorStoreIndexWrapper = self.__create_vector_index_store(persist)
    return RetrievalQA.from_llm(
        llm=llm,
        # retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        retriever=index.vectorstore.as_retriever(),
    )
  
  def get_conversational_retrieval_chain(self,llm: BaseLanguageModel,persist:bool):
    index: VectorStoreIndexWrapper = self.__create_vector_index_store(persist)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        # retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        retriever=index.vectorstore.as_retriever(),
    )
  
  def __create_vector_index_store(self, persist:bool):
    if persist and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        if persist:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"},embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")).from_loaders(self.loaders)
        else:
            index = VectorstoreIndexCreator(embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")).from_loaders(self.loaders)
    
    return index
  
class ChainFactory():
    def __init__(self, llm:str) -> None:
       match llm:
          case "gpt-3.5-turbo":
            self.llm = ChatOpenAI(model= "gpt-3.5-turbo",temperature= 0.3)
            pass
          case "gpt-4":
            self.llm = ChatOpenAI(model= "gpt-4",temperature= 0.3)
            pass
          case "gemini-pro":
            genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))
            self.llm = ChatGoogleGenerativeAI(convert_system_message_to_human= True, model= "gemini-pro",temperature= 0.3)
            pass
          case "llama-default":
            token = os.getenv('LLAMA_API_TOKEN')
            self.llm = ChatLlamaAPI(client=LlamaAPI(api_token= token))
            pass
          case "bard":
            self.llm = BardLLM()
            pass
    
    def create_conversational_retrieval_chain(self, persist:bool, loaders:[BaseLoader]):
      return Chain(loaders= loaders).get_conversational_retrieval_chain(llm= self.llm,persist= persist)

    def create_retrieval_QA_chain(self, persist:bool, loaders:[BaseLoader]):
      return Chain(loaders= loaders).get_retrieval_QA_chain(llm= self.llm,persist= persist)



# chain = ChainFactory("gpt-3.5-turbo").create_retrieval_QA_chain(False,loaders=[TextLoader("./data/isg.txt")])
# # question = "Ali' nin verdiği borcun faiz oranı %10 dur, Ali kendi parasının üstünde borç veremez, Veli borcunu 2 ay içinde geri ödemeli"
# question = """
# İşyerlerinde havalandırma kaç şekilde yapılır?

# a. 1

# b. 2

# c. 5

# d. 4

# e. 3

# """


# # question = """
# # Ali, Veli'den aylık %4.42 faiz oranıyla 3 yıllığına 3 TL borç aldı.  
# # Daha sonra, yıllık %10 faizle elindeki tüm parayı bankaya yatırdı. 
# # 3 yıl sonra bakadan bu parayı çekip daha sonra Ali Veliye borcunu ödediği zaman Ali'nin net karı ne kadar olacaktır?
# # """




# # question = "Ali ve Veli de kaçar tl var?"
# result = chain.run(question)
# # result = chain.run({'question':question,'chat_history':[] })

# print(result)



# # from langchain.prompts import PromptTemplate
# # from langchain.chains.question_answering import load_qa_chain

# # prompt_template = """
# #   Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
# #   provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
# #   Context:\n {context}?\n
# #   Question: \n{question}\n

# #   Answer:
# # """

# # prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])


# # from langchain_google_genai import ChatGoogleGenerativeAI
# # model = ChatGoogleGenerativeAI(model="gemini-pro",
# #                              temperature=0.3)

     

# # chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
     

# # response = chain(
# #     {"input_documents":docs, "question": question}
# #     , return_only_outputs=True)