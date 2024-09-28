from typing import List
from dotenv import load_dotenv
import os
from uuid import uuid4

from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
# for when we aren't using gen ai embeddings
# from langchain_core.embeddings import FakeEmbeddings
# embeddings = FakeEmbeddings(size=4096)
class MongoWrapper():
    load_dotenv()

    client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
    db_name = os.getenv("DB_NAME")
    collection_name = os.getenv("COLLECTION_NAME")
    atlas_vector_search_index_name = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    MONGODB_COLLECTION = client[db_name][collection_name]

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=gemini_embeddings,
        #index_name=atlas_vector_search_index_name,
    )

    def add_to_vector_store(self, documents: List[Document]):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)

    def retrieve_vector_store(self, query):
        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k":3, "score_threshold":0.3}
        )
        
        return retriever.invoke(query)
        





