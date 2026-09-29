#Graph settings
plot_config = {

    #save_plot
    "save_plot" : False,

    #Cooling time/Data offset
    "offset" : 0,

    #Graph linestyle
    "linewidth" : 2.0,

    #Figure size
    "fig_width" : 12,
    "fig_height" : 7,

    #Axis
    "plot_axis_range_x" : [1e0, 1e6],
    "plot_axis_range_y" : [1e0, 1e10],

    "xticks_fontsize" : 12,
    "yticks_fontsize" : 12,

    #Titles; no slashes allowed
    "plot_title" : f"Radiotoxicity of Spent Fuel incl. Decay Products", 
    #"plot_title" : f"Material sent to final repository",

    #"plot_subtitle" : "SF at discharge, UO2, 4.5%, 65 GWd/t, Adults",
    #"plot_subtitle" : "SF at discharge, UO2, 4.5%, 65 GWd/t, Adults vs. Infants",
    #"plot_subtitle" : "SF at discharge, MOX, 65 GWd/t, Infants",
    "plot_subtitle" : "SF at discharge, UO2, 4.5%, 65 GWd/t, n$_{repro. cyc.}$=10, Adults",

    "plot_xlabel" : "Time (years)",
    "plot_ylabel" : "Radiotoxicity [Sv/t$_{IHM}$]",

    #Footnote
    "show_footnote" : False,
    #"footnote_text" : "IHM = Initial Heavy Metal\nSF = Spent Fuel\nPart. eff.s: U = 99.9%, Pu = 99.5%, MA = 99.95%",
    "footnote_text" : "res = residuals\nPart. eff.s: U = 99.88%, Pu = 99.88%, MA = varied",

    #Font name and sizes
    "font_name" : 'DejaVu Sans',
    "title_fontsize" : 14,
    "label_fontsize" : 13,
    "legend_fontsize" : 10,
    "subtitle_fontsize" : 12,
    "linewidth": 2,

    #Legend location
    "show_legend" : True,
    "plot_legend_loc" : 'upper right',
    "legend_outside" : False,  #False = inside
    #legend_order" : ["Total adults", "Minor Actinides adults", "Fission Products adults", "Natural Uranium (8.41t) adults", "Total infants", "Minor Actinides infants", "Fission Products infants"],

    #Grid
    "plot_grid_show" : True,
    "plot_grid_which" : 'major',
    "plot_grid_linestyle" : '--',
    "plot_grid_linewidth" : 0.5,

    #resolution
    "dpi" : 300,
}