import geopandas as gpd
from config import settings

def read_gdb_layers():
    gdb_path = settings.GDB_PATH
    return gpd.read_file(gdb_path)

def get_layer_names():
    gdb = gpd.read_file(settings.GDB_PATH, driver='FileGDB')
    return list(gdb.keys())

def get_layer_data(layer_name):
    gdb = gpd.read_file(settings.GDB_PATH, driver='FileGDB', layer=layer_name)
    return gdb.to_dict(orient='records')

# Add more GDB-related functions as needed