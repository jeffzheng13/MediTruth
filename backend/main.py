from yt_to_facts import get_health_facts_from_yt_url
from pubmed import CustomPubMedAPIWrapper
from connectMongo import MongoWrapper
from factCheck import fact_check

from dotenv import load_dotenv
import os
import time
from langchain_community.utilities.pubmed import PubMedAPIWrapper

def main():
    load_dotenv()
    facts = get_health_facts_from_yt_url("https://www.youtube.com/watch?v=KPh-qbnWoBA&t=4s", os.getenv("GEMINI_API_KEY"))
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    print(facts)
    wrapper = CustomPubMedAPIWrapper()

    mongo_conn = MongoWrapper()
    for info in facts[1:2]:
        terms = info["search_terms"]
        try: 
            docIterator = wrapper.load_docs(terms)
            # If there are documents to add to the vector store
            if len(docIterator) > 0:
                mongo_conn.add_to_vector_store(docIterator)
                print("Data added to vector store")
            else:
                print("No data found for search terms")
        except Exception as e:
            print(e)
            pass
            
        print(terms)
        print(info["fact"])
        research_data = mongo_conn.retrieve_vector_store(info["fact"])
        print(research_data)

        faxsfr = fact_check(research_data, info["fact"], gemini_key=os.getenv("GEMINI_KEY"), temperature=0)
        print(faxsfr)



if __name__ == "__main__":
    main()
    