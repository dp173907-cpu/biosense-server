from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/data')
def data():
    alpha = round(random.uniform(5, 10), 2)
    beta = round(random.uniform(5, 12), 2)

    state = "Stress" if beta > alpha else "Relax"

    return jsonify({
        "alpha": alpha,
        "beta": beta,
        "state": state
    })

if __name__ == "__main__":
    app.run()