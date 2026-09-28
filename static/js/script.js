// ==========================================
// RUN SIMULATION
// ==========================================

async function runSimulation() {

    const damHeight =
        document.getElementById("dam_height").value;

    const waterLevel =
        document.getElementById("water_level").value;

    const breachWidth =
        document.getElementById("breach_width").value;

    const breachTime =
        document.getElementById("breach_time").value;


    try {

        const response = await fetch(
            "/simulate",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    scenario: "dam_breach",

                    dam_name:
                        document.getElementById(
                            "dam_name"
                        ).value,

                    dam_height:
                        damHeight,

                    water_level:
                        waterLevel,

                    breach_width:
                        breachWidth,

                    breach_time:
                        breachTime

                })

            }
        );


        const data =
            await response.json();


        // ======================================
        // CHECK FOR ERROR
        // ======================================

        if (!data.success) {

            alert(data.error);

            return;

        }


        // ======================================
        // GET RESULT
        // ======================================

        const result =
            data.result;


        // ======================================
        // SAVE RESULT FOR DASHBOARD
        // ======================================

        sessionStorage.setItem(
            "simulationResult",
            JSON.stringify(result)
        );


        // ======================================
        // OPEN DASHBOARD
        // ======================================

        window.location.href =
            "/dashboard";


    }

    catch (error) {

        alert(
            "Error connecting to server."
        );

        console.error(error);

    }

}


// ==========================================
// CREATE FLOOD RISK MAP
// ==========================================

function createMap(points) {

    const mapElement =
        document.getElementById("map");


    // Clear old map

    mapElement.innerHTML = "";


    // ======================================
    // NO FLOOD DATA
    // ======================================

    if (
        !points ||
        points.length === 0
    ) {

        mapElement.innerHTML =
            "<p>No significant inundation detected.</p>";

        return;

    }


    // ======================================
    // MAP CENTER
    // ======================================

    const centerLat =
        points[0].lat;

    const centerLon =
        points[0].lon;


    // ======================================
    // CREATE MAP
    // ======================================

    const map =
        L.map("map")
        .setView(
            [
                centerLat,
                centerLon
            ],
            13
        );


    // ======================================
    // OPENSTREETMAP
    // ======================================

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {

            attribution:
                "&copy; OpenStreetMap contributors"

        }

    ).addTo(map);


    // ======================================
    // ADD FLOOD POINTS
    // ======================================

    points.forEach(
        point => {


            let color =
                "green";


            // LOW RISK

            if (
                point.risk === 1
            ) {

                color =
                    "green";

            }


            // MEDIUM RISK

            if (
                point.risk === 2
            ) {

                color =
                    "orange";

            }


            // HIGH RISK

            if (
                point.risk === 3
            ) {

                color =
                    "red";

            }


            // ==================================
            // CREATE CIRCLE
            // ==================================

            L.circleMarker(

                [
                    point.lat,
                    point.lon
                ],

                {

                    radius: 6,

                    color:
                        color,

                    fillColor:
                        color,

                    fillOpacity:
                        0.7

                }

            )


            // ==================================
            // POPUP
            // ==================================

            .bindPopup(

                "<b>Flood Depth:</b> "
                + point.depth
                + " m<br>"

                + "<b>Risk Level:</b> "
                + getRiskName(
                    point.risk
                )

            )


            .addTo(map);

        }
    );

}


// ==========================================
// RISK NAME
// ==========================================

function getRiskName(risk) {

    if (risk === 3) {

        return "High";

    }

    if (risk === 2) {

        return "Medium";

    }

    if (risk === 1) {

        return "Low";

    }

    return "No Risk";

}