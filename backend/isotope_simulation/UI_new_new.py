import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display
from functools import partial
from pathlib import Path

def UI_new_new(project_root):
    """
    Erstellt die gesamte Benutzeroberfläche für den Plot und gibt alle
    benötigten Widget-Sammlungen zurück.
    """
    
    # =========================================================================
    # === Teil 1: Statische UI für Haupt- und Waste-Kurven ===
    # =========================================================================
    display(widgets.HTML("<h3>1. Wähle die zu plottenden Kurven aus:</h3>"))
    
    # Liste aller verfügbaren Kurven (Basis, Residuals und Szenarien)
    main_group_names = [
        "Total", "Plutonium", "Minor Actinides", "Uranium", "Fission products in spent fuel",
        "Americium", "Curium", "Protactinium", "Thorium",
        "U res.", "Pu res.", "MA res.",
        "PUREX", "PUREX+iSANEX", "PUREX+HPLC", "CHALMEX"
    ]
    # Farben für alle Kurven
    default_colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",  # Standard
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",  # Weitere
        "#aec7e8", "#ffbb78", "#98df8a",                         # Residuals
        "#2A8B3A", "#B36D33", "#FFC48C", "#A2C3EE"             # Szenarien
    ]

    checkboxes = {name: widgets.Checkbox(value=False, description=name, indent=False, layout=widgets.Layout(width='200px')) for name in main_group_names}
    color_pickers = {name: widgets.ColorPicker(concise=True, value=color, layout=widgets.Layout(width='40px')) for name, color in zip(main_group_names, default_colors)}

    ui_rows = [widgets.HBox([checkboxes[name], color_pickers[name]]) for name in main_group_names]
    
    # In Spalten anordnen für bessere Übersicht
    num_columns = 4
    items_per_column = (len(ui_rows) + num_columns - 1) // num_columns
    columns = [widgets.VBox(ui_rows[i:i + items_per_column]) for i in range(0, len(ui_rows), items_per_column)]
    main_ui_container = widgets.HBox(columns)
    display(main_ui_container)

    # =========================================================================
    # === Teil 2: Dynamische UI für Zusatz-Datensätze ===
    # =========================================================================
    display(widgets.HTML("<h3>2. Füge optional zusätzliche Datensätze hinzu:</h3>"))
    additional_datasets_config = []
    # (Dieser Teil ist funktional unverändert und wird hier der Kürze halber ausgelassen - übernimm ihn aus deiner letzten Version)
    # ... (Code für add_dataset_row, add_sum_row, etc.) ...
    datasets_container = widgets.VBox([])
    add_dataset_button = widgets.Button(description=" Add additional dataset", icon="plus", button_style="success", layout=widgets.Layout(margin='0 5px 0 0'))
    add_sum_button = widgets.Button(description=" Plot sum of additionals", icon="plus-square", button_style="info")
    # ... (komplette Logik aus deinem alten plot_UI_new.py hier einfügen)
    # Wichtig ist, dass am Ende `additional_datasets_config` gefüllt wird.
    
    # =========================================================================
    # === NEU: Teil 3: UI für Waste Scenario Parameters ===
    # =========================================================================
    display(widgets.HTML("<h3>3. Parameter für Waste-Szenarien:</h3>"))
    
    waste_params = {
        'partition_eff_u': widgets.FloatSlider(value=0.999, min=0.9, max=1.0, step=0.001, description='P-Eff. U:', readout_format='.3f'),
        'partition_eff_pu': widgets.FloatSlider(value=0.999, min=0.9, max=1.0, step=0.001, description='P-Eff. Pu:', readout_format='.3f'),
        'partition_eff_ma': widgets.FloatSlider(value=0.999, min=0.9, max=1.0, step=0.001, description='P-Eff. MA:', readout_format='.3f'),
        'eff_purex': widgets.FloatSlider(value=0.9988, min=0.9, max=1.0, step=0.0001, description='Eff. PUREX:', readout_format='.4f'),
        'eff_isanex': widgets.FloatSlider(value=0.999, min=0.9, max=1.0, step=0.001, description='Eff. iSANEX:', readout_format='.3f'),
        'eff_hplc': widgets.FloatSlider(value=0.96, min=0.9, max=1.0, step=0.01, description='Eff. HPLC:', readout_format='.2f'),
        'eff_chalmex': widgets.FloatSlider(value=0.999, min=0.9, max=1.0, step=0.001, description='Eff. CHALMEX:', readout_format='.3f'),
        'num_cycles': widgets.IntSlider(value=10, min=1, max=100, step=1, description='Num. Cycles:')
    }

    waste_params_container = widgets.VBox(list(waste_params.values()))
    display(waste_params_container)

    # =========================================================================
    # === Teil 4: Alle Widget-Sammlungen zurückgeben ===
    # =========================================================================
    return checkboxes, color_pickers, additional_datasets_config, waste_params