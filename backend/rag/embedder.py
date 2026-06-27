from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

VECTORSTORE_PATH = "vectorstore"

def embed_document(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_PATH
    )
    vectorstore.persist()
    return f"✅ Embedded {len(chunks)} chunks from {os.path.basename(file_path)}"


def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )