from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import pinecone 
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
import time


# get configuratuin settings
load_dotenv()
#oai_endpoint = os.getenv("OAI_ENDPOINT")
oai_key = os.getenv("OAI_KEY")


os.environ['OPENAI_API_KEY'] = oai_key



# ...................................................................

dir = 'data/'

def doc_preprocessing(directory):
    loader = DirectoryLoader(
        directory,
        glob='**/*.pdf',     # only the PDFs
        show_progress=True
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=20
    )
    docs_split = text_splitter.split_documents(docs)

    texts = [str(doc) for doc in docs_split]
    return texts


docs_split = doc_preprocessing(dir)
# ...................................................................


# Embedding documents with OpenAI
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
query_result = embeddings.embed_query("Hello world")
print(len(query_result))


# Define a function to create embeddings
# @st.cache_resource
def create_embeddings(texts):
    embeddings_list = []
    for text in texts:
        text = text.replace("\n", " ")
        res = embeddings.embed_query(text)
        embeddings_list.append(res)
    return embeddings_list

dataset = create_embeddings(docs_split)


# ...................................................................

from pinecone import Pinecone


PINECONE_API_KEY = os.getenv("PINE_CONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINE_CONE_ENV")

# initialize connection to pinecone (get API key at app.pc.io)
api_key = os.environ.get('PINECONE_API_KEY') or PINECONE_API_KEY
environment = os.environ.get('PINECONE_ENVIRONMENT') or PINECONE_ENVIRONMENT

# ...................................................................



query = "what is chronic condition?"

# create the query vector
xq = embeddings.embed_query(query)

# now query
xc = index.query(vector=xq, top_k=1, include_metadata=False)
print(xc)


for result in xc['matches']:
    print(f"{round(result['score'], 2)}: {result['metadata']['text']}")


llm = ChatOpenAI()


doc_db = embedding_db()

def retrieval_answer(query):
    qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type='stuff',
    retriever=doc_db.as_retriever(),
    )
    query = query
    result = qa.run(query)
    return result

def main():
    st.title("Question and Answering App powered by LLM and Pinecone")

    text_input = st.text_input("Ask your query...") 
    if st.button("Ask Query"):
        if len(text_input)>0:
            st.info("Your Query: " + text_input)
            answer = retrieval_answer(text_input)
            st.success(answer)

print("I am happy to be here!")

if __name__ == "__main__":
    main()

