from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Categories and words
categories = {
    "Animals": ["elephant", "giraffe", "kangaroo", "dolphin", "penguin", "tiger", "lion", "leopard", "cheetah", "jaguar", "panda", "koala", "sloth", "orangutan", "lemur" , "wolf", "fox", "coyote", "hyena", "jackal", "crocodile", "alligator", "gecko", "chameleon", "iguana" ],
    "Countries": ["usa", "canada", "australia", "brazil", "india", "china", "russia", "japan", "germany", "france", "mexico", "south africa", "egypt", "argentina", "italy", "spain", "united kingdom", "south korea", "nigeria", "saudi arabia", "turkey", "indonesia", "thailand", "vietnam", "egypt"],
    "Movies": [
  "the lion king", 
"jurassic park", 
"avatar", 
"the godfather", 
"forrest gump", 
"inception", 
"the dark knight", 
"titanic", 
"pulp fiction", 
"the shawshank redemption", 
"the matrix", 
"the avengers", 
"interstellar", 
"the godfather: part ii", 
"gladiator", 
"the prestige", 
"fight club", 
"star wars: a new hope", 
"the silence of the lambs", 
"the departed"

],
"Sports": ["soccer", "basketball", "tennis", "rugby", "cricket", "hockey", "volleyball", "baseball", "golf", "badminton", "swimming", "boxing", "wrestling", "karate", "judo", "cycling", "skiing", "snowboarding", "surfing", "gymnastics", "athletics", "table tennis", "archery", "fencing", "equestrian", "motor racing"],
"Technology": [
  "artificial intelligence", "blockchain", "quantum computing", "cloud computing", "internet of things",
  "5G", "machine learning", "virtual reality", "augmented reality", "cybersecurity",
  "robotics", "biotechnology", "renewable energy", "3D printing", "nanotechnology",
  "data analytics", "edge computing", "digital twins", "autonomous vehicles", "smart cities",
  "big data", "cryptocurrency", "web3", "AI ethics", "wearable technology"
]

}

# ASCII art for Hangman stages
HANGMAN_STAGES = [
    """
     -----
     |   |
         |
         |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    --------
    """,
    """
     ------
     |    |
     O    |
    /|\\  |
          |
          |
    --------
    """,
    """
     ------
     |    |
     O    |
    /|\\  |
    /     |
          |
    --------
    """,
    """
     ------
     |    |
     O    |
    /|\\  |
    / \\  |
          |
    --------
    """
]


# Game state
game_state = {
    "word": "",
    "guesses": [],
    "incorrect_guesses": 0,
    "category": "",
    "hint_used": False
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    category = data.get("category")
    if category not in categories:
        return jsonify({"error": "Invalid category"}), 400

    word = random.choice(categories[category])
    print(f"Selected word: {word}")  # Debugging
    game_state.update({
        "word": word,
        "guesses": [],
        "incorrect_guesses": 0,
        "category": category,
        "hint_used": False
    })
    return jsonify({"message": "Game started!", "word_length": len(word)})

@app.route('/guess', methods=['POST'])
def guess():
    data = request.json
    letter = data.get("letter", "").lower()

    if not letter.isalpha() or len(letter) != 1:
        return jsonify({"error": "Invalid input"}), 400

    if letter in game_state["guesses"]:
        return jsonify({"error": "Letter already guessed"}), 400

    game_state["guesses"].append(letter)

    # Check if the letter is correct
    if letter in game_state["word"]:
        current_state = "".join(
            [char if char in game_state["guesses"] else "_" for char in game_state["word"]]
        )
        if "_" not in current_state:
            return jsonify({"message": "You win!", "game_over": True, "current_state": current_state})
        return jsonify({"message": "Correct!", "game_over": False, "current_state": current_state})
    else:
        # Incorrect guess, increment incorrect guesses count
        game_state["incorrect_guesses"] += 1

        # Check if the game has reached the maximum number of incorrect guesses
        if game_state["incorrect_guesses"] >= len(HANGMAN_STAGES) - 1:
            # Show the final hangman stage and end the game
            return jsonify({
                "message": "You lose!",
                "game_over": True,
                "word": game_state["word"],
                "current_state": "".join(
                    [char if char in game_state["guesses"] else "_" for char in game_state["word"]]
                ),
                "stage": HANGMAN_STAGES[-1]  # Show the final hangman stage
            })

        # Show the current hangman stage for incorrect guesses
        stage = HANGMAN_STAGES[game_state["incorrect_guesses"]]
        return jsonify({
            "message": "Incorrect!",
            "game_over": False,
            "current_state": "".join(
                [char if char in game_state["guesses"] else "_" for char in game_state["word"]]
            ),
            "stage": stage
        })


@app.route('/hint', methods=['GET'])
def hint():
    if game_state["hint_used"]:
        return jsonify({"error": "Hint already used"}), 400
    
    for letter in game_state["word"]:
        if letter not in game_state["guesses"]:
            game_state["hint_used"] = True
            return jsonify({"hint": letter})
    return jsonify({"error": "No hint available"}), 400

if __name__ == '__main__':
    app.run(debug=True)
