from openai import OpenAI
from dotenv import load_dotenv
import os
import math
import streamlit as st

load_dotenv()
embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")
llm_model=os.getenv("OPENAI_MODEL")
question = ""

client = OpenAI()

#define cosine similarity
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot/(norm1 * norm2) if norm1 and norm2 else 0.0

#chunk text with overlap
def chunk_text_with_overlap(text, size=500, overlap=100):
    chunk_text=[]
    for i in range(0, len(text), size-overlap):
        chunk_text.append([text[i:i+size]])
    return chunk_text

#chunk the input text and embed vectors
def embedfiletext(text):
    #text = fd.getuploadedfiletext()
    if not text:
        return []
    chunk_text=chunk_text_with_overlap(text)
    chunked_text_vectors = []
    for chunk in chunk_text:
        chunk_text_embeddings = client.embeddings.create(
        model=embedding_model,
        input=chunk
        )
        chunked_text_vectors.append({
            "text":chunk,
            "embeddings": chunk_text_embeddings.data[0].embedding
        })
    return chunked_text_vectors

#embed the question
def embed_question(question):
    question_embedding = client.embeddings.create(
        model = embedding_model,
        input = question
    ).data[0].embedding
    return question_embedding

#find the cosine similarity and return results
def findanswers(file_text, question):
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = embedfiletext()
    
    chunked_text_vectors = st.session_state.embeddings

    if not chunked_text_vectors:
        return "Please upload a file"

    #question = fd.getquestion()
    question_embedding = embed_question(question)
    scores = []

    for chunked_text_vector in chunked_text_vectors:
        chunked_vector = chunked_text_vector["embeddings"]
        similarity = cosine_similarity(chunked_vector, question_embedding)
        scores.append((similarity, chunked_text_vector["text"]))

    scores.sort(key = lambda x:x[0], reverse=True)

    context = "\n\n".join(x[1] for x in scores[:3])

    response = client.responses.create(
        model = llm_model,
        input = f""" Answer the question using only the context below.
                If the answer is not found, say "Not found in document".
                Context:
                {context}
    
                 Question:
                {question}"""
    )

    return response.output_text