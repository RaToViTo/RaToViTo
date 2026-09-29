import pandas as pd
import ipywidgets as widgets
from IPython.display import display


GROUP_NAMES = [
    "Total", "Plutonium", "Minor Actinides", "Uranium", "Fission Products",
    "Americium", "Curium", "Protactinium", "Thorium",
]

GROUP_COLORS = [
    "#202020", "#e67e22", "#2ca02c", "#d62728", "#1f77b4", "#7f7f7f",
    "#17becf", "#8c564b", "#e377c2", "#bcbd22", "#9467bd", "#ff9896",
    "#aec7e8", "#ffbb78", "#98df8a", "#c5b0d5", "#c49c94", "#f7b6d2",
    "#9edae5",
]

LINESTYLES = [("Solid", "-"), ("Dashed", "--"), ("Dotted", ":"), ("Dash-dot", "-.")]
ISOTOPE_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]


def plot_UI_inv(excel_file_fuel, selected_sheet):
    fuel_df = pd.read_excel(str(excel_file_fuel), sheet_name=selected_sheet, skiprows=1)
    fuel_df.columns = fuel_df.columns.astype(str).str.strip()
    if "Nuclide" not in fuel_df.columns:
        raise ValueError("The selected fuel sheet must contain a 'Nuclide' column.")

    initial_isotopes = sorted(set(
        fuel_df["Nuclide"].dropna().astype(str).str.strip()
    ))
    checkboxes = {}
    color_pickers = {}
    linestyle_selectors = {}

    def make_row(name, color):
        checkbox = widgets.Checkbox(
            value=False,
            description=name,
            indent=False,
            layout=widgets.Layout(width="190px"),
        )
        color_picker = widgets.ColorPicker(
            concise=True,
            value=color,
            layout=widgets.Layout(width="45px"),
        )
        linestyle = widgets.Dropdown(
            options=LINESTYLES,
            value="-",
            layout=widgets.Layout(width="90px"),
        )
        checkboxes[name] = checkbox
        color_pickers[name] = color_picker
        linestyle_selectors[name] = linestyle
        return widgets.HBox([checkbox, color_picker, linestyle])

    group_rows = [
        make_row(name, GROUP_COLORS[index % len(GROUP_COLORS)])
        for index, name in enumerate(GROUP_NAMES)
    ]
    isotope_rows = [
        make_row(name, ISOTOPE_COLORS[index % len(ISOTOPE_COLORS)])
        for index, name in enumerate(initial_isotopes)
    ]

    def columns(rows, count):
        items_per_column = max(1, (len(rows) + count - 1) // count)
        return [
            widgets.VBox(rows[index * items_per_column:(index + 1) * items_per_column])
            for index in range(count)
        ]

    groups_panel = widgets.HBox(columns(group_rows, 3))
    isotope_panel = widgets.Box(
        columns(isotope_rows, 4),
        layout=widgets.Layout(max_height="480px", overflow_y="auto"),
    )
    isotope_accordion = widgets.Accordion(children=[isotope_panel])
    isotope_accordion.set_title(0, f"Initial spent-fuel isotopes ({len(initial_isotopes)})")
    isotope_accordion.selected_index = 0

    display(widgets.VBox([
        widgets.HTML("<b>Select groups and initial isotopes; set a color and line style for each curve.</b>"),
        widgets.HTML("<b>Groups</b>"),
        groups_panel,
        isotope_accordion,
    ]))

    return checkboxes, color_pickers, linestyle_selectors