const input = document.getElementById("user-input");

async function sendMessage() {
    const imageInput = document.getElementById("image-input");
    const chatBox = document.getElementById("chat-box");
    const bsbox = document.getElementById("image-input2");
    const message = input.value.trim();
    const imageFile = imageInput.files[0];
    const bs = bsbox.files[0];

   if (!imageFile || !message || !bs) {
       // Optional: Add a visual shake or alert here if missing inputs
       return;
   }

    input.value = "";
    // We don't clear file inputs immediately so user can ask follow ups,
    // but based on your original logic, we clear them:
    imageInput.value = "";
    bsbox.value = "";

    // User message
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    if (message) userDiv.textContent = message;
    chatBox.appendChild(userDiv);

    // Bot message container
    const botDiv = document.createElement("div");
    botDiv.className = "message bot";
    chatBox.appendChild(botDiv);

    // Initial loading state
    botDiv.innerHTML = '<span style="color:#94a3b8;">Thinking...</span>';
    chatBox.scrollTop = chatBox.scrollHeight;

    const formData = new FormData();
    formData.append("message", message);
    if (imageFile) formData.append("story", imageFile);
    if (bs) formData.append("backstory", bs);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // Interactive Menu (New Control Panel Style)
        botDiv.innerHTML = `
        <div class="control-panel">
            <button class="control-btn" id="btn-down" title="Download JSON">Download RESULTS.CSV</button>
            <button class="control-btn primary" id="btn-text" title="Show Visual Cards">Show Results</button>
            <button class="control-btn" id="btn-both">Both Actions</button>
        </div>
        <div id="results-container"></div>
        `;

        const downloadBtn = botDiv.querySelector("#btn-down");
        const textBtn = botDiv.querySelector("#btn-text");
        const bothBtn = botDiv.querySelector("#btn-both");
        const resultsContainer = botDiv.querySelector("#results-container");

        // --- Event Handlers ---

        downloadBtn.onclick = () => {
            downloadJSON(data, "response.json");
        };

        const renderCards = async () => {
             resultsContainer.innerHTML = "";

             for (const row of data) {
                 const card = document.createElement("div");
                 card.className = "result-card";

                 // Consistency Logic
                 const isnotConsistent = row.judgment.toLowerCase().includes("inconsistent");
                 const statusClass = isnotConsistent ? "pill-inconsistent" : "pill-consistent";
                 const statusLabel = isnotConsistent ? "Inconsistent" : "Consistent";

                 // Confidence Logic
                 const confVal = parseFloat(row.confidence); // Assuming 0 to 1
                 const confPercent = Math.round(confVal * 100);
                 const barColor = isnotConsistent ? "#f87171" : "#4ade80";

                 // Claim Logic (Handle empty claims)
                 let claimHtml = `<div class="card-claim">"${row.claim}"</div>`;
                 if (!row.claim || row.claim === "null" || row.claim === "") {
                     claimHtml = `<div class="card-claim placeholder-text">No specific claim summary available.</div>`;
                 }

                 // Build Card HTML
                 card.innerHTML = `
                    <div class="card-header">
                        <span class="char-name">${row.character}</span>
                        <span class="status-pill ${statusClass}">
                            ${statusLabel}
                        </span>
                    </div>

                    <div class="card-body">
                        ${claimHtml}

                        <div class="meter-container">
                            <div class="progress-track">
                                <div class="progress-fill" style="width: 100%; background-color: ${barColor};"></div>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer">
                        <button class="evidence-btn evidence-link">
                            👁 Show Evidence
                        </button>
                    </div>
                 `;

                 // Attach Event Listener for Modal
                 const btn = card.querySelector(".evidence-btn");
                 btn.onclick = () => openModal(row.evidence);

                 resultsContainer.appendChild(card);

                 // Animation delay
                 await new Promise(r => setTimeout(r, 20));
                 chatBox.scrollTop = chatBox.scrollHeight;
             }
        };

        textBtn.onclick = async () => {
            // Toggle active state visualization if desired
            textBtn.classList.add("primary");
            await renderCards();
        };

        bothBtn.onclick = async () => {
            downloadJSON(data, "response.json");
            await renderCards();
        };

    } catch (error) {
        botDiv.textContent = "Error: " + error.message;
    }
}

// --- MODAL FUNCTIONS ---

function openModal(evidenceText) {
    const modal = document.getElementById("evidence-modal");
    const modalText = document.getElementById("modal-text");
    modalText.textContent = evidenceText || "No detailed evidence provided.";
    modal.style.display = "flex";
}

function closeModal() {
    document.getElementById("evidence-modal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("evidence-modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// --- UPLOAD TRIGGERS ---
// Kept logic to append text so backend works, but UI uses icons now.

function trig() {
    document.getElementById("image-input").click();
    if (input.value.length > 0 && !input.value.includes("Story Attached")) {
        input.value += " [Story Attached]";
        return;
    }
    if(input.value.length === 0) input.value = "[Story Attached]";
}

function trigg() {
    document.getElementById("image-input2").click();
    if (input.value.length > 0 && !input.value.includes("Backstory Attached")) {
        input.value += " [Backstory Attached]";
        return;
    }
    if(input.value.length === 0) input.value = "[Backstory Attached]";
}

input.addEventListener("keyup", (e) => {
    if (e.key === "Enter") sendMessage();
});

function downloadJSON(data) {
  const blob = new Blob(
    [JSON.stringify(data, null, 2)],
    { type: "application/json" }
  );

  const a = document.createElement("a");
  a.href = "/csv";
  a.download = "results.csv";
  a.click();

  URL.revokeObjectURL(a.href);
}