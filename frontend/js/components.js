// function createAccordionItem(id, fact, description, seconds) {
//     return `
//       <div class="accordion-item">
//         <h2 class="accordion-header" id="heading${id}">
//           <button
//             class="accordion-button"
//             type="button"
//             data-mdb-toggle="collapse"
//             data-mdb-target="#collapse${id}"
//             aria-expanded="true"
//             aria-controls="collapse${id}"
//           >
//             <i class="fas fa-check-circle" style="color: green"></i>
//             <span class="ms-2">${fact}</span>
//           </button>
//         </h2>
//         <div
//           id="collapse${id}"
//           class="accordion-collapse collapse show"
//           aria-labelledby="heading${id}"
//           data-mdb-parent="#accordionExample"
//           data-seconds="${seconds}"
//         >
//           <div class="accordion-body">
//             ${description}
//             <strong style="color: green">${fact}</strong>
//           </div>
//         </div>
//       </div>
//     `;
// }

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
              Similarity: ${similarity}
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
