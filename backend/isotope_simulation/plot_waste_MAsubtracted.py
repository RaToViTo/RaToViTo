def plot(chooser, checkboxes, color_pickers, excel_file_fuel, selected_sheet,
                     selected_DC, save_plot, offset, plot_config, ref_values, ref_config,
                     partition_eff_u, partition_eff_pu, partition_eff_ma,
                     scenario_colors=None,
                     show_fp2=False, second_fp_path=None, fp2_colorpicker=None, fp2_label=None, fp2_linestyle=None, fp2_marker=None,
                     show_ma2=False, ma2_path=None, ma2_colorpicker=None, ma2_label=None, ma2_linestyle=None, ma2_marker=None,
                     show_pu2=False, pu2_path=None, pu2_colorpicker=None, pu2_label=None, pu2_linestyle=None, pu2_marker=None,
                     show_total2=False, total2_path=None, total2_colorpicker=None, total2_label=None, total2_linestyle=None, total2_marker=None):

    import os
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    from IPython.display import Image, display

    # --- TIME STEPS ---
    time_steps_path = os.path.join(chooser.selected_path, "time_steps.pkl")
    with open(time_steps_path, "rb") as f:
        time_steps = pickle.load(f)

    # --- LOAD RT DATA ---
    rt_data = {}
    for folder in os.listdir(chooser.selected_path):
        folder_path = os.path.join(chooser.selected_path, folder)
        if os.path.isdir(folder_path) and folder.startswith("depletion_"):
            rt_file = os.path.join(folder_path, "RT.pkl")
            if os.path.exists(rt_file):
                with open(rt_file, "rb") as f:
                    rt_dict = pickle.load(f)
                isotope = folder.replace("depletion_", "")
                rt_sum = np.array(rt_dict.get("RT_sum", []))
                rt_data[isotope] = rt_sum

    # Dataset second FP
    rt_data_fp2 = {}
    if second_fp_path is not None:
        for folder in os.listdir(second_fp_path):
            folder_path = os.path.join(second_fp_path, folder)
            if os.path.isdir(folder_path) and folder.startswith("depletion_"):
                rt_file = os.path.join(folder_path, "RT.pkl")
                if os.path.exists(rt_file):
                    with open(rt_file, "rb") as f:
                        rt_dict = pickle.load(f)
                    isotope = folder.replace("depletion_", "")
                    rt_sum = np.array(rt_dict.get("RT_sum", []))
                    rt_data_fp2[isotope] = rt_sum
    else:
        rt_data_fp2 = None

    # Dataset MA
    rt_data_ma2 = {}
    if ma2_path is not None:
        for folder in os.listdir(ma2_path):
            folder_path = os.path.join(ma2_path, folder)
            if os.path.isdir(folder_path) and folder.startswith("depletion_"):
                rt_file = os.path.join(folder_path, "RT.pkl")
                if os.path.exists(rt_file):
                    with open(rt_file, "rb") as f:
                        rt_dict = pickle.load(f)
                    isotope = folder.replace("depletion_", "")
                    rt_sum = np.array(rt_dict.get("RT_sum", []))
                    rt_data_ma2[isotope] = rt_sum
    else:
        rt_data_ma2 = None

    # Dataset Pu
    rt_data_pu2 = {}
    if pu2_path is not None:
        for folder in os.listdir(pu2_path):
            folder_path = os.path.join(pu2_path, folder)
            if os.path.isdir(folder_path) and folder.startswith("depletion_"):
                rt_file = os.path.join(folder_path, "RT.pkl")
                if os.path.exists(rt_file):
                    with open(rt_file, "rb") as f:
                        rt_dict = pickle.load(f)
                    isotope = folder.replace("depletion_", "")
                    rt_sum = np.array(rt_dict.get("RT_sum", []))
                    rt_data_pu2[isotope] = rt_sum
    else:
        rt_data_pu2 = None

    # Dataset Total
    rt_data_total2 = {}
    if total2_path is not None:
        for folder in os.listdir(total2_path):
            folder_path = os.path.join(total2_path, folder)
            if os.path.isdir(folder_path) and folder.startswith("depletion_"):
                rt_file = os.path.join(folder_path, "RT.pkl")
                if os.path.exists(rt_file):
                    with open(rt_file, "rb") as f:
                        rt_dict = pickle.load(f)
                    isotope = folder.replace("depletion_", "")
                    rt_sum = np.array(rt_dict.get("RT_sum", []))
                    rt_data_total2[isotope] = rt_sum
    else:
        rt_data_total2 = None

    # --- GROUP DEFINITIONS ---
    groups = {
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
        'Lawrencium' : ['Lr252', 'Lr253', 'Lr253_m1', 'Lr254', 'Lr255', 'Lr256', 'Lr257', 'Lr258', 'Lr259', 'Lr260', 'Lr261', 'Lr262'],
        'Minor Actinides': ['Np225', 'Np226', 'Np227', 'Np228', 'Np229', 'Np230', 'Np231', 'Np232', 'Np233', 'Np234', 'Np235', 'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'Np240', 'Np241', 'Np242', 'Np243', 'Np244', 'Am231', 'Am232', 'Am233', 'Am234', 'Am235', 'Am236', 'Am237', 'Am238', 'Am239', 'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Am245', 'Am246', 'Am246_m1', 'Am247', 'Am248', 'Am249', 'Cm233', 'Cm234', 'Cm235', 'Cm236', 'Cm237', 'Cm238', 'Cm239', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Cm251', 'Bk235', 'Bk237', 'Bk238', 'Bk240', 'Bk241', 'Bk242', 'Bk243', 'Bk244', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249', 'Bk250', 'Bk251', 'Bk253', 'Bk254', 'Cf237', 'Cf238', 'Cf239', 'Cf240', 'Cf241', 'Cf242', 'Cf243', 'Cf244', 'Cf245', 'Cf246', 'Cf247', 'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cf255', 'Cf256', 'Es240', 'Es241', 'Es242', 'Es243', 'Es244', 'Es245', 'Es246', 'Es247', 'Es248', 'Es249', 'Es250', 'Es251', 'Es252', 'Es253', 'Es254', 'Es254_m1', 'Es255', 'Es256', 'Es257', 'Es258', 'Fm242', 'Fm243', 'Fm244', 'Fm245', 'Fm246', 'Fm247', 'Fm248', 'Fm249', 'Fm250', 'Fm251', 'Fm252', 'Fm253', 'Fm254', 'Fm255', 'Fm256', 'Fm257', 'Fm258', 'Fm259', 'Fm260'],
        'Fission Products': []  # All others
    }

    # --- SELECTION FROM UI ---
    selected_items = [name for name, cb in checkboxes.items() if cb.value]
    selected_groups = [name for name in selected_items if name in groups]
    individual_isotopes = [name for name in selected_items if name not in groups and name != "Total"]
    color_map = {name: color_pickers[name].value for name in selected_items}
    linestyle_map = {name: '-' for name in selected_items}  # Default linestyle
    marker_map = {name: 'none' for name in selected_items}  # Default marker

    # --- INITIALIZE RESULTS ---
    group_rt = {}

    # --- COLLECT GROUP ISOTOPES ---
    all_group_isotopes = set()
    for gname, members in groups.items():
        all_group_isotopes.update(members)

    # --- CALCULATE GROUPS ---
    for group in selected_groups:
        if group in ["Total", "Fission Products"]:
            continue
        group_rt[group] = np.zeros_like(time_steps)
        for iso in groups[group]:
            if iso in rt_data:
                group_rt[group] += rt_data[iso]

    # --- INDIVIDUAL ISOTOPES ---
    for iso in individual_isotopes:
        if iso in rt_data:
            group_rt[iso] = rt_data[iso]

    # --- FISSION PRODUCTS ---
    if "Fission Products" in selected_groups:
        group_rt["Fission Products"] = np.zeros_like(time_steps)
        unassigned_isotopes = [iso for iso in rt_data if iso not in all_group_isotopes]
        for iso in unassigned_isotopes:
            group_rt["Fission Products"] += rt_data[iso]

    # --- Fission Products from additional path (always add when requested) ---
    if show_fp2 and rt_data_fp2 is not None:
        group_rt[fp2_label] = np.zeros_like(time_steps)
        for iso in rt_data_fp2:
            if iso not in all_group_isotopes:
                group_rt[fp2_label] += rt_data_fp2[iso]

        color_map[fp2_label] = fp2_colorpicker.value
        linestyle_map[fp2_label] = fp2_linestyle.value if fp2_linestyle is not None else '-'
        marker_map[fp2_label] = fp2_marker.value if fp2_marker is not None else 'none'

        if fp2_label not in selected_items:
            selected_items.append(fp2_label)

    # --- MA from additional path ---
    if show_ma2 and rt_data_ma2 is not None:
        group_rt[ma2_label] = np.zeros_like(time_steps)
        for iso in groups["Minor Actinides"]:
            if iso in rt_data_ma2:
                group_rt[ma2_label] += rt_data_ma2[iso]

        color_map[ma2_label] = ma2_colorpicker.value
        linestyle_map[ma2_label] = ma2_linestyle.value if ma2_linestyle is not None else '-'
        marker_map[ma2_label] = ma2_marker.value if ma2_marker is not None else 'none'

        if ma2_label not in selected_items:
            selected_items.append(ma2_label)

    # --- Pu from additional path ---
    if show_pu2 and rt_data_pu2 is not None:
        group_rt[pu2_label] = np.zeros_like(time_steps)
        for iso in groups["Plutonium"]:
            if iso in rt_data_pu2:
                group_rt[pu2_label] += rt_data_pu2[iso]

        color_map[pu2_label] = pu2_colorpicker.value
        linestyle_map[pu2_label] = pu2_linestyle.value if pu2_linestyle is not None else '-'
        marker_map[pu2_label] = pu2_marker.value if pu2_marker is not None else 'none'

        if pu2_label not in selected_items:
            selected_items.append(pu2_label)

    # --- Total from additional path ---
    if show_total2 and rt_data_total2 is not None:
        group_rt[total2_label] = np.zeros_like(time_steps)
        for iso in rt_data_total2:
            group_rt[total2_label] += rt_data_total2[iso]

        color_map[total2_label] = total2_colorpicker.value
        linestyle_map[total2_label] = total2_linestyle.value if total2_linestyle is not None else '-'
        marker_map[total2_label] = total2_marker.value if total2_marker is not None else 'none'

        if total2_label not in selected_items:
            selected_items.append(total2_label)

    # --- TOTAL (nur Basis-Kurven, NICHT additional) ---
    if "Total" in selected_items:
        additional_labels = set()
        if show_fp2 and fp2_label:
            additional_labels.add(fp2_label)
        if show_ma2 and ma2_label:
            additional_labels.add(ma2_label)
        if show_pu2 and pu2_label:
            additional_labels.add(pu2_label)
        if show_total2 and total2_label:
            additional_labels.add(total2_label)
        
        group_rt["Total"] = np.zeros_like(time_steps)
        for name in selected_items:
            if name != "Total" and name not in additional_labels and name in group_rt:
                group_rt["Total"] += group_rt[name]

    # --- MA-REMAINING-Szenarien (ε_MA * MA_sum) ---
    eff_u_arr  = np.atleast_1d(np.asarray(partition_eff_u, dtype=float))
    eff_pu_arr = np.atleast_1d(np.asarray(partition_eff_pu, dtype=float))
    eff_ma_arr = np.atleast_1d(np.asarray(partition_eff_ma, dtype=float))

    if not (eff_u_arr.shape == eff_pu_arr.shape == eff_ma_arr.shape):
        raise ValueError("partition_eff_u, _pu und _ma müssen die gleiche Länge haben.")

    # MA-Summe (Original)
    ma_sum = np.zeros_like(time_steps)
    for iso in groups["Minor Actinides"]:
        if iso in rt_data:
            ma_sum += rt_data[iso]

    scenario_curves = []
    for i, ema in enumerate(eff_ma_arr):
        ema = float(ema)
        curve = ema * ma_sum
        pct = 100.0 * ema
        label = f"MA remaining {pct:.2f}% (set {i+1})"
        group_rt[label] = curve
        scenario_curves.append(curve)

    # Legacy-Key (falls extern genutzt)
    group_rt["MA remaining"] = scenario_curves[0] if len(scenario_curves) > 0 else np.zeros_like(time_steps)

    ## --- FPs + Residuals ---
    #adjusted_fp_rt = np.copy(adjusted_fp_partition)
    #for iso in groups["Minor Actinides"]:
    #    if iso in rt_data:
    #        delta = rt_data[iso] * (1 - partition_eff_ma) * (1 - transmut_eff)
    #        adjusted_fp_rt += delta - rt_data[iso] * (1 - partition_eff_ma)
    #group_rt["FPs + Residuals"] = adjusted_fp_rt

    # --- Partitioned Groups ---
    if "U res." in selected_items:
        group_rt["U res."] = np.zeros_like(time_steps)
        for iso in groups["Uranium"]:
            if iso in rt_data:
                group_rt["U res."] += rt_data[iso] * (1 - partition_eff_u)

    if "Pu res." in selected_items:
        group_rt["Pu res."] = np.zeros_like(time_steps)
        for iso in groups["Plutonium"]:
            if iso in rt_data:
                group_rt["Pu res."] += rt_data[iso] * (1 - partition_eff_pu)

    j = 0
    ema = float(eff_ma_arr[j])

    if "MA res." in selected_items:
        group_rt["MA res."] = np.zeros_like(time_steps)
        for iso in groups["Minor Actinides"]:
            if iso in rt_data:
                group_rt["MA res."] += rt_data[iso] * ema

    # --- PLOTTING ---
    fig = plt.figure(figsize=(plot_config["fig_width"], plot_config["fig_height"]), dpi=plot_config["dpi"])

    for i, name in enumerate(selected_items):
        if name not in group_rt:
            continue
        data = group_rt[name]
        if np.all(data == 0):
            continue
        t = time_steps + offset
        color = color_map.get(name, None)
        linestyle = linestyle_map.get(name, '-')
        marker = marker_map.get(name, 'none')
        z = 100 if name == "Total" else 1
        plt.plot(t, data, label=name, color=color, linestyle=linestyle, marker=marker, linewidth=plot_config["linewidth"], zorder=z)

    # draw scenario curves if provided
    if scenario_colors is not None:
        scenario_keys = [k for k in group_rt.keys() if k.startswith("MA remaining ")]
        def sort_key(x):
            try:
                return int(x.split("(")[-1].split(")")[0].split()[-1])  # ... (set i)
            except Exception:
                return 0
        scenario_keys = sorted(scenario_keys, key=sort_key)

    t = time_steps + offset
    for i, key in enumerate(scenario_keys):
        data = group_rt[key]
        if np.all(data == 0):
            continue
        color = scenario_colors[i] if i < len(scenario_colors) else None
        plt.plot(t, data, label=key, linewidth=plot_config["linewidth"], color=color)


    if plot_config["show_footnote"]:
        fig.subplots_adjust(bottom=0.15)
        fig.text(0.91, 0.02, plot_config["footnote_text"],
                 ha='right', va='bottom', fontsize=12)

    for var_name, config in ref_config.items():
        if var_name in ref_values:
            y = ref_values[var_name]
            marker = config.get("marker", "none")
            # Create a line across the entire x-axis range with multiple points for markers
            x_range = np.array(plot_config["plot_axis_range_x"])
            # Create evenly spaced points on log scale for marker placement
            x_points = np.logspace(np.log10(x_range[0]), np.log10(x_range[1]), num=20)
            y_points = np.full_like(x_points, y)
            plt.plot(x_points, y_points, label=config["label"], linestyle=config["linestyle"],
                     linewidth=config["linewidth"], color=config["color"], marker=marker, markersize=6, fillstyle='full')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(plot_config["plot_axis_range_x"])
    plt.ylim(plot_config["plot_axis_range_y"])
    plt.xlabel(plot_config["plot_xlabel"], fontsize=plot_config["label_fontsize"], fontname=plot_config["font_name"])
    plt.ylabel(plot_config["plot_ylabel"], fontsize=plot_config["label_fontsize"], fontname=plot_config["font_name"])
    plt.title(plot_config["plot_title"], fontsize=plot_config["title_fontsize"], fontname=plot_config["font_name"], pad=26, loc='center')
    plt.suptitle(plot_config["plot_subtitle"], fontsize=plot_config["subtitle_fontsize"], fontname=plot_config["font_name"], y=0.91, x=0.511)

    if plot_config.get("show_legend", True):
        if plot_config["legend_outside"]:
            plt.legend(loc=plot_config["plot_legend_loc"],
                       bbox_to_anchor=ref_config["legend_bbox_anchor"],
                       borderaxespad=0,
                       prop={'size': plot_config["legend_fontsize"], 'family': plot_config["font_name"]})
        else:
            plt.legend(loc=plot_config["plot_legend_loc"],
                       prop={'size': plot_config["legend_fontsize"], 'family': plot_config["font_name"]})

    plt.xticks(fontsize=plot_config["xticks_fontsize"])
    plt.yticks(fontsize=plot_config["yticks_fontsize"])
    plt.grid(visible=plot_config["plot_grid_show"],
             which=plot_config["plot_grid_which"],
             linestyle=plot_config["plot_grid_linestyle"],
             linewidth=plot_config["plot_grid_linewidth"])

    graphs_folder = os.path.join(os.getcwd(), "Graphs")
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plot_name = f'{timestamp}_{selected_sheet}_{selected_DC}_{plot_config["plot_title"]}.png'
    plot_path = os.path.join(graphs_folder, plot_name)

    if save_plot:
        plt.savefig(plot_path, dpi=plot_config["dpi"], bbox_inches='tight')
        plt.close()
        display(Image(plot_path, width=1000))
    else:
        plt.show()

    # return computed results and adjusted time array for post‑processing or further plotting
    return group_rt, time_steps + offset
