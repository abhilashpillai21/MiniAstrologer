import chromadb
import os
from dotenv import load_dotenv
#from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import utils
import streamlit as st
import uuid
from openai import OpenAI
import hashlib

load_dotenv()
client = OpenAI()

#create/load a Chroma client
chroma_client = chromadb.PersistentClient(path = "vectordb")

#create/get a collection
try:
    vector_collection = chroma_client.get_collection(name = "astro_collection")
except:
    vector_collection = chroma_client.create_collection(name="astro_collection", 
                                embedding_function= OpenAIEmbeddingFunction(
                                    model_name=os.getenv("OPENAI_EMBEDDING_MODEL")
                                ))

#add chunks to the collection

def findanswers(text, question):

    file_hash =  hashlib.md5(text.encode()).hexdigest()
    documents = []
    metadatas = []
    ids = []

    
    for i, document in enumerate(utils.chunk_text_with_overlap(text)):
        documents.append(document)
        metadatas.append({"source" : st.session_state.last_file})
        ids.append(f"{file_hash}_{i}")

    if "added_files" not in st.session_state:
        st.session_state.added_files = set()    
    
    if file_hash not in st.session_state.added_files:  
        vector_collection.add(
            ids = ids,
            metadatas= metadatas,
            documents = documents
        )    
        st.session_state.added_files.add(file_hash)
    
    results = vector_collection.query(
        query_texts=[question],
        n_results=5
    )

    top_chunks = list(zip(results["distances"][0], results["documents"][0]))

    context = "\n\n".join(f"""Source {i+1} : score:{score:.4f}\n{text}""" for i, (score, text) in enumerate(top_chunks))

    input=f"""You are answering questions about an uploaded document.
    Use the retrieved context as the basis for your answer.
    You should reason carefully, combine relevant parts, and explain the answer clearly in your own words.

    Rules:
    - Do not make up facts not supported by the retrieved context.
    - You may draw reasonable inferences if they are strongly supported by the context.
    - If the answer is partially supported, say what is supported and what is uncertain.
    - If the answer is not in the context, say that clearly.

    Return:
    1. A direct answer
    2. Why this answer follows from the retrieved context
    3. What is uncertain or missing, if anything
    4. The most relevant sources

    Retrieved context:
    {context}

    Question:
    {question}
    """

    response = client.responses.create(
        input=input,
        model =os.getenv("OPENAI_MODEL"),
    )

    return response.output_text, top_chunks