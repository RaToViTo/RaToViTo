import numpy as np


def find_intersections(x, y, target_value):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    intersections = []

    for i in range(len(y) - 1):
        y1 = y[i] - target_value
        y2 = y[i + 1] - target_value

        # Exakter Treffer
        if y1 == 0:
            intersections.append(x[i])

        # Kurve kreuzt target_value zwischen zwei Punkten
        elif y1 * y2 < 0:
            x_intersection = x[i] + (
                (target_value - y[i])
                * (x[i + 1] - x[i])
                / (y[i + 1] - y[i])
            )
            intersections.append(x_intersection)

    # Letzten Punkt berücksichtigen
    if len(y) > 0 and y[-1] == target_value:
        intersections.append(x[-1])

    return intersections


def print_curve_intersections(group_rt, adjusted_time_steps, target_value):
    """
    Find and print all intersections between curves and a target value.
    """

    for name, curve_data in group_rt.items():
        if np.all(curve_data == 0):
            continue

        # Handle multidimensional curve data
        if len(curve_data.shape) > 1:
            for i in range(curve_data.shape[0]):
                single_curve = curve_data[i, :]

                intersections = find_intersections(
                    adjusted_time_steps,
                    single_curve,
                    target_value,
                )

                if intersections:
                    formatted_intersections = [
                        f"{round(float(t), 2)} years"
                        for t in intersections
                    ]
                    print(
                        f"The curve '{name}' (row {i + 1}) "
                        f"intersects the target value {target_value} "
                        f"at: {formatted_intersections}"
                    )
                else:
                    print(
                        f"The curve '{name}' (row {i + 1}) "
                        f"does not intersect the target value "
                        f"{target_value}."
                    )

            continue

        # Handle one-dimensional curve data
        intersections = find_intersections(
            adjusted_time_steps,
            curve_data,
            target_value,
        )

        if intersections:
            formatted_intersections = [
                f"{round(float(t), 2)} years"
                for t in intersections
            ]
            print(
                f"The curve '{name}' intersects the target value "
                f"{target_value} at: {formatted_intersections}"
            )
        else:
            print(
                f"The curve '{name}' does not intersect the target "
                f"value {target_value}."
            )
