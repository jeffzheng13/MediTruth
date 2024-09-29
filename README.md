# MediTruth

<img src="frontend/img/health-photo.jpg" alt="MediTruth Logo" width="300"/>

## Inspiration
Our project was inspired by doom-scrolling. YouTube shorts, Tiktok, and Instagram reels have boomed in popularity in recent years. So has health-related content involving these short-form content. With so much misinformation, we wanted to find a way to combat this. Hence, MediTruth.

## What it does
MediTruth takes these short-form videos and extracts information being presented as facts. As such, we then validate these facts using medical journals and summarize them for you. This provides a way to educate yourself and not succumb to misinformation. 

## How we built it
We utilized LangChain and Google's Gemini LLM a bunch. We also used PubMed's API to get article data. Next the information was then split and stored in MongoDB where we can look up answers to combat or support the facts presented in the video using similarity search. The frontend was then built simply using HTML/CSS.

## Challenges we ran into
This was probably the smoothest hackathon, we've competed in. While it was mostly smooth sailing, there was some hiccups. Getting the data from PubMed was extremely difficult. A lot of the documents are not readily free and so getting the documents was difficult. This was made even harder when PubMed rate limits their API and the articles are much more technical than the average YT/TikTok video.

## Accomplishments that we're proud of
We are proud of making such an overall polished product. It performs decently well and provides good information to the user.

## What we learned
We learned how to create a full-stack application and incorporate AI. It was our first experience using a LLM and there were many struggles prompting it to get the right output.

## What's next for MediTruth
We hope to make this application even faster and perhaps being able to verify in realtime. Additionally, we want to create an extension out of it, so it doesn't require uploading a video which can be clunky. We would also like to incorporate this into mobile form somehow as well.