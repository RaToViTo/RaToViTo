def read_RTs(chooser):

    import os
    import pickle

    rt_data = {}

    for folder in os.listdir(chooser.selected_path):
        folder_path = os.path.join(chooser.selected_path, folder)
        if os.path.isdir(folder_path) and folder.startswith("depletion_"):
            isotope = folder.replace("depletion_", "")
            
            rt_file = os.path.join(folder_path, "RT.pkl")
            if not os.path.exists(rt_file):
                print(f"RT file {rt_file} not found – skipping {folder}.")
                continue
            
            with open(rt_file, "rb") as f:
                rt_dict = pickle.load(f)
            
            rt_sum = rt_dict.get("RT_sum")
            if rt_sum is None:
                print(f"No 'RT_sum' found in {rt_file}.")
                continue
            
            rt_data[isotope] = rt_sum
            formatted_rt_sum = [f"{float(x):.6e}" for x in rt_sum]
            print(f"RT sum for {isotope}: {formatted_rt_sum}\n")

    print("All RT values successfully read and displayed.")
    return rt_data
