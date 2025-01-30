# Modified Fuel Assembly Map Analyzer and Visualizer, For Square Lattice
# Author : Alfonsus Rahmadi Putranto
# This script is able to visualize and analyze modified FA 
# before implementing it in Deterministic/Monte Carlo code
# Multiple kind of fuel pin is possible, up to 5 different kind of fuel pin
# Important rule, the filename shoud follows nPin_<free text>.txt
# Important rule, guide tube is represented as 0 or 'O'

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

def FA_reader(filename):
    # Try reading the FA Map as integer
    try :
        fa_map = np.loadtxt(filename)
    # Try reading the FA Map as string
    except :
        with open(filename) as f:
            fa_map = np.array([line.strip().split() for line in f.readlines()])

    # Get the nPin/2 of from the first part of file name
    nPin = int(filename.split('_')[0].split('.')[0])

    # Calculate the number of different kind of fuel pin based on dtype
    unique_pin = np.unique(fa_map)
    num_unique_pin = len(unique_pin)

    # Assign different color for each kind of fuel pin
    colors = ["#5f4584", "#c81414", "#007e1e", "#006bff", "#2f4858", "#5f4584"]
    color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_pin)}

    analysis = {
        'nPin': nPin,
        'fa_map': fa_map,
        'unique_pin': unique_pin,
        'num_unique_pin': num_unique_pin,
        'color_map': color_map
    }

    return analysis

def FA_visualizer(params, analysis):
    # Unpack parameters
    fuel_radius = params['fuel_radius']
    gap = params['gap']
    cladding_thickness = params['cladding_thickness']
    nPin = params['nPin']
    pitch_size = params['pitch_size']
    FA_size = params['FA_size']
    
    # Unpack analysis
    fa_map = analysis['fa_map']
    color_map = analysis['color_map']
    
    # Create figure
    fig = go.Figure()
    
    # Draw FA based on even/odd number of pins
    if nPin % 2 == 0:
        # For even number of pins
        pin_range = range(nPin//2)
        for i in pin_range:
            for j in pin_range:
                x_center = j * pitch_size + pitch_size / 2
                y_center = i * pitch_size + pitch_size / 2

                # Add moderator background
                fig.add_shape(
                    type="rect",
                    x0=j * pitch_size,
                    y0=i * pitch_size,
                    x1=(j+1) * pitch_size,
                    y1=(i+1) * pitch_size,
                    line=dict(color="green", width=1),
                    fillcolor="lightblue",
                    opacity=0.7
                )
                
                # Add pin components based on pin type
                if fa_map[i][j] != 0 and fa_map[i][j] != 'O':  # If not guide tube
                    # Add cladding
                    fig.add_shape(
                        type="circle",
                        x0=x_center - (fuel_radius + gap + cladding_thickness),
                        y0=y_center - (fuel_radius + gap + cladding_thickness),
                        x1=x_center + (fuel_radius + gap + cladding_thickness),
                        y1=y_center + (fuel_radius + gap + cladding_thickness),
                        line=dict(color="green", width=1),
                        fillcolor="green",
                        opacity=0.4
                    )
                    
                    # Add gap
                    fig.add_shape(
                        type="circle",
                        x0=x_center - (fuel_radius + gap),
                        y0=y_center - (fuel_radius + gap),
                        x1=x_center + (fuel_radius + gap),
                        y1=y_center + (fuel_radius + gap),
                        line=dict(color="yellow", width=1),
                        fillcolor="yellow",
                        opacity=0.7
                    )
                    
                    # Add fuel
                    fig.add_shape(
                        type="circle",
                        x0=x_center - fuel_radius,
                        y0=y_center - fuel_radius,
                        x1=x_center + fuel_radius,
                        y1=y_center + fuel_radius,
                        line=dict(color="red", width=1),
                        fillcolor=color_map[fa_map[i][j]],
                        opacity=0.9
                    )
        x_in, y_in = 0, 0
        x_out, y_out = FA_size/2 + 1, FA_size/2 + 1

    else:
        # For odd number of pins
        pin_range = range((nPin+1)//2)
        for i in pin_range:
            for j in pin_range:
                x_center = j * pitch_size
                y_center = i * pitch_size

                # Add moderator background
                fig.add_shape(
                    type="rect",
                    x0=(2*j-1)/2 * pitch_size,
                    y0=(2*i-1)/2 * pitch_size,
                    x1=(2*j+1)/2 * pitch_size,
                    y1=(2*i+1)/2 * pitch_size,
                    line=dict(color="green", width=1),
                    fillcolor="lightblue",
                    opacity=0.7
                )
                
                # Add pin components based on pin type
                if fa_map[i][j] != 0 and fa_map[i][j] != 'O':  # If not guide tube
                    # Add cladding
                    fig.add_shape(
                        type="circle",
                        x0=x_center - (fuel_radius + gap + cladding_thickness),
                        y0=y_center - (fuel_radius + gap + cladding_thickness),
                        x1=x_center + (fuel_radius + gap + cladding_thickness),
                        y1=y_center + (fuel_radius + gap + cladding_thickness),
                        line=dict(color="green", width=1),
                        fillcolor="green",
                        opacity=0.4
                    )
                    
                    # Add gap
                    fig.add_shape(
                        type="circle",
                        x0=x_center - (fuel_radius + gap),
                        y0=y_center - (fuel_radius + gap),
                        x1=x_center + (fuel_radius + gap),
                        y1=y_center + (fuel_radius + gap),
                        line=dict(color="yellow", width=1),
                        fillcolor="yellow",
                        opacity=0.7
                    )
                    
                    # Add fuel
                    fig.add_shape(
                        type="circle",
                        x0=x_center - fuel_radius,
                        y0=y_center - fuel_radius,
                        x1=x_center + fuel_radius,
                        y1=y_center + fuel_radius,
                        line=dict(color="red", width=1),
                        fillcolor=color_map[fa_map[i][j]],
                        opacity=0.9
                    )
        x_in, y_in = -pitch_size/2, -pitch_size/2
        x_out, y_out = FA_size/2 + 1, FA_size/2 + 1

    # Update layout
    fig.update_layout(
        width=800,
        height=800,
        showlegend=True,
        plot_bgcolor='white',
        title='Fuel Assembly Layout (1/4 Symmetry)'
    )

    # Update axes
    fig.update_xaxes(
        range=[x_in, x_out],
        scaleanchor='y',
        scaleratio=1,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )
    fig.update_yaxes(
        range=[y_in, y_out],
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )

    fig.show()
    return 0
