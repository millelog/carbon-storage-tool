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
    <MapContainer center={[39.8097343, -98.5556199]} zoom={3} style={{ height: '100%', width: '100%' }}>
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
    <div className="flex flex-col h-screen w-screen">
      <header className="bg-gray-800 text-white p-4">
        <h1 className="text-3xl font-bold">Carbon Storage Site Mapping Inquiry Tool</h1>
      </header>
      <div className="flex flex-1 flex-col sm:flex-row overflow-hidden">
        <div className="sm:w-1/4 w-full p-4 overflow-y-auto">
          <Card className="mb-4">
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
          <Card>
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
        <div className="flex-1 p-4">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Map View</CardTitle>
            </CardHeader>
            <CardContent className="h-[calc(100%-4rem)]">
              {selectedLayer && <Map key={selectedLayer} layerName={selectedLayer} />}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;