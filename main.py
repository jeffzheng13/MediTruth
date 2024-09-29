from yt_to_facts import get_health_facts_from_yt_url
from pubmed import CustomPubMedAPIWrapper
from connectMongo import MongoWrapper

from dotenv import load_dotenv
import os
import time
from langchain_community.utilities.pubmed import PubMedAPIWrapper

load_dotenv()
facts = get_health_facts_from_yt_url("https://www.youtube.com/watch?v=KPh-qbnWoBA&t=4s", os.getenv("GOOGLE_API_KEY"))

wrapper = CustomPubMedAPIWrapper()
wrapper2 = PubMedAPIWrapper()
wrapper2.base_url_efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?sort=relevance&"
wrapper2.base_url_esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?sort=relevance&"
wrapper2.sleep_time = 0.5

mongo_conn = MongoWrapper()
for info in facts[0:1]:
    terms = info["search_terms"]
    #uncomment to add more docs to database
    # try: 
    #     docIterator = wrapper.load_docs(terms)
    #     time.sleep(2)
    #     docIterator2 = wrapper2.load_docs(terms)
    #finally:
        #mongo_conn.add_to_vector_store(docIterator)
        #mongo_conn.add_to_vector_store(docIterator2)
    print(terms)
    print(info["fact"])
    print(mongo_conn.retrieve_vector_store(info["fact"]))
    