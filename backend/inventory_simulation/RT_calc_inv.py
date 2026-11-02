def RT_calc_inv(chooser, excel_file_DC, selected_DC, excel_file_fuel, selected_sheet):
    
    import h5py
    import pandas as pd
    from pathlib import Path
    import openmc.deplete
    import os
    import pickle
    import numpy as np

    print("Starting RT calculation...")

    def get_selected_index(results):
        index_mat_dict = results[0].index_mat
        selected_index = list(index_mat_dict.keys())[0]
        print(f"Material index used: {selected_index}")
        return selected_index

    results_path = Path(chooser.selected_path) / "depletion_results.h5"
    results = openmc.deplete.Results(results_path)
    selected_index = get_selected_index(results)

    # Function to normalize nuclide names
    def normalize_nuclide_name(nuclide_name):
        """Appends '_m1' to isotopes ending with 'm'."""
        if nuclide_name.endswith('m') and not nuclide_name.endswith('_m1'):
            return nuclide_name + '_m1'  # Example: Rh101m -> Rh101_m1
        return nuclide_name

    # Read DC excel file
    df = pd.read_excel(excel_file_DC, sheet_name=selected_DC, engine='openpyxl')

    # Dictionaries for decay constants and DC values
    decay_constants = {}
    DC_values = {}

    # Extract decay constants and DC values from the Excel file
    for index, row in df.iterrows():
        try:
            # Assumption: Isotope name is in the first column (index 0)
            isotope = str(row.iloc[0]).strip()  # Isotope name
            decay_constant = float(str(row.iloc[2]).replace(',', '.'))  # Decay constant
            DC_value = float(str(row.iloc[3]).replace(',', '.'))  # DC value

            # Store in dictionaries
            decay_constants[isotope] = decay_constant
            DC_values[isotope] = DC_value

        except ValueError as ve:
            # print(f"Error processing row {index + 1}: {ve}. Skipping this row.")
            pass
        except Exception as e:
            # print(f"General error in row {index + 1}: {e}. Skipping this row.")
            pass

    #Import fuel density
    df = pd.read_excel(excel_file_fuel, sheet_name=selected_sheet, skiprows=1)
    fuel_density = df["Fuel Density [g/cc]"].dropna().iloc[0]
    
    
    # Open HDF5 file
    with h5py.File(results_path, 'r') as file:

        # Access the nuclides group
        nuclides_group = file['nuclides']

        # Extract time vector
        sample_nuclide = list(nuclides_group.keys())[0]
        time, _ = results.get_atoms(str(selected_index), sample_nuclide)
        time /= (365 * 24 * 60 * 60)  # Seconds → Years

        # Extract concentrations
        concentrations = {}
        for nuclide_name in nuclides_group.keys():
            _, conc = results.get_atoms(str(selected_index), nuclide_name, nuc_units="atom/cm3")
            concentrations[nuclide_name] = conc
        
        RT_results = {}

        # Iterate over all nuclides in the HDF5 file
        for nuclide_name in nuclides_group.keys():
            # Skip nuclides with the suffix '_m2'
            if nuclide_name.endswith('_m2'):
                continue

            # Normalize the nuclide name
            nuclide_name_normalized = normalize_nuclide_name(nuclide_name)

            # Check if decay constant and DC value are available
            if nuclide_name_normalized in decay_constants and nuclide_name_normalized in DC_values:
                decay_constant = decay_constants[nuclide_name_normalized]
                DC_value = DC_values[nuclide_name_normalized]

                try:
                    # Retrieve concentrations
                    time, concentrations = results.get_atoms(str(selected_index), nuclide_name, nuc_units="atom/cm3")

                    # Debugging line: Output retrieved concentrations
                    # print(f"Retrieved concentrations for {nuclide_name}: {concentrations}")

                    # Step 1: Convert concentration from n/cm^3 to n/g
                    concentrations_ng = [value / fuel_density for value in concentrations]

                    # Step 2: Convert concentration from n/g to n/(metric) tonne
                    concentrations_nt = [value * 1_000_000 for value in concentrations_ng]

                    # Calculate activity (concentration * decay constant)
                    activity = [value * decay_constant for value in concentrations_nt]

                    # Calculate RT (activity * DC value)
                    RT = [a * DC_value for a in activity]

                    # Store the results
                    RT_results[nuclide_name] = RT
                except Exception as e:
                    print(f"Error retrieving data for {nuclide_name}: {e}")
            else:
                # print(f"Decay constant or DC value not found for {nuclide_name_normalized}.")
                continue


    # Function to format the output
    def format_float_list(float_list, num_values=100):
        return '[' + ', '.join(f'{x:.6e}' for x in float_list[:num_values]) + (', ...' if len(float_list) > num_values else '') + ']'

    # Ausgabe der Ergebnisse
    # print("\nRT values computed:")
    # for nuclide, rt in RT_results.items():
        # print(f"{nuclide}: {format_float_list(rt)}")

    print(f"\nNumber of computed isotopes: {len(RT_results)}")
    # if time is not None:
        # print(f"Time steps: {format_float_list(time)}")

    # Save RT data as RT.pkl
    pickle_file = Path(chooser.selected_path) / "RT.pkl"

    # Prepare data for saving
    data_to_save = {
        'times': time,
        'RT_results': RT_results
    }

    # Function to save data with Pickle
    def save_data_with_pickle(data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    # Save data in output_dir
    save_data_with_pickle(data_to_save, pickle_file)
    
    # Load RT.pkl
    with open(pickle_file, 'rb') as f:
        loaded_data = pickle.load(f)

    # Extract RT results and times from the loaded data
    times = loaded_data.get('times', [])
    RT_results = loaded_data.get('RT_results', {})

    # Convert time from seconds to years
    times_in_years = [t / (3.154e+7) for t in times]  # Convert to years
    times_in_years

    plot_dir = chooser.selected_path
    print(f"RT calculation completed and results saved!")


    return RT_results