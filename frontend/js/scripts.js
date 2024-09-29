import { createAccordionItem } from "./components.js";

function scrubVideoTo(seconds) {
    const videoUrl = document.getElementById("youtube-video").src;
    const urlWithTimestamp = `${videoUrl}?start=${seconds}`;
    document.getElementById("youtube-video").src = urlWithTimestamp;
}

function updateVideo() {
    const videoUrl = document.getElementById("video-url").value;
    const embedUrl = videoUrl.includes("watch?v=")
        ? videoUrl.replace("watch?v=", "embed/")
        : "https://www.youtube.com/embed/404";

    // Call backend to get facts, timestamps
    const data = [
        {
            timestamp: "00:00:12.689",
            fact: "Fingernails grow twice as quickly as toenails.",
            value: true,
            citation: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2565713/",
            title: "The Dynamic Skeleton",
            description:
                "This paper discusses the regeneration of bone tissue.",
        },
        {
            timestamp: "00:00:19.119",
            fact: "The human body skeleton does not regenerate.",
            value: false,
            citation: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2565713/",
            title: "The Dynamic Skeleton",
            description:
                "Over the course of 10 years, the entire human body will regenerate an entirely new skeleton.",
        },
        {
            timestamp: "00:00:32.553",
            fact: "The smallest bone in your body is the stapes.",
            value: true,
            citation: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2565713/",
            title: "The Dynamic Skeleton",
            description:
                "This paper discusses the anatomy and function of the stapes bone in the human ear.",
        },
    ];
    const parsedData = data.map((item) => {
        const timeParts = item.timestamp.split(":");
        const seconds =
            parseInt(timeParts[0]) * 3600 +
            parseInt(timeParts[1]) * 60 +
            Math.floor(parseFloat(timeParts[2]));
        return { ...item, timestamp: seconds };
    });

    const accordionContainer = document.getElementById("accordionExample");
    accordionContainer.innerHTML = parsedData
        .map((item, index) =>
            createAccordionItem(
                index,
                item.fact,
                item.description,
                item.timestamp,
                item.citation,
                item.title,
                item.value
            )
        )
        .join("");
    document.getElementById("youtube-video").src = embedUrl;
}

document.querySelectorAll(".accordion-collapse").forEach((element) => {
    element.addEventListener("shown.bs.collapse", function () {
        const seconds = element.getAttribute("data-seconds");
        scrubVideoTo(seconds);
    });
});
