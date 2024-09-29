from typing import List, Tuple
import os
from uuid import uuid4

from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# for when we aren't using gen ai embeddings
# from langchain_core.embeddings import FakeEmbeddings
# embeddings = FakeEmbeddings(size=4096)
class MongoWrapper():
    client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
    db_name = os.getenv("DB_NAME")
    collection_name = os.getenv("COLLECTION_NAME")
    atlas_vector_search_index_name = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    MONGODB_COLLECTION = client[db_name][collection_name]

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=gemini_embeddings,
        index_name=atlas_vector_search_index_name,
    )

    #splits documents returned from PubMedAPIWrapper
    def _text_split(self, paper):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 200, length_function=len)
        return text_splitter.split_documents(paper)

    #checks if document already exists
    def _check_doc_exists(self, doc: Document) -> bool:
        if not doc.metadata: 
            return False
        
        docTitle = doc.metadata["Title"]
        if self.MONGODB_COLLECTION.find_one({"Title": docTitle}):
            return True

        return False

    def add_to_vector_store(self, documents: List[Document]) -> None:
        # using document title as unique identifier
        unadded_docs = []
        for doc in documents:
            if self._check_doc_exists(doc):
                continue
            else:
                unadded_docs.append(doc)
                
        documents = self._text_split(unadded_docs)
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)

    def retrieve_vector_store(self, query) -> List[Tuple[Document, float]]:
        # retriever = self.vector_store.as_retriever(
        #     search_type="similarity_score_threshold",
        #     search_kwargs={"k":1, "score_threshold":0.3}
        # )
        
        # return retriever.invoke(query)
        results = self.vector_store.similarity_search_with_score(query, k=3)
        # filtering by 0.5
        results = [results for _, score in results if score >= 0.5]

        return results





