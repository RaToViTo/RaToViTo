def plot_UI(chooser):
    import ipywidgets as widgets
    from IPython.display import display
    import os, math

    group_names = [
        "Total", "Plutonium", "Pu res.",
        "Minor Actinides", "MA res.",
        "Uranium", "U res.",
        "Fission Products", "FPs + res.",
        "Neptunium", "Americium", "Curium", "Berkelium", "Californium",
        "Einsteinium", "Fermium", "Protactinium", "Thorium", "Actinium",
        "Mendelevium", "Nobelium", "Lawrencium"
    ]

    def get_isotopes(path):
        return sorted(folder.replace("depletion_", "") for folder in os.listdir(path) if folder.startswith("depletion_"))

    def make_group_row(name):
        cb = widgets.Checkbox(value=False, description=name, indent=False, layout=widgets.Layout(width="220px"))
        cp = widgets.ColorPicker(value="#1f77b4", layout=widgets.Layout(width="96px"), style={'description_width': '0px'})
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
    isotope_names = get_isotopes(chooser_path)
    checkboxes, color_pickers = {}, {}

    group_rows = [make_group_row(name) for name in group_names]
    group_columns = split_vertically(group_rows, n_cols=4)
    group_grid = widgets.HBox([widgets.VBox(col) for col in group_columns])

    isotope_names_sorted = sorted(isotope_names)
    isotope_rows = [make_isotope_row(name) for name in isotope_names_sorted]
    isotope_columns = split_vertically(isotope_rows, n_cols=4)
    isotope_grid = widgets.HBox([widgets.VBox(col) for col in isotope_columns])

    ui = widgets.VBox([
        widgets.HTML("<b>Select groups and/or isotopes and assign colors</b>"),
        widgets.HTML("<b>Groups and important elements:</b>"),
        group_grid,
        widgets.HTML("<b>Individual Isotopes:</b>"),
        isotope_grid
    ])

    display(ui)
    return checkboxes, color_pickers
