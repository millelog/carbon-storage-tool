# schemas.py

from pydantic import BaseModel
from typing import List, Dict, Any

class LayerInfo(BaseModel):
    name: str

class LayerData(BaseModel):
    layer_name: str
    data: List[Dict[str, Any]]

class FeatureInfo(BaseModel):
    id: int
    properties: Dict[str, Any]
    geometry: Dict[str, Any]
class DetailedLayerInfo(BaseModel):
    name: str
    geometry_type: str
    feature_count: int
    attributes: List[str]