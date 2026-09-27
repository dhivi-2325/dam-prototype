async function runSimulation() {

    const damHeight =
        document.getElementById(
            "dam_height"
        ).value;


    const waterLevel =
        document.getElementById(
            "water_level"
        ).value;


    const breachWidth =
        document.getElementById(
            "breach_width"
        ).value;


    const breachTime =
        document.getElementById(
            "breach_time"
        ).value;


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


        if (!data.success) {

            alert(data.error);

            return;
        }


        const result =
            data.result;


        document.getElementById(
            "max_depth"
        ).innerText =
            result.max_depth;


        document.getElementById(
            "area"
        ).innerText =
            result.inundated_area;


        let riskStatus = "Low";


        if (result.max_depth > 1.5) {

            riskStatus = "Medium";
        }


        if (result.max_depth > 3) {

            riskStatus = "High";
        }


        document.getElementById(
            "risk"
        ).innerText =
            riskStatus;


        createMap(
            result.points
        );

    }

    catch (error) {

        alert(
            "Error connecting to server."
        );

        console.error(error);
    }
}



function createMap(points) {

    const mapElement =
        document.getElementById(
            "map"
        );


    mapElement.innerHTML = "";


    if (points.length === 0) {

        mapElement.innerHTML =
            "<p>No significant inundation detected.</p>";

        return;
    }


    const centerLat =
        points[0].lat;


    const centerLon =
        points[0].lon;


    const map =
        L.map("map")
        .setView(
            [
                centerLat,
                centerLon
            ],
            13
        );


    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {

            attribution:
                "&copy; OpenStreetMap contributors"

        }
    ).addTo(map);


    points.forEach(
        point => {

            let color =
                "blue";


            if (
                point.risk === 2
            ) {

                color =
                    "orange";
            }


            if (
                point.risk === 3
            ) {

                color =
                    "red";
            }


            L.circleMarker(

                [
                    point.lat,
                    point.lon
                ],

                {

                    radius: 6,

                    color: color,

                    fillColor:
                        color,

                    fillOpacity:
                        0.7
                }

            )

            .bindPopup(

                "Flood Depth: "
                + point.depth
                + " m<br>"
                + "Risk Level: "
                + point.risk

            )

            .addTo(map);

        }
    );
}