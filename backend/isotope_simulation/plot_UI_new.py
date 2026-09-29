# In backend/isotope_simulation/plot_UI_new.py

import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display
from functools import partial
from pathlib import Path

def plot_UI_new(project_root):
    additional_datasets_config = []
    datasets_container = widgets.VBox([])

    add_dataset_button = widgets.Button(
        description=" Add additional dataset",
        icon="plus",
        button_style="success"
    )

    sum_color_picker = widgets.ColorPicker(description="Sum Color:", value="#000000", layout=widgets.Layout(width="220px"))
    sum_marker_picker = widgets.Dropdown(options=['', 'o', 's', '^', 'D', 'x', '+', '*'], description="Sum Marker:", value='', layout=widgets.Layout(width="220px"))
    sum_linestyle_picker = widgets.Dropdown(options=['-', '--', ':', '-.'], description="Sum Style:", value=':', layout=widgets.Layout(width="220px"))

    sum_config = {
        "row_type": "sum",
        "color": sum_color_picker,
        "marker": sum_marker_picker,
        "linestyle": sum_linestyle_picker
    }

    sum_config_box = widgets.HBox([sum_color_picker, sum_marker_picker, sum_linestyle_picker], layout=widgets.Layout(display='none', margin='5px 0 0 20px'))
    sum_checkbox = widgets.Checkbox(value=False, description="Plot sum of additionals",style={'description_width': 'initial'})
    
    def on_sum_checkbox_change(change):
        is_checked = change['new']
        if is_checked:
            sum_config_box.layout.display = 'flex'
            if sum_config not in additional_datasets_config:
                additional_datasets_config.append(sum_config)
        else:
            sum_config_box.layout.display = 'none'
            if sum_config in additional_datasets_config:
                additional_datasets_config.remove(sum_config)

    sum_checkbox.observe(on_sum_checkbox_change, names='value')


    def add_dataset_row(b):
        """Wird aufgerufen, wenn der Plus-Button geklickt wird."""
        
        # --- Widgets erstellen (wie bisher) ---
        label_input = widgets.Text(value='', placeholder='Custom legend label', description='Label:', style={'description_width': 'initial'},
                                    layout=widgets.Layout(width="220px"))
        type_dropdown = widgets.Dropdown(options=["MA", "FP", "Pu", "Total"], description="Type:", layout=widgets.Layout(width="180px"))
        color_picker = widgets.ColorPicker(description="Color:", value="#ff7f0e", layout=widgets.Layout(width="180px"))
        
        linestyle_picker = widgets.Dropdown(
            options=[('Dashed', '--'), ('Solid', '-'), ('Dotted', ':'), ('Dash-Dot', '-.')],
            description="Linestyle:", value='--', layout=widgets.Layout(width="180px")
        )
        
        marker_picker = widgets.Dropdown(
            options=[('None', ''), ('Cross', 'x'), ('Circle', 'o'), ('Square', 's')],
            description="Marker:", value='', layout=widgets.Layout(width="180px")
        )
        
        start_path = Path(project_root) / "simulation results"
        start_path.mkdir(parents=True, exist_ok=True)
        file_chooser = FileChooser(str(start_path), title='Select Dataset')
        file_chooser.show_only_dirs = True
        
        remove_button = widgets.Button(icon="trash", layout=widgets.Layout(width="40px"))

        # --- Layout organisieren (wie bisher) ---
        top_row = widgets.HBox(
            [label_input, type_dropdown, color_picker, marker_picker, linestyle_picker, remove_button],
            layout=widgets.Layout(align_items='flex-end')
        )
        bottom_row = widgets.HBox([file_chooser])

        # === KORREKTUR HIER: Padding auf 0 setzen, um die Einrückung zu entfernen ===
        full_row_ui = widgets.VBox([
            top_row, 
            bottom_row, 
            widgets.HTML('<hr style="border-top: 1px solid #ccc; margin-top: 10px;">')
        ], layout=widgets.Layout(
                margin='10px 0 0 0', # Behält den Abstand nach oben
                padding='0'         # Entfernt die Einrückung
        ))

        # --- Konfiguration speichern und anzeigen (wie bisher) ---
        row_config = {
            "row_type": "dataset",
            "label": label_input,
            "type": type_dropdown,
            "path": file_chooser,
            "color": color_picker,
            "marker": marker_picker,
            "linestyle": linestyle_picker,
            "ui_row": full_row_ui
        }
        additional_datasets_config.append(row_config)

        datasets_container.children = list(datasets_container.children) + [full_row_ui]
        
        def on_remove_clicked(config_to_remove, b):
            additional_datasets_config.remove(config_to_remove)
            new_children = [child for child in datasets_container.children if child != config_to_remove["ui_row"]]
            datasets_container.children = new_children
            
        remove_button.on_click(partial(on_remove_clicked, row_config))

    add_dataset_button.on_click(add_dataset_row)
    
    final_ui = widgets.VBox([
        add_dataset_button,
        datasets_container,
        widgets.HTML('<hr style="border-top: 2px solid #aaa; margin-top: 15px;">'),
        sum_checkbox,
        sum_config_box
    ])
    
    display(final_ui)
    
    return additional_datasets_config