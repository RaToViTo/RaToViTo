# /backend/isotope_simulation/plot.py

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from IPython.display import display, Image

# (Hilfsfunktionen `load_rt_data_from_path` und `find_intersections` bleiben hier)
# ...

def plot_new_new(chooser, checkboxes, color_pickers, additional_datasets, waste_params,
         excel_file_fuel, selected_sheet, selected_DC, plot_config, ref_values, ref_config):
    try:
        # =========================================================================
        # === 1. Konfigurationen und Parameter auslesen ===
        # =========================================================================
        # ... (Dein ganzer plot_config Block für Styling) ...
        save_plot = plot_config.get("save_plot", False)
        linewidth = plot_config.get("linewidth", 2.0)
        
        # --- NEU: Parameter aus den Waste-Widgets auslesen ---
        partition_eff_u = waste_params['partition_eff_u'].value
        partition_eff_pu = waste_params['partition_eff_pu'].value
        partition_eff_ma = waste_params['partition_eff_ma'].value
        eff_purex = waste_params['eff_purex'].value
        eff_isanex = waste_params['eff_isanex'].value
        eff_hplc = waste_params['eff_hplc'].value
        eff_chalmex = waste_params['eff_chalmex'].value
        num_cycles = waste_params['num_cycles'].value

        # =========================================================================
        # === 2. Daten laden und Gruppen definieren ===
        # =========================================================================
        time_steps_path = os.path.join(chooser.selected_path, "time_steps.pkl")
        with open(time_steps_path, "rb") as f:
            time_steps = pickle.load(f)
            
        main_rt_data = load_rt_data_from_path(chooser.selected_path)
        
        # --- Gruppendefinitionen (aus deinem alten Skript) ---
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
        'Fission products': []
    }
        
        # =========================================================================
        # === 3. Berechnungen durchführen ===
        # =========================================================================
        group_rt = {}
        selected_names = {name for name, cb in checkboxes.items() if cb.value}

        # --- Basis-Gruppen und Residuals ---
        for name in selected_names:
            if name in group_rt: continue # Falls schon berechnet

            if name == "Total":
                group_rt[name] = sum(main_rt_data.values()) if main_rt_data else np.zeros_like(time_steps)
            
            elif name == "Fission products in spent fuel":
                all_group_isotopes = {iso for members in groups.values() for iso in members}
                group_rt[name] = sum(data for iso, data in main_rt_data.items() if iso not in all_group_isotopes)

            elif name == "U res.":
                u_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Uranium", []))
                group_rt[name] = u_sum * (1 - partition_eff_u)

            elif name == "Pu res.":
                pu_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Plutonium", []))
                group_rt[name] = pu_sum * (1 - partition_eff_pu)

            elif name == "MA res.":
                ma_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Minor Actinides", []))
                group_rt[name] = ma_sum * (1 - partition_eff_ma)
            
            elif name in groups: # Für Standardgruppen wie "Americium", "Curium", etc.
                group_rt[name] = sum(main_rt_data.get(iso, 0) for iso in groups[name])

        # --- Szenarien-Berechnungen ---
        scenario_names = {"PUREX", "PUREX+iSANEX", "PUREX+HPLC", "CHALMEX"}
        if selected_names.intersection(scenario_names):
            # Benötigte Basissummen nur einmal berechnen
            all_group_isotopes = {iso for members in groups.values() for iso in members}
            fps_scenario = sum(data for iso, data in main_rt_data.items() if iso not in all_group_isotopes)
            u_pu_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Uranium", []) + groups.get("Plutonium", []))
            ma_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Minor Actinides", []))
            
            isanex_ma_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Americium", []) + groups.get("Curium", []))
            hplc_ma_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Americium", []) + groups.get("Curium", [])) # Annahme, anpassen falls nötig
            chalmex_ma_sum = sum(main_rt_data.get(iso, 0) for iso in groups.get("Americium", []))

            # Szenarien berechnen, wenn ausgewählt
            if "PUREX" in selected_names:
                group_rt["PUREX"] = fps_scenario + num_cycles * u_pu_sum * (1 - eff_purex) + ma_sum
            if "PUREX+iSANEX" in selected_names:
                group_rt["PUREX+iSANEX"] = fps_scenario + num_cycles * u_pu_sum * (1 - eff_purex) + num_cycles * isanex_ma_sum * (1 - eff_isanex)
            if "PUREX+HPLC" in selected_names:
                group_rt["PUREX+HPLC"] = fps_scenario + num_cycles * u_pu_sum * (1 - eff_purex) + num_cycles * hplc_ma_sum * (1 - eff_hplc)
            if "CHALMEX" in selected_names:
                group_rt["CHALMEX"] = fps_scenario + num_cycles * u_pu_sum * (1 - eff_purex) + num_cycles * chalmex_ma_sum * (1 - eff_chalmex)

        # =========================================================================
        # === 4. Zusätzliche Datensätze verarbeiten (NEU & SAUBER) ===
        # =========================================================================
        # ... (Hier der saubere Loop, der die alten `show_fp2` etc. ersetzt) ...
        # (Beachte: Die Logik hier ist jetzt viel einfacher als im alten Skript)
        
        # =========================================================================
        # === 5. Plotten ===
        # =========================================================================
        fig, ax = plt.subplots(figsize=(plot_config.get("fig_width", 12), plot_config.get("fig_height", 7)), dpi=plot_config.get("dpi", 300))

        # --- EINE Plot-Schleife für alles ---
        for name, data in group_rt.items():
            if np.any(data):
                color = color_pickers.get(name).value if name in color_pickers else 'gray' # Sicherheitsabfrage
                ax.plot(time_steps, data, label=name, color=color, linewidth=linewidth)

        # (Hier der Rest der Plot-Logik: Achsen, Titel, Legende, Speichern...)
        # ... Verwende die verbesserte Titel-Logik: `ax.set_title(...)` mit `\n` ...
        # ...

        plt.show() # oder Speichern-Logik
        return group_rt, time_steps
        
    except Exception as e:
        import traceback
        traceback.print_exc()
