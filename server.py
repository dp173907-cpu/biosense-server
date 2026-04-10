from flask import Flask, jsonify, render_template
import random
import threading
import time

app = Flask(__name__)

# 🔥 GLOBAL STATE
running = False

current_alpha = 0
current_beta = 0
current_state = "Stopped"

last_alpha = 0
last_beta = 0
final_result = "Stopped"


# 🔥 BACKGROUND DATA GENERATION (SYNC FOR ALL CLIENTS)
def generate_data():
    global current_alpha, current_beta, current_state
    global last_alpha, last_beta, final_result, running

    while True:
        if running:
            current_alpha = round(random.uniform(5, 10), 2)
            current_beta = round(random.uniform(6, 12), 2)

            last_alpha = current_alpha
            last_beta = current_beta

            current_state = "Running"

        time.sleep(1)


# 🔥 START THREAD
threading.Thread(target=generate_data, daemon=True).start()


# 🌐 WEB PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ▶ START
@app.route("/start")
def start():
    global running, current_state, final_result

    running = True
    current_state = "Running"
    final_result = "Running"

    return "Started"


# ⏹ STOP
@app.route("/stop")
def stop():
    global running, current_state, final_result

    running = False

    # 🔥 FINAL RESULT CALCULATION
    if last_beta > last_alpha:
        final_result = "Stress"
    else:
        final_result = "Relax"

    current_state = final_result

    return "Stopped"


# 📡 DATA API (SAME FOR APP + WEB)
@app.route("/data")
def data():
    global current_alpha, current_beta, current_state

    # 🔥 DURING RUN → SHOW LIVE VALUES
    if running:
        state = "Running"
    else:
        state = current_state  # Stress / Relax after stop

    return jsonify({
        "alpha": current_alpha,
        "beta": current_beta,
        "state": state
    })


if __name__ == "__main__":
    app.run()
