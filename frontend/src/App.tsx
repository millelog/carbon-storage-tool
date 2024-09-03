import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapContainer, TileLayer, GeoJSON, ScaleControl, useMap } from 'react-leaflet';
import * as L from 'leaflet';
import LayerInfo from './components/LayerInfo';
import { Loader2 } from "lucide-react"
import 'leaflet/dist/leaflet.css';

interface BasicLayer {
  name: string;
}

interface LayerSchema {
  name: string;
  properties: string[];
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [layers, setLayers] = useState<BasicLayer[]>([]);
  const [selectedLayer, setSelectedLayer] = useState<string | null>(null);
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [layerSchema, setLayerSchema] = useState<LayerSchema | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    console.log('Fetching layers');
    setIsLoading(true);
    fetch(`${API_URL}/layers`)
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then((data: BasicLayer[]) => {
        console.log('Received layers:', data);
        setLayers(data);
        if (data.length > 0) setSelectedLayer(data[0].name);
      })
      .catch(e => {
        console.error('Error fetching layers:', e);
        setError(e.message);
      })
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    if (selectedLayer) {
      setIsLoading(true);
      console.log('Fetching GeoJSON for layer:', selectedLayer);
      fetch(`${API_URL}/layers/${selectedLayer}/geojson`)
        .then(response => {
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          return response.json();
        })
        .then(data => {
          console.log('Received GeoJSON data:', data);
          console.log('Number of features:', data.features.length);
          console.log('Sample feature:', data.features[0]);
          setGeoJsonData(data);
        })
        .catch(e => {
          console.error('Error fetching GeoJSON:', e);
          setError(e.message);
        })
        .finally(() => setIsLoading(false));

      console.log('Fetching schema for layer:', selectedLayer);
      fetch(`${API_URL}/layers/${selectedLayer}/schema`)
        .then(response => {
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          return response.json();
        })
        .then((data: LayerSchema) => {
          console.log('Received schema data:', data);
          setLayerSchema(data);
        })
        .catch(e => {
          console.error('Error fetching schema:', e);
          setError(e.message);
        });
    }
  }, [selectedLayer]);


  const onEachFeature = useCallback((feature: any, layer: any) => {
    if (feature.properties) {
      const popupContent = Object.entries(feature.properties)
        .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
        .join('<br>');
      layer.bindPopup(popupContent);
    }
  }, []);

  const getLayerStyle = useCallback((feature: any) => {
    const baseStyle = {
      radius: 8,
      fillColor: "#ff7800",
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
    };

    switch (feature.geometry.type) {
      case 'LineString':
      case 'MultiLineString':
        return {
          ...baseStyle,
          fillColor: undefined,
          fillOpacity: undefined,
        };
      case 'Polygon':
      case 'MultiPolygon':
        return {
          ...baseStyle,
          fillOpacity: 0.3,
        };
      default:
        return baseStyle;
    }
  }, []);

  const MapContent = () => {
    const map = useMap();

    useEffect(() => {
      if (geoJsonData) {
        map.eachLayer((layer) => {
          if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
          }
        });

        L.geoJSON(geoJsonData, {
          onEachFeature: onEachFeature,
          style: getLayerStyle,
          pointToLayer: (feature, latlng) => {
            return L.circleMarker(latlng, getLayerStyle(feature));
          }
        }).addTo(map);
      }
    }, [geoJsonData, map]);

    return null;
  };

  if (error) return <div>Error: {error}</div>;

  return (
    <div className="flex flex-col h-screen w-screen">
      <header className="bg-gray-800 text-white p-4">
        <h1 className="text-3xl font-bold">Carbon Storage Site Mapping Inquiry Tool</h1>
      </header>
      <div className="flex flex-1 flex-col lg:flex-row overflow-hidden">
        <div className="lg:w-1/4 w-full max-w-xl p-4 overflow-y-auto">
          <Card className="mb-4">
            <CardHeader>
              <CardTitle>Layer Selection</CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={selectedLayer || ''} onValueChange={setSelectedLayer}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a layer" />
                </SelectTrigger>
                <SelectContent className='z-50'>
                  {layers.map((layer) => (
                    <SelectItem key={layer.name} value={layer.name}>
                      {layer.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>
          {selectedLayer && layerSchema && <LayerInfo schema={layerSchema} />}
        </div>
        <div className="flex-1 p-4 relative">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Map View</CardTitle>
            </CardHeader>
            <CardContent className="h-[calc(100%-4rem)]">
              <MapContainer center={[39.8097343, -98.5556199]} zoom={5} style={{ height: '100%', width: '100%' }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <MapContent />
                <ScaleControl position="bottomleft" />
              </MapContainer>
              {isLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[1000]">
                  <Loader2 className="h-8 w-8 animate-spin text-white" />
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
