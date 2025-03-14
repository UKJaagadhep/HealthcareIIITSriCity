from huggingface_hub import hf_hub_download
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.llms.base import LLM
from dotenv import load_dotenv
import os
import warnings
import requests
from typing import Optional, List
import pinecone #Import pinecone
from pinecone.grpc import PineconeGRPC as Pinecone_
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = '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'

# Custom GroqLLM class
class GroqLLM(LLM):
    """
    Custom LangChain LLM wrapper for Groq's API.
    """
    api_key: str
    model: str
    endpoint: str = "https://api.groq.com/openai/v1/chat/completions"

    @property
    def _llm_type(self):
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": self.model,
        }
        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            raise ValueError(f"Groq API request failed: {response.text}")
        data = response.json()
        return data["choices"][0]["message"]["content"]

class RAGGale():
    def __init__(self, GROQ_API_KEY):
        GROQ_MODEL = "llama3-8b-8192"
        self.llm = GroqLLM(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL
        )

        # Prompt template
        prompt_template = """
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context : {context}
        Question : {question}

        Provide a comprehensive response, including all relevant details, explanations, and necessary background information. Use structured formatting if needed.
        Only have new information that is not already in the user input. The information must be from our database.

        Detailed answer :
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        self.chain_type_kwargs = {"prompt": prompt}

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        index_name = "chatbot-flash"
        #Initialize pinecone.
        pc = Pinecone_(api_key=PINECONE_API_KEY)
        #pc = pinecone.Pinecone(api_key=PINECONE_API_KEY) #This is the corrected line.
        #Corrected pinecone connection.
        '''index_info = pc.describe_index(index_name)
        host_url = index_info["host"]
        index = pinecone.Index(index_name, host="https://chatbot-flash-2mcydbp.svc.aped-4627-b74a.pinecone.io") #Use the pc instance to access index.
        #self.docsearch = Pinecone(index, embeddings.embed_query, "_medical_")'''
        self.docsearch = PineconeVectorStore(
            index_name=index_name,
            embedding=embeddings,
            namespace="_medical_"
        )


    def retrieve(self, user_input):
        # RetrievalQA chain with Groq LLM
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.docsearch.as_retriever(search_kwargs={'k': 2}),
            return_source_documents=True,
            chain_type_kwargs=self.chain_type_kwargs
        )

        result = qa({"query": user_input})
        response = result["result"]
        return response
