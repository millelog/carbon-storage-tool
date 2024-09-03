from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, inspect
from ..database import get_db
from ..models import SiteInfo, Fault, UrbanArea
from pydantic import BaseModel
from typing import List, Dict, Any
from geoalchemy2.functions import ST_AsGeoJSON, ST_Transform
import json
import time

router = APIRouter()

class LayerInfo(BaseModel):
    name: str
    properties: List[str]

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class GeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

# In-memory cache
cache = {}
CACHE_EXPIRATION = 3600  # 1 hour in seconds

async def execute_geojson_query(db: AsyncSession, query):
    result = await db.execute(query)
    features = []
    for row in result.fetchall():
        feature = row[0]
        if isinstance(feature, str):
            feature = json.loads(feature)
        if isinstance(feature.get('geometry'), str):
            feature['geometry'] = json.loads(feature['geometry'])
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}

def get_model_properties(model):
    return [column.name for column in inspect(model).columns if column.name != 'geom']

@router.get("/layers", response_model=List[LayerInfo])
async def get_layers():
    return [
        LayerInfo(name="sites", properties=get_model_properties(SiteInfo)),
        LayerInfo(name="faults", properties=get_model_properties(Fault)),
        LayerInfo(name="urban_areas", properties=get_model_properties(UrbanArea)),
    ]

async def get_cached_geojson(cache_key: str, query_func, db: AsyncSession):
    current_time = time.time()
    if cache_key in cache:
        cached_data, expiration_time = cache[cache_key]
        if current_time < expiration_time:
            return cached_data

    result = await query_func(db)
    cache[cache_key] = (result, current_time + CACHE_EXPIRATION)
    return result

@router.get("/layers/sites/geojson", response_model=dict)
async def get_sites_geojson(db: AsyncSession = Depends(get_db)):
    cache_key = "sites_geojson"
    
    async def query_func(db):
        query = select(
            func.jsonb_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(ST_Transform(SiteInfo.geom, 4326)),
                'properties', func.jsonb_build_object(
                    'id', SiteInfo.id,
                    'state', SiteInfo.state,
                    'agencycd', SiteInfo.agencycd,
                    'siteno', SiteInfo.siteno,
                    'sitename', SiteInfo.sitename,
                    'declatva', SiteInfo.declatva,
                    'declongva', SiteInfo.declongva,
                    'horzdatum', SiteInfo.horzdatum,
                    'altva', SiteInfo.altva,
                    'altunits', SiteInfo.altunits,
                    'welldepth', SiteInfo.welldepth,
                    'nataquifercd', SiteInfo.nataquifercd,
                    'nataqfrdesc', SiteInfo.nataqfrdesc,
                    'sitetype', SiteInfo.sitetype,
                    'aquifertype', SiteInfo.aquifertype
                )
            )
        ).select_from(SiteInfo)

        return await execute_geojson_query(db, query)

    return await get_cached_geojson(cache_key, query_func, db)

@router.get("/layers/urban_areas/geojson", response_model=dict)
async def get_urban_areas_geojson(db: AsyncSession = Depends(get_db)):
    cache_key = "urban_areas_geojson"
    
    async def query_func(db):
        query = select(
            func.jsonb_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(ST_Transform(UrbanArea.geom, 4326)),
                'properties', func.jsonb_build_object(
                    'id', UrbanArea.id,
                    'uace10', UrbanArea.uace10,
                    'geoid10', UrbanArea.geoid10,
                    'name10', UrbanArea.name10,
                    'namelsad10', UrbanArea.namelsad10,
                    'lsad10', UrbanArea.lsad10,
                    'mtfcc10', UrbanArea.mtfcc10,
                    'uatyp10', UrbanArea.uatyp10,
                    'funcstat10', UrbanArea.funcstat10,
                    'aland10', UrbanArea.aland10,
                    'awater10', UrbanArea.awater10,
                    'intptlat10', UrbanArea.intptlat10,
                    'intptlon10', UrbanArea.intptlon10,
                    'shape_length', UrbanArea.shape_length,
                    'shape_area', UrbanArea.shape_area
                )
            )
        ).select_from(UrbanArea)
        
        return await execute_geojson_query(db, query)

    return await get_cached_geojson(cache_key, query_func, db)

@router.get("/layers/faults/geojson", response_model=dict)
async def get_faults_geojson(db: AsyncSession = Depends(get_db)):
    cache_key = "faults_geojson"
    
    async def query_func(db):
        query = select(
            func.jsonb_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(ST_Transform(Fault.geom, 4326)),
                'properties', func.jsonb_build_object(
                    'id', Fault.id,
                    'fnode_', Fault.fnode_,
                    'tnode_', Fault.tnode_,
                    'lpoly_', Fault.lpoly_,
                    'rpoly_', Fault.rpoly_,
                    'length', Fault.length,
                    'kbf_', Fault.kbf_,
                    'kbf_id', Fault.kbf_id,
                    'desc_', Fault.desc_,
                    'ltype', Fault.ltype,
                    'long_desc', Fault.long_desc,
                    'alc', Fault.alc,
                    'descltype', Fault.descltype,
                    'shape_length', Fault.shape_length
                )
            )
        ).select_from(Fault)

        return await execute_geojson_query(db, query)

    return await get_cached_geojson(cache_key, query_func, db)

@router.get("/layers/{layer_name}/schema", response_model=LayerInfo)
async def get_layer_schema(layer_name: str):
    layers = {
        "sites": SiteInfo,
        "faults": Fault,
        "urban_areas": UrbanArea,
    }
    if layer_name not in layers:
        raise HTTPException(status_code=404, detail="Layer not found")
    return LayerInfo(name=layer_name, properties=get_model_properties(layers[layer_name]))