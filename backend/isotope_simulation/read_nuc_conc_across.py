def read_nuc_conc_across(chooser, target_nuclide_2):

    import os
    import pickle

    collected_values = {}

    # Cycle through all folders in the base folder
    for folder in os.listdir(chooser.selected_path):
        folder_path = os.path.join(chooser.selected_path, folder)
        if os.path.isdir(folder_path):
            pickle_file = os.path.join(folder_path, "concentrations.pkl")
            if os.path.exists(pickle_file):
                with open(pickle_file, "rb") as f:
                    concentrations = pickle.load(f)
                if target_nuclide_2 in concentrations:
                    collected_values[folder] = concentrations[target_nuclide_2]
                else:
                    print(f"{target_nuclide_2} not found in {folder}.")
            else:
                print(f"The file '{pickle_file}' could not be found in {folder}.")

    # Output of the collected values in scientific notation
    print(f"Concentrations for {target_nuclide_2}:")
    for folder, values in collected_values.items():
        formatted_values = [f"{float(x):.6e}" for x in values]
        print(f"{folder}: {formatted_values}")