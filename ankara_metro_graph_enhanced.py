import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# Create a graph
G = nx.Graph()

# Define metro lines with their stations and colors
metro_lines = {
    "M1": {
        "stations": ["KIZILAY", "SIHHİYE", "ULUS", "AKM", "AKKÖPRÜ", "İVEDİK", "YENİMAHALLE", "DEMETEVLER", "HASTANE"],
        "color": "red"
    },
    "M2": {
        "stations": ["KIZILAY", "NECATİBEY", "MİLLİ KÜTÜPHANE", "SÖĞÜTÖZÜ", "MTA", "ODTÜ", "BİLKENT", 
                     "TARIM BAKANLIĞI DANIŞTAY", "BEYTEPE", "ÜMİTKÖY", "ÇAYYOLU", "KORU"],
        "color": "blue"
    },
    "M3": {
        "stations": ["HASTANE", "MACUNKÖY", "OSTİM", "BATIKENT", "BATI MERKEZ", "MESA", "BOTANİK", 
                    "İSTANBUL YOLU", "ERYAMAN 1-2", "ERYAMAN 5", "DEVLET MAHALLESİ", 
                    "HARİKALAR DİYARI", "FATİH", "GOP", "OSB TÖREKENT"],
        "color": "orange"
    },
    "M4": {
        "stations": ["AKM", "ASKİ", "DIŞKAPI", "METEOROLOJİ", "BELEDİYE", "MECİDİYE", "KUYUBAŞI", "DUTLUK", "ŞEHİTLER"],
        "color": "green"
    },
    "A1": {
        "stations": ["AŞTİ", "EMEK", "BAHÇELİEVLER", "BEŞEVLER", "ANADOLU", "MALTEPE", "DEMİRTEPE", 
                    "KIZILAY", "KOLEJ", "KURTULUŞ", "DİKİMEVİ"],
        "color": "purple"
    }
}

# Add nodes and edges for each metro line
for line_name, line_data in metro_lines.items():
    stations = line_data["stations"]
    color = line_data["color"]
    
    # Add attributes to stations (nodes)
    for station in stations:
        if station not in G:
            G.add_node(station, lines=[line_name])
        else:
            G.nodes[station]["lines"].append(line_name)
    
    # Connect stations on the same line
    for i in range(len(stations) - 1):
        G.add_edge(stations[i], stations[i + 1], line=line_name, color=color)

# Function to define custom positions for a more schematic map
def create_custom_layout():
    # Start with initial positions
    pos = {}
    
    # M1 line (horizontal west to east with a bend)
    m1_stations = metro_lines["M1"]["stations"]
    for i, station in enumerate(m1_stations):
        if i <= 3:  # First part is horizontal
            pos[station] = (i * 2, 0)
        else:  # Second part bends up
            pos[station] = (3 * 2 + (i-3) * 1.5, (i-3) * 1.5)
    
    # M2 line (south to north from KIZILAY)
    m2_stations = metro_lines["M2"]["stations"]
    for i, station in enumerate(m2_stations):
        if station == "KIZILAY":  # Already positioned by M1
            continue
        pos[station] = (0, -(i) * 1.5)  # Going south from KIZILAY
    
    # M3 line (continues from HASTANE)
    m3_stations = metro_lines["M3"]["stations"]
    base_x = pos["HASTANE"][0]
    base_y = pos["HASTANE"][1]
    for i, station in enumerate(m3_stations):
        if station == "HASTANE":  # Already positioned
            continue
        pos[station] = (base_x + (i) * 1.5, base_y + (i) * 0.5)  # Going northeast
    
    # M4 line (from AKM heading north)
    m4_stations = metro_lines["M4"]["stations"]
    base_x = pos["AKM"][0]
    base_y = pos["AKM"][1]
    for i, station in enumerate(m4_stations):
        if station == "AKM":  # Already positioned
            continue
        pos[station] = (base_x, base_y + (i) * 1.5)  # Going north
    
    # A1 line - Improved layout with smoother curve and better spacing
    a1_stations = metro_lines["A1"]["stations"]
    kizilay_index = a1_stations.index("KIZILAY")
    
    # Get KIZILAY position (already set)
    kizilay_x, kizilay_y = pos["KIZILAY"]
    
    # Stations before KIZILAY (coming from west)
    for i in range(kizilay_index):
        # Create an arc approaching KIZILAY from southwest
        # Use a more linear layout with a slight curve
        distance = (kizilay_index - i) * 1.2
        # Calculate x position with decreasing spacing as we get closer to KIZILAY
        x_offset = -distance * 1.1
        # Calculate y position with a gentle curve
        y_offset = -0.8 * np.sqrt(distance)
        
        pos[a1_stations[i]] = (kizilay_x + x_offset, kizilay_y + y_offset)
    
    # Stations after KIZILAY (going east)
    for i in range(kizilay_index + 1, len(a1_stations)):
        # Create an arc continuing east-northeast from KIZILAY
        distance = (i - kizilay_index) * 1.2
        # Calculate positions along a gentle curve
        x_offset = distance * 1.1
        # Use a mirrored curve going slightly upward
        y_offset = 0.8 * np.sqrt(distance)
        
        pos[a1_stations[i]] = (kizilay_x + x_offset, kizilay_y + y_offset)
    
    return pos

