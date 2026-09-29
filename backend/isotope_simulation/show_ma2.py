import sys
from pathlib import Path
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display

def show_ma2(project_root: Path = None,
             ma_label: str = "Minor Actinides infants"):
    # 1) Determine the base directory
    if project_root is None:
        project_root = Path.cwd()
    start_path = project_root / "simulation results"

    # 2) Build the widgets
    show_ma2_checkbox = widgets.Checkbox(
        value=False,
        description="Show additional MA curve",
        indent=False,
        layout=widgets.Layout(width="260px")
    )

    ma2_chooser = FileChooser(path=str(start_path))
    ma2_chooser.title = f'Select dataset'
    ma2_chooser.show_only_dirs = True
    ma2_chooser.layout = widgets.Layout(width='70%')

    ma2_colorpicker = widgets.ColorPicker(
        value="#ff7f0e",
        description="MA Color:",
        layout=widgets.Layout(width="200px")
    )

    ma2_linestyle = widgets.Dropdown(
        options={'-': '-', '--': '--', '-.': '-.', ':': ':'},
        value='-',
        description="Linestyle:",
        layout=widgets.Layout(width="180px")
    )

    ma2_marker = widgets.Dropdown(
        options={'none': 'none', 'o': 'o', 's': 's', '^': '^', 'v': 'v', 'd': 'd', 'D': 'D', '*': '*', '+': '+', 'x': 'x'},
        value='none',
        description="Marker:",
        layout=widgets.Layout(width="180px")
    )

    # Controls container and hidden box
    ma2_controls = widgets.HBox([ma2_chooser, ma2_colorpicker, ma2_linestyle, ma2_marker])
    ma2_chooser_box = widgets.VBox([ma2_controls])
    ma2_chooser_box.layout.display = 'none'

    # Toggle visibility callback
    def _toggle(change):
        ma2_chooser_box.layout.display = 'flex' if change.new else 'none'
    show_ma2_checkbox.observe(_toggle, names='value')

    # 3) Display everything
    display(widgets.VBox([show_ma2_checkbox, ma2_chooser_box]))

    # 4) Inject widget names into the notebook's global namespace
    main_mod = sys.modules['__main__']
    main_mod.show_ma2_checkbox = show_ma2_checkbox
    main_mod.ma2_chooser       = ma2_chooser
    main_mod.ma2_colorpicker   = ma2_colorpicker
    main_mod.ma2_linestyle     = ma2_linestyle
    main_mod.ma2_marker        = ma2_marker
    main_mod.ma2_label         = ma_label
