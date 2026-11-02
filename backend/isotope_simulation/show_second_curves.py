import sys
from pathlib import Path

import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display


_CURVE_CONFIG = {
    "ma": {
        "prefix": "ma2",
        "checkbox": "Show additional MA curve",
        "color_label": "MA Color:",
        "color": "#ff7f0e",
        "label": "Minor Actinides infants",
    },
    "fp": {
        "prefix": "fp2",
        "checkbox": "Show additional FP curve",
        "color_label": "FP2 Color:",
        "color": "#1f77b4",
        "label": "Fission Products infants",
    },
    "pu": {
        "prefix": "pu2",
        "checkbox": "Show additional Pu curve",
        "color_label": "Pu Color:",
        "color": "#2ca02c",
        "label": "Plutonium infants",
    },
    "total": {
        "prefix": "total2",
        "checkbox": "Show additional Total curve",
        "color_label": "Total Color:",
        "color": "#d62728",
        "label": "Total infants",
    },
}

_LINESTYLES = {"-": "-", "--": "--", "-.": "-.", ":": ":"}
_MARKERS = {
    "none": "none",
    "o": "o",
    "s": "s",
    "^": "^",
    "v": "v",
    "d": "d",
    "D": "D",
    "*": "*",
    "+": "+",
    "x": "x",
}


def show_additional_curve(curve, project_root: Path = None, label=None):
    """Display the checkbox and controls for one additional dataset curve."""
    if curve not in _CURVE_CONFIG:
        raise ValueError(f"Unknown additional curve type: {curve!r}")

    config = _CURVE_CONFIG[curve]
    prefix = config["prefix"]
    if project_root is None:
        project_root = Path.cwd()
    start_path = project_root / "simulation results"

    checkbox = widgets.Checkbox(
        value=False,
        description=config["checkbox"],
        indent=False,
        layout=widgets.Layout(width="260px"),
    )
    chooser = FileChooser(path=str(start_path))
    chooser.title = "Select dataset"
    chooser.show_only_dirs = True
    chooser.layout = widgets.Layout(width="70%")

    colorpicker = widgets.ColorPicker(
        value=config["color"],
        description=config["color_label"],
        layout=widgets.Layout(width="200px"),
    )
    linestyle = widgets.Dropdown(
        options=_LINESTYLES,
        value="-",
        description="Linestyle:",
        layout=widgets.Layout(width="180px"),
    )
    marker = widgets.Dropdown(
        options=_MARKERS,
        value="none",
        description="Marker:",
        layout=widgets.Layout(width="180px"),
    )

    controls = widgets.HBox([chooser, colorpicker, linestyle, marker])
    chooser_box = widgets.VBox([controls])
    chooser_box.layout.display = "none"

    def toggle(change):
        chooser_box.layout.display = "flex" if change.new else "none"

    checkbox.observe(toggle, names="value")
    display(widgets.VBox([checkbox, chooser_box]))

    main_mod = sys.modules["__main__"]
    setattr(main_mod, f"show_{prefix}_checkbox", checkbox)
    setattr(main_mod, f"{prefix}_chooser", chooser)
    setattr(main_mod, f"{prefix}_colorpicker", colorpicker)
    setattr(main_mod, f"{prefix}_linestyle", linestyle)
    setattr(main_mod, f"{prefix}_marker", marker)
    setattr(main_mod, f"{prefix}_label", config["label"] if label is None else label)


def show_total_adds(project_root: Path = None,
                    total_label: str = "Total of additionals"):
    """Display controls for the sum of all additional curves."""
    if project_root is None:
        project_root = Path.cwd()

    checkbox = widgets.Checkbox(
        value=False,
        description="Show total of additionals",
        indent=False,
        layout=widgets.Layout(width="260px"),
    )
    colorpicker = widgets.ColorPicker(
        value="#000000",
        description="Total Color:",
        layout=widgets.Layout(width="200px"),
        style={"description_width": "initial"},
    )
    linestyle = widgets.Dropdown(
        options=_LINESTYLES,
        value="-",
        description="Linestyle:",
        layout=widgets.Layout(width="200px"),
    )
    marker = widgets.Dropdown(
        options=_MARKERS,
        value="none",
        description="Marker:",
        layout=widgets.Layout(width="200px"),
    )

    controls = widgets.HBox([colorpicker, linestyle, marker])
    controls.layout.display = "none"

    def toggle(change):
        controls.layout.display = "flex" if change.new else "none"

    checkbox.observe(toggle, names="value")
    display(widgets.HBox([checkbox, controls]))

    main_mod = sys.modules["__main__"]
    main_mod.show_total_adds_checkbox = checkbox
    main_mod.total_adds_colorpicker = colorpicker
    main_mod.total_adds_linestyle = linestyle
    main_mod.total_adds_marker = marker
    main_mod.total_adds_label = total_label
