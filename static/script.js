let currentCategory = "";
let currentGameId = null;

function startGame(category) {
    currentCategory = category;
    document.getElementById("category-selection").style.display = "none";
    document.getElementById("game-area").style.display = "block";

    fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: category })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            currentGameId = data.game_id;
            updateWord(data.word_length);
        }
    });
}

function updateWord(wordLength) {
    const wordDisplay = document.getElementById("word-display");
    const placeholder = "_ ".repeat(wordLength).trim();
    wordDisplay.textContent = placeholder;
}

function makeGuess() {
    const input = document.getElementById("guess-input");
    const letter = input.value.trim().toLowerCase();
    input.value = ""; // Clear the input field

    fetch('/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letter: letter })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Alert for errors like "Letter already guessed"
        } else if (data.game_over) {
            alert(data.message); // "You lose!" or "You win!"
            if (data.word) alert("The word was: " + data.word); // Reveal the word
            location.reload(); // Reload the page to start a new game
        } else {
            updateWordState(data.current_state); // Update displayed word
            document.getElementById("message").textContent = data.message; // Correct/Incorrect message
            document.getElementById("hangman-art").textContent = data.stage || ""; // Update hangman art
        }
    })
    .catch(error => console.error('Error:', error));
}


function updateWordState(wordState) {
    const wordDisplay = document.getElementById("word-display");
    wordDisplay.textContent = wordState.split("").join(" ");
}

function getHint() {
    fetch(`/hint?game_id=${currentGameId}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(`Hint: ${data.hint}`);
        }
    });
}
