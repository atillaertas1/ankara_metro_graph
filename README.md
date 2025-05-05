# Ankara Metro Graph Model for Discrete Mathematics

This project models the Ankara metro system as a graph network, similar to the London Underground style map.

## Features

- Visual representation of Ankara's metro lines (M1, M2, M3, M4, A1)
- Color-coded lines with clear station names
- Identification of transfer stations
- Path finding functionality between any two stations
- Detailed route instructions with transfer information

## Files

- `ankara_metro_graph.py` - Basic graph model with spring layout
- `ankara_metro_graph_enhanced.py` - Enhanced version with custom layout for a more metro-map-like appearance


## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run one of the scripts:
   ```
   python ankara_metro_graph.py
   ```
   or for the enhanced version:
   ```
   python ankara_metro_graph_enhanced.py
   ```

## Output

The scripts will:
1. Generate a visualization of the Ankara metro network saved as PNG
   - `ankara_metro_map.png` from the basic version
   - `ankara_metro_map_enhanced.png` from the enhanced version
2. Display the graph in a window
3. Print network statistics including transfer stations
4. Show example routes between stations

## Usage Examples

- The scripts include examples for finding paths between stations
- You can modify the example routes or add your own by using the `find_shortest_path()` or `detailed_route()` functions
- The A1-specific script includes station distance calculation functionality

## Customization

- The layout can be adjusted in all versions:
  - Basic version: modify the `pos` parameter in the spring_layout function
  - Enhanced version: adjust the coordinate calculations in the `create_custom_layout()` function
- Colors and visual properties can be modified in the visualization section

Emrecan Gök / Atilla Ertaş
