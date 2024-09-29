let player;

// Load the IFrame Player API code asynchronously.
const tag = document.createElement("script");
tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// Replace the 'youtube-video' element with an <iframe> and YouTube player after the API code downloads.
function onYouTubeIframeAPIReady() {
    player = new YT.Player("youtube-video", {
        events: {
            onReady: onPlayerReady,
        },
    });
}

function onPlayerReady(event) {
    // Player is ready
}

function scrubVideoTo(seconds) {
    if (player && player.seekTo) {
        player.seekTo(seconds, true);
        player.playVideo();
    } else {
        console.error("YouTube player is not initialized.");
    }
}

function createAccordionItem(
    id,
    fact,
    description,
    seconds,
    citation,
    title,
    similarity,
    isTrue
) {
    const iconClass = isTrue ? "fa-check-circle" : "fa-times-circle";
    const iconColor = isTrue ? "green" : "red";
    return `
      <div class="accordion-item">
        <h2 class="accordion-header" id="heading${id}">
          <button
            class="accordion-button collapsed"
            type="button"
            data-mdb-toggle="collapse"
            data-mdb-target="#collapse${id}"
            aria-expanded="false"
            aria-controls="collapse${id}"
            onclick="handleAccordionClick(${seconds})"
          >
            <i class="fas ${iconClass}" style="color: ${iconColor}"></i>
            <span class="ms-2">${fact}</span>
          </button>
        </h2>
        <div
          id="collapse${id}"
          class="accordion-collapse collapse"
          aria-labelledby="heading${id}"
          data-mdb-parent="#accordionExample"
          data-seconds="${seconds}"
        >
          <div class="accordion-body">
            ${description}
            <div class="citation">
              <a href="${citation}" target="_blank">${title}</a>
            </div>
            <div class="similarity">
              Confidence: ${similarity}
            </div>
          </div>
        </div>
      </div>
    `;
}

function handleAccordionClick(seconds) {
    // Scrubs to the correct time in the video and starts playing
    const videoUrl = document.getElementById("youtube-video").src;
    const urlWithTimestamp = `${videoUrl}?start=${seconds}&autoplay=1`;
    document.getElementById("youtube-video").src = urlWithTimestamp;
}

export { scrubVideoTo };
