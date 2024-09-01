from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import geopandas as gpd
import fiona
import json
from config import settings
from schemas import LayerInfo
from functools import lru_cache

router = APIRouter()

# Use LRU cache to store up to 32 layers in memory
@lru_cache(maxsize=32)
def read_layer(layer_name: str):
    try:
        return gpd.read_file(settings.GDB_PATH, layer=layer_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading layer '{layer_name}': {str(e)}")

def list_layers():
    try:
        return fiona.listlayers(settings.GDB_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing layers: {str(e)}")

@router.get("/layers", response_model=List[LayerInfo])
def get_layers():
    """Get a list of all layers in the GDB file."""
    layers = list_layers()
    return [LayerInfo(name=layer) for layer in layers]

@router.get("/layers/{layer_name}/schema", response_model=Dict[str, str])
def get_layer_schema(layer_name: str):
    """Get the schema (column names and types) for a specific layer."""
    layer = read_layer(layer_name)
    return {col: str(dtype) for col, dtype in layer.dtypes.items()}

@router.get("/layers/{layer_name}/sample")
def get_layer_sample(layer_name: str, limit: int = Query(5, ge=1, le=100)):
    """Get a sample of records from a specific layer as GeoJSON."""
    layer = read_layer(layer_name)
    sample = layer.head(limit)
    
    # Convert to GeoJSON
    geojson = json.loads(sample.to_crs(epsg=4326).to_json())
    return geojson

@router.get("/layers/{layer_name}/bounds", response_model=Optional[Dict[str, float]])
def get_layer_bounds(layer_name: str):
    """Get the bounding box of a specific layer."""
    layer = read_layer(layer_name)
    if not layer.empty and layer.geometry.notna().any():
        bounds = layer.total_bounds
        return {
            "min_x": bounds[0],
            "min_y": bounds[1],
            "max_x": bounds[2],
            "max_y": bounds[3]
        }
    else:
        return None

@router.get("/layers/{layer_name}/feature-count", response_model=int)
def get_feature_count(layer_name: str):
    """Get the number of features in a specific layer."""
    layer = read_layer(layer_name)
    return len(layer)

@router.get("/layers/{layer_name}/geometry-type", response_model=Optional[str])
def get_geometry_type(layer_name: str):
    """Get the geometry type of a specific layer."""
    layer = read_layer(layer_name)
    if not layer.empty and layer.geometry.notna().any():
        return layer.geometry.geom_type.iloc[0]
    else:
        return None

@router.get("/layers/{layer_name}/spatial-info", response_model=Dict[str, Optional[str]])
def get_spatial_info(layer_name: str):
    """Get spatial information about a specific layer."""
    layer = read_layer(layer_name)
    if not layer.empty and layer.geometry.notna().any():
        return {
            "geometry_type": layer.geometry.geom_type.iloc[0],
            "crs": str(layer.crs) if layer.crs else None
        }
    else:
        return {
            "geometry_type": None,
            "crs": None
        }

@router.get("/layers/{layer_name}/geojson")
def get_layer_geojson(layer_name: str, limit: Optional[int] = Query(None, ge=1, le=1000)):
    """Get the entire layer (or a subset) as GeoJSON."""
    layer = read_layer(layer_name)
    if limit:
        layer = layer.head(limit)
    
    # Convert to GeoJSON
    geojson = json.loads(layer.to_crs(epsg=4326).to_json())
    return geojson