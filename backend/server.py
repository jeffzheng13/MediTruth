from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from yt_to_facts import get_health_facts_from_yt_url

load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
gemini_key = os.getenv("GEMINI_API_KEY")


@app.route('/get_facts', methods=['GET'])
def get_facts():
    # /get_facts?url=https://youtube.com/id
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    data = get_health_facts_from_yt_url(url, gemini_key)

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
