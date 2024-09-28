from util import ms_to_hmsms
from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import yt_dlp
import requests
import re

topic_prompt = """
        You are tasked with taking a JSON input with Youtube transcript data and returning a paragraph summary of the topics covered in the video, of about 4-6 sentences. Only mention the health related topics in the video. If the video does not contain any health-related topics, return an empty string.
        {data}
    """

facts_prompt = """
        You are tasked with taking a JSON input with Youtube transcript data and extract only the health-related facts that can be verified as either true or false. Exclude any facts that are not directly related to health or health sciences (e.g., facts about non-health-related history, politics, or general knowledge). Present the health facts in a way that is self-explanatory and does not require additional context from the original text, do not include any phrases that reference the video - replace any instance of 'it' with the actual thing. Avoid including opinions, subjective statements, or descriptive language that cannot be empirically verified, such as words like often, important, better, good, bad, typically, effective, critical, or beneficial. Avoid duplicate facts, if they have already been generated. If the transcript contains no health-related facts, return ONLY an empty dictionary. Your output should be JSON format, with key-value pairs that look like this:
        "00:00:00.659": "Fact 1",
        "00:00:01.659": "Fact 2",
        "00:00:02.020": "Fact 3",
        Here is the input:
        {data}
    """

safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
}


def get_health_facts_from_yt_url(url: str, gemini_key: str, temperature: int = 0, ):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
    }

    # 1. read transcript data
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        automatic_captions: dict = info_dict['automatic_captions']
        subtitles: dict = info_dict['subtitles']
        combined_captions = {**automatic_captions, **subtitles}
        combined_captions = {k: v for k,
                             v in combined_captions.items() if 'en' in k}
        combined_captions = [v[0] for v in combined_captions.values()]

        json3_captions = [x for x in combined_captions if x['ext'] == 'json3']
        json3_urls = [x['url'] for x in json3_captions]

        captions = requests.get(json3_urls[0]).json()

        word_timestamps = {}
        for event in captions['events']:
            if 'segs' in event:
                base_timestamp = event['tStartMs']
                for seg in event['segs']:
                    word_timestamp = base_timestamp + seg.get('tOffsetMs', 0)
                    word = seg['utf8'].replace('\n', '').strip()
                    if word:
                        word_timestamps[ms_to_hmsms(word_timestamp)] = word

    # 2. setup gemini and prompt
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    topic_response = model.generate_content(
        topic_prompt.format(data=json.dumps(word_timestamps, indent=4)),
        generation_config={"temperature": temperature})

    facts_response = model.generate_content(
        facts_prompt.format(data=json.dumps(word_timestamps, indent=4)),
        generation_config={"temperature": temperature},
        safety_settings=safety_settings)

    matches = re.match(r'\{[^{}]*?(?:\n[^{}]*?)*\}', facts_response.text)
    if not matches:
        raise Exception("Invalid response from model: " + facts_response.text)

    cleaned_facts_response = matches.group(0)
    facts_dict = json.loads(cleaned_facts_response)
    response = {'topics': topic_response.text, 'facts': facts_dict}
    return response
