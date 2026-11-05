#Graph settings
plot_config = {

    #save_plot
    "save_plot" : False,

    #Cooling time/Data offset
    "offset" : 0,

    #Graph linestyle
    "linewidth" : 1.0,

    #Figure size
    "fig_width" : 3,
    "fig_height" : 3,

    #Axis
    "plot_axis_range_x" : [1e0, 1e6],
    "plot_axis_range_y" : [1e0, 1e10],

    "xaxis_ticks": 6,
    "yaxis_ticks": 8,
    "xticks_fontsize" : 5,
    "yticks_fontsize" : 5,

    #Titles; no slashes allowed
    "show_title": True,
    "plot_title" : f"Radiotoxicity of Spent Fuel incl. Decay Products", 
    #"plot_title" : f"Material sent to final repository",

    "show_subtitle": True,
    #"plot_subtitle" : "SF at discharge, UO2, 4.5%, 65 GWd/t, Adults",
    "plot_subtitle" : "SNF at discharge, UO2, 4.5%, 65 GWd/t, n$_{repro. cyc.}$=10, Adults",
    #"plot_subtitle" : "SF at discharge, MOX, 65 GWd/t, Infants",
    #"plot_subtitle" : "SF at discharge, UO2, 4.5%, 65 GWd/t, n$_{repro. cyc.}$=10, Adults",

    "plot_xlabel" : "Time (years)",
    "plot_ylabel" : "Radiotoxicity [Sv/t$_{IHM}$]",

    #Footnote
    "show_footnote" : False,
    #"footnote_text" : "IHM = Initial Heavy Metal\nSF = Spent Fuel\nPart. eff.s: U = 99.9%, Pu = 99.5%, MA = 99.95%",
    "footnote_text" : "Part. eff.s: U = 99.88%,\nPu = 99.88%, MA = 99.99%",

    #Font name and sizes
    "font_name" : 'DejaVu Sans',
    "title_fontsize" : 5,
    "label_fontsize" : 6,
    "legend_fontsize" : 4,
    "subtitle_fontsize" : 4,
    "linewidth": 1,

    #Legend
    "show_legend" : False,
    "plot_legend_loc" : 'upper right',
    "legend_outside" : False,  #False = inside
    #legend_order" : ["Total adults", "Minor Actinides adults", "Fission Products adults", "Natural Uranium (8.41t) adults", "Total infants", "Minor Actinides infants", "Fission Products infants"],

    #Line labels
    "show_line_labels": True,
    "line_label_fontsize": 4.3,
    "line_label_color": "black",
    "line_labels": {
        #"Total": {"x": 5e1, "y": 4e8},
        #"Plutonium": {"x": 1.2e0, "y": 180e6},
        #"Pu res.": {"x": 1e2, "y": 1e4},
        #"Minor Actinides Adults": {"x": 5e2, "y": 2.3e6},
        #"Minor Actinides Infants": {"x": 1.3e3, "y": 4e7},
        #"MA res.": {"x": 1e2, "y": 1e4},
        #"Uranium": {"x": 1.3e1, "y": 4e3},
        #"U res.": {"x": 1e2, "y": 1e4},
        "Fission Products": {"x": 5.5e2, "y": 1.5e4},
        #"Fission products Infants": {"x": 6.8e1, "y": 7.7e8},
        #"FPs + res.": {"x": 1e2, "y": 1e4},
        #"Americium": {"x": 1e2, "y": 1e4},
        #"Curium": {"x": 1e2, "y": 1e4},
        #"Protactinium": {"x": 1e2, "y": 1e4},
        #"Thorium": {"x": 1e2, "y": 1e4},
        #"PUREX": {"x": 1e2, "y": 1e4},
        #"PUREX+iSANEX": {"x": 1e2, "y": 1e4},
        #"PUREX+HPLC": {"x": 1e2, "y": 1e4},
        #"CHALMEX": {"x": 1e2, "y": 1e4},
        "Nat. U (8.41t) Adults": {"x": 1.3e0, "y": 3.4e5},
        #"Nat. U (8.41t) Infants": {"x": 1.3e0, "y": 8.5e6},
        "McArthur River/Key Lake": {"x": 1.5e0, "y": 5e3},
        "Inkai": {"x": 1.5e0, "y": 5e1},
        "Theo. clearance value": {"x": 1.5e0, "y": 8e0},
    },
    
    #Grid
    "plot_grid_show" : True,
    "plot_grid_which" : 'major',
    "plot_grid_linestyle" : '--',
    "plot_grid_linewidth" : 0.3,

    #resolution
    "dpi" : 300,
}