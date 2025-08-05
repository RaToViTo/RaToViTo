def plot_UI_inv():
    import ipywidgets as widgets
    from IPython.display import display

    # === Group definition ===
    group_names = [
        "Total", "Plutonium", "Minor Actinoides", "Uranium", "Fission Products", "Decay Products",
        "Neptunium", "Americium", "Curium", "Berkelium", "Californium",
        "Einsteinium", "Fermium", "Protactinium", "Thorium", "Actinium",
        "Mendelevium", "Nobelium", "Lawrencium"
    ]

    # === Prepare widgets ===
    checkboxes = {}
    color_pickers = {}

    def make_group_row(name):
        cb = widgets.Checkbox(value=False, description=name, indent=False, layout=widgets.Layout(width="150px"))
        cp = widgets.ColorPicker(value="#1f77b4", layout=widgets.Layout(width="120px"))
        checkboxes[name] = cb
        color_pickers[name] = cp
        return widgets.HBox([cb, cp])

    # Column 1 & 2 of groups
    group_rows_col1 = [make_group_row(name) for name in group_names[:10]]
    group_rows_col2 = [make_group_row(name) for name in group_names[10:]]

    # === Input fields for isotopes ===
    isotope_textboxes = []
    isotope_colors = []

    for _ in range(10):
        txt = widgets.Text(placeholder="e.g. Am241", layout=widgets.Layout(width="100px"))
        cp = widgets.ColorPicker(value="#1f77b4", layout=widgets.Layout(width="120px"))
        isotope_textboxes.append(txt)
        isotope_colors.append(cp)

    isotope_inputs = [widgets.HBox([txt, cp]) for txt, cp in zip(isotope_textboxes, isotope_colors)]

    # === Title row ===
    group_title_col1 = widgets.HTML("<b>Groups and important elements:</b>")
    group_title_col2 = widgets.HTML("")  # leave empty
    isotope_title = widgets.HTML("<b style='margin-left:439px;'>Individual Isotopes:</b>")

    title_row = widgets.HBox([group_title_col1, group_title_col2, isotope_title])

    # === Assemble===
    ui = widgets.VBox([
        widgets.HTML("<b>Select groups and/or isotopes and assign colors</b>"),
        title_row,
        widgets.HBox([
            widgets.VBox(group_rows_col1),
            widgets.VBox(group_rows_col2, layout=widgets.Layout(margin='0 0 0 30px')),
            widgets.VBox(isotope_inputs, layout=widgets.Layout(margin='0 0 0 60px'))  # Spacing to the right
    ])
    ])    

    display(ui)

    return checkboxes, color_pickers, isotope_textboxes, isotope_colors