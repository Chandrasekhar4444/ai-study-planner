from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

VECTORSTORE_PATH = "vectorstore"

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )

def ask_question(question: str) -> str:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    result = qa_chain.invoke({"query": question})
    return result["result"]
