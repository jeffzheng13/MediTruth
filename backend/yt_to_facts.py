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
        [
            {
                "timestamp": 12689,
                "fact": "Fingernails grow twice as quickly as toenails.",
                "search_terms": "fingernails, toenails, growth"
            },
            {
                "timestamp": 19119,
                "fact": "Over the course of 10 years, the entire human body will regenerate an entirely new skeleton.",
                "search_terms": "skeleton, regeneration, human body"
            },
            {
                "timestamp": 32553,
                "fact": "The smallest bone in your body is the stapes.",
                "search_terms": "smallest bone, stapes, body"
            }
        ]
        Here is the the input transcript data:
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

        if json3_urls == []:
            return {}

        captions = requests.get(json3_urls[0]).json()

        word_timestamps = {}
        for event in captions['events']:
            if 'segs' in event:
                base_timestamp = event['tStartMs']
                for seg in event['segs']:
                    word_timestamp = base_timestamp + seg.get('tOffsetMs', 0)
                    word = seg['utf8'].replace('\n', '').strip()
                    if word:
                        word_timestamps[word_timestamp] = word

    # 2. setup gemini and prompt
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    print(facts_prompt + json.dumps(word_timestamps, indent=4))

    # topic_response = model.generate_content(
    #     topic_prompt.format(data=json.dumps(word_timestamps, indent=4)),
    #     generation_config={"temperature": temperature})

    facts_response = model.generate_content(
        facts_prompt + json.dumps(word_timestamps, indent=4),
        generation_config={"temperature": temperature},
        safety_settings=safety_settings)

    start = facts_response.text.find('[')
    end = facts_response.text.rfind(']')
    if start == -1 or end == -1:
        raise Exception("Invalid response from model: " + facts_response.text)
    cleaned_facts_response = facts_response.text[start:end+1]

    facts_dict = json.loads(cleaned_facts_response)
    return facts_dict


# load_dotenv()
# data = get_health_facts_from_yt_url(
#     "https://www.youtube.com/watch?v=KPh-qbnWoBA", os.getenv("GEMINI_KEY"), 0)
# with open('output.json', 'w') as outfile:
#     json.dump(data, outfile, indent=4)
