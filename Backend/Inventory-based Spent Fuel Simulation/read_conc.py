#Read concentrations
def debug_read_conc(chooser):
    
    import h5py
    import pandas as pd
    from pathlib import Path
    import openmc.deplete
    import os
    import pickle
    import numpy as np

    results_path = Path(chooser.selected_path) / "depletion_results.h5"
    results = openmc.deplete.Results(results_path)

    # Open the HDF5 file and read the nuclides
    with h5py.File(results_path, 'r') as file:
        # Access the `results` data
        index_mat_dict = results[0].index_mat  # Access the indices and materials
        print("Available indices:", index_mat_dict.keys())  # List of available indices

        # Dynamic selection of an index
        selected_index = None
        for index in index_mat_dict.keys():
            material = index_mat_dict[index]  # Material for index
            print(f"Material for index {index}: {material}")
            
            # Select the index (e.g., based on the material index)
            # Here, we take the first index to work with the concentrations
            if selected_index is None:
                selected_index = index  

        if selected_index is None:
            raise ValueError("No valid index found!")

        print(f"Selected index: {selected_index}")

        # Access the nuclides group
        nuclides_group = file['nuclides']

        # Create an empty dictionary to store the nuclide concentrations
        concentrations = {}

        # Iterate over all nuclides in the nuclides group
        for nuclide_name in nuclides_group.keys():
            nuclide = nuclides_group[nuclide_name]
            
            # Use the selected index
            time, conc = results.get_atoms(str(selected_index), nuclide_name, nuc_units="atom/cm3")  # Dynamisch mit selected_index
            
            # Store the concentration for each nuclide
            concentrations[nuclide_name] = conc

        # Take the time points of the nuclides
        if concentrations:
            sample_nuclide = list(concentrations.keys())[0]
            time, _ = results.get_atoms(str(selected_index), sample_nuclide)

            time /= (365 * 24 * 60 * 60)  # Optional: Convertion to years
            # Output the time points and concentrations
            print("time steps [a]:", time)
            
            # Iterate over all stored concentrations and output them formatted
            for nuclide_name, conc in concentrations.items():
                formatted_nuclide_name = nuclide_name[0].lower() + nuclide_name[1:]  # Adjust the formatting
                print(f"n_{nuclide_name}: {conc}")  # Output concentration
        else:
            print("No nuclides found.")
