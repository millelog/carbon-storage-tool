import os
from dotenv import load_dotenv
import geopandas as gpd
import fiona

# Load environment variables
load_dotenv()

# Get the path to the geodatabase from the environment variable
gdb_path = os.getenv('DEV_GDB')

if not gdb_path:
    raise ValueError("DEV_GDB environment variable not set")

print(f"Analyzing geodatabase: {gdb_path}")

# List all layers in the geodatabase
layers = fiona.listlayers(gdb_path)
print(f"\nFound {len(layers)} layers:")

for layer_name in layers:
    print(f"\nAnalyzing layer: {layer_name}")
    
    # Read the layer into a GeoDataFrame
    gdf = gpd.read_file(gdb_path, layer=layer_name)
    
    # Get basic information
    print(f"  Geometry Type: {gdf.geom_type.iloc[0]}")
    print(f"  Feature Count: {len(gdf)}")
    
    # Get spatial reference information
    if gdf.crs:
        print(f"  Coordinate Reference System: {gdf.crs.to_string()}")
    else:
        print("  Coordinate Reference System: None")
    
    # Get extent
    bounds = gdf.total_bounds
    print(f"  Extent: XMin: {bounds[0]}, YMin: {bounds[1]}, XMax: {bounds[2]}, YMax: {bounds[3]}")
    
    # Get field information
    print(f"  Fields ({len(gdf.columns)}):")
    for column in gdf.columns:
        if column != 'geometry':
            print(f"    - {column} ({gdf[column].dtype})")
    
    # Additional statistical information for numeric columns
    numeric_columns = gdf.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        print("  Numeric Field Statistics:")
        for column in numeric_columns:
            print(f"    - {column}:")
            print(f"      Min: {gdf[column].min()}")
            print(f"      Max: {gdf[column].max()}")
            print(f"      Mean: {gdf[column].mean()}")
            print(f"      Median: {gdf[column].median()}")

print("\nReconnaissance complete.")