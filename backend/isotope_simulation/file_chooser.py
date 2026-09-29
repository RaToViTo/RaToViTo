def file_chooser(start_path):
    from ipyfilechooser import FileChooser
    import ipywidgets as widgets
    from IPython.display import display

    chooser = FileChooser(str(start_path))
    chooser.title = 'Select simulation results folder'
    chooser.show_only_dirs = True
    chooser.layout = widgets.Layout(width='100%') 
    display(chooser)
    return chooser
