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

#load_dotenv()
client = OpenAI()

#create/load a Chroma client
chroma_client = chromadb.PersistentClient(path = "vectordb")

#create/get a collection
try:
    vector_collection = chroma_client.get_collection(name = "astro_collection")
except:
    vector_collection = chroma_client.create_collection(name="astro_collection", 
                                embedding_function= OpenAIEmbeddingFunction(
                                    api_key=os.getenv("OPENAI_API_KEY"), #switch off in local copy
                                    model_name=os.getenv("OPENAI_EMBEDDED_MODEL")
                                ))

#add chunks to the collection

def findanswers(text, question):

    file_hash =  hashlib.md5(text.encode()).hexdigest()
    documents = []
    metadatas = []
    ids = []

    
    for i, document in enumerate(utils.chunk_text_with_overlap(text)):
        documents.append(document)
        metadatas.append({"source" : st.session_state.last_file,
                          "file_hash": str(file_hash)})
        ids.append(f"{file_hash}_{i}")

    if not documents:
        return "No readable text found in the uploaded file.", []

    if "added_files" not in st.session_state:
        st.session_state.added_files = set()    
    
    if file_hash not in st.session_state.added_files:  
        vector_collection.upsert(
            ids = ids,
            metadatas= metadatas,
            documents = documents
        )    
        st.session_state.added_files.add(file_hash)
    
    results = vector_collection.query(
        query_texts=[question],
        n_results=5,
        where={"file_hash": file_hash}
    )

    top_chunks = list(zip(results["distances"][0], results["documents"][0]))

    context = "\n\n".join(f"""Source {i+1} : score:{distance:.4f}\n{text}""" for i, (distance, text) in enumerate(top_chunks))

    input=f"""You are answering questions about an uploaded document.
    Use the retrieved context as the basis for your answer.
    You should reason carefully, combine relevant parts, and explain the answer clearly in your own words.

    Rules:
    - Do not make up facts not supported by the retrieved context.
    - You may draw reasonable inferences if they are strongly supported by the context.
    - If the answer is partially supported, say what is supported and what is uncertain.
    - If the answer is not in the context, say that clearly.
    - You can use Jaimini, Parashari, Varahi intrepretation but strictly use the data in the retrieved content without adding anything from outside.
    - The retrieved content may not explicity state certain inferences which can be made by studying the birthcharts. 
    - You must use astrological reasoning to infer that from the retrieved content. 
    - If content doesnt have the data required to make the inference, state so.

    Return without any headings:
    1. A direct answer. Answer should be complete not generic
    2. If anything is uncertain or missing, then state so
    3. Methodology and data used

    Retrieved context:
    {context}

    Question:
    {question}
    """

    response = client.responses.create(
        input=input,
        model =os.getenv("OPENAI_API_MODEL"),
    )

    return response.output_text, top_chunks