def simulation_inv(project_root, main_output_dir, excel_file_fuel, time_steps, selected_sheet, selected_DC, chain_file):
    
    import os
    import sys
    import math
    import openmc
    import shutil
    import pickle
    import random
    import numpy as np
    import pandas as pd
    import openmc.deplete
    from pathlib import Path
    from datetime import datetime
    import matplotlib.pyplot as plt
    from IPython.display import Image, display
    from openmc.deplete import IndependentOperator, MicroXS

    print(f"Starting simulation...")

    os.chdir(project_root)

    # Empty Data for Depletion-Operator
    empty_data = np.empty((0, 0))
    empty_nuclides = []
    empty_reactions = []
    empty_micro_xs = openmc.deplete.MicroXS(empty_data, empty_nuclides, empty_reactions)
    empty_fluxes = [None]

    # New subfolder for all depletion simulations in the sim results folder
    timestamp_results = datetime.now().strftime('%Y%m%d_%H%M%S')
    simulations_dir = project_root / "Simulation results" / f"{timestamp_results}_{selected_sheet}_{selected_DC}_Inventory-based Spent Fuel Simulation_results"
    os.makedirs(simulations_dir, exist_ok=True)

    # Data import from excel
    df = pd.read_excel(str(excel_file_fuel), sheet_name=selected_sheet, skiprows=1)  # Skip first row

    # Global value for percent_type (assumed for all rows)
    percent_type = df["Percent_Type"].dropna().iloc[0]

    # List of all isotopes from the Excel file
    all_isotopes = df["Nuclide"].dropna().unique()

    def save_concentrations(results_file, output_dir):
        # Load results
        results = openmc.deplete.Results(results_file)
        
        # Determination of the material index (first material)
        index_mat_dict = results[0].index_mat
        selected_index = list(index_mat_dict.keys())[0]
        print(f"Material index used: {selected_index}")
        
        concentrations = {}
        
        # Iterate over all nuclides present in the first result
        for nuclide_name in results[0].index_nuc.keys():
            try:
                # Time and concentration (in “atom/cm3”) are extracted for each nuclide
                time, conc = results.get_atoms(str(selected_index), nuclide_name, nuc_units="atom/cm3")
                concentrations[nuclide_name] = conc
            except Exception as e:
                print(f"Error when extracting {nuclide_name}: {e}")
        
        # Saving the concentration dictionary as a pickle file
        pickle_file = os.path.join(output_dir, "concentrations.pkl")
        with open(pickle_file, 'wb') as f:
            pickle.dump(concentrations, f)
        print(f"concentrations.pkl saved in {pickle_file}")

        return selected_index

    # Simulation
    # Get global values such as `percent_type` and `fuel_density` directly from the relevant cells
    percent_type = df["Percent_Type"].dropna().iloc[0]  # Take the first non-empty value
    fuel_density = df["Fuel Density [g/cc]"].dropna().iloc[0]

    # Create the Spent Fuel material for the current isotope (name: SpentFuel_<isotope>)
    spent_fuel = openmc.Material(name="SpentFuel")
    spent_fuel.volume = 1.0
    spent_fuel.depletable = True
    spent_fuel.set_density("g/cc", fuel_density)

    # Add nuclide elements
    if percent_type == "wo":
        fraction_col = "w%"
    else:
        fraction_col = "a%"

    for _, row in df.iterrows():
        # For SF material: Add nuclides
        if not pd.isna(row["Nuclide"]):  # Consider only nuclides
            spent_fuel.add_nuclide(row["Nuclide"], row[fraction_col], percent_type=percent_type)

    # Summarize materials
    materials = openmc.Materials([spent_fuel])

    # Create OpenMC operator with the new material
    operator = openmc.deplete.IndependentOperator(materials, empty_fluxes, [empty_micro_xs], chain_file)

    power = 0.0  # No neutron flux, only decay

    # Create OpenMC integrator for this single simulation
    integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power, timestep_units='a')

    # Subfolder for this isotope in simulations_dir
    output_dir = simulations_dir

    original_cwd = os.getcwd()
    os.chdir(output_dir)

    # Start simulation
    integrator.integrate()

    os.chdir(original_cwd)

    # Save results as pickle
    depletion_results_file = os.path.join(output_dir, "depletion_results.h5")
    if os.path.exists(depletion_results_file):
        selected_index = save_concentrations(depletion_results_file, output_dir)
    else:
        print(f"Depletion result file not found in {output_dir}")
        selected_index = None

    print("\nSimulation completed!")
    #return selected_index