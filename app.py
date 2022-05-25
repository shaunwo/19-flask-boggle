from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "Chicken fears Maximus"

# default page / board
@app.route("/")
def homepage():
    
    """Creating a new board for the game"""
    board = boggle_game.make_board()

    """Adding the board variable to the session, and resetting a couple keys"""
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    """Displaying the board on the screen"""
    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

# checking the word
@app.route("/check-word")
def check_word():
   
    """Checking to see if the word chosen is a valid word (is in the words.txt file"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    """Reurning the result of the check in a JSON object"""
    return jsonify({'result': response})

# posting the score
@app.route("/post-score", methods=["POST"])
def post_score():
    
    """Fincing current score from the JSON object, and pulling highscore and number of plays from the session"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    """Increasing the number of plays, and checking the high score"""
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    """If a new high score is set..."""
    return jsonify(brokeRecord=score > highscore)