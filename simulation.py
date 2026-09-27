import numpy as np


def run_simulation(
    dam_height,
    water_level,
    breach_width,
    breach_time
):

    # Create a simple terrain grid
    size = 80

    x = np.linspace(-4, 4, size)
    y = np.linspace(-4, 4, size)

    X, Y = np.meshgrid(x, y)

    # Create synthetic valley terrain
    terrain = (
        15
        + 2.0 * np.abs(Y)
        + 0.8 * X**2
        + 0.5 * np.sin(X * 2)
    )

    # Dam location
    dam_x = 0
    dam_y = 0

    # Distance from dam
    distance = np.sqrt(
        (X - dam_x)**2 +
        (Y - dam_y)**2
    )

    # Initial flood source depth
    source_depth = max(
        water_level - terrain.min(),
        1
    )

    # Breach effect
    breach_factor = np.clip(
        breach_width / 20,
        0.2,
        2.0
    )

    # Breach time effect
    time_factor = np.clip(
        60 / max(breach_time, 1),
        0.2,
        2.0
    )

    # Flood propagation distance
    propagation_distance = (
        3.5 *
        breach_factor *
        time_factor
    )

    # Calculate flood depth
    flood_depth = (
        source_depth *
        np.exp(
            -distance /
            propagation_distance
        ) *
        breach_factor
    )

    flood_depth = np.maximum(
        flood_depth,
        0
    )

    # Remove areas outside flood region
    flood_depth[
        distance >
        propagation_distance * 1.5
    ] = 0

    # Maximum flood depth
    max_depth = float(
        np.max(flood_depth)
    )

    # Calculate inundated area
    cell_area = 100

    inundated_cells = np.sum(
        flood_depth > 0.5
    )

    inundated_area = float(
        inundated_cells *
        cell_area
    )

    # Risk classification
    risk = np.zeros_like(
        flood_depth,
        dtype=int
    )

    risk[
        (flood_depth > 0.5) &
        (flood_depth <= 1.5)
    ] = 1

    risk[
        (flood_depth > 1.5) &
        (flood_depth <= 3)
    ] = 2

    risk[
        flood_depth > 3
    ] = 3

    # Create map points
    points = []

    for i in range(0, size, 2):

        for j in range(0, size, 2):

            if flood_depth[i, j] > 0.5:

                points.append({

                    "lat":
                        float(
                            11.0 +
                            Y[i, j] * 0.01
                        ),

                    "lon":
                        float(
                            78.0 +
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

    return {

        "max_depth":
            round(max_depth, 2),

        "inundated_area":
            round(inundated_area, 2),

        "points":
            points
    }