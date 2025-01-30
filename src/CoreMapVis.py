# Modified Core Map Analyzer and Visualizer, For Square Lattice
# Author : Alfonsus Rahmadi Putranto
# This script is able to visualize and analyze modified CoreMap
# before implementing it in Deterministic/Monte Carlo code
# Multiple kind of FA is possible, up to 6 different kind of FA
# Denoted in the FA index from 0 to 6, as 0 means absence of FA, and 1 to 6 means presence of different FA
# Additional function is made to read string input, with general rule of 'O' for empty space

import numpy as np
import math
import plotly.graph_objects as go

# Info reader for the pin/FA parameters
def info_reader(filename) :
    params = {}
    # Read the input file, the output from initial visualization
    with open("input.txt") as f:
        # Read every line
        for line in f:
            if ':' in line:
                # Get the keyword and value
                key, value = line.strip().split(':')
                key = key.strip()
                value = value.strip()
                
                # Most of values are float, only one integer in nPin
                try:
                    # Convert to float all values
                    value = float(value)
                    # For nPin, convert to integer
                    if key in ['nPin']:
                        value = int(value)
                except ValueError:
                    # Keep as string if conversion fails
                    pass
                
                params[key] = value

    return params

# Core reader for integer or string FA name
def core_reader(filename):
    # Read the FA file for 1/4 symmetry
    try:
        # Try reading as int array first
        core_map = np.loadtxt(filename)
    except:
        # If fails, read as string array
        with open(filename, 'r') as f:
            core_map = np.array([line.strip().split() for line in f.readlines()])

    # Calculate the number of different kind of FA based on dtype
    if np.issubdtype(core_map.dtype, np.number):
        unique_FA = np.unique(core_map[core_map != 0])
        empty_condition = lambda x: x > 0
    else:
        unique_FA = np.unique(core_map[core_map != 'O'])
        empty_condition = lambda x: x != 'O'
    
    num_unique_FA = len(unique_FA)

    # Assign different color for each kind of FA
    colors = ["#ff6637", "#56423c", "#bda69f", "#40ad25", "#007700"]
    color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_FA)}

    # Rediscribe FA distribution
    fa_per_layer = np.sum([empty_condition(x) for x in core_map], axis=1)
    total_fa = np.sum([empty_condition(x) for x in core_map])

    analysis = {
        'num_unique_FA': num_unique_FA,
        'unique_FA': unique_FA,
        'color_map': color_map,
        'fa_per_layer': fa_per_layer,
        'total_fa': total_fa,
        'core_map' : core_map
    }

    return analysis
    

def CoreMapVisualizer(analysis, params):
    # Unpack the analysis and params
    # Unpack parameters
    core_radius = params['core_radius']
    active_core_radius = params['active_core_radius']
    FA_size = params['FA_size']
    num_FA = params['num_FA']
    unique_FA = analysis['unique_FA']
    color_map = analysis['color_map']
    core_map = analysis['core_map']

    # Create figure
    fig = go.Figure()

    # Draw the core boundary circle (outer)
    fig.add_shape(
        type="circle",
        x0=-core_radius,
        y0=-core_radius,
        x1=core_radius,
        y1=core_radius,
        fillcolor="lightgrey",
        opacity=0.5,
        line=dict(color="blue", width=2),
        layer='below'
    )

    # Draw the inner circle (active core)
    fig.add_shape(
        type="circle",
        x0=-active_core_radius,
        y0=-active_core_radius,
        x1=active_core_radius,
        y1=active_core_radius,
        fillcolor="lightblue",
        opacity=0.5,
        line=dict(color="green", width=2),
        layer='below'
    )

    # Check the dtype of core_map to determine how to handle empty positions
    if np.issubdtype(core_map.dtype, np.number):
        # For numeric arrays (int/float)
        empty_condition = lambda x: x > 0
    else:
        # For string arrays
        empty_condition = lambda x: x != 'O'

    # Draw FA based on core map
    if num_FA % 2 == 0:
        in_x, in_y = 0, 0
        for i in range(len(core_map)):
            for j in range(len(core_map[i])):
                if empty_condition(core_map[i][j]):
                    fig.add_shape(
                        type="rect",
                        x0=j*FA_size,
                        y0=i*FA_size,
                        x1=(j+1)*FA_size,
                        y1=(i+1)*FA_size,
                        line=dict(color="black", width=1),
                        fillcolor=color_map[core_map[i][j]],
                        opacity=1
                    )
    else:
        in_x, in_y = -FA_size/2, -FA_size/2
        for i in range(len(core_map)):
            for j in range(len(core_map[i])):
                if empty_condition(core_map[i][j]):
                    fig.add_shape(
                        type="rect",
                        x0=(2*j-1)/2*FA_size,
                        y0=(2*i-1)/2*FA_size,
                        x1=(2*j+1)/2*FA_size,
                        y1=(2*i+1)/2*FA_size,
                        line=dict(color="black", width=1),
                        fillcolor=color_map[core_map[i][j]],
                        opacity=1
                    )

    # Add rectangles for legends for each unique FA
    for value in unique_FA:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color=color_map[value],
                    size=15,
                    symbol='square'
                ),
                name=f'FA {value}',
                showlegend=True
            )
        )

    # Update layout
    fig.update_layout(
        width=800,
        height=800,
        showlegend=True,
        plot_bgcolor='white',
        title='Core Map (1/4 Symmetry)'
    )

    # Update axes
    fig.update_xaxes(
        range=[in_x, core_radius + 10],
        scaleanchor='y',
        constrain='domain',
        scaleratio=1,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )
    fig.update_yaxes(
        range=[in_y, core_radius + 10],
        gridcolor='lightgrey',
        constrain='domain',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )

    fig.show()

    return 0
