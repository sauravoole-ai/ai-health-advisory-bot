document.addEventListener("DOMContentLoaded", () => {
    const DISCLAIMER = "This is not a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation.";

    let chatHistory = [];

    // Live AIoT voice state
    let liveVoiceMuted = false;
    let lastLiveUpdatedAt = null;
    let lastSpokenLiveStatus = null;
    let normalLiveSpoken = false;
    let lastCautionSpeakTime = 0;
    let lastEmergencySpeakTime = 0;

    // -------------------------------------------------------
    // Navigation: Sidebar modules
    // -------------------------------------------------------

    const navButtons = document.querySelectorAll("[data-target]");
    const panels = document.querySelectorAll(".module-panel");
    const pageTitle = document.getElementById("pageTitle");

    function openPanel(targetId) {
        const targetPanel = document.getElementById(targetId);
        if (!targetPanel) return;

        panels.forEach((panel) => panel.classList.remove("active-panel"));

        document.querySelectorAll(".nav-item").forEach((item) => {
            item.classList.toggle("active", item.dataset.target === targetId);
        });

        targetPanel.classList.add("active-panel");

        if (pageTitle) {
            pageTitle.textContent = targetPanel.dataset.title || "Dashboard";
        }

        if (window.innerWidth < 900) {
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    }

    navButtons.forEach((button) => {
        button.addEventListener("click", () => {
            openPanel(button.dataset.target);
        });
    });

    window.openHealthPanel = openPanel;

    // -------------------------------------------------------
    // Vitals sub-tabs: Manual Entry / Live Monitor
    // -------------------------------------------------------

    const submodeButtons = document.querySelectorAll("[data-vitals-tab]");
    const vitalsSubpanels = document.querySelectorAll(".vitals-subpanel");

    submodeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.vitalsTab;

            submodeButtons.forEach((btn) => btn.classList.remove("active"));
            vitalsSubpanels.forEach((panel) => panel.classList.remove("active-subpanel"));

            button.classList.add("active");
            document.getElementById(targetId)?.classList.add("active-subpanel");
        });
    });

    // -------------------------------------------------------
    // Helpers
    // -------------------------------------------------------

    function safeText(value, fallback = "--") {
        if (value === undefined || value === null || value === "") return fallback;
        return String(value);
    }

    function isEmergencyStatus(status, riskLevel = "") {
        const text = `${status} ${riskLevel}`.toLowerCase();
        return (
            text.includes("emergency") ||
            text.includes("critical") ||
            text.includes("danger")
        );
    }

    function isCautionStatus(status, riskLevel = "") {
        const text = `${status} ${riskLevel}`.toLowerCase();
        return (
            text.includes("caution") ||
            text.includes("warning") ||
            text.includes("high") ||
            text.includes("moderate") ||
            text.includes("abnormal")
        );
    }

    function setLoading(button, loadingText, isLoading) {
        if (!button) return;

        if (isLoading) {
            button.dataset.originalText = button.innerText;
            button.innerText = loadingText;
            button.disabled = true;
        } else {
            button.innerText = button.dataset.originalText || button.innerText;
            button.disabled = false;
        }
    }

    function speakText(text) {
        if (!("speechSynthesis" in window)) return;

        const cleanText = String(text || "")
            .replace(/[*#_`>|]/g, " ")
            .replace(/-{2,}/g, " ")
            .replace(/\s+/g, " ")
            .trim();

        if (!cleanText) return;

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = "en-IN";
        utterance.rate = 0.92;
        utterance.pitch = 1;
        utterance.volume = 1;

        window.speechSynthesis.speak(utterance);
    }

    // -------------------------------------------------------
    // Manual Vitals Analysis
    // -------------------------------------------------------

    const vitalsForm = document.getElementById("vitalsForm");
    const analyzeBtn = document.getElementById("analyzeBtn");

    const vitalsResult = document.getElementById("vitalsResult");
    const resultStatus = document.getElementById("resultStatus");
    const riskBadge = document.getElementById("riskBadge");
    const reportSpo2 = document.getElementById("reportSpo2");
    const reportBpm = document.getElementById("reportBpm");
    const reportRisk = document.getElementById("reportRisk");
    const shortAdvice = document.getElementById("shortAdvice");
    const aiAdvice = document.getElementById("aiAdvice");
    const emergencyBanner = document.getElementById("emergencyBanner");

    vitalsForm?.addEventListener("submit", async (event) => {
        event.preventDefault();

        const spo2Input = document.getElementById("spo2");
        const bpmInput = document.getElementById("bpm");
        const symptomsInput = document.getElementById("symptoms");

        const payload = {
            spo2: Number(spo2Input.value),
            bpm: Number(bpmInput.value),
            symptoms: symptomsInput.value.trim()
        };

        try {
            setLoading(analyzeBtn, "Analyzing...", true);

            const response = await fetch("/api/analyze-health", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok) {
                alert(result.message || "Unable to analyze health data.");
                return;
            }

            showManualVitalsResult(result);
        } catch (error) {
            console.error(error);
            alert("Something went wrong while analyzing health data.");
        } finally {
            setLoading(analyzeBtn, "Analyze Health", false);
        }
    });

    function showManualVitalsResult(result) {
        vitalsResult?.classList.remove("hidden");

        if (resultStatus) resultStatus.innerText = safeText(result.status);
        if (riskBadge) riskBadge.innerText = safeText(result.risk_level);
        if (reportSpo2) reportSpo2.innerText = `${safeText(result.received_data?.spo2)}%`;
        if (reportBpm) reportBpm.innerText = safeText(result.received_data?.bpm);
        if (reportRisk) reportRisk.innerText = safeText(result.risk_level);
        if (shortAdvice) shortAdvice.innerText = safeText(result.short_advice);
        if (aiAdvice) aiAdvice.innerText = safeText(result.ai_advice);

        if (isEmergencyStatus(result.status, result.risk_level)) {
            emergencyBanner?.classList.remove("hidden");
        } else {
            emergencyBanner?.classList.add("hidden");
        }
    }

    document.getElementById("copyVitalsBtn")?.addEventListener("click", async () => {
        const text = [
            `Status: ${resultStatus?.innerText || "--"}`,
            `Risk: ${reportRisk?.innerText || "--"}`,
            `SpO2: ${reportSpo2?.innerText || "--"}`,
            `BPM: ${reportBpm?.innerText || "--"}`,
            "",
            `Short Advice: ${shortAdvice?.innerText || "--"}`,
            "",
            `AI Advice: ${aiAdvice?.innerText || "--"}`,
            "",
            DISCLAIMER
        ].join("\n");

        await navigator.clipboard.writeText(text);
        alert("Vitals advice copied.");
    });

    document.getElementById("downloadVitalsBtn")?.addEventListener("click", () => {
        window.print();
    });

    document.getElementById("clearVitalsBtn")?.addEventListener("click", () => {
        vitalsResult?.classList.add("hidden");
        vitalsForm?.reset();
    });

    // -------------------------------------------------------
    // AI Health Chat: typed chatbot
    // -------------------------------------------------------

    const chatWindow = document.getElementById("chatWindow");
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");

    function addMessage(role, text) {
        if (!chatWindow) return;

        const message = document.createElement("div");
        message.className = role === "user" ? "message user-message" : "message bot-message";

        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.innerText = role === "user" ? "You" : "AI";

        const bubble = document.createElement("div");
        bubble.className = "bubble";

        const paragraph = document.createElement("p");
        paragraph.innerText = text;

        bubble.appendChild(paragraph);
        message.appendChild(avatar);
        message.appendChild(bubble);

        chatWindow.appendChild(message);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    window.addHealthChatMessage = addMessage;

    chatForm?.addEventListener("submit", async (event) => {
        event.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        addMessage("user", message);
        chatInput.value = "";

        try {
            setLoading(sendBtn, "Sending...", true);

            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message,
                    history: chatHistory
                })
            });

            const result = await response.json();

            if (!response.ok) {
                addMessage("bot", result.reply || "Unable to generate response.");
                return;
            }

            const reply = result.reply || "No response received.";
            addMessage("bot", reply);

            chatHistory.push({
                role: "user",
                content: message
            });

            chatHistory.push({
                role: "assistant",
                content: reply
            });
        } catch (error) {
            console.error(error);
            addMessage("bot", "Something went wrong while contacting the AI assistant.");
        } finally {
            setLoading(sendBtn, "Send", false);
        }
    });

    document.getElementById("copyChatBtn")?.addEventListener("click", async () => {
        const botMessages = chatWindow?.querySelectorAll(".bot-message .bubble p");

        if (!botMessages || botMessages.length === 0) {
            alert("No AI reply to copy.");
            return;
        }

        const latestReply = botMessages[botMessages.length - 1].innerText;
        await navigator.clipboard.writeText(latestReply);
        alert("Latest AI reply copied.");
    });

    document.getElementById("downloadChatBtn")?.addEventListener("click", () => {
        window.print();
    });

    document.getElementById("clearChatBtn")?.addEventListener("click", () => {
        chatHistory = [];

        if (!chatWindow) return;

        chatWindow.innerHTML = `
            <div class="message bot-message">
                <div class="avatar">AI</div>
                <div class="bubble">
                    <p>Hello. I can help with basic health-related questions, symptoms, precautions, vitals and when to seek medical help.</p>
                    <small>${DISCLAIMER}</small>
                </div>
            </div>
        `;
    });

    // -------------------------------------------------------
    // Live Monitor / AIoT Mode
    // -------------------------------------------------------

    const liveConnectionBadge = document.getElementById("liveConnectionBadge");
    const liveSpo2 = document.getElementById("liveSpo2");
    const liveBpm = document.getElementById("liveBpm");
    const liveStatus = document.getElementById("liveStatus");
    const liveDevice = document.getElementById("liveDevice");
    const liveUpdated = document.getElementById("liveUpdated");
    const liveAiAdvice = document.getElementById("liveAiAdvice");
    const liveEmergencyBanner = document.getElementById("liveEmergencyBanner");
    const liveVoiceState = document.getElementById("liveVoiceState");

    async function fetchLatestSensorData({ manualRefresh = false } = {}) {
        try {
            const response = await fetch("/api/latest-sensor-data");
            const result = await response.json();

            if (!result.available) {
                updateLiveWaitingState();

                if (manualRefresh) {
                    alert("No live sensor data received yet.");
                }

                return;
            }

            updateLiveMonitor(result);
        } catch (error) {
            console.error(error);

            if (liveConnectionBadge) {
                liveConnectionBadge.innerText = "Offline";
                liveConnectionBadge.className = "connection-badge offline";
            }
        }
    }

    function updateLiveWaitingState() {
        if (liveConnectionBadge) {
            liveConnectionBadge.innerText = "Waiting";
            liveConnectionBadge.className = "connection-badge waiting";
        }
    }

    function updateLiveMonitor(result) {
        const received = result.received_data || {};
        const currentUpdatedAt = result.updated_at || "";

        if (liveConnectionBadge) {
            liveConnectionBadge.innerText = "Connected";
            liveConnectionBadge.className = "connection-badge connected";
        }

        if (liveSpo2) liveSpo2.innerText = `${safeText(received.spo2)}%`;
        if (liveBpm) liveBpm.innerText = safeText(received.bpm);
        if (liveStatus) liveStatus.innerText = safeText(result.status);
        if (liveDevice) liveDevice.innerText = safeText(result.device_id);
        if (liveUpdated) liveUpdated.innerText = safeText(result.updated_at);
        if (liveAiAdvice) liveAiAdvice.innerText = safeText(result.ai_advice, "No AI advice received.");

        if (isEmergencyStatus(result.status, result.risk_level)) {
            liveEmergencyBanner?.classList.remove("hidden");
        } else {
            liveEmergencyBanner?.classList.add("hidden");
        }

        if (currentUpdatedAt && currentUpdatedAt !== lastLiveUpdatedAt) {
            handleLiveVoice(result);
            lastLiveUpdatedAt = currentUpdatedAt;
        }
    }

    function handleLiveVoice(result) {
        if (liveVoiceMuted) return;

        const status = result.status || "";
        const risk = result.risk_level || "";
        const now = Date.now();

        const statusChanged = lastSpokenLiveStatus && lastSpokenLiveStatus !== status;
        const emergency = isEmergencyStatus(status, risk);
        const caution = isCautionStatus(status, risk);

        let shouldSpeak = false;

        // First available reading: speak once.
        if (!lastSpokenLiveStatus) {
            shouldSpeak = true;
        }

        // Any risk/status change: always speak.
        if (statusChanged) {
            shouldSpeak = true;
        }

        // Emergency: speak more frequently, but not every 3 seconds.
        if (emergency && now - lastEmergencySpeakTime > 20000) {
            shouldSpeak = true;
            lastEmergencySpeakTime = now;
        }

        // Caution: speak occasionally on meaningful updates.
        if (caution && !emergency && now - lastCautionSpeakTime > 45000) {
            shouldSpeak = true;
            lastCautionSpeakTime = now;
        }

        // Normal: speak once, then stay silent unless status changes.
        if (!caution && !emergency && !normalLiveSpoken) {
            shouldSpeak = true;
            normalLiveSpoken = true;
        }

        if (!shouldSpeak) return;

        const spokenAdvice = buildLiveSpokenAdvice(result);
        speakText(spokenAdvice);

        lastSpokenLiveStatus = status;
    }

    function buildLiveSpokenAdvice(result) {
        const received = result.received_data || {};

        return [
            "Live health advisory received from sensor.",
            `SpO2 is ${safeText(received.spo2)} percent.`,
            `Heart rate is ${safeText(received.bpm)} beats per minute.`,
            `Current status is ${safeText(result.status)}.`,
            safeText(result.short_advice, ""),
            safeText(result.ai_advice, ""),
            DISCLAIMER
        ].join(" ");
    }

    document.getElementById("speakLiveAdviceBtn")?.addEventListener("click", () => {
        const currentAdvice = liveAiAdvice?.innerText || "";

        if (!currentAdvice || currentAdvice.includes("No sensor data")) {
            alert("No live advice available yet.");
            return;
        }

        speakText(currentAdvice);
    });

    document.getElementById("muteLiveVoiceBtn")?.addEventListener("click", (event) => {
        liveVoiceMuted = !liveVoiceMuted;

        event.target.innerText = liveVoiceMuted ? "Unmute Live Voice" : "Mute Live Voice";

        if (liveVoiceState) {
            liveVoiceState.innerText = liveVoiceMuted ? "Muted" : "Smart Mode";
        }

        if (liveVoiceMuted && "speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }
    });

    document.getElementById("refreshLiveBtn")?.addEventListener("click", () => {
        fetchLatestSensorData({ manualRefresh: true });
    });

    fetchLatestSensorData();
    setInterval(fetchLatestSensorData, 3000);
});