import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

interface Layer {
  name: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
console.log('API_URL:', API_URL);

function Map({ layerName }: { layerName: string }) {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Fetching GeoJSON for layer:', layerName);
    fetch(`${API_URL}/layers/${layerName}/geojson`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        console.log('GeoJSON Response:', response);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Received GeoJSON data:', data);
        setGeoJsonData(data);
      })
      .catch(e => {
        console.error('Error fetching GeoJSON:', e);
        setError(e.message);
      });
  }, [layerName]);

  if (error) return <div>Error loading map data: {error}</div>;

  return (
    <MapContainer center={[0, 0]} zoom={2} style={{ height: '400px', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {geoJsonData && <GeoJSON data={geoJsonData} />}
    </MapContainer>
  );
}

function App() {
  const [layers, setLayers] = useState<Layer[]>([]);
  const [selectedLayer, setSelectedLayer] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Fetching layers');
    fetch(`${API_URL}/layers`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        console.log('Layers Response:', response);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data: Layer[]) => {
        console.log('Received layers:', data);
        setLayers(data);
        if (data.length > 0) {
          setSelectedLayer(data[0].name);
        }
      })
      .catch(e => {
        console.error('Error fetching layers:', e);
        setError(e.message);
      });
  }, []);

  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">GDB Viewer</h1>
      <Card>
        <CardHeader>
          <CardTitle>Layer Selection</CardTitle>
        </CardHeader>
        <CardContent>
          <Select value={selectedLayer} onValueChange={setSelectedLayer}>
            <SelectTrigger>
              <SelectValue placeholder="Select a layer" />
            </SelectTrigger>
            <SelectContent>
              {layers.map((layer) => (
                <SelectItem key={layer.name} value={layer.name}>
                  {layer.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>
      <Card className="mt-4">
        <CardHeader>
          <CardTitle>Map View</CardTitle>
        </CardHeader>
        <CardContent>
          {selectedLayer && <Map layerName={selectedLayer} />}
        </CardContent>
      </Card>
      <Card className="mt-4">
        <CardHeader>
          <CardTitle>Layer Information</CardTitle>
        </CardHeader>
        <CardContent>
          <Button onClick={() => alert(`Selected Layer: ${selectedLayer}`)}>
            Show Layer Info
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;