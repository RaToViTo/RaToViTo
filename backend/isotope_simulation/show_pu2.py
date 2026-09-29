import sys
from pathlib import Path
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display

def show_pu2(project_root: Path = None,
             pu_label: str = "Plutonium infants"):
    # 1) Determine the base directory
    if project_root is None:
        project_root = Path.cwd()
    start_path = project_root / "simulation results"

    # 2) Build the widgets
    show_pu2_checkbox = widgets.Checkbox(
        value=False,
        description="Show additional Pu curve",
        indent=False,
        layout=widgets.Layout(width="260px")
    )

    pu2_chooser = FileChooser(path=str(start_path))
    pu2_chooser.title = f'Select dataset'
    pu2_chooser.show_only_dirs = True
    pu2_chooser.layout = widgets.Layout(width='70%')

    pu2_colorpicker = widgets.ColorPicker(
        value="#2ca02c",
        description="Pu Color:",
        layout=widgets.Layout(width="200px")
    )

    pu2_linestyle = widgets.Dropdown(
        options={'-': '-', '--': '--', '-.': '-.', ':': ':'},
        value='-',
        description="Linestyle:",
        layout=widgets.Layout(width="180px")
    )

    pu2_marker = widgets.Dropdown(
        options={'none': 'none', 'o': 'o', 's': 's', '^': '^', 'v': 'v', 'd': 'd', 'D': 'D', '*': '*', '+': '+', 'x': 'x'},
        value='none',
        description="Marker:",
        layout=widgets.Layout(width="180px")
    )

    # Controls container and hidden box
    pu2_controls = widgets.HBox([pu2_chooser, pu2_colorpicker, pu2_linestyle, pu2_marker])
    pu2_chooser_box = widgets.VBox([pu2_controls])
    pu2_chooser_box.layout.display = 'none'

    # Toggle visibility callback
    def _toggle(change):
        pu2_chooser_box.layout.display = 'flex' if change.new else 'none'
    show_pu2_checkbox.observe(_toggle, names='value')

    # 3) Display everything
    display(widgets.VBox([show_pu2_checkbox, pu2_chooser_box]))

    # 4) Inject widget names into the notebook's global namespace
    main_mod = sys.modules['__main__']
    main_mod.show_pu2_checkbox = show_pu2_checkbox
    main_mod.pu2_chooser       = pu2_chooser
    main_mod.pu2_colorpicker   = pu2_colorpicker
    main_mod.pu2_linestyle     = pu2_linestyle
    main_mod.pu2_marker        = pu2_marker
    main_mod.pu2_label         = pu_label
