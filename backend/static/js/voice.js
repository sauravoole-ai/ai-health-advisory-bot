document.addEventListener("DOMContentLoaded", () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const speechSupported = Boolean(SpeechRecognition);
    const ttsSupported = "speechSynthesis" in window;

    let recognition = null;
    let isListening = false;
    let autoMode = false;
    let isSpeaking = false;
    let lastSpokenText = "";

    const autoVoiceBtn = document.getElementById("autoVoiceBtn");
    const startVoiceBtn = document.getElementById("startVoiceBtn");
    const speakLatestBtn = document.getElementById("speakLatestBtn");
    const stopVoiceBtn = document.getElementById("stopVoiceBtn");
    const voiceStatus = document.getElementById("voiceStatus");
    const voiceOrb = document.getElementById("voiceOrb");
    const voiceOrbText = document.getElementById("voiceOrbText");

    function getChatInput() {
        return document.getElementById("chatInput");
    }

    function getSendButton() {
        return document.getElementById("sendBtn");
    }

    function getChatWindow() {
        return document.getElementById("chatWindow");
    }

    function setStatus(message, state = "idle") {
        if (voiceStatus) {
            voiceStatus.innerText = message;
        }

        if (voiceOrb) {
            voiceOrb.classList.remove("listening", "speaking");

            if (state === "listening") {
                voiceOrb.classList.add("listening");
            }

            if (state === "speaking") {
                voiceOrb.classList.add("speaking");
            }
        }

        if (voiceOrbText) {
            if (state === "listening") {
                voiceOrbText.innerText = "Listening";
            } else if (state === "speaking") {
                voiceOrbText.innerText = "Speaking";
            } else if (autoMode) {
                voiceOrbText.innerText = "Auto";
            } else {
                voiceOrbText.innerText = "Idle";
            }
        }
    }

    function openChatSilently() {
        if (typeof window.openHealthPanel === "function") {
            window.openHealthPanel("chatModule");
        }
    }

    function openVoicePanel() {
        if (typeof window.openHealthPanel === "function") {
            window.openHealthPanel("voiceModule");
        }
    }

    function cleanTextForSpeech(text) {
        return String(text || "")
            .replace(/[*#_`>|]/g, " ")
            .replace(/-{2,}/g, " ")
            .replace(/\s+/g, " ")
            .replace(
                /This is not a medical diagnosis\. Please consult a qualified healthcare professional for proper evaluation\./gi,
                "This is not a medical diagnosis. Please consult a qualified healthcare professional."
            )
            .trim();
    }

    function getLatestReplyText() {
        const chatWindow = getChatWindow();
        if (!chatWindow) return "";

        const botMessages = chatWindow.querySelectorAll(".bot-message");

        if (botMessages.length > 0) {
            const latest = botMessages[botMessages.length - 1];
            return latest.innerText.trim();
        }

        return chatWindow.innerText.trim();
    }

    function speakText(text, afterSpeak = null) {
        if (!ttsSupported) {
            setStatus("Text-to-speech is not supported in this browser.");
            if (typeof afterSpeak === "function") afterSpeak();
            return;
        }

        const cleanText = cleanTextForSpeech(text);

        if (!cleanText) {
            setStatus("No AI reply found to speak.");
            if (typeof afterSpeak === "function") afterSpeak();
            return;
        }

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = "en-IN";
        utterance.rate = 0.92;
        utterance.pitch = 1;
        utterance.volume = 1;

        isSpeaking = true;
        setStatus("Speaking the AI response...", "speaking");

        utterance.onend = () => {
            isSpeaking = false;
            lastSpokenText = cleanText;

            if (typeof afterSpeak === "function") {
                afterSpeak();
            } else {
                setStatus("Voice response completed.");
            }
        };

        utterance.onerror = () => {
            isSpeaking = false;
            setStatus("Could not speak the response.");
            if (typeof afterSpeak === "function") afterSpeak();
        };

        window.speechSynthesis.speak(utterance);
    }

    function waitForNewBotReply(previousText, callback) {
        const chatWindow = getChatWindow();

        if (!chatWindow) {
            setStatus("Chat window not found.");
            return;
        }

        let timeoutId = null;

        const observer = new MutationObserver(() => {
            const latestText = getLatestReplyText();

            if (
                latestText &&
                latestText.length > 20 &&
                latestText !== previousText &&
                latestText !== lastSpokenText
            ) {
                clearTimeout(timeoutId);
                observer.disconnect();
                callback(latestText);
            }
        });

        observer.observe(chatWindow, {
            childList: true,
            subtree: true,
            characterData: true
        });

        timeoutId = setTimeout(() => {
            observer.disconnect();

            const latestText = getLatestReplyText();

            if (latestText && latestText !== previousText) {
                callback(latestText);
            } else {
                setStatus("No new AI reply detected. You can try again.");

                if (autoMode) {
                    setTimeout(startAutoListening, 900);
                }
            }
        }, 18000);
    }

    function sendVoiceTextToChat(spokenText) {
        const chatInput = getChatInput();
        const sendButton = getSendButton();

        if (!chatInput || !sendButton) {
            setStatus("Chat input or send button not found.");
            return;
        }

        const previousReply = getLatestReplyText();

        openChatSilently();

        chatInput.value = spokenText;
        chatInput.dispatchEvent(new Event("input", { bubbles: true }));
        chatInput.dispatchEvent(new Event("change", { bubbles: true }));

        setStatus(`Captured: "${spokenText}". Sending to AI...`);

        setTimeout(() => {
            sendButton.click();

            openVoicePanel();

            waitForNewBotReply(previousReply, (replyText) => {
                speakText(replyText, () => {
                    if (autoMode) {
                        setStatus("Listening again. Speak your next question.", "listening");
                        setTimeout(startAutoListening, 900);
                    } else {
                        setStatus("Voice response completed.");
                    }
                });
            });
        }, 350);
    }

    function createRecognition({ auto = false } = {}) {
        if (!speechSupported) {
            setStatus("Speech recognition is not supported here. Use Google Chrome for best results.");
            return null;
        }

        const rec = new SpeechRecognition();
        rec.lang = "en-IN";
        rec.interimResults = false;
        rec.continuous = false;

        rec.onstart = () => {
            isListening = true;
            setStatus(
                auto ? "Auto Mode listening. Speak your question..." : "Listening. Speak your question...",
                "listening"
            );
        };

        rec.onresult = (event) => {
            const spokenText = event.results[0][0].transcript.trim();

            if (!spokenText) {
                setStatus("No clear speech captured. Try again.");
                return;
            }

            isListening = false;
            setStatus("Speech captured. Processing...");

            sendVoiceTextToChat(spokenText);
        };

        rec.onerror = (event) => {
            isListening = false;

            if (event.error === "not-allowed") {
                autoMode = false;
                updateAutoButton();
                setStatus("Microphone permission denied. Allow mic access and try again.");
                return;
            }

            if (event.error === "no-speech") {
                setStatus("No speech detected.");

                if (autoMode) {
                    setTimeout(startAutoListening, 900);
                }

                return;
            }

            setStatus(`Voice error: ${event.error}`);

            if (autoMode) {
                setTimeout(startAutoListening, 1200);
            }
        };

        rec.onend = () => {
            isListening = false;
        };

        return rec;
    }

    function startSingleListening() {
        if (isListening || isSpeaking) return;

        recognition = createRecognition({ auto: false });

        if (recognition) {
            try {
                recognition.start();
            } catch (error) {
                setStatus("Voice engine is restarting. Try again.");
            }
        }
    }

    function startAutoListening() {
        if (!autoMode || isListening || isSpeaking) return;

        recognition = createRecognition({ auto: true });

        if (recognition) {
            try {
                recognition.start();
            } catch (error) {
                setStatus("Voice engine is restarting...");
                setTimeout(startAutoListening, 1000);
            }
        }
    }

    function updateAutoButton() {
        if (!autoVoiceBtn) return;

        autoVoiceBtn.innerText = autoMode ? "Stop Auto Mode" : "Start Auto Mode";

        if (autoMode) {
            autoVoiceBtn.classList.add("danger-btn");
        } else {
            autoVoiceBtn.classList.remove("danger-btn");
        }
    }

    function toggleAutoMode() {
        if (!speechSupported) {
            setStatus("Speech recognition is not supported here. Use Google Chrome.");
            return;
        }

        autoMode = !autoMode;
        updateAutoButton();

        if (autoMode) {
            openVoicePanel();
            setStatus("Auto Mode started. Speak after the listening indicator appears.");
            setTimeout(startAutoListening, 500);
        } else {
            stopAllVoice();
            setStatus("Auto Mode stopped.");
        }
    }

    function speakLatestReply() {
        const latestReply = getLatestReplyText();

        if (!latestReply) {
            setStatus("No AI reply found yet.");
            return;
        }

        speakText(latestReply);
    }

    function stopAllVoice() {
        autoMode = false;
        updateAutoButton();

        if (recognition && isListening) {
            try {
                recognition.stop();
            } catch (error) {
                console.warn("Recognition stop error:", error);
            }
        }

        if (ttsSupported) {
            window.speechSynthesis.cancel();
        }

        isListening = false;
        isSpeaking = false;
        setStatus("Voice stopped.");
    }

    autoVoiceBtn?.addEventListener("click", toggleAutoMode);
    startVoiceBtn?.addEventListener("click", startSingleListening);
    speakLatestBtn?.addEventListener("click", speakLatestReply);
    stopVoiceBtn?.addEventListener("click", stopAllVoice);

    if (!speechSupported) {
        setStatus("Speech recognition is not supported in this browser. Use Google Chrome for Voice Chat.");
    } else {
        setStatus("Ready. Click Auto Mode and allow microphone access.");
    }
});