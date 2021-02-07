import flask

app = flask.Flask(__name__)

@app.route('/save_data')
def get_save_file():
    return dict(
        name='jack'
    )


app.run('0.0.0.0', 1337)
