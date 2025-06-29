window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';

document.body.addEventListener('keydown', (e) => {
  if (e.key === 'v') {
    recognition.start();
  }
});

recognition.onresult = (event) => {
  const text = event.results[0][0].transcript.toLowerCase();
  if (text.includes("open courses")) window.location.href = "/form";
  if (text.includes("show admin")) window.location.href = "/admin";
};
