import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from IPython.display import display, Image

# =========================================================================
# === HILFSFUNKTIONEN ===
# =========================================================================

def load_rt_data_from_path(path):
    """Lädt alle RT.pkl-Dateien aus einem gegebenen Pfad und gibt sie als Dictionary zurück."""
    rt_data = {}
    if not path or not os.path.exists(path):
        return rt_data
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path) and folder.startswith("depletion_"):
            rt_file = os.path.join(folder_path, "RT.pkl")
            if os.path.exists(rt_file):
                with open(rt_file, "rb") as f:
                    rt_dict = pickle.load(f)
                isotope = folder.replace("depletion_", "")
                rt_sum = np.array(rt_dict.get("RT_sum", []))
                rt_data[isotope] = rt_sum
    return rt_data

def aggregate_rt_data_for_additional(rt_data, data_type, groups, time_steps):
    """Aggregiert Radiotoxizitäts-Daten NUR für die 'additional datasets' UI."""
    if not rt_data: return np.zeros_like(time_steps)

    # === KORREKTUR: Verwende die exakten Namen aus dem 'groups'-Dictionary ===
    group_map = {
        "MA": "Minor Actinides",
        "Pu": "Plutonium",
        # "FP" wird speziell behandelt, da die Gruppe dynamisch berechnet wird
    }

    # Fall 1: Total wird wie bisher berechnet
    if data_type == "Total":
        return sum(rt_data.values()) if rt_data else np.zeros_like(time_steps)
    
    # === NEU: Spezielle Logik für Fission Products, analog zur Hauptfunktion ===
    if data_type == "FP":
        # Finde alle Isotope, die in *anderen* Gruppen definiert sind
        all_defined_isotopes = set()
        for name, members in groups.items():
            # 'Fission Products' selbst ausschließen, da die Liste anfangs leer ist
            if name != 'Fission Products':
                all_defined_isotopes.update(members)
        
        fp_sum = np.zeros_like(time_steps)
        for iso, data in rt_data.items():
            # Addiere, wenn das Isotop NICHT in einer der anderen Gruppen ist
            if iso not in all_defined_isotopes:
                fp_sum += data
        return fp_sum

    # Fall 3: MA und Pu (und andere zukünftige) werden über das korrigierte Mapping gefunden
    group_name = group_map.get(data_type)
    if not group_name:
        print(f"Warnung: Datentyp '{data_type}' für zusätzliche Datensätze nicht erkannt.")
        return np.zeros_like(time_steps)

    isotopes_to_sum = groups.get(group_name, [])
    if not isotopes_to_sum:
        print(f"Warnung: Gruppe '{group_name}' enthält keine Isotope.")
        return np.zeros_like(time_steps)

    aggregated_sum = np.zeros_like(time_steps)
    for iso in isotopes_to_sum:
        if iso in rt_data:
            aggregated_sum += rt_data[iso]
    return aggregated_sum

def find_intersections(time, curve, target_value):
    """Findet die Zeitpunkte, an denen eine Kurve einen Zielwert schneidet."""
    if curve is None or len(curve) == 0:
        return []
    # Find indices where the sign of (curve - target) changes
    crossings = np.where(np.diff(np.sign(curve - target_value)))[0]
    intersections = []
    for idx in crossings:
        t1, t2 = time[idx], time[idx + 1]
        y1, y2 = curve[idx], curve[idx + 1]
        # Linear interpolation to find the exact time of intersection
        t_intersect = t1 + (target_value - y1) * (t2 - t1) / (y2 - y1)
        intersections.append(t_intersect)
    return intersections

# =========================================================================
# === HAUPT-PLOT-FUNKTION ===
# =========================================================================

