from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/checkYTVideo', )
def checkVid():
    yt_link = request.args.get('ytlink')
    yt_regex = re.compile(r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*')

    if not yt_link:
        return jsonify({"error": "No YouTube link provided"}), 400

    if not yt_regex.match(yt_link):
        return jsonify({"error": "Invalid YouTube link"}), 400

    return jsonify({"message": "Valid YouTube link"}), 200
