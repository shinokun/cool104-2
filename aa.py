from flask import Flask, render_template, request
import game_main
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def restart():
    p = game_main.Cool()
    p.main
    return p


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)