def plot(chooser, checkboxes, color_pickers, additional_datasets, excel_file_fuel, selected_sheet, selected_DC, plot_config, ref_values, ref_config):
    try:
        # ---------------------------------------------------------------------
        # 1. Konfigurationen und Grundeinstellungen laden
        # ---------------------------------------------------------------------
        # Allgemein
        save_plot = plot_config.get("save_plot", False)
        offset = plot_config.get("offset", 0)
        linewidth = plot_config.get("linewidth", 2.0)
        dpi = plot_config.get("dpi", 300)

        # Figure size
        fig_width = plot_config.get("fig_width", 12)
        fig_height = plot_config.get("fig_height", 7)

        # Achsen
        plot_axis_range_x = plot_config.get("plot_axis_range_x", [1e0, 1e6])
        plot_axis_range_y = plot_config.get("plot_axis_range_y", [1e0, 1e10])
        plot_xlabel = plot_config.get("plot_xlabel", "Time (years)")
        plot_ylabel = plot_config.get("plot_ylabel", "Radiotoxicity [Sv/tIHM]")
        xticks_fontsize = plot_config.get("xticks_fontsize", 12)
        yticks_fontsize = plot_config.get("yticks_fontsize", 12)

        # Titel
        plot_title = plot_config.get("plot_title", "Radiotoxicity of Spent Fuel")
        plot_subtitle = plot_config.get("plot_subtitle", "")

        # Fußnote
        show_footnote = plot_config.get("show_footnote", False)
        footnote_text = plot_config.get("footnote_text", "")

        # Schriften
        font_name = plot_config.get("font_name", 'DejaVu Sans')
        title_fontsize = plot_config.get("title_fontsize", 14)
        label_fontsize = plot_config.get("label_fontsize", 13)
        legend_fontsize = plot_config.get("legend_fontsize", 10)
        subtitle_fontsize = plot_config.get("subtitle_fontsize", 12)

        # Legende
        show_legend = plot_config.get("show_legend", True)
        plot_legend_loc = plot_config.get("plot_legend_loc", 'upper right')
        legend_outside = plot_config.get("legend_outside", False)
        legend_order = plot_config.get("legend_order") # Kann None sein

        # Gitter
        plot_grid_show = plot_config.get("plot_grid_show", True)
        plot_grid_which = plot_config.get("plot_grid_which", 'major')
        plot_grid_linestyle = plot_config.get("plot_grid_linestyle", '--')
        plot_grid_linewidth = plot_config.get("plot_grid_linewidth", 0.5)

        # ---------------------------------------------------------------------
        # 2. Haupt-Daten und Zeitachse laden
        # ---------------------------------------------------------------------
        time_steps_path = os.path.join(chooser.selected_path, "time_steps.pkl")
        with open(time_steps_path, "rb") as f:
            time_steps = pickle.load(f)
        
        main_rt_data = load_rt_data_from_path(chooser.selected_path)
        
        # --- GROUP DEFINITIONS ---
        groups = {
            'Total': [],
            'Neptunium': ['Np225', 'Np226', 'Np227', 'Np228', 'Np229', 'Np230', 'Np231', 'Np232', 'Np233', 'Np234', 'Np235', 'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'Np240', 'Np241', 'Np242', 'Np243', 'Np244'],
            'Americium': ['Am231', 'Am232', 'Am233', 'Am234', 'Am235', 'Am236', 'Am237', 'Am238', 'Am239', 'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Am245', 'Am246', 'Am246_m1', 'Am247', 'Am248', 'Am249'],
            'Curium': ['Cm233', 'Cm234', 'Cm235', 'Cm236', 'Cm237', 'Cm238', 'Cm239', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Cm251'],
            #'Berkelium': ['Bk235', 'Bk237', 'Bk238', 'Bk240', 'Bk241', 'Bk242', 'Bk243', 'Bk244', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249', 'Bk250', 'Bk251', 'Bk253', 'Bk254'],
            #'Californium': ['Cf237', 'Cf238', 'Cf239', 'Cf240', 'Cf241', 'Cf242', 'Cf243', 'Cf244', 'Cf245', 'Cf246', 'Cf247', 'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cf255', 'Cf256'],
            #'Einsteinium': ['Es240', 'Es241', 'Es242', 'Es243', 'Es244', 'Es245', 'Es246', 'Es247', 'Es248', 'Es249', 'Es250', 'Es251', 'Es252', 'Es253', 'Es254', 'Es254_m1', 'Es255', 'Es256', 'Es257', 'Es258'],
            #'Fermium': ['Fm242', 'Fm243', 'Fm244', 'Fm245', 'Fm246', 'Fm247', 'Fm248', 'Fm249', 'Fm250', 'Fm251', 'Fm252', 'Fm253', 'Fm254', 'Fm255', 'Fm256', 'Fm257', 'Fm258', 'Fm259', 'Fm260'],    
            'Plutonium': ['Pu228', 'Pu229', 'Pu230', 'Pu231', 'Pu232', 'Pu233', 'Pu234', 'Pu235', 'Pu236', 'Pu237', 'Pu237_m1', 'Pu238', 'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Pu243', 'Pu244', 'Pu245', 'Pu246', 'Pu247'],
            'Uranium': ['U217', 'U218', 'U219', 'U220', 'U222', 'U223', 'U224', 'U225', 'U226', 'U227', 'U228', 'U229', 'U230', 'U231', 'U232', 'U233', 'U234', 'U235', 'U235_m1', 'U236', 'U237', 'U238', 'U239', 'U240', 'U241', 'U242'],
            'Protactinium': ['Pa227', 'Pa228', 'Pa229', 'Pa230', 'Pa231', 'Pa232', 'Pa233', 'Pa234', 'Pa234_m1', 'Pa235', 'Pa236', 'Pa237'],
            'Thorium': ['Th223', 'Th224', 'Th226', 'Th227', 'Th228', 'Th229', 'Th230', 'Th231', 'Th232', 'Th233', 'Th234', 'Th235', 'Th236'],
            #'Actinium': ['Ac223', 'Ac224', 'Ac225', 'Ac226', 'Ac227', 'Ac228', 'Ac230', 'Ac231', 'Ac232', 'Ac233'],
            #'Mendelevium': ['Md244', 'Md245', 'Md245_m1', 'Md246', 'Md247', 'Md247_m1', 'Md248', 'Md248_m1', 'Md249', 'Md250', 'Md251', 'Md252', 'Md253', 'Md254', 'Md254_m1', 'Md255', 'Md256', 'Md257', 'Md258', 'Md258_m1', 'Md259', 'Md260'],
            #'Nobelium': ['No250', 'No251', 'No252', 'No253', 'No254', 'No254_m1', 'No255', 'No256', 'No257', 'No258', 'No259', 'No260', 'No261', 'No262'],
            #'Lawrencium' : ['Lr252', 'Lr253', 'Lr253_m1', 'Lr254', 'Lr255', 'Lr256', 'Lr257', 'Lr258', 'Lr259', 'Lr260', 'Lr261', 'Lr262'],
            'Minor Actinides': ['Np225', 'Np226', 'Np227', 'Np228', 'Np229', 'Np230', 'Np231', 'Np232', 'Np233', 'Np234', 'Np235', 'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'Np240', 'Np241', 'Np242', 'Np243', 'Np244', 'Am231', 'Am232', 'Am233', 'Am234', 'Am235', 'Am236', 'Am237', 'Am238', 'Am239', 'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Am245', 'Am246', 'Am246_m1', 'Am247', 'Am248', 'Am249', 'Cm233', 'Cm234', 'Cm235', 'Cm236', 'Cm237', 'Cm238', 'Cm239', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Cm251', 'Bk235', 'Bk237', 'Bk238', 'Bk240', 'Bk241', 'Bk242', 'Bk243', 'Bk244', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249', 'Bk250', 'Bk251', 'Bk253', 'Bk254', 'Cf237', 'Cf238', 'Cf239', 'Cf240', 'Cf241', 'Cf242', 'Cf243', 'Cf244', 'Cf245', 'Cf246', 'Cf247', 'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cf255', 'Cf256', 'Es240', 'Es241', 'Es242', 'Es243', 'Es244', 'Es245', 'Es246', 'Es247', 'Es248', 'Es249', 'Es250', 'Es251', 'Es252', 'Es253', 'Es254', 'Es254_m1', 'Es255', 'Es256', 'Es257', 'Es258', 'Fm242', 'Fm243', 'Fm244', 'Fm245', 'Fm246', 'Fm247', 'Fm248', 'Fm249', 'Fm250', 'Fm251', 'Fm252', 'Fm253', 'Fm254', 'Fm255', 'Fm256', 'Fm257', 'Fm258', 'Fm259', 'Fm260'],
            'Fission Products': []  # All others
            }

        # ---------------------------------------------------------------------
        # 3. KORRIGIERTE Logik: Haupt-Gruppen aus der primären UI berechnen
        # ---------------------------------------------------------------------
        group_rt = {}
        selected_group_names = [name for name, cb in checkboxes.items() if cb.value]

        # Schritt A: Berechne alle spezifischen, ausgewählten Gruppen
        for name in selected_group_names:
            if name in groups:
                current_sum = np.zeros_like(time_steps)
                for iso in groups[name]:
                    if iso in main_rt_data:
                        current_sum += main_rt_data[iso]
                group_rt[name] = current_sum

        # Schritt B: Berechne "Fission Products", falls ausgewählt
        if "Fission Products" in selected_group_names:
            all_defined_isotopes = set()
            for name, members in groups.items():
                all_defined_isotopes.update(members)
            
            fp_sum = np.zeros_like(time_steps)
            for iso, data in main_rt_data.items():
                if iso not in all_defined_isotopes:
                    fp_sum += data
            group_rt["Fission Products"] = fp_sum

        # Schritt C: Berechne "Total", falls ausgewählt (Summe ALLER Rohdaten)
        if "Total" in selected_group_names:
            if main_rt_data:
                group_rt["Total"] = sum(main_rt_data.values())
            else:
                group_rt["Total"] = np.zeros_like(time_steps)

        # ---------------------------------------------------------------------
        # 4. Plot erstellen und Haupt-Daten plotten
        # ---------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(plot_config.get("fig_width", 12), plot_config.get("fig_height", 7)), dpi=plot_config.get("dpi", 300))

        # Plotte nur die Kurven, die auch berechnet wurden
        for name in selected_group_names:
            if name in group_rt and np.any(group_rt[name] > 0):
                ax.plot(time_steps + offset, group_rt[name], label=name, color=color_pickers[name].value, linewidth=linewidth)

        # ---------------------------------------------------------------------
        # 5. Zusätzliche Datensätze und deren Summe verarbeiten und plotten
        # ---------------------------------------------------------------------
        # (Dieser Teil war bereits korrekt und bleibt unverändert)
        all_adds_y_data = []
        time_steps_for_sum = time_steps + offset
        sum_config = None

        for config in additional_datasets:
            if config.get("row_type") == "sum":
                sum_config = config
                continue
            
            path = config["path"].selected_path
            data_type = config["type"].value
            if not path: continue

            additional_rt_data = load_rt_data_from_path(path)
            # Verwende die dedizierte Hilfsfunktion
            aggregated_data = aggregate_rt_data_for_additional(additional_rt_data, data_type, groups, time_steps)
            
            if np.any(aggregated_data > 0):
                # === HIER IST DIE LOGIK FÜR DAS NEUE LABEL ===
                custom_label = config["label"].value.strip()  # .strip() entfernt Leerzeichen
                
                if custom_label:
                    # Verwende das vom Benutzer eingegebene Label
                    label = custom_label
                else:
                    # Fallback, falls kein Label eingegeben wurde
                    label = f"Add. {data_type} ({os.path.basename(path)})"
                # ===============================================

                ax.plot(time_steps_for_sum, aggregated_data, label=label, 
                        color=config["color"].value, 
                        marker=config["marker"].value, 
                        linestyle=config["linestyle"].value, # <-- liest jetzt "linestyle"
                        linewidth=linewidth)
                all_adds_y_data.append(aggregated_data)

        # Dann die Summe der zusätzlichen Datensätze plotten, falls gewünscht
        if sum_config and all_adds_y_data:
            total_adds_sum = sum(all_adds_y_data)
            ax.plot(time_steps_for_sum, total_adds_sum, label='Sum of Additionals',
                    color=sum_config["color"].value, marker=sum_config["marker"].value,
                    linestyle=sum_config["linestyle"].value, linewidth=linewidth)

        # ---------------------------------------------------------------------
        # 6. Referenzlinien plotten
        # ---------------------------------------------------------------------
        for var_name, config in ref_config.items():
            if var_name in ref_values:
                y = ref_values[var_name]
                x_points = np.logspace(np.log10(plot_axis_range_x[0]), np.log10(plot_axis_range_x[1]), num=20)
                y_points = np.full_like(x_points, y)
                ax.plot(x_points, y_points, label=config["label"], linestyle=config["linestyle"],
                        linewidth=config["linewidth"], color=config["color"], marker=config.get("marker", "none"))


        # ---------------------------------------------------------------------
        # 7. Plot-Styling und Layout
        # ---------------------------------------------------------------------
        ax.set_xscale('log')
        ax.set_yscale('log')
        if plot_axis_range_x: ax.set_xlim(plot_axis_range_x)
        if plot_axis_range_y: ax.set_ylim(plot_axis_range_y)

        ax.set_xlabel(plot_config.get("plot_xlabel", ""), fontsize=plot_config.get("label_fontsize"))
        ax.set_ylabel(plot_config.get("plot_ylabel", ""), fontsize=plot_config.get("label_fontsize"))

        # Titles
        main_title = plot_config.get("plot_title", "")
        subtitle = plot_config.get("plot_subtitle", "")

        full_title = f"{main_title}\n{subtitle}"
        ax.set_title(
            full_title,
            loc='center', # Zentriert den Titelblock
            wrap=True,    # Erlaubt automatischen Umbruch, falls nötig
            fontsize=plot_config.get("subtitle_fontsize") # Ggf. anpassen
        )

        ax.tick_params(axis='x', labelsize=plot_config.get("xticks_fontsize", 12))
        ax.tick_params(axis='y', labelsize=plot_config.get("yticks_fontsize", 12))
        ax.grid(visible=plot_config.get("plot_grid_show", True), which=plot_config.get("plot_grid_which", 'major'),
                linestyle=plot_config.get("plot_grid_linestyle", '--'), linewidth=plot_config.get("plot_grid_linewidth", 0.5))

        if plot_config.get("show_legend", True):
            handles, labels = ax.get_legend_handles_labels()
            # Hier kann Ihre komplexe Logik zur Sortierung der Legende stehen, falls nötig
            ax.legend(handles, labels, loc=plot_config.get("plot_legend_loc", 'best'), fontsize=plot_config.get("legend_fontsize"))

        if plot_config.get("show_footnote", False):
            fig.text(0.5, 0.01, plot_config.get("footnote_text", ""), ha='center', fontsize=10)
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        else:
            fig.tight_layout(rect=[0, 0, 1, 0.95])

        # ---------------------------------------------------------------------
        # 8. Speichern oder Anzeigen
        # ---------------------------------------------------------------------
        if save_plot:
            graphs_folder = os.path.join(os.getcwd(), "Graphs")
            os.makedirs(graphs_folder, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            plot_name = f'{timestamp}_{selected_sheet}_{selected_DC}.png'.replace(" ", "_")
            plot_path = os.path.join(graphs_folder, plot_name)
            plt.savefig(plot_path, dpi=plot_config.get("dpi", 300), bbox_inches='tight')
            plt.close(fig)
            display(Image(plot_path, width=1000))
        else:
            plt.show()

        # ---------------------------------------------------------------------
        # 9. Schnittpunkte berechnen und ausgeben (optional)
        # ---------------------------------------------------------------------
        target_value = 256000  # Beispiel-Zielwert
        print("\n--- Intersection Analysis ---")
        for name, curve in group_rt.items():
            intersections = find_intersections(time_steps + offset, curve, target_value)
            if intersections:
                print(f"'{name}' crosses {target_value} at: {[f'{t:.2f}' for t in intersections]} years")

        return group_rt, time_steps + offset

    except Exception as e:
        print(f"Ein Fehler ist beim Plotten aufgetreten: {e}")
        import traceback
        traceback.print_exc()
