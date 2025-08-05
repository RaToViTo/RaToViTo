def plot_inv(project_root, chooser, checkboxes, color_pickers, isotope_textboxes, isotope_colors, excel_file_fuel, selected_sheet, selected_DC, save_plot, offset, ref_values, ref_config,  plot_config):

    import os
    import pickle
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    from datetime import datetime
    from IPython.display import Image, display
    from pathlib import Path

    # --- Load RT.pkl ---
    plot_dir = chooser.selected_path
    pickle_file = os.path.join(plot_dir, 'RT.pkl')
    with open(pickle_file, 'rb') as f:
        loaded_data = pickle.load(f)

    times = loaded_data.get('times', [])
    RT_results = loaded_data.get('RT_results', {})

    # --- Convert time to years ---
    times_in_years = [t / (3.154e+7) for t in times]

    # --- GROUP DEFINITIONS ---
    groups_dict = {
        'Total': [],
        'Neptunium': ['Np225', 'Np226', 'Np227', 'Np228', 'Np229', 'Np230', 'Np231', 'Np232', 'Np233', 'Np234', 'Np235', 'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'Np240', 'Np241', 'Np242', 'Np243', 'Np244'],
        'Americium': ['Am231', 'Am232', 'Am233', 'Am234', 'Am235', 'Am236', 'Am237', 'Am238', 'Am239', 'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Am245', 'Am246', 'Am246_m1', 'Am247', 'Am248', 'Am249'],
        'Curium': ['Cm233', 'Cm234', 'Cm235', 'Cm236', 'Cm237', 'Cm238', 'Cm239', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Cm251'],
        'Berkelium': ['Bk235', 'Bk237', 'Bk238', 'Bk240', 'Bk241', 'Bk242', 'Bk243', 'Bk244', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249', 'Bk250', 'Bk251', 'Bk253', 'Bk254'],
        'Californium': ['Cf237', 'Cf238', 'Cf239', 'Cf240', 'Cf241', 'Cf242', 'Cf243', 'Cf244', 'Cf245', 'Cf246', 'Cf247', 'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cf255', 'Cf256'],
        'Einsteinium': ['Es240', 'Es241', 'Es242', 'Es243', 'Es244', 'Es245', 'Es246', 'Es247', 'Es248', 'Es249', 'Es250', 'Es251', 'Es252', 'Es253', 'Es254', 'Es254_m1', 'Es255', 'Es256', 'Es257', 'Es258'],
        'Fermium': ['Fm242', 'Fm243', 'Fm244', 'Fm245', 'Fm246', 'Fm247', 'Fm248', 'Fm249', 'Fm250', 'Fm251', 'Fm252', 'Fm253', 'Fm254', 'Fm255', 'Fm256', 'Fm257', 'Fm258', 'Fm259', 'Fm260'],
        'Plutonium': ['Pu228', 'Pu229', 'Pu230', 'Pu231', 'Pu232', 'Pu233', 'Pu234', 'Pu235', 'Pu236', 'Pu237', 'Pu237_m1', 'Pu238', 'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Pu243', 'Pu244', 'Pu245', 'Pu246', 'Pu247'],
        'Uranium': ['U217', 'U218', 'U219', 'U220', 'U222', 'U223', 'U224', 'U225', 'U226', 'U227', 'U228', 'U229', 'U230', 'U231', 'U232', 'U233', 'U234', 'U235', 'U235_m1', 'U236', 'U237', 'U238', 'U239', 'U240', 'U241', 'U242'],
        'Protactinium': ['Pa227', 'Pa228', 'Pa229', 'Pa230', 'Pa231', 'Pa232', 'Pa233', 'Pa234', 'Pa234_m1', 'Pa235', 'Pa236', 'Pa237'],
        'Thorium': ['Th223', 'Th224', 'Th226', 'Th227', 'Th228', 'Th229', 'Th230', 'Th231', 'Th232', 'Th233', 'Th234', 'Th235', 'Th236'],
        'Actinium': ['Ac223', 'Ac224', 'Ac225', 'Ac226', 'Ac227', 'Ac228', 'Ac230', 'Ac231', 'Ac232', 'Ac233'],
        'Mendelevium': ['Md244', 'Md245', 'Md245_m1', 'Md246', 'Md247', 'Md247_m1', 'Md248', 'Md248_m1', 'Md249', 'Md250', 'Md251', 'Md252', 'Md253', 'Md254', 'Md254_m1', 'Md255', 'Md256', 'Md257', 'Md258', 'Md258_m1', 'Md259', 'Md260'],
        'Nobelium': ['No250', 'No251', 'No252', 'No253', 'No254', 'No254_m1', 'No255', 'No256', 'No257', 'No258', 'No259', 'No260', 'No261', 'No262'],
        'Lawrencium': ['Lr252', 'Lr253', 'Lr253_m1', 'Lr254', 'Lr255', 'Lr256', 'Lr257', 'Lr258', 'Lr259', 'Lr260', 'Lr261', 'Lr262'],
        'Minor Actinoides': ['Np225', 'Np226', 'Np227', 'Np228', 'Np229', 'Np230', 'Np231', 'Np232', 'Np233', 'Np234', 'Np235', 'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'Np240', 'Np241', 'Np242', 'Np243', 'Np244', 'Am231', 'Am232', 'Am233', 'Am234', 'Am235', 'Am236', 'Am237', 'Am238', 'Am239', 'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Am245', 'Am246', 'Am246_m1', 'Am247', 'Am248', 'Am249', 'Cm233', 'Cm234', 'Cm235', 'Cm236', 'Cm237', 'Cm238', 'Cm239', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Cm251', 'Bk235', 'Bk237', 'Bk238', 'Bk240', 'Bk241', 'Bk242', 'Bk243', 'Bk244', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249', 'Bk250', 'Bk251', 'Bk253', 'Bk254', 'Cf237', 'Cf238', 'Cf239', 'Cf240', 'Cf241', 'Cf242', 'Cf243', 'Cf244', 'Cf245', 'Cf246', 'Cf247', 'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cf255', 'Cf256', 'Es240', 'Es241', 'Es242', 'Es243', 'Es244', 'Es245', 'Es246', 'Es247', 'Es248', 'Es249', 'Es250', 'Es251', 'Es252', 'Es253', 'Es254', 'Es254_m1', 'Es255', 'Es256', 'Es257', 'Es258', 'Fm242', 'Fm243', 'Fm244', 'Fm245', 'Fm246', 'Fm247', 'Fm248', 'Fm249', 'Fm250', 'Fm251', 'Fm252', 'Fm253', 'Fm254', 'Fm255', 'Fm256', 'Fm257', 'Fm258', 'Fm259', 'Fm260'],
        'Fission Products': [],
        'Decay Products' : []  # All others
    }

    # --- CLASSIFY SELECTIONS ---
    selected_items = [name for name, cb in checkboxes.items() if cb.value]
    selected_groups = [name for name in selected_items if name in groups_dict]
    individual_isotopes = [box.value.strip() for box in isotope_textboxes if box.value.strip()]

    # --- Set Colors ---
    color_map = {}
    for name in selected_items:
        color_map[name] = color_pickers[name].value
    for txt, cp in zip(isotope_textboxes, isotope_colors):
        if txt.value.strip():
            color_map[txt.value.strip()] = cp.value

    # --- Init group sums ---
    group_sums = {}

    # --- Load Isotope List from Excel ---
    fuel_df = pd.read_excel(str(excel_file_fuel), sheet_name=selected_sheet, skiprows=1)
    fuel_df.columns = fuel_df.columns.str.strip()  # Remove spaces if necessary

    # If the column is named "Nuclide":
    nuclide_list = fuel_df['Nuclide'].dropna().astype(str).tolist()

    # --- All Isotopes from Groups ---
    group_isotopes = set()
    for members in groups_dict.values():
        group_isotopes.update(members)

    # --- Fission Isotopes: Excel list minus group isotopes ---
    fission_isotopes = [iso for iso in nuclide_list if iso not in group_isotopes]

    fission_in_rt = [iso for iso in fission_isotopes if iso in RT_results]
    fission_not_in_rt = [iso for iso in fission_isotopes if iso not in RT_results]

    # --- All isotopes in RT.pkl ---
    all_isotopes_in_RT = set(RT_results.keys())

    # --- Decay Isotopes: Everything else in RT.pkl ---
    decay_isotopes = list(all_isotopes_in_RT - group_isotopes - set(fission_isotopes))

    # --- Calculate Fission Products ---
    if "Fission Products" in selected_groups:
        fission_sum = np.zeros(len(times_in_years))
        for iso in fission_isotopes:
            if iso in RT_results:
                fission_sum += np.array(RT_results[iso], dtype=np.float64)
        group_sums["Fission Products"] = fission_sum

    # --- Calculate Decay Products ---
    if "Decay Products" in selected_groups:
        decay_sum = np.zeros(len(times_in_years))
        for iso in decay_isotopes:
            if iso in RT_results:
                decay_sum += np.array(RT_results[iso], dtype=np.float64)
        group_sums["Decay Products"] = decay_sum

    # --- Calculate other groups ---
    for group in selected_groups:
        if group in ["Fission Products", "Decay Products"]:
            continue
        group_sums[group] = np.zeros(len(times))
        for iso in groups_dict[group]:
            if iso in RT_results:
                group_sums[group] += np.array(RT_results[iso], dtype=np.float64)

    # --- Add individual isotopes ---
    for iso in individual_isotopes:
        if iso in RT_results:
            group_sums[iso] = np.array(RT_results[iso], dtype=np.float64)

    # --- Calculate Total ---
    if "Total" in selected_items:
        group_sums["Total"] = np.zeros(len(times))
        for name in selected_groups + individual_isotopes:
            if name != "Total" and name in group_sums:
                group_sums["Total"] += group_sums[name]

    # --- Plotting ---
    fig = plt.figure(figsize=(plot_config["fig_width"], plot_config["fig_height"]), dpi=plot_config["dpi"])
    for i, (label, data) in enumerate(group_sums.items()):
        if not np.any(data > 0):
            continue
        color = color_map.get(label, f"C{i}")
        times_with_offset = [t + offset for t in times_in_years]
        line, = plt.plot(times_with_offset, data, label=label, color=color, linewidth=plot_config["linewidth"])

    # Adding a horizontal line for ref value
    for var_name, config in ref_config.items():
        if var_name in ref_values:
            ref_value = ref_values[var_name]
            plt.axhline(
                y=ref_value,
                label=config["label"],
                linestyle=config["linestyle"],
                linewidth=config["linewidth"],
                color=config["color"]
            )

    # --- Styling ---
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(plot_config["plot_axis_range_x"])
    plt.ylim(plot_config["plot_axis_range_y"])
    plt.xlabel(plot_config["plot_xlabel"], fontsize=plot_config["label_fontsize"], fontname=plot_config["font_name"])
    plt.ylabel(plot_config["plot_ylabel"], fontsize=plot_config["label_fontsize"], fontname=plot_config["font_name"])
    plt.title(plot_config["plot_title"], fontsize=plot_config["title_fontsize"], fontname=plot_config["font_name"], pad=26, loc='center')
    plt.suptitle(plot_config["plot_subtitle"], fontsize=plot_config["subtitle_fontsize"], fontname=plot_config["font_name"], y=0.91, x=0.511)
    plt.text(1.06, 0.5, " ", transform=plt.gca().transAxes, alpha=0)

    # Plot legend
    if plot_config.get("show_legend", True):  # Default is True if not set
        if plot_config["legend_outside"]:
            plt.legend(
                loc=plot_config["plot_legend_loc"],
                bbox_to_anchor=ref_config["legend_bbox_anchor"],
                borderaxespad=0,
                prop={'size': plot_config["legend_fontsize"], 'family': plot_config["font_name"]}
            )
        else:
            plt.legend(
                loc=plot_config["plot_legend_loc"],
                prop={'size': plot_config["legend_fontsize"], 'family': plot_config["font_name"]}
            )

    plt.xticks(fontsize=plot_config["xticks_fontsize"])
    plt.yticks(fontsize=plot_config["yticks_fontsize"])
    plt.grid(visible=plot_config["plot_grid_show"], which=plot_config["plot_grid_which"], linestyle=plot_config["plot_grid_linestyle"], linewidth=plot_config["plot_grid_linewidth"])

    if plot_config["show_footnote"]:
        fig.subplots_adjust(bottom=0.15)
        fig.text(0.91, 0.02, plot_config["footnote_text"],
                 ha='right', va='bottom', fontsize=12)

    # --- Save ---
    graphs_folder = Path(project_root) / "Graphs"
    graphs_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plot_name = f'{timestamp}_{plot_config["plot_title"]}.png'
    plot_path = graphs_folder / plot_name

    if save_plot:
        plt.savefig(plot_path, dpi=plot_config["dpi"], bbox_inches='tight')
        plt.close()
        display(Image(str(plot_path), width=1000))
    
    else:
        plt.show()


    return decay_isotopes, all_isotopes_in_RT, group_isotopes, fission_isotopes