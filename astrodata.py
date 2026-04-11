import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./chromadb"))
astro_collection = client.create_collection("asto_collection")

def getcollection()->chromadb.Collection:
    return astro_collection



