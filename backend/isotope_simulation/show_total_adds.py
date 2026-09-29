import sys
from pathlib import Path
import ipywidgets as widgets
from IPython.display import display

def show_total_adds(project_root: Path = None,
                    total_label: str = "Total of additionals"):
    """
    Erstellt eine Checkbox und Widgets für die Anzeige der Summe aller zusätzlichen Kurven.
    Die Widgets werden rechtsbündig in einer Zeile angezeigt, ähnlich wie bei "Show additional Total curve".
    """
    if project_root is None:
        project_root = Path.cwd()

    # Checkbox für die Anzeige der Total-Kurve
    show_total_adds_checkbox = widgets.Checkbox(
        value=False,
        description="Show total of additionals",
        indent=False,
        layout=widgets.Layout(width="260px")
    )

    # Widgets für Farbe, Linienstil und Marker
    total_adds_colorpicker = widgets.ColorPicker(
        value="#000000",
        description="Total Color:",
        layout=widgets.Layout(width="200px"),
        style={'description_width': 'initial'}
    )

    total_adds_linestyle = widgets.Dropdown(
        options={'-': '-', '--': '--', '-.': '-.', ':': ':'},
        value='-',
        description="Linestyle:",
        layout=widgets.Layout(width="200px")
    )

    total_adds_marker = widgets.Dropdown(
        options={'none': 'none', 'o': 'o', 's': 's', '^': '^', 'v': 'v', 'd': 'd', 'D': 'D', '*': '*', '+': '+', 'x': 'x'},
        value='none',
        description="Marker:",
        layout=widgets.Layout(width="200px")
    )

    # Container für die Widgets (Farbe, Linienstil, Marker)
    total_adds_controls = widgets.HBox([
        total_adds_colorpicker,
        total_adds_linestyle,
        total_adds_marker
    ])

    # Container für die Checkbox und die Widgets
    total_adds_box = widgets.HBox([show_total_adds_checkbox, total_adds_controls])

    # Sichtbarkeit der Widgets steuern
    def _toggle(change):
        total_adds_controls.layout.display = 'flex' if change.new else 'none'
    show_total_adds_checkbox.observe(_toggle, names='value')
    total_adds_controls.layout.display = 'none'  # Standardmäßig ausgeblendet

    # Zeige die Widgets an
    display(total_adds_box)

    # Injiziere die Widget-Namen in den globalen Namensraum
    main_mod = sys.modules['__main__']
    main_mod.show_total_adds_checkbox = show_total_adds_checkbox
    main_mod.total_adds_colorpicker = total_adds_colorpicker
    main_mod.total_adds_linestyle = total_adds_linestyle
    main_mod.total_adds_marker = total_adds_marker
    main_mod.total_adds_label = total_label