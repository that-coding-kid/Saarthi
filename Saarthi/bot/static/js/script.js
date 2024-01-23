

document.addEventListener("DOMContentLoaded", () => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatBox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.getElementById("send-btn");
    const chatBotNameElement = document.getElementById('chatbot-name'); // New line
    const recordButton = document.getElementById('recordButton');
    const statusIndicator = document.getElementById('statusIndicator');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const statusElement = document.getElementById('status');
    var selectedLanguage = 'en';

    let mediaRecorder;
    let chunks = [];

    function getCSRFToken() {
                return true;
            }

    function showLoadingIndicator() {
                loadingIndicator.style.display = 'block';
            }
    window.updateLanguage =function() {
        selectedLanguage = document.getElementById('languageDropdown').value;
    }

    function hideLoadingIndicator() {
                loadingIndicator.style.display = 'none';
            }
    
async function speakText(text, language) {
  try {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    
    // Wrap the speak function in a promise to catch errors
    await new Promise((resolve, reject) => {
      utterance.onend = resolve;
      utterance.onerror = reject;
      speechSynthesis.speak(utterance);
    });
  } catch (error) {
    console.error("Error speaking text:", error);
  }
}

    function createVoiceButton(text, language) {
        const voiceButton = document.createElement("button");
        voiceButton.textContent = "Listen";
        voiceButton.addEventListener("click", function () {
            speakText(text, language);
        });
        return voiceButton;
    }

    function send_text_query(){
      const textQuery = chatInput.value.trim();
      if (textQuery !== ""){
        const textContainer = document.createElement('div');
        textContainer.className = 'chat-message-container text-message';
        textContainer.textContent = textQuery;
        chatBox.appendChild(textContainer);

        
        chatBox.scrollTop = chatBox.scrollHeight;
        const csrfToken = getCSRFToken();
            if (csrfToken) {
        fetch('/send_text_query/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ text_query: textQuery , language: selectedLanguage }),
        })
        .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Display the bot's response in the chatbox
                        const answerContainer = document.createElement('div');
                        answerContainer.className = 'chat-message-container t-mess';
                        const answerText = typeof data.answer_text === 'object'
                            ? data.answer_text.text
                            : data.answer_text;
                        answerContainer.textContent=answerText;

                        chatBox.appendChild(answerContainer);
                        chatBox.scrollTop = chatBox.scrollHeight;
                         }else {
                        console.error('Error processing text query.');
                    }
                })
                .catch(error => console.error('Error sending text query:', error)); 
                chatInput.value = "";
                           

      }}
    }
    function appendMessage(message, isUser) {
        const messageElement = document.createElement('div');
        messageElement.className = isUser ? 'user-message' : 'bot-message';
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    }
    navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = function (event) {
                        if (event.data.size > 0) {
                            chunks.push(event.data);
                        }
                    };

                    mediaRecorder.onstop = function () {
                        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
                        chunks = [];

                        showLoadingIndicator(); // Show loading animation while transcribing

                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'recording.wav');
                        formData.append('language', selectedLanguage);
                        const csrfToken = getCSRFToken();
                        if (csrfToken) {
                            fetch('/save_audio/', {
                                method: 'POST',
                                body: formData,
                                headers: {
                                    'X-CSRFToken': csrfToken,
                                },
                            })
                            .then(response => response.json())
                            .then(data => {
                                hideLoadingIndicator(); // Hide loading animation after transcribing

                                if (data.status === 'success') {
                                    console.log('Audio saved successfully.');
                                    console.log('Transcribed Text:', data.transcribed_text);
                                    console.log('Result:', data.result);

                                    // Wrap transcribed text and answer text in separate containers
                                    const transcribedContainer = document.createElement('div');
                                    transcribedContainer.className = 'chat-message-container transcribed-message';
                                    const answerContainer = document.createElement('div');
                                    answerContainer.className = 'chat-message-container answer-message';


                                    // Ensure that data.transcribed_text is a string
                                    const transcribedText = typeof data.transcribed_text === 'object'
                                        ? data.transcribed_text.text
                                        : data.transcribed_text;

                                    const answerText = typeof data.answer_text === 'object'
                                        ? data.answer_text.text
                                        : data.answer_text;
                                    

                                    transcribedContainer.textContent = transcribedText;
                                    answerContainer.textContent = answerText;
                                    const voiceButton = createVoiceButton(answerText, selectedLanguage);
                                    answerContainer.appendChild(voiceButton);
                                    chatBox.appendChild(transcribedContainer);
                                    chatBox.appendChild(answerContainer);
                                    chatBox.scrollTop = chatBox.scrollHeight;
                                } else {
                                    console.error('Error saving audio.');
                                }
                            });
                        } else {
                            console.error('CSRF token not found.');
                        }
                    };

    recordButton.addEventListener('click', function () {
                        if (mediaRecorder.state === 'inactive') {
                            mediaRecorder.start();
                            recordButton.textContent = 'Stop';
                            statusIndicator.style.display = 'block';
                        } else {
                            mediaRecorder.stop();
                            recordButton.textContent = 'Record';
                            statusIndicator.style.display = 'none';
                        }
                    });
                })
                .catch(function (error) {
                    console.error('Error accessing microphone:', error);
                });

    appendMessage('Welcome! Type or record your message.', false);
 

    chatbotToggler.addEventListener("click", () => {
        document.body.classList.toggle("show-chatbot");
    });
    sendChatBtn.addEventListener('click', send_text_query);

});

