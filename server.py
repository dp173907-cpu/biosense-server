from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

running = False
alpha = 0
beta = 0
state = "Stopped"

# 🔥 STORE LAST VALUES
last_alpha = 0
last_beta = 0
final_result = "Stopped"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start():
    global running, state
    running = True
    state = "Running"
    return "Started"


@app.route("/stop")
def stop():
    global running, final_result, last_alpha, last_beta

    running = False

    # 🔥 CALCULATE FINAL RESULT
    if last_beta > last_alpha:
        final_result = "Stress"
    else:
        final_result = "Relax"

    return "Stopped"


@app.route("/data")
def data():
    global alpha, beta, state, last_alpha, last_beta

    if running:
        alpha = round(random.uniform(5, 10), 2)
        beta = round(random.uniform(6, 12), 2)

        last_alpha = alpha
        last_beta = beta

        state = "Stress" if beta > alpha else "Relax"

    else:
        # 🔥 SHOW FINAL RESULT AFTER STOP
        alpha = last_alpha
        beta = last_beta
        state = final_result

    return jsonify({
        "alpha": alpha,
        "beta": beta,
        "state": state
    })


if __name__ == "__main__":
    app.run()
