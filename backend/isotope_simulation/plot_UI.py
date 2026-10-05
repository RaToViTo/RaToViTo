# =========================================================================
# === IMPORTS GEHÖREN IMMER AN DEN ANFANG DER DATEI ===
# =========================================================================
import ipywidgets as widgets
from IPython.display import display
import os
import math

# Importiere die UI-Helfer, damit sie im ganzen Modul bekannt sind
from .show_ma2 import show_ma2
from .show_fp2 import show_fp2
from .show_pu2 import show_pu2
from .show_total2 import show_total2
from .show_total_adds import show_total_adds
# =========================================================================


def plot_UI(chooser, include_efficiency_inputs=False):
    group_names = [
        "Total", "Plutonium", "Pu res.",
        "Minor Actinides", "MA res.",
        "Uranium", "U res.",
        "Fission products", "FPs + res.",
        "Americium", "Curium", "Protactinium", "Thorium",
        "PUREX", "PUREX+iSANEX", "PUREX+HPLC", "CHALMEX",
    ]
    scenario_colors = {
        "PUREX": "#2A8B3A",
        "PUREX+iSANEX": "#B36D33",
        "PUREX+HPLC": "#FFC48C",
        "CHALMEX": "#A2C3EE",
    }
    scenario_names = tuple(scenario_colors)

    def get_isotopes(path):
        return sorted(folder.replace("depletion_", "") for folder in os.listdir(path) if folder.startswith("depletion_"))

    def make_group_row(name):
        cb = widgets.Checkbox(value=False, description=name, indent=False, layout=widgets.Layout(width="220px"))
        cp = widgets.ColorPicker(value=scenario_colors.get(name, "#1f77b4"), layout=widgets.Layout(width="96px"), style={'description_width': '0px'})
        checkboxes[name] = cb
        color_pickers[name] = cp
        return widgets.HBox([cb, cp], layout=widgets.Layout(align_items='center', margin='0 10px 4px 0'))

    def make_isotope_row(name):
        cb = widgets.Checkbox(value=False, description=name, indent=False, layout=widgets.Layout(width="220px"))
        cp = widgets.ColorPicker(value="#1f77b4", layout=widgets.Layout(width="96px"), style={'description_width': '0px'})
        checkboxes[name] = cb
        color_pickers[name] = cp
        return widgets.HBox([cb, cp], layout=widgets.Layout(align_items='center', margin='0 10px 4px 0'))

    def split_vertically(data_rows, n_cols):
        n_rows = math.ceil(len(data_rows) / n_cols)
        columns = [[] for _ in range(n_cols)]
        for idx, row in enumerate(data_rows):
            col_idx = idx // n_rows
            columns[col_idx].append(row)
        return columns

    chooser_path = chooser.selected_path
    checkboxes, color_pickers = {}, {}

    group_rows = [make_group_row(name) for name in group_names]
    group_columns = split_vertically(group_rows, n_cols=4)
    group_grid = widgets.HBox([widgets.VBox(col) for col in group_columns])

    efficiency_inputs = {
        "eff_purex": widgets.BoundedFloatText(value=0.9988, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "eff_isanex": widgets.BoundedFloatText(value=0.999, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "eff_hplc": widgets.BoundedFloatText(value=0.96, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "eff_chalmex": widgets.BoundedFloatText(value=0.999, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "num_cycles": widgets.BoundedIntText(value=10, min=1, max=1000, step=1, layout=widgets.Layout(width="140px", height="32px")),
        "partition_eff_u": widgets.BoundedFloatText(value=0.9988, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "partition_eff_pu": widgets.BoundedFloatText(value=0.9988, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
        "partition_eff_ma": widgets.BoundedFloatText(value=0.9999, min=0, max=1, step=0.0001, layout=widgets.Layout(width="140px", height="32px")),
    }
    efficiency_labels = {
        "eff_purex": "PUREX:",
        "eff_isanex": "PUREX+iSANEX:",
        "eff_hplc": "PUREX+HPLC:",
        "eff_chalmex": "CHALMEX:",
        "num_cycles": "Fuel cycles:",
        "partition_eff_u": "U separation:",
        "partition_eff_pu": "Pu separation:",
        "partition_eff_ma": "MA separation:",
    }
    efficiency_rows = {
        key: widgets.HBox([
            widgets.Label(value=efficiency_labels[key], layout=widgets.Layout(width="130px", height="32px")),
            widget,
        ], layout=widgets.Layout(display="none", align_items="center", margin="0 0 2px 0"))
        for key, widget in efficiency_inputs.items()
    }
    efficiency_panel = widgets.VBox([
        widgets.HTML("<b>Scenario efficiencies</b>"),
        *efficiency_rows.values(),
    ], layout=widgets.Layout(display="none", margin="4px 0 8px 0"))

    def update_efficiency_visibility(change=None):
        selected_scenarios = {
            name for name in scenario_names
            if checkboxes[name].value
        }

        selected_residuals = (
            checkboxes["U res."].value
            or checkboxes["Pu res."].value
            or checkboxes["MA res."].value
        )

        efficiency_panel.layout.display = (
            "" if selected_scenarios or selected_residuals else "none"
        )

        efficiency_rows["eff_purex"].layout.display = (
            "" if "PUREX" in selected_scenarios else "none"
        )
        efficiency_rows["eff_isanex"].layout.display = (
            "" if "PUREX+iSANEX" in selected_scenarios else "none"
        )
        efficiency_rows["eff_hplc"].layout.display = (
            "" if "PUREX+HPLC" in selected_scenarios else "none"
        )
        efficiency_rows["eff_chalmex"].layout.display = (
            "" if "CHALMEX" in selected_scenarios else "none"
        )

        efficiency_rows["num_cycles"].layout.display = (
            "" if selected_scenarios else "none"
        )

        efficiency_rows["partition_eff_u"].layout.display = (
            "" if checkboxes["U res."].value else "none"
        )
        efficiency_rows["partition_eff_pu"].layout.display = (
            "" if checkboxes["Pu res."].value else "none"
        )
        efficiency_rows["partition_eff_ma"].layout.display = (
            "" if checkboxes["MA res."].value else "none"
        )


    for name in scenario_names:
        checkboxes[name].observe(
            update_efficiency_visibility,
            names="value"
        )

    for name in ["U res.", "Pu res.", "MA res."]:
        checkboxes[name].observe(
            update_efficiency_visibility,
            names="value"
        )


    # === ANFANG: AUSKOMMENTIERTER TEIL FÜR INDIVIDUAL ISOTOPES ===
    # Das Laden und Erstellen der Isotope-UI wurde hier entfernt/auskommentiert.
    # 
    # isotope_names = get_isotopes(chooser_path)
    # isotope_names_sorted = sorted(isotope_names)
    # isotope_rows = [make_isotope_row(name) for name in isotope_names_sorted]
    # isotope_columns = split_vertically(isotope_rows, n_cols=4)
    # isotope_grid = widgets.HBox([widgets.VBox(col) for col in isotope_columns])
    # === ENDE: AUSKOMMENTIERTER TEIL ===


    ui = widgets.VBox([
        widgets.HTML("<b>Select groups and/or isotopes and assign colors</b>"),
        widgets.HTML("<b>Groups and important elements:</b>"),
        group_grid,
        efficiency_panel,
        # === ANFANG: AUSKOMMENTIERTER TEIL FÜR INDIVIDUAL ISOTOPES ===
        # Die Anzeige der Isotope-UI wurde hier ebenfalls entfernt.
        #
        # widgets.HTML("<b>Individual Isotopes:</b>"),
        # isotope_grid
        # === ENDE: AUSKOMMENTIERTER TEIL ===
    ])

    display(ui)
    if include_efficiency_inputs:
        return checkboxes, color_pickers, efficiency_inputs
    return checkboxes, color_pickers


def full_ui(chooser):
    """
    Diese eine Funktion ruft alle UI-Komponenten auf und gibt die
    wichtigen Widgets für die Plot-Funktion zurück.
    """
    # 1. Rufe alle einzelnen UI-Funktionen auf, damit sie ihre Widgets anzeigen
    # Das funktioniert jetzt, weil die Imports ganz oben im Modul stehen.
    show_ma2()
    show_fp2()
    show_pu2()
    show_total2()
    show_total_adds()

    # 2. Rufe die ursprüngliche plot_UI auf, um die Checkboxen/Picker zu bekommen
    checkboxes, color_pickers = plot_UI(chooser)

    # 3. Gib die Werte zurück, die das Notebook später braucht
    return checkboxes, color_pickers