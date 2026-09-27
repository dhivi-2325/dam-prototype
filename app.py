from flask import Flask, render_template, request, jsonify
from simulation import run_simulation

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():

    data = request.get_json()

    try:
        dam_height = float(data["dam_height"])
        water_level = float(data["water_level"])
        breach_width = float(data["breach_width"])
        breach_time = float(data["breach_time"])

        result = run_simulation(
            dam_height,
            water_level,
            breach_width,
            breach_time
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)