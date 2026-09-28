from flask import Flask, render_template, request, jsonify
from simulation import run_simulation

app = Flask(__name__)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# DAM BREACH PAGE
# ==========================================

@app.route("/dam-breach")
def dam_breach():
    return render_template("dam_breach.html")


# ==========================================
# NATURAL OUTBREAK PAGE
# ==========================================

@app.route("/natural-outbreak")
def natural_outbreak():
    return render_template("natural_outbreak.html")


# ==========================================
# DASHBOARD PAGE
# ==========================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ==========================================
# SIMULATION
# ==========================================

@app.route("/simulate", methods=["POST"])
def simulate():

    data = request.get_json() or {}

    try:

        # Get scenario
        scenario = data.get("scenario")

        # ======================================
        # DAM BREACH
        # ======================================

        if scenario == "dam_breach":

            dam_name = data.get("dam_name", "").strip()

            dam_height = float(
                data["dam_height"]
            )

            water_level = float(
                data["water_level"]
            )

            breach_width = float(
                data["breach_width"]
            )

            breach_time = float(
                data["breach_time"]
            )


            # Check dam selection

            if dam_name == "":
                raise ValueError(
                    "Please select a dam."
                )


            # Run simulation

            result = run_simulation(

                scenario="dam_breach",

                dam_height=dam_height,

                water_level=water_level,

                breach_width=breach_width,

                breach_time=breach_time

            )


            # Add information for dashboard

            result["scenario"] = "Dam Breach"

            result["location_name"] = dam_name


        # ======================================
        # NATURAL OUTBREAK
        # ======================================

        elif scenario == "natural_outbreak":

            lake_name = data.get(
                "lake_name",
                ""
            ).strip()


            water_level = float(
                data["water_level"]
            )

            outburst_width = float(
                data["breach_width"]
            )

            outburst_time = float(
                data["breach_time"]
            )


            # Check lake selection

            if lake_name == "":
                raise ValueError(
                    "Please select a natural lake."
                )


            # Run simulation

            result = run_simulation(

                scenario="natural_outbreak",

                water_level=water_level,

                breach_width=outburst_width,

                breach_time=outburst_time

            )


            # Add information for dashboard

            result["scenario"] = "Natural Outbreak"

            result["location_name"] = lake_name


        # ======================================
        # INVALID SCENARIO
        # ======================================

        else:

            raise ValueError(
                "Invalid scenario selected."
            )


        # ======================================
        # SEND RESULT TO FRONTEND
        # ======================================

        return jsonify({

            "success": True,

            "result": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)