from flask import Flask, jsonify, request, render_template_string
import random

app = Flask(__name__)

# 🔥 GLOBAL STATE
isMonitoring = False

# 📡 DATA API
@app.route('/data')
def data():
    if not isMonitoring:
        return jsonify({
            "alpha": 0,
            "beta": 0,
            "state": "Stopped"
        })

    alpha = round(random.uniform(5, 10), 2)
    beta = round(random.uniform(5, 12), 2)
    state = "Stress" if beta > alpha else "Relax"

    return jsonify({
        "alpha": alpha,
        "beta": beta,
        "state": state
    })

# ▶ START MONITORING
@app.route('/start')
def start():
    global isMonitoring
    isMonitoring = True
    return "Started"

# ⏹ STOP MONITORING
@app.route('/stop')
def stop():
    global isMonitoring
    isMonitoring = False
    return "Stopped"

# 🌐 DASHBOARD
@app.route('/')
def dashboard():
    return render_template_string("""
    <html>
    <body style="background:#0f172a;color:white;text-align:center;padding-top:50px;">
        <h1>🧠 BioSense</h1>
        <h2 id="state">Loading...</h2>
        <p id="alpha"></p>
        <p id="beta"></p>

        <script>
        function fetchData(){
            fetch('/data')
            .then(r=>r.json())
            .then(d=>{
                document.getElementById("alpha").innerText = "Alpha: "+d.alpha;
                document.getElementById("beta").innerText = "Beta: "+d.beta;
                document.getElementById("state").innerText = d.state;
            });
        }
        setInterval(fetchData,1000);
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run()
