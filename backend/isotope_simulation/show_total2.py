import sys
from pathlib import Path
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display

def show_total2(project_root: Path = None,
                total_label: str = "Total infants"):
    # 1) Determine the base directory
    if project_root is None:
        project_root = Path.cwd()
    start_path = project_root / "simulation results"

    # 2) Build the widgets
    show_total2_checkbox = widgets.Checkbox(
        value=False,
        description="Show additional Total curve",
        indent=False,
        layout=widgets.Layout(width="260px")
    )

    total2_chooser = FileChooser(path=str(start_path))
    total2_chooser.title = f'Select dataset'
    total2_chooser.show_only_dirs = True
    total2_chooser.layout = widgets.Layout(width='70%')

    total2_colorpicker = widgets.ColorPicker(
        value="#d62728",
        description="Total Color:",
        layout=widgets.Layout(width="200px")
    )

    total2_linestyle = widgets.Dropdown(
        options={'-': '-', '--': '--', '-.': '-.', ':': ':'},
        value='-',
        description="Linestyle:",
        layout=widgets.Layout(width="180px")
    )

    total2_marker = widgets.Dropdown(
        options={'none': 'none', 'o': 'o', 's': 's', '^': '^', 'v': 'v', 'd': 'd', 'D': 'D', '*': '*', '+': '+', 'x': 'x'},
        value='none',
        description="Marker:",
        layout=widgets.Layout(width="180px")
    )

    # Controls container and hidden box
    total2_controls = widgets.HBox([total2_chooser, total2_colorpicker, total2_linestyle, total2_marker])
    total2_chooser_box = widgets.VBox([total2_controls])
    total2_chooser_box.layout.display = 'none'

    # Toggle visibility callback
    def _toggle(change):
        total2_chooser_box.layout.display = 'flex' if change.new else 'none'
    show_total2_checkbox.observe(_toggle, names='value')

    # 3) Display everything
    display(widgets.VBox([show_total2_checkbox, total2_chooser_box]))

    # 4) Inject widget names into the notebook's global namespace
    main_mod = sys.modules['__main__']
    main_mod.show_total2_checkbox = show_total2_checkbox
    main_mod.total2_chooser       = total2_chooser
    main_mod.total2_colorpicker   = total2_colorpicker
    main_mod.total2_linestyle     = total2_linestyle
    main_mod.total2_marker        = total2_marker
    main_mod.total2_label         = total_label
