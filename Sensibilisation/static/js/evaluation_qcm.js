
const totalQuestions = {{ total_questions }};
let currentIndex = 0;
let answers = {};
const questionCards = document.querySelectorAll('.question-card');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
      function showQuestion(index) {
          questionCards.forEach((card, i) => {
              card.classList.toggle('active', i === index);
          });

          prevBtn.style.display = index === 0 ? 'none' : 'block';

          if (index === totalQuestions - 1) {
              nextBtn.style.display = 'none';
              submitBtn.classList.add('active');
          } else {
              nextBtn.style.display = 'block';
              submitBtn.classList.remove('active');
          }

          updateProgress();
      }

      function updateProgress() {
          const answered = Object.keys(answers).length;
          const percent = (answered / totalQuestions) * 100;
          progressFill.style.width = percent + '%';
          progressText.textContent = `${answered}/${totalQuestions}`;
      }

      function loadSavedAnswer(index) {
          const questionCard = questionCards[index];
          const questionId = questionCard.dataset.id;
          const savedValue = answers[questionId];

          if (savedValue !== undefined) {
              const options = questionCard.querySelectorAll('.option');
              options.forEach((opt, i) => {
                  if (i === savedValue) {
                      opt.classList.add('selected');
                  } else {
                      opt.classList.remove('selected');
                  }
              });
          }
      }

      // Option click handlers
      questionCards.forEach((card, idx) => {
          const options = card.querySelectorAll('.option');
          const questionId = card.dataset.id;

          options.forEach((opt, optIdx) => {
              opt.addEventListener('click', () => {
                  options.forEach(o => o.classList.remove('selected'));
                  opt.classList.add('selected');
                  answers[questionId] = optIdx;
                  updateProgress();
              });
          });
      });

      // Navigation
      prevBtn.addEventListener('click', () => {
          if (currentIndex > 0) {
              currentIndex--;
              showQuestion(currentIndex);
              loadSavedAnswer(currentIndex);
          }
      });

      nextBtn.addEventListener('click', () => {
          const currentQuestion = questionCards[currentIndex];
          const questionId = currentQuestion.dataset.id;

          if (answers[questionId] === undefined) {
              alert('Please select an answer before continuing.');
              return;
          }

          if (currentIndex < totalQuestions - 1) {
              currentIndex++;
              showQuestion(currentIndex);
              loadSavedAnswer(currentIndex);
          }
      });

      // Submit quiz
      submitBtn.addEventListener('click', async () => {
          if (Object.keys(answers).length < totalQuestions) {
              alert(`Please answer all questions. ${totalQuestions - Object.keys(answers).length} remaining.`);
              return;
          }

          submitBtn.disabled = true;
          submitBtn.textContent = 'Submitting...';

          try {
              const response = await fetch('/sensibilisation/submit-qcm/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: JSON.stringify({ answers: answers })
              });

              const data = await response.json();

              if (response.ok) {
                  showResults(data);
              } else {
                  alert('Error: ' + (data.error || 'Unknown error'));
              }
          } catch (error) {
              alert('Network error. Please try again.');
          } finally {
              submitBtn.disabled = false;
              submitBtn.textContent = 'Submit Quiz';
          }
      });

      function showResults(data) {
          document.getElementById('questionsContainer').style.display = 'none';
          document.querySelector('.navigation').style.display = 'none';
          document.querySelector('.progress-bar').style.display = 'none';

          const resultContainer = document.getElementById('resultContainer');
          resultContainer.classList.add('show');

          const scoreCircle = document.getElementById('scoreCircle');
          const resultMessage = document.getElementById('resultMessage');

          const percentage = data.percentage;
          const passed = percentage >= 80;

          scoreCircle.textContent = Math.round(percentage) + '%';
          scoreCircle.classList.add(passed ? 'score-pass' : 'score-fail');

          if (passed) {
              resultMessage.innerHTML = `
                  <strong>🎉 Congratulations!</strong><br>
                  You scored ${percentage}% and passed the quiz.<br>
                  Your security awareness certificate has been recorded.
              `;
              resultMessage.classList.add('result-pass');
          } else {
              resultMessage.innerHTML = `
                  <strong>⚠️ Score: ${percentage}%</strong><br>
                  The passing score is 80%. Please review the training material and try again.<br>
                  Score: ${data.score}/${data.total}
              `;
              resultMessage.classList.add('result-fail');
          }
      }

      function closeWindow() {
          window.close();
      }

      function getCookie(name) {
          let value = "; " + document.cookie;
          let parts = value.split("; " + name + "=");
          if (parts.length === 2) return parts.pop().split(";").shift();
      }

      // Initialize
      showQuestion(0);