# Get custom positioned layout
pos = create_custom_layout()

# Create figure with a white background
plt.figure(figsize=(16, 12), facecolor='white')

# Draw each metro line with its own style
for line_name, line_data in metro_lines.items():
    stations = line_data["stations"]
    color = line_data["color"]
    
    # Get edges for this line
    line_edges = []
    for i in range(len(stations) - 1):
        line_edges.append((stations[i], stations[i+1]))
    
    # Draw line edges with thicker lines
    if line_name == "A1":
        # Make A1 line more distinctive
        nx.draw_networkx_edges(G, pos, edgelist=line_edges, width=5, alpha=0.9, edge_color=color, style='solid')
    else:
        nx.draw_networkx_edges(G, pos, edgelist=line_edges, width=4, alpha=0.7, edge_color=color)

# Identify transfer stations
transfer_stations = [node for node, data in G.nodes(data=True) if len(data["lines"]) > 1]
regular_stations = [node for node in G.nodes() if node not in transfer_stations]

# Draw regular stations (white circles with black borders)
nx.draw_networkx_nodes(G, pos, nodelist=regular_stations, node_size=300, 
                      node_color='white', edgecolors='black', linewidths=1.5)

# Draw transfer stations (larger black circles)
nx.draw_networkx_nodes(G, pos, nodelist=transfer_stations, node_size=500,
                      node_color='black', edgecolors='white', linewidths=1.5)

# Add station labels with a white background for better readability
for node, (x, y) in pos.items():
    plt.text(x, y-0.3, node, fontsize=8, ha='center', va='top', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='none', alpha=0.7))

# Create custom legend
legend_elements = []
for line_name, line_data in metro_lines.items():
    legend_elements.append(
        Line2D([0], [0], color=line_data["color"], lw=4, label=f'{line_name}')
    )
# Add station types to legend
legend_elements.append(
    Line2D([0], [0], marker='o', color='w', markerfacecolor='white', markeredgecolor='black',
          markersize=10, label='Regular Station')
)
legend_elements.append(
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markeredgecolor='white',
          markersize=10, label='Transfer Station')
)

plt.legend(handles=legend_elements, loc="best", fontsize=10)
plt.title("Ankara Metro Network", size=20, pad=20)
plt.axis('off')
plt.tight_layout()

# Add some statistics as text
plt.figtext(0.02, 0.02, 
            f"Number of stations: {G.number_of_nodes()}\n"
            f"Number of connections: {G.number_of_edges()}\n"
            f"Transfer stations: {len(transfer_stations)}", 
            fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

# Save the figure with high resolution
plt.savefig("ankara_metro_map_enhanced.png", dpi=300, bbox_inches="tight", facecolor='white')
plt.show()

# Print network statistics
print(f"Number of stations: {G.number_of_nodes()}")
print(f"Number of connections: {G.number_of_edges()}")
print(f"Transfer stations: {transfer_stations}")
print(f"Average shortest path length: {nx.average_shortest_path_length(G):.2f}")

# Function to find shortest path between stations
def find_shortest_path(start_station, end_station):
    if start_station not in G or end_station not in G:
        return "One or both stations not found in network"
    
    path = nx.shortest_path(G, start_station, end_station)
    return path

# Enhanced version: include which lines to take and where to transfer
def detailed_route(start_station, end_station):
    if start_station not in G or end_station not in G:
        return "One or both stations not found in network"
    
    path = nx.shortest_path(G, start_station, end_station)
    
    # Determine which lines to take and where to transfer
    route_details = []
    current_line = None
    
    for i in range(len(path) - 1):
        edge_data = G.get_edge_data(path[i], path[i+1])
        line = edge_data["line"]
        
        if current_line != line:
            if current_line:
                route_details.append(f"Transfer at {path[i]} to {line} line")
            else:
                route_details.append(f"Take {line} line from {path[i]}")
            current_line = line
    
    route_details.append(f"Arrive at {path[-1]}")
    
    return {
        "path": path,
        "steps": route_details,
        "total_stations": len(path) - 1
    }

# Example of detailed route
print("\nDetailed route from KIZILAY to OSB TÖREKENT:")
route = detailed_route("KIZILAY", "OSB TÖREKENT")
for step in route["steps"]:
    print(step)
print(f"Total stations: {route['total_stations']}")

# Another example
print("\nDetailed route from AŞTİ to KORU:")
route = detailed_route("AŞTİ", "KORU")
for step in route["steps"]:
    print(step)
print(f"Total stations: {route['total_stations']}") 