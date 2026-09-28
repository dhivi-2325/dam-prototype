import numpy as np


def run_simulation(
    scenario,
    water_level,
    breach_width,
    breach_time,
    dam_height=None
):

    # ==========================================
    # GRID SIZE
    # ==========================================

    size = 80

    x = np.linspace(-4, 4, size)
    y = np.linspace(-4, 4, size)

    X, Y = np.meshgrid(x, y)


    # ==========================================
    # SYNTHETIC TERRAIN
    # ==========================================

    terrain = (
        15
        + 2.0 * np.abs(Y)
        + 0.8 * X**2
        + 0.5 * np.sin(X * 2)
    )


    # ==========================================
    # SOURCE LOCATION
    # ==========================================

    source_x = 0
    source_y = 0


    distance = np.sqrt(
        (X - source_x) ** 2
        +
        (Y - source_y) ** 2
    )


    # ==========================================
    # WATER DEPTH
    # ==========================================

    if scenario == "dam_breach":

        # Water level cannot exceed dam height

        if dam_height is not None:

            effective_water_level = min(
                water_level,
                dam_height
            )

        else:

            effective_water_level = water_level


    else:

        # Natural lake outbreak

        effective_water_level = water_level


    source_depth = max(
        effective_water_level - terrain.min(),
        1
    )


    # ==========================================
    # BREACH / OUTBURST FACTOR
    # ==========================================

    breach_factor = np.clip(
        breach_width / 20,
        0.2,
        2.0
    )


    # ==========================================
    # TIME FACTOR
    # ==========================================

    time_factor = np.clip(
        60 / max(breach_time, 1),
        0.2,
        2.0
    )


    # ==========================================
    # PROPAGATION DISTANCE
    # ==========================================

    propagation_distance = (
        3.5
        * breach_factor
        * time_factor
    )


    # ==========================================
    # FLOOD DEPTH
    # ==========================================

    flood_depth = (

        source_depth

        *

        np.exp(
            -distance
            /
            propagation_distance
        )

        *

        breach_factor

    )


    # Remove negative values

    flood_depth = np.maximum(
        flood_depth,
        0
    )


    # ==========================================
    # LIMIT FLOOD EXTENT
    # ==========================================

    flood_depth[
        distance >
        propagation_distance * 1.5
    ] = 0


    # ==========================================
    # MAXIMUM FLOOD DEPTH
    # ==========================================

    max_depth = float(
        np.max(flood_depth)
    )


    # ==========================================
    # CELL AREA
    # ==========================================

    cell_area = 100


    # ==========================================
    # RISK CLASSIFICATION
    # ==========================================

    risk = np.zeros_like(
        flood_depth,
        dtype=int
    )


    # LOW RISK
    # 0.5 - 1.5 m

    risk[
        (flood_depth > 0.5)
        &
        (flood_depth <= 1.5)
    ] = 1


    # MEDIUM RISK
    # 1.5 - 3 m

    risk[
        (flood_depth > 1.5)
        &
        (flood_depth <= 3)
    ] = 2


    # HIGH RISK
    # > 3 m

    risk[
        flood_depth > 3
    ] = 3


    # ==========================================
    # AREA CALCULATIONS
    # ==========================================

    total_inundated_cells = np.sum(
        flood_depth > 0.5
    )

    high_risk_cells = np.sum(
        risk == 3
    )

    medium_risk_cells = np.sum(
        risk == 2
    )

    low_risk_cells = np.sum(
        risk == 1
    )


    # ==========================================
    # AREA VALUES
    # ==========================================

    inundated_area = (
        total_inundated_cells
        * cell_area
    )

    high_risk_area = (
        high_risk_cells
        * cell_area
    )

    medium_risk_area = (
        medium_risk_cells
        * cell_area
    )

    low_risk_area = (
        low_risk_cells
        * cell_area
    )


    # ==========================================
    # MAP POINTS
    # ==========================================

    points = []


    # Take every second grid point
    # to keep the map lightweight

    for i in range(0, size, 2):

        for j in range(0, size, 2):

            if flood_depth[i, j] > 0.5:

                points.append({

                    "lat":
                        float(
                            11.0
                            +
                            Y[i, j] * 0.01
                        ),

                    "lon":
                        float(
                            78.0
                            +
                            X[i, j] * 0.01
                        ),

                    "depth":
                        round(
                            float(
                                flood_depth[i, j]
                            ),
                            2
                        ),

                    "risk":
                        int(
                            risk[i, j]
                        )

                })


    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return {

        "max_depth":
            round(
                max_depth,
                2
            ),

        "inundated_area":
            round(
                float(
                    inundated_area
                ),
                2
            ),

        "high_risk_area":
            round(
                float(
                    high_risk_area
                ),
                2
            ),

        "medium_risk_area":
            round(
                float(
                    medium_risk_area
                ),
                2
            ),

        "low_risk_area":
            round(
                float(
                    low_risk_area
                ),
                2
            ),

        "points":
            points

    }