def read_conc_parent_DPs(chooser, target_nuclide_1):

    import os
    import pickle

    simulation_folder = os.path.join(chooser.selected_path, f"depletion_{target_nuclide_1}")
    pickle_file = os.path.join(simulation_folder, "concentrations.pkl")

    if not os.path.exists(pickle_file):
        print(f"The file '{pickle_file}' could not be found!")
    else:
        with open(pickle_file, 'rb') as f:
            concentrations = pickle.load(f)

        print(f"Concentrations of nuclide {target_nuclide_1}':")
        for nuclide_name, conc_values in concentrations.items():
            print(f"{nuclide_name}: {conc_values}")