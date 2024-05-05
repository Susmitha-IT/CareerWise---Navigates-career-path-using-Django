const quizContainer = document.getElementById('quiz');
const resultContainer = document.getElementById('result');
const submitButton = document.getElementById('submit');
const retryButton = document.getElementById('retry');
const showAnswerButton = document.getElementById('showAnswer');

let currentQuestion = 0;
let score = 0;
let incorrectAnswers = [];

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function displayQuestion() {
    const questionData = quizData[currentQuestion];

    const questionElement = document.createElement('div');
    questionElement.className = 'question';
    
    // Create a span element for the question number with custom styling
    const questionNumberSpan = document.createElement('span');
    questionNumberSpan.style.color = 'blue'; // Example color
    questionNumberSpan.style.fontWeight = 'bold'; // Example font weight
    questionNumberSpan.textContent = `Question ${currentQuestion + 1}: `;
    
    // Append the question number span to the question element
    questionElement.appendChild(questionNumberSpan);
    
    // Append the question text to the question element
    questionElement.innerHTML += questionData.question;

    const optionsElement = document.createElement('div');
    optionsElement.className = 'options';

    const shuffledOptions = [...questionData.options];
    shuffleArray(shuffledOptions);

    for (let i = 0; i < shuffledOptions.length; i++) {
        const option = document.createElement('label');
        option.className = 'option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'quiz';
        radio.value = shuffledOptions[i];

        const optionText = document.createTextNode(shuffledOptions[i]);

        option.appendChild(radio);
        option.appendChild(optionText);
        optionsElement.appendChild(option);
    }

    quizContainer.innerHTML = '';
    quizContainer.appendChild(questionElement);
    quizContainer.appendChild(optionsElement);
}


function checkAnswer() {
    const selectedOption = document.querySelector('input[name="quiz"]:checked');
    if (selectedOption) {
        const answer = selectedOption.value;
        if (answer === quizData[currentQuestion].answer) {
            score++;
        } else {
            incorrectAnswers.push({
                question: quizData[currentQuestion].question,
                incorrectAnswer: answer,
                correctAnswer: quizData[currentQuestion].answer,
            });
        }
        currentQuestion++;
        selectedOption.checked = false;
        if (currentQuestion < quizData.length) {
            displayQuestion();
        } else {
            displayResult();
        }
    }
}
function displayResult() {
    quizContainer.style.display = 'none';
    submitButton.style.display = 'none';
    retryButton.style.display = 'inline-block';
    showAnswerButton.style.display = 'inline-block';

    // Calculate the percentage score
    const percentageScore = (score / quizData.length) * 100;

    // Determine the feedback based on the percentage score
    let feedback;
    if (percentageScore >= 90) {
        feedback = `Congratulations! Your score of ${score} out of ${quizData.length} is excellent. You have demonstrated outstanding knowledge and aptitude in the quiz topics. Keep up the fantastic work!`;
    } else if (percentageScore >= 80) {
        feedback = `Well done! Your score of ${score} out of ${quizData.length} is very good. You have shown strong proficiency in the quiz topics. Keep striving for excellence!`;
    } else if (percentageScore >= 60) {
        feedback = `Good job! Your score of ${score} out of ${quizData.length} is commendable. You have a solid understanding of the quiz topics. Keep practicing to enhance your skills further.`;
    } else if (percentageScore >= 40) {
        feedback = `You're on the right track! Your score of ${score} out of ${quizData.length} shows a decent grasp of the quiz topics. Focus on areas where you can improve, and don't hesitate to seek assistance if needed.`;
    } else if (percentageScore >= 20) {
        feedback = `There's room for improvement. Your score of ${score} out of ${quizData.length} indicates some gaps in your understanding of the quiz topics. Identify areas for growth and dedicate extra effort to strengthen your skills.`;
    } else {
        feedback = `It's an opportunity to learn. Your score of ${score} out of ${quizData.length} suggests significant challenges in understanding the quiz topics. Don't be discouraged; use this experience as motivation to seek help and improve.`;
    }
    // Apply CSS styles to the feedback
    resultContainer.innerHTML = feedback;
    resultContainer.style.fontFamily = 'Arial, sans-serif';
    resultContainer.style.fontSize = '18px';
    resultContainer.style.lineHeight = '1.6';
    resultContainer.style.padding = '20px';
    resultContainer.style.border = '2px solid #ccc';
    resultContainer.style.borderRadius = '5px';
    resultContainer.style.backgroundColor = '#f9f9f9';
    resultContainer.style.color = '#333';
}


function retryQuiz() {
    currentQuestion = 0;
    score = 0;
    incorrectAnswers = [];
    quizContainer.style.display = 'block';
    submitButton.style.display = 'inline-block';
    retryButton.style.display = 'none';
    showAnswerButton.style.display = 'none';
    resultContainer.innerHTML = '';
    displayQuestion();
}

function showAnswer() {
    quizContainer.style.display = 'none';
    submitButton.style.display = 'none';
    retryButton.style.display = 'inline-block';
    showAnswerButton.style.display = 'none';

    let incorrectAnswersHtml = '';
    for (let i = 0; i < incorrectAnswers.length; i++) {
        incorrectAnswersHtml += `
        <p>
          <strong>Question:</strong> ${incorrectAnswers[i].question}<br><br>
          <strong style='color:red;'>Your Answer:</strong> ${incorrectAnswers[i].incorrectAnswer}<br>
          <strong style='color:green;'>Correct Answer:</strong> ${incorrectAnswers[i].correctAnswer}
        </p>
      `;
    }

    resultContainer.innerHTML = `
      <p>You scored ${score} out of ${quizData.length}!</p>
      <p>Incorrect Answers:</p>
      ${incorrectAnswersHtml}
    `;
}

submitButton.addEventListener('click', checkAnswer);
retryButton.addEventListener('click', retryQuiz);
showAnswerButton.addEventListener('click', showAnswer);


// Fetch quiz data from the backend
fetch('/quiz/quiz-data/')
  .then(response => response.json())
  .then(data => {
    window.quizData = data;
    displayQuestion();
  })
  .catch(error => console.error('Error fetching quiz data:', error));
