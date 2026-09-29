import pickle
from pathlib import Path


def read_RTs_inv(chooser):
    rt_file = Path(chooser.selected_path) / "RT.pkl"
    with rt_file.open("rb") as file:
        data = pickle.load(file)

    rt_results = data.get("RT_results", {})
    for nuclide, values in rt_results.items():
        formatted_values = [f"{float(value):.6e}" for value in values]
        print(f"RT sum for {nuclide}: {formatted_values}")

    print("All inventory radiotoxicity values successfully read and displayed.")
    return rt_results