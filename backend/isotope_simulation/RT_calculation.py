def RT_calculation(chooser, excel_file_fuel, selected_sheet, excel_file_DC, selected_DC):

    import os
    import pickle
    import openmc
    import openmc.deplete
    import numpy as np
    import pandas as pd

    print("Starting RT calculation...")

    def extract_timesteps(chooser):

        time_steps = None
        for folder in os.listdir(chooser.selected_path):
            folder_path = os.path.join(chooser.selected_path, folder)
            if os.path.isdir(folder_path) and folder.startswith("depletion_"):
                depletion_results_file = os.path.join(folder_path, "depletion_results.h5")
                if os.path.exists(depletion_results_file):
                    results = openmc.deplete.Results(depletion_results_file)
                    selected_index = list(results[0].index_mat.keys())[0]
                    sample_nuclide = list(results[0].index_nuc.keys())[0]
                    time_sec, _ = results.get_atoms(str(selected_index), sample_nuclide, nuc_units="atom/cm3")
                    time_steps = time_sec / 31557600.0  # convert seconds to years

                    # Save time_steps as .pkl
                    pkl_path = os.path.join(chooser.selected_path, "time_steps.pkl")
                    with open(pkl_path, "wb") as f:
                        pickle.dump(time_steps, f)
                    # print(f"time_steps extracted and saved to: {pkl_path}")
                    break

        if time_steps is None:
            raise ValueError("No depletion_results.h5 found in the base folder.")

        return time_steps

    time_steps = extract_timesteps(chooser)

    #Import fuel density
    df = pd.read_excel(excel_file_fuel, sheet_name=selected_sheet, skiprows=1)
    fuel_density = df["Fuel Density [g/cc]"].dropna().iloc[0]

    # Import decay_constants and DCs
    def load_decay_data(excel_file_DC, selected_DC):
        df_dc = pd.read_excel(excel_file_DC, sheet_name=selected_DC, engine='openpyxl', header=2)
        decay_constants = {}
        DC_values = {}
        for index, row in df_dc.iterrows():
            try:
                isotope = str(row.iloc[0]).strip()
                decay_constants[isotope] = float(str(row.iloc[2]).replace(',', '.'))
                DC_values[isotope] = float(str(row.iloc[3]).replace(',', '.'))
            except Exception as e:
                print(f"Error in line {index}: {e} – Line skipped.")

        return decay_constants, DC_values

    decay_constants, DC_values = load_decay_data(excel_file_DC, selected_DC)

    # Function of RT-Calculation
    def calculate_rt_sum(concentrations, fuel_density, decay_constants, DC_values):
        rt_arrays = []
        for nuclide, conc_values in concentrations.items():
            conc_arr = np.array(conc_values, dtype=float)
            norm_name = nuclide
            if norm_name.endswith('m') and not norm_name.endswith('_m1'):
                norm_name += '_m1'
            if norm_name in decay_constants and norm_name in DC_values:
                d_const = decay_constants[norm_name]
                DC_val = DC_values[norm_name]
                rt_arr = conc_arr * d_const * DC_val
                rt_arrays.append(rt_arr)
            else:
                pass
        if rt_arrays:
            rt_sum_unnorm = np.nansum(np.array(rt_arrays), axis=0)
            rt_sum_norm = (rt_sum_unnorm / fuel_density) * 1e6
        else:
            rt_sum_norm = np.array([])
        return rt_sum_norm

    # Iterate over all Subfolders (mother nuclides)
    rt_data = {}  # Saves RT-sum-arry for each nuclide

    for folder in os.listdir(chooser.selected_path):
        folder_path = os.path.join(chooser.selected_path, folder)
        if os.path.isdir(folder_path) and folder.startswith("depletion_"):
            # Extract nuclide name (e.g."depletion_U235" -> "U235")
            isotope = folder.replace("depletion_", "")
            
            conc_file = os.path.join(folder_path, "concentrations.pkl")
            if not os.path.exists(conc_file):
                print(f"File {conc_file} not found – skipping {folder}.")
                continue
            with open(conc_file, "rb") as f:
                concentrations = pickle.load(f)
            # Calculation RT sum
            rt_sum = calculate_rt_sum(concentrations, fuel_density, decay_constants, DC_values)
            rt_data[isotope] = rt_sum
            
            # Output of RT sum (per nuclide)
            #print(f"\nNuclide '{isotope}' processed:")
            #print(f"Time steps (years): {[f'{t:.6e}' for t in time_steps]}")
            formatted_rt_sum = [f"{float(x):.6e}" for x in rt_sum]
            #print(f"RT sum for {isotope}: {formatted_rt_sum}")
            
            # Save in RT.pkl with time_steps
            rt_dict = {'RT_sum': rt_sum.tolist(), 'time_steps': time_steps.tolist()}
            rt_file = os.path.join(folder_path, "RT.pkl")
            with open(rt_file, "wb") as f:
                pickle.dump(rt_dict, f)
            #print(f"RT of {isotope} calculated and saved in {rt_file}.")

    print(f"RT calculation completed and results saved!")

    return rt_data
