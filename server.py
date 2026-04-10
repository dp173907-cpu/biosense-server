from flask import Flask, jsonify, render_template_string
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

# 🔥 LIVE DASHBOARD
@app.route('/')
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BioSense Live Dashboard</title>
        <style>
            body {
                background: #0f172a;
                color: white;
                font-family: Arial;
                text-align: center;
                padding-top: 50px;
            }
            .card {
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                width: 300px;
                margin: auto;
                box-shadow: 0 0 10px #000;
            }
            h1 { color: #38bdf8; }
            .stress { color: red; }
            .relax { color: #22c55e; }
        </style>
    </head>
    <body>

        <div class="card">
            <h1>🧠 BioSense</h1>
            <h2 id="state">Loading...</h2>
            <p id="alpha">Alpha: --</p>
            <p id="beta">Beta: --</p>
        </div>

        <script>
            function fetchData() {
                fetch('/data')
                .then(res => res.json())
                .then(data => {
                    document.getElementById("alpha").innerText = "Alpha: " + data.alpha;
                    document.getElementById("beta").innerText = "Beta: " + data.beta;

                    let stateEl = document.getElementById("state");
                    stateEl.innerText = data.state;

                    if (data.state === "Stress") {
                        stateEl.className = "stress";
                    } else {
                        stateEl.className = "relax";
                    }
                });
            }

            setInterval(fetchData, 1000);
            fetchData();
        </script>

    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run()
