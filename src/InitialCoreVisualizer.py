# Initial reactor core mapper for square assembies, constant core radius
# Author : Alfonsus Rahmadi Putranto
# This script will maximize the number of FA in the diameter, with certain tolerance that is represented in the core_gap variable below
# Input in FA : fuel radius, gap, cladding thickness, Npin per FA, fuel to moderator ratio
# To be calculated : Number of FA in the diameter, Number of overall FA
# Output : 1/4 symmetry of the core visualization and Fuel assembly map

# Mainly used in the beginning of optimization, to easily determine fuel zones in core map
# In FA case, can be used to choose the positions of water rod or poison fuel
# Output can be pasted in most Monte Carlo code, 
# at the most some modification is needed to change int to string  

import math
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

def init_core_map(fuel_radius, gap, cladding_thickness, nPin, fuel_to_moderator_ratio, core_radius, core_gap_scale):

    # Calculate pitch size based on fuel to moderator ratio
    clad_radius = fuel_radius + gap + cladding_thickness
    pin_area = clad_radius**2 * math.pi / fuel_to_moderator_ratio
    pitch_size = pin_area**(1/2)

    # Calculate the size of fuel assembly
    FA_size = pitch_size * nPin

    # Calculate the number of FA, already in 1/4 symmetry, would be number of grids in the visualizer
    core_gap = core_gap_scale*FA_size # Can be scaled according to the desired gap
    active_core_radius = core_radius - core_gap
    num_FA = round(active_core_radius/FA_size)

    # Visualize the core, using 1st quadrant symmetry

    # Calculation for each layer
    # See if the number of FA is odd or even
    if num_FA % 2 == 0:
        # For even number FA, the horizontal axis would be the bottom part of the FA, while the vertical axis would be the left part
        # Get and array of y coordinate for the topside of each layer, as the limiting parameter of number of FA in each layer
        num_layer = num_FA
        y_coord = np.array([FA_size*i for i in np.arange(1, num_layer+1)])

        # From the circle equation, we can determine the number of FA for each layer in the vertical axis
        # x^2 + y^2 = r^2, with r^2 = (core_radius)^2
        x_coord = np.array([math.sqrt(core_radius**2 - y**2) for y in y_coord])
        num_FA_layer = np.array([math.floor(x/FA_size) for x in x_coord])
        
        # Sum up the number of FA in each layer
        total_FA = np.sum(num_FA_layer)

    else :
        # For odd number FA, the horizontal and vertical axis would be the midpoint of the FA
        # Get and array of y coordinate for the midpoint of each layer, as the limiting parameter of number of FA in each layer 
        # Use the function of i/2 where i are odd number
        num_layer = num_FA
        y_coord = np.array([FA_size*i/2 for i in np.arange(1,2*num_layer+1,2)])

        # From the circle equation, we can determine the number of FA for each layer in the vertical axis
        # x^2 + y^2 = r^2, with r^2 = (active_core_radius)^2
        x_coord = np.array([math.sqrt(core_radius**2 - y**2) for y in y_coord])
        num_FA_layer = np.array([math.floor(x/FA_size) for x in x_coord])

    # Make a matrix to store the FA positions (1 for FA present, 0 for empty)
    mat_size = math.ceil(num_FA)
    core_map = np.zeros((mat_size, mat_size))

    for layer, num_fa in enumerate(num_FA_layer):
        for i in range(int(num_fa)):
            core_map[layer][i] = 1


    # Visualize both the 1/4 core map and the single fuel assembly map

    # Create subplots with 1 row and 2 columns
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Core Map (1/4 Symmetry)", "Single Fuel Assembly"))

    # Column 1, the 1/4 core map, plotted on the left

    # Draw the core boundary circle
    # Light grey color, positioned at the most back
    fig.add_shape(
        type="circle",
        x0=-core_radius,
        y0=-core_radius,
        x1=core_radius,
        y1=core_radius,
        fillcolor="lightgrey",
        opacity=0.5,
        line=dict(color="blue", width=2),
        layer='below',
        name='Core Boundary',
        row=1, col=1
    )

    # Draw the inner circle
    # Blue color, positioned at the middle
    fig.add_shape(
        type="circle",
        x0=-active_core_radius,
        y0=-active_core_radius,
        x1=active_core_radius,
        y1=active_core_radius,
        fillcolor="lightblue",
        opacity=0.5,
        line=dict(color="green", width=2),
        layer='below',
        name='Imaginary Core Boundary',
        row=1, col=1
    )

    # Draw the FA

    # For even number FA, the square go from 0,0 to n_pin*FA_size, n_pin*FA_size
    # Following patter of (i,j)*FA_size for bottom left corner, (i+1, j+1)*FA_size for top right corner
    if num_FA % 2 == 0:
        # Add the fuel assemblies as squares
        for i in range(len(core_map)):
            for j in range(len(core_map[i])):
                if core_map[i][j] == 1:
                    # Create a square for each FA
                    fig.add_shape(
                        type="rect",
                        x0=j*FA_size,
                        y0=i*FA_size,
                        x1=(j+1)*FA_size,
                        y1=(i+1)*FA_size,
                        line=dict(color="black", width=1),
                        fillcolor="red",
                        opacity=1,
                        name='FA',
                        row=1, col=1
                    )
        in_x, in_y = 0, 0

    # For odd number FA, the square go from -FA_size/2,-FA_size/2 to FA_size/2, FA_size/2
    # Following patter of (2i-1,2j-1)*FA_size for bottom left corner, (2i+1, 2j+1)*FA_size for top right corner
    else: 
        # Add the fuel assemblies as squares
        for i in range(len(core_map)):
            for j in range(len(core_map[i])):
                if core_map[i][j] == 1:
                    # Create a square for each FA
                    fig.add_shape(
                        type="rect",
                        x0=(2*j-1)/2*FA_size,
                        y0=(2*i-1)/2*FA_size,
                        x1=(2*j+1)/2*FA_size,
                        y1=(2*i+1)/2*FA_size,
                        line=dict(color="black", width=1),
                        fillcolor="red",
                        opacity=1,
                        name='FA',
                        row=1, col=1
                    )
        in_x, in_y = -FA_size/2, -FA_size/2

    # Column 2, the single fuel assembly map also 1/4 symettry

    # For even FA, the horizontal and vertical axis overlapped with the botom and left part of the FA
    # Following patter of (i,j)*FA_size for bottom left corner, (i+1, j+1)*FA_size for top right corner
    if nPin % 2 == 0:
        # For even number of pins
        pin_range = range(nPin//2)
        for i in pin_range:
            for j in pin_range:
                x_center = j * pitch_size + pitch_size / 2
                y_center = i * pitch_size + pitch_size / 2

                # Add moderator (outermost)
                fig.add_shape(
                    type="rect",
                    x0=j * pitch_size,
                    y0=i * pitch_size,
                    x1=(j+1) * pitch_size,
                    y1=(i+1) * pitch_size,
                    line=dict(color="green", width=1),
                    fillcolor="lightblue",
                    opacity=0.7,
                    row=1, col=2
                )
                
                # Add cladding (outermost)
                fig.add_shape(
                    type="circle",
                    x0=x_center - (fuel_radius + gap + cladding_thickness),
                    y0=y_center - (fuel_radius + gap + cladding_thickness),
                    x1=x_center + (fuel_radius + gap + cladding_thickness),
                    y1=y_center + (fuel_radius + gap + cladding_thickness),
                    line=dict(color="green", width=1),
                    fillcolor="green",
                    opacity=0.3,
                    row=1, col=2
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
                    opacity=0.5,
                    row=1, col=2
                )
                
                # Add fuel (innermost)
                fig.add_shape(
                    type="circle",
                    x0=x_center - fuel_radius,
                    y0=y_center - fuel_radius,
                    x1=x_center + fuel_radius,
                    y1=y_center + fuel_radius,
                    line=dict(color="red", width=1),
                    fillcolor="red",
                    opacity=0.7,
                    row=1, col=2
                )
        x_in_fa, y_in_fa = 0 , 0
        x_out_fa, y_out_fa = FA_size/2 + 1, FA_size/2 + 1

    else:
        # For odd number of pins
        pin_range = range((nPin+1)//2)
        for i in pin_range:
            for j in pin_range:
                x_center = j * pitch_size
                y_center = i * pitch_size

                # Add moderator (outermost)
                fig.add_shape(
                    type="rect",
                    x0=(2*j-1)/2 * pitch_size,
                    y0=(2*i-1)/2 * pitch_size,
                    x1=(2*j+1)/2 * pitch_size,
                    y1=(2*i+1)/2 * pitch_size,
                    line=dict(color="green", width=1),
                    fillcolor="lightblue",
                    opacity=0.7,
                    row=1, col=2
                )
                
                # Add cladding (outermost)
                fig.add_shape(
                    type="circle",
                    x0=x_center - (fuel_radius + gap + cladding_thickness),
                    y0=y_center - (fuel_radius + gap + cladding_thickness),
                    x1=x_center + (fuel_radius + gap + cladding_thickness),
                    y1=y_center + (fuel_radius + gap + cladding_thickness),
                    line=dict(color="green", width=1),
                    fillcolor="green",
                    opacity=0.3,
                    row=1, col=2
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
                    opacity=0.5,
                    row=1, col=2
                )
                
                # Add fuel (innermost)
                fig.add_shape(
                    type="circle",
                    x0=x_center - fuel_radius,
                    y0=y_center - fuel_radius,
                    x1=x_center + fuel_radius,
                    y1=y_center + fuel_radius,
                    line=dict(color="red", width=1),
                    fillcolor="red",
                    opacity=0.7,
                    row=1, col=2
                )
        x_in_fa, y_in_fa = -pitch_size/2 , -pitch_size/2
        x_out_fa, y_out_fa = FA_size/2 + 1, FA_size/2 + 1

    # Update layout for the two subplots
    fig.update_layout(
        width=1600,
        height=800,
        showlegend=True,
        plot_bgcolor='white'
    )

    # Update axes for core map, adjusted to the 1/4 symmetry and odd/even FA
    fig.update_xaxes(
        range=[in_x, core_radius + 10],
        scaleanchor=None,
        constrain='domain',
        scaleratio=1,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        row=1, col=1
    )
    fig.update_yaxes(
        range=[in_y, core_radius + 10],
        gridcolor='lightgrey',
        constrain='domain',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        row=1, col=1
    )

    # Update axes for single fuel assembly, use different scale anchor to avoid bad scaling
    fig.update_xaxes(
        range=[x_in_fa, x_out_fa],
        scaleanchor=None,
        scaleratio=1,
        constrain='domain',
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        row=1, col=2
    )
    fig.update_yaxes(
        range=[y_in_fa, y_out_fa],
        constrain='domain',
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        row=1, col=2
    )

    fig.show()

    # Export the 1/4 symettry core map as max_core.txt
    np.savetxt("max_core.txt", core_map, fmt='%d')

    # Export inputed parameters as input.txt
    with open("input.txt", "w") as f:
        f.write("fuel_radius: " + str(fuel_radius) + "\n")
        f.write("gap: " + str(gap) + "\n")
        f.write("cladding_thickness: " + str(cladding_thickness) + "\n")
        f.write("nPin: " + str(nPin) + "\n")
        f.write("fuel_to_moderator_ratio: " + str(fuel_to_moderator_ratio) + "\n")
        f.write("core_radius: " + str(core_radius) + "\n")
        f.write("core_gap: " + str(core_gap) + "\n")
        f.write("active_core_radius: " + str(active_core_radius) + "\n")
        f.write("num_FA: " + str(num_FA) + "\n")
        f.write("FA_size: " + str(FA_size) + "\n")
        f.write("pitch_size: " + str(pitch_size) + "\n")
        f.close()

    # Make 1/4 symmetry FA matrix full of ones
    if nPin % 2 == 0:
        mat_size = nPin//2
    else:
        mat_size = (nPin+1)//2

    mat_FA = np.ones((mat_size, mat_size))

    # Export the 1/4 symettry single fuel assembly map as <nPin>_allfuel_FA.txt
    # First line explecites the size of the matrix
    filename = "%d_allfuel_FA.txt" % nPin
    np.savetxt(filename, mat_FA, fmt='%d')

    return pitch_size, core_gap, active_core_radius, num_FA, num_FA_layer, core_map, mat_FA

# Main function
# Inputs
fuel_radius = 0.4096  # in cm
gap = 0.0084         # in cm 
cladding_thickness = 0.0572  # in cm
nPin = 16       # 17x17 assembly typical for PWR
fuel_to_moderator_ratio = 0.45  # typical PWR value
core_radius = 170    # in cm
core_gap_scale = 0.5 # Can be scaled according to the desired gap
