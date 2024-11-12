from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.secret_key = 'mmBoss3473'  
boggle_game = Boggle()

@app.route('/')
def home():
    """Display the Boggle board and initialize session data for scores."""
    if 'board' not in session:
        session['board'] = boggle_game.make_board()
    if 'highscore' not in session:
        session['highscore'] = 0
    if 'nplays' not in session:
        session['nplays'] = 0

    board = session['board']
    highscore = session['highscore']
    nplays = session['nplays']

    return render_template('board.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    """Process the user's guess and check if it's valid."""
    guess = request.json.get('guess', '').upper()  

    if not guess:
        return jsonify({'result': 'no-guess'}), 400  # Handle empty guess

    board = session.get('board')
    result = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': result})

@app.route('/end_game', methods=['POST'])
def end_game():
    """Update high score and number of plays if the game ends."""
    score = request.json.get('score', 0)

    session['nplays'] = session.get('nplays', 0) + 1
    session['highscore'] = max(score, session.get('highscore', 0))

    return jsonify(new_highscore=session['highscore'], nplays=session['nplays'])

if __name__ == "__main__":
    app.run(debug=True) 