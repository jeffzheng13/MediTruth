# MediTruth

<img src="frontend/img/health-photo.jpg" alt="MediTruth Logo" width="300"/>

## Inspiration

Our project was inspired by doom-scrolling. YouTube shorts, Tiktok, and Instagram reels have boomed in popularity in recent years. So has health-related content involving these short-form content. With so much misinformation, we wanted to find a way to combat this - MediTruth.

## What it does

MediTruth takes these short-form videos and extracts information being presented as facts. We then flag these facts as true or false using medical journals and provide reasoning. This provides a way to educate yourself and not succumb to misinformation.

## How we built it

We utilized LangChain and Google's Gemini LLM, and PubMed's API to get article data. Next the information was then split and stored in MongoDB where we can look up answers to combat or support the facts presented in the video using similarity search. The frontend was then built simply using HTML/CSS.

## Challenges we ran into

This was probably the smoothest hackathon we've competed in. While it was mostly smooth sailing, there was some hiccups. Getting the data from PubMed was extremely difficult. A lot of the documents are not readily free and so getting the documents was difficult. This was made even harder when PubMed rate limits their API and the articles are much more technical than the average YT/TikTok video.

## Accomplishments that we're proud of

We are proud of making such an overall polished product. It performs decently well and provides good information to the user.

## What we learned

We learned how to create a full-stack application and incorporate AI. It was our first experience using a LLM and there were many struggles prompting it to get the right output.

## What's next for MediTruth

We plan to implement real-time fact checking support so the user does not have to wait until the entire video is analyzed (facts would populate as the video played). Additionally, we would implement the software also as a Chrome extension, which reduces the clunkiness of having to copy and paste a link - the extension could recognize videos and analyze in the background whenever a page is loaded. We also plan to add support for Instagram, TikTok, and other social media platforms.
