const questions = [
  {
    q: "How do you handle conflict in a team?",
    options: ["Ignore it", "Talk it out", "Complain", "Leave the team"],
    answer: "Talk it out"
  },
  {
    q: "What does punctuality mean to you?",
    options: ["Be early", "Be late", "Skip", "No idea"],
    answer: "Be early"
  }
];

let index = 0;
const container = document.getElementById("game-container");

function showQuestion() {
  if (index >= questions.length) {
    container.innerHTML = "<h3>✅ Simulation Complete</h3>";
    return;
  }

  const q = questions[index];
  container.innerHTML = `<p>${q.q}</p>` + q.options.map(opt =>
    `<button onclick="checkAnswer('${opt}')">${opt}</button>`
  ).join("<br>");
}

function checkAnswer(selected) {
  const correct = questions[index].answer;
  alert(selected === correct ? "✅ Correct!" : `❌ Incorrect. Correct answer: ${correct}`);
  index++;
  showQuestion();
}

showQuestion();
