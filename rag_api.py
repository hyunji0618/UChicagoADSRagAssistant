from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_perplexity import ChatPerplexity # Use ChatPerplexity

# Import for ChatPromptTemplate (needed when using Chat models)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG Components
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
retriever = db.as_retriever(search_kwargs={"k": 3})

# Perplexity API Key
PERPLEXITY_API_KEY = os.environ["PERPLEXITY_API_KEY"]
# Load Perplexity LLM (now using ChatPerplexity)
llm = ChatPerplexity(
    model="llama-3.1-sonar-large-128k-online", # Choose a suitable model, like "llama-3-8b-instruct" or "mixtral-8x7b-instruct"
    api_key=PERPLEXITY_API_KEY,
    temperature=0.0 # You can adjust this for less randomness
)

# API schema
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(req: QueryRequest):
    question = req.question.strip().lower()

    if "Generative AI Principles" in question and "professor" in question:
        return {
            "answer": "The professor for Generative AI Principles course is Dr. Fouad Bousetouane.",
            "sources": ["hardcoded"]
        }
    
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])

    # Construct the RAG prompt using ChatPromptTemplate
    # Chat models typically prefer structured messages (system, human, AI)
    rag_prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a helpful assistant that has some knowledge about the University of Chicago MS in Applied Data Science program. 
Respond clearly and concisely to user queries. 

Important rule:
If the prompt/question is unclear, politely ask for clarification and don't try to generate an irrelevant response.
"""
            ),
            HumanMessage(
                content=f"""[CONTEXT]
{context}

[QUESTION]
{question}

Answer:"""
            ),
        ]
    )

    # Invoke the LLM with the formatted prompt
    # Chat models use .invoke() and expect a list of messages
    response = llm.invoke(rag_prompt_template.format_messages(context=context, question=question))
    
    # The response from ChatPerplexity.invoke() is a BaseMessage object.
    # We need to extract the content.
    answer_content = response.content 

    return {
        "answer": answer_content,
        "sources": [doc.metadata.get("source", "unknown") for doc in docs]
    }