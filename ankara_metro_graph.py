import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

# Prepare for visualization
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, seed=42, k=0.5)  # k controls the distance between nodes

# Draw edges with their respective line colors
for line_name, line_data in metro_lines.items():
    line_edges = [(u, v) for u, v, d in G.edges(data=True) if d["line"] == line_name]
    nx.draw_networkx_edges(G, pos, edgelist=line_edges, width=2.5, alpha=0.8, edge_color=line_data["color"])

# Draw all nodes
node_colors = []
transfer_stations = []

# Identify transfer stations (stations that appear in multiple lines)
for node, data in G.nodes(data=True):
    if len(data["lines"]) > 1:
        transfer_stations.append(node)
        node_colors.append("black")
    else:
        node_colors.append("white")

nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors, edgecolors="black")

# Draw station labels
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

# Create legend for metro lines
legend_patches = []
for line_name, line_data in metro_lines.items():
    legend_patches.append(mpatches.Patch(color=line_data["color"], label=line_name))

plt.legend(handles=legend_patches, loc="upper right")
plt.title("Ankara Metro Network", size=15)
plt.axis("off")
plt.tight_layout()

# Save the figure
plt.savefig("ankara_metro_map.png", dpi=300, bbox_inches="tight")
plt.show()

# Print basic network statistics
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

# Example usage
print("\nExample: Shortest path from KIZILAY to OSB TÖREKENT")
print(find_shortest_path("KIZILAY", "OSB TÖREKENT"))

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