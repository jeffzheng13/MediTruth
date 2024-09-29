from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from yt_to_facts import get_health_facts_from_yt_url
from pubmed import CustomPubMedAPIWrapper
from connectMongo import MongoWrapper
from factCheck import fact_check
import re

load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
gemini_key = os.getenv("GEMINI_API_KEY")

@app.route('/health_check', methods=["GET"])
def health_check():
    return jsonify({"msg": "API running"}), 200

@app.route('/check_facts', methods=['GET'])
# /check_facts?url=https://youtube.com/id
def check_facts():
    url = request.args.get('url')
    yt_regex = re.compile(r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*')
    if not url:
        return jsonify({"error": "No YouTube link provided"}), 400

    if not yt_regex.match(url):
        return jsonify({"error": "Invalid YouTube link"}), 400


    facts = get_health_facts_from_yt_url(url, gemini_key)

    wrapper = CustomPubMedAPIWrapper()
    mongo_conn = MongoWrapper()

    result = []

    for fact in facts:
        terms = fact["search_terms"]
        try: 
            docIterator = wrapper.load_docs(terms)
            mongo_conn.add_to_vector_store(docIterator)
        except Exception as e:
            pass

        research_data = mongo_conn.retrieve_vector_store(fact["fact"])
        output = fact_check(research_data, fact["fact"], gemini_key=gemini_key, temperature=0)
        combined_result = {**fact, **output}
        result.append(combined_result)

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
