import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Bookmark, Plus, Trash2 } from "lucide-react";

export interface Marker {
  id: string;
  time: number;
  label: string;
  color?: string;
}

interface TimelineMarkersProps {
  markers: Marker[];
  duration: number;
  currentTime: number;
  onAddMarker: (marker: Omit<Marker, "id">) => void;
  onRemoveMarker: (id: string) => void;
  onSeekToMarker: (time: number) => void;
}

export const TimelineMarkers: React.FC<TimelineMarkersProps> = ({
  markers,
  duration,
  currentTime,
  onAddMarker,
  onRemoveMarker,
  onSeekToMarker,
}) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [newMarkerTime, setNewMarkerTime] = useState(0);
  const [newMarkerLabel, setNewMarkerLabel] = useState("");

  const handleAddMarker = () => {
    if (newMarkerLabel.trim()) {
      onAddMarker({
        time: newMarkerTime,
        label: newMarkerLabel,
        color: "#ff0000",
      });
      setNewMarkerLabel("");
      setShowAddForm(false);
    }
  };

  return (
    <Card className="p-4 bg-card border-border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-foreground flex items-center gap-2">
          <Bookmark className="w-4 h-4" />
          Marcadores
        </h3>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowAddForm(true)}
        >
          <Plus className="w-3 h-3 mr-1" />
          Adicionar
        </Button>
      </div>

      {showAddForm && (
        <div className="p-3 border rounded mb-4 space-y-2">
          <input
            type="number"
            value={newMarkerTime}
            onChange={(e) => setNewMarkerTime(Number(e.target.value))}
            placeholder="Tempo (s)"
            className="w-full px-2 py-1 border rounded text-sm"
            min={0}
            max={duration}
            step={0.1}
          />
          <input
            type="text"
            value={newMarkerLabel}
            onChange={(e) => setNewMarkerLabel(e.target.value)}
            placeholder="Descrição"
            className="w-full px-2 py-1 border rounded text-sm"
          />
          <div className="flex gap-2">
            <Button size="sm" onClick={handleAddMarker}>
              Adicionar
            </Button>
            <Button size="sm" variant="outline" onClick={() => setShowAddForm(false)}>
              Cancelar
            </Button>
          </div>
        </div>
      )}

      <div className="space-y-2 max-h-40 overflow-y-auto">
        {markers.map((marker) => (
          <div
            key={marker.id}
            className="flex items-center justify-between p-2 bg-muted rounded"
          >
            <div className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: marker.color || "#ff0000" }}
              />
              <span className="text-sm">{marker.label}</span>
              <span className="text-xs text-muted-foreground">
                {marker.time.toFixed(1)}s
              </span>
            </div>
            <div className="flex gap-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onSeekToMarker(marker.time)}
              >
                Ir
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemoveMarker(marker.id)}
              >
                <Trash2 className="w-3 h-3" />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
