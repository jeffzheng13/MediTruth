var videoURL = "https://www.youtube.com/embed/404";
var videoId = videoURL.split("/").pop();
var tag = document.createElement("script");
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;

function onYouTubeIframeAPIReady() {
    videoURL = document.getElementById("video-url").value;
    console.log(videoURL);
    player = new YT.Player("player", {
        height: "315",
        width: "560",
        videoId: videoId,
        events: {
            onReady: {},
        },
    });
    console.log(player);
}

function scrubVideoTo(seconds) {
    const s = parseInt(seconds);
    player.seekTo(s, true);
    player.playVideo();
}

async function updateVideo() {
    videoURL = document.getElementById("video-url").value;
    const videoId = videoURL.slice(-11);
    const embedUrl = `https://www.youtube.com/embed/${videoId}`;

    document.getElementById("loading-indicator").style.display = "flex";
    document.getElementById("main-content").style.display = "none";

    // Call backend to get facts, timestamps
    const encodedUrl = encodeURIComponent(videoURL);
    try {
        const response = await fetch(`http://127.0.0.1:5000/check_facts?url=${encodedUrl}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
        const accordionContainer = document.getElementById("accordionExample");
        accordionContainer.innerHTML = data
            .map((item, index) =>
                createAccordionItem(
                    index,
                    item.fact,
                    item.description,
                    Math.floor(parseFloat(item.timestamp) / 1000),
                    item.citation,
                    item.title,
                    `${(item.similarity * 100).toFixed(2)}%`,
                    item.value
                )
            )
            .join("");
    } catch (error) {
        console.error("Error fetching facts:", error);
    }

    videoURL = document.getElementById("video-url").value;
    player.loadVideoById(videoId);

    document.getElementById("loading-indicator").style.display = "none";
    document.getElementById("main-content").style.display = "flex";
}

function createAccordionItem(index, fact, description, timestamp, citation, title, similarityPercentage, value) {
    if (value === "true") {
        valueColor = "green";
    } else if (value === "false") {
        valueColor = "red";
    } else {
        valueColor = "yellow";
    }

    return `<div class="accordion-item">
                <h2 class="accordion-header" id="heading${index}">
                <button
                    class="accordion-button collapsed"
                    type="button"
                    data-mdb-toggle="collapse"
                    data-mdb-target="#collapse${index}"
                    aria-expanded="false"
                    aria-controls="collapse${index}"
                    onclick="scrubVideoTo(${timestamp})">
                        <i class="fas fa-info-circle" style="color: ${valueColor}"></i>
                        <span class="ms-2">${fact}</span>
                    </button>
                </h2>
                <div
                    id="collapse${index}"
                    class="accordion-collapse collapse"
                    aria-labelledby="heading${index}"
                    data-mdb-parent="#accordionExample"
                    data-seconds="${timestamp}"
                >
                <div class="accordion-body">
                    ${description}
                    <div class="citation">
                        <a href="${citation}" target="_blank">${title}</a>
                    </div>
                    <div class="similarity">
                        Similarity: ${similarityPercentage}
                    </div>
                </div>
            </div>
        </div>`;
}
