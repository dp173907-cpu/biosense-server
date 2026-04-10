from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

running = False
alpha = 0
beta = 0
state = "Stopped"
final_result = "N/A"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start():
    global running, state, final_result
    running = True
    state = "Running"
    final_result = "N/A"
    return "Started"


@app.route("/stop")
def stop():
    global running, state, final_result, alpha, beta
    running = False

    # 🔥 FINAL RESULT LOGIC
    if beta > alpha:
        final_result = "Stress"
    else:
        final_result = "Relax"

    state = final_result
    return "Stopped"


@app.route("/data")
def data():
    global alpha, beta, state

    if running:
        alpha = round(random.uniform(5, 10), 2)
        beta = round(random.uniform(6, 12), 2)

        state = "Stress" if beta > alpha else "Relax"

    return jsonify({
        "alpha": alpha,
        "beta": beta,
        "state": state
    })


if __name__ == "__main__":
    app.run()
