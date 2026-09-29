import sys
from pathlib import Path
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display

def show_fp2(project_root: Path = None,
             fp2_label: str = "Fission Products infants"):
    # 1) Determine the base directory
    if project_root is None:
        project_root = Path.cwd()
    start_path = project_root / "simulation results"

    # 2) Build the widgets
    show_fp2_checkbox = widgets.Checkbox(
        value=False,
        description="Show additional FP curve",
        indent=False,
        layout=widgets.Layout(width="260px")
    )

    fp2_chooser = FileChooser(path=str(start_path))
    fp2_chooser.title = f'Select dataset'
    fp2_chooser.show_only_dirs = True
    fp2_chooser.layout = widgets.Layout(width='70%')

    fp2_colorpicker = widgets.ColorPicker(
        value="#1f77b4",
        description="FP2 Color:",
        layout=widgets.Layout(width="200px")
    )

    fp2_linestyle = widgets.Dropdown(
        options={'-': '-', '--': '--', '-.': '-.', ':': ':'},
        value='-',
        description="Linestyle:",
        layout=widgets.Layout(width="180px")
    )

    fp2_marker = widgets.Dropdown(
        options={'none': 'none', 'o': 'o', 's': 's', '^': '^', 'v': 'v', 'd': 'd', '*': '*', '+': '+', 'x': 'x'},
        value='none',
        description="Marker:",
        layout=widgets.Layout(width="180px")
    )

    # Controls container and hidden box
    fp2_controls = widgets.HBox([fp2_chooser, fp2_colorpicker, fp2_linestyle, fp2_marker])
    fp2_chooser_box = widgets.VBox([fp2_controls])
    fp2_chooser_box.layout.display = 'none'

    # Toggle visibility callback
    def _toggle(change):
        fp2_chooser_box.layout.display = 'flex' if change.new else 'none'
    show_fp2_checkbox.observe(_toggle, names='value')

    # 3) Display everything
    display(widgets.VBox([show_fp2_checkbox, fp2_chooser_box]))

    # 4) Inject widget names into the notebook's global namespace
    main_mod = sys.modules['__main__']
    main_mod.show_fp2_checkbox = show_fp2_checkbox
    main_mod.fp2_chooser       = fp2_chooser
    main_mod.fp2_colorpicker   = fp2_colorpicker
    main_mod.fp2_linestyle     = fp2_linestyle
    main_mod.fp2_marker        = fp2_marker
    main_mod.fp2_label         = fp2_label
