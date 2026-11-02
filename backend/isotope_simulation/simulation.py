# Simulation of Indivdual Spent Fuel Nuclides
def simulation(project_root, main_output_dir, excel_file_fuel, time_steps, selected_sheet, selected_DC, chain_file):

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

    # Empty Data for Depletion-Operator
    empty_data = np.empty((0, 0))
    empty_nuclides = []
    empty_reactions = []
    empty_micro_xs = openmc.deplete.MicroXS(empty_data, empty_nuclides, empty_reactions)
    empty_fluxes = [None]

    os.makedirs(main_output_dir, exist_ok=True)

    # New subfolder for all depletion simulations in the sim results folder
    timestamp_results = datetime.now().strftime('%Y%m%d_%H%M%S')
    simulations_dir = os.path.join(main_output_dir, f"{timestamp_results}_{selected_sheet}_{selected_DC}_Isotope-based Spent Fuel Simulation_results")
    os.makedirs(simulations_dir, exist_ok=True)

    # Change to the main directory
    os.chdir(project_root)

    # Data import from excel
    df = pd.read_excel(excel_file_fuel, sheet_name=selected_sheet, skiprows=1)  # skip first row

    # Global value for percent_type (assumed for all rows)
    percent_type = df["Percent_Type"].dropna().iloc[0]

    # List of all isotopes from the Excel file
    all_isotopes = df["Nuclide"].dropna().unique()

    # Save start directory
    original_dir = os.getcwd()

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

    # Simulation for each isotope
    for isotope in all_isotopes:
        print(f"Starting simulation for {isotope}...")
        
        # Filter the data for the current isotope
        df_isotope = df[df["Nuclide"] == isotope]
        if df_isotope.empty:
            print(f"No data found for isotope {isotope}. Skipping.")
            continue
        
        # If there are several lines, the first one is used
        row = df_isotope.iloc[0]
        # Individual density and concentration from the Excel file (column “Indiv_Density”)
        indiv_density = row["Indiv_Density"]
        concentration = row["Concentration"]
        
        # Output of the values used
        print(f"For {isotope} is used: Density = {indiv_density} g/cc, Concentration = {concentration}")
        
        # Create the Spent Fuel material for the current isotope (Name: SpentFuel_<Isotop>)
        spent_fuel = openmc.Material(name=f"SpentFuel_{isotope}")
        spent_fuel.volume = 1.0
        spent_fuel.depletable = True
        spent_fuel.set_density("g/cc", indiv_density)
        spent_fuel.add_nuclide(isotope, concentration, percent_type=percent_type)
        
        # Summarize materials
        materials = openmc.Materials([spent_fuel])
        
        # Create OpenMC operator with the new material
        operator = openmc.deplete.IndependentOperator(materials, empty_fluxes, [empty_micro_xs], chain_file)

        power = 0.0  # No neutron flux, only decay
        
        # Create OpenMC integrator for single simulation
        integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power, timestep_units='a')
        
        # Subfolder for this isotope in simulations_dir
        output_dir = os.path.join(simulations_dir, f"depletion_{isotope}")
        shutil.rmtree(output_dir, ignore_errors=True)  # Delete previous results, if available
        os.makedirs(output_dir, exist_ok=True)
        
        # Set working directory to the new folder
        os.chdir(output_dir)
        
        # Start simulation for this isotope
        integrator.integrate()
        
        # Save results as pickle
        depletion_results_file = os.path.join(output_dir, "depletion_results.h5")
        if os.path.exists(depletion_results_file):
            save_concentrations(depletion_results_file, output_dir)
        else:
            print(f"Depletion result file not found in {output_dir}")
        
        # Switch back to the original directory
        os.chdir(original_dir)
        
        print(f"Simulation for {isotope} completed. Results saved in {output_dir}/depletion_results.h5")

    print("\nAll individual simulations completed!")