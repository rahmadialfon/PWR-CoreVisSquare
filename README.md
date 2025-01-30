# Reactor Core and Fuel Assembly Visualization Tools

A comprehensive Python-based toolkit for visualizing and analyzing nuclear reactor core configurations and fuel assembly designs, with support for both PWR-like configurations and customized layouts.

## Features

### Initial Core Visualizer
- Automated core map generation based on geometric constraints of core size
- Quarter-symmetry visualization of reactor core
- Detailed fuel assembly pin layout
- Support for both even and odd number of assemblies
- Automatic parameter calculation and export
- Interactive visualization using Plotly

### Modified Core Map Visualizer
- Support for up to 6 different fuel assembly types
- Handles both numeric and string-based inputs
- Quarter-symmetry core visualization
- Customizable color schemes for different assembly types
- Interactive legend and layout
- Automatic analysis of assembly distribution

### Fuel Assembly Map Visualizer
- Detailed pin-by-pin visualization
- Support for multiple fuel pin types (up to 5)
- Quarter-symmetry representation
- Visualization of fuel, gap, and cladding
- Compatible with both numeric and string inputs
- Interactive display with customizable features

## Installation Requirements

```bash
pip install numpy plotly
```

## Usage Example

```python
# Initial Core Visualization
fuel_radius = 0.4096        # cm
gap = 0.0084               # cm
cladding_thickness = 0.0572 # cm
nPin = 17                  # typical PWR assembly
fuel_to_moderator_ratio = 0.45
core_radius = 170          # cm
core_gap_scale = 0.5

# Initialize and visualize
init_core_map(fuel_radius, gap, cladding_thickness, nPin, 
              fuel_to_moderator_ratio, core_radius, core_gap_scale)
```

## Usage Examples in Jupyter Notebook

There's an examples.ipynb that runs all three cases. Clone the repo and it should run smoothly.

## File Naming Conventions
- Fuel assembly files: Must follow format `nPin_<description>.txt`
- Guide tube or water rod in the FA visualizer must always be inputted as '0' or 'O' in the input map file


## Output Files
- `max_core.txt`: Core map matrix
- `input.txt`: Input parameters
- `{n}_allfuel_FA.txt`: Fuel assembly matrix
- Interactive visualizations in HTML format

## Applications
- Initial core design optimization
- Fuel loading pattern studies
- Educational demonstrations
- Monte Carlo code input preparation
- Burnup zone visualization
- Fuel assembly design analysis

## Author
Alfonsus Rahmadi Putranto

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
