from flask import Flask, render_template, request, session, redirect
from boggle import Boggle

app = Flask(__name__)
app.secret_key = 'mmBoss3473'
boggle_game = Boggle()

@app.route('/')
def home():
    """"""
    if 'board' not in session:
        session['board'] = boggle_game.make_board()

        board = session['board']
        return render_template('board.html', board=board)
    
@qpp.route('/submit_guess', methods=['POST'])    
def submit_guess():
    """"""
    guess = request.form['guess'].upper()
    board = session.get('board')

    result = boggle_game.check_valid_word(board, guess)

    if result =='ok':
        message = f"{guess} is a valid word."
    elif result == 'not on the board':
        message = f"{guess} is not on the board."     
    else:
        message = f'{guess} is not a valid word.'

    return render_template('board.html', board=board, message=message)   

if __name__ == '__main__':
    app.run(debug=True)