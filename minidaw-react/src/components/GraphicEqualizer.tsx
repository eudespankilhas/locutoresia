import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Sliders } from "lucide-react";

export interface EQ10BandSettings {
  "32": number;
  "64": number;
  "125": number;
  "250": number;
  "500": number;
  "1k": number;
  "2k": number;
  "4k": number;
  "8k": number;
  "16k": number;
}

export const defaultEQ10Band: EQ10BandSettings = {
  "32": 0,
  "64": 0,
  "125": 0,
  "250": 0,
  "500": 0,
  "1k": 0,
  "2k": 0,
  "4k": 0,
  "8k": 0,
  "16k": 0,
};

interface GraphicEqualizerProps {
  settings: EQ10BandSettings;
  onChange: (settings: EQ10BandSettings) => void;
  trackName: string;
}

export const GraphicEqualizer: React.FC<GraphicEqualizerProps> = ({ settings, onChange, trackName }) => {
  const [expanded, setExpanded] = useState(false);

  const updateBand = (frequency: keyof EQ10BandSettings, value: number) => {
    onChange({
      ...settings,
      [frequency]: value,
    });
  };

  const eqBands = [
    { freq: "32", label: "32Hz", color: "bg-red-500" },
    { freq: "64", label: "64Hz", color: "bg-orange-500" },
    { freq: "125", label: "125Hz", color: "bg-yellow-500" },
    { freq: "250", label: "250Hz", color: "bg-green-500" },
    { freq: "500", label: "500Hz", color: "bg-teal-500" },
    { freq: "1k", label: "1kHz", color: "bg-blue-500" },
    { freq: "2k", label: "2kHz", color: "bg-indigo-500" },
    { freq: "4k", label: "4kHz", color: "bg-purple-500" },
    { freq: "8k", label: "8kHz", color: "bg-pink-500" },
    { freq: "16k", label: "16kHz", color: "bg-gray-500" },
  ];

  return (
    <Card className="p-4 bg-card border-border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-foreground flex items-center gap-2">
          <Sliders className="w-4 h-4" />
          Equalizador 10 Bandas
        </h3>
        <button
          className="text-sm text-muted-foreground hover:text-foreground"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "Recolher" : "Expandir"}
        </button>
      </div>

      {expanded && (
        <div className="space-y-4">
          <div className="grid grid-cols-10 gap-2">
            {eqBands.map((band) => (
              <div key={band.freq} className="flex flex-col items-center space-y-2">
                <Label className="text-xs font-medium">{band.label}</Label>
                <div className="relative h-32 w-full flex flex-col items-center justify-center">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-1 bg-muted h-full rounded" />
                  </div>
                  <Slider
                    value={[settings[band.freq as keyof EQ10BandSettings]]}
                    onValueChange={([value]) => updateBand(band.freq as keyof EQ10BandSettings, value)}
                    min={-12}
                    max={12}
                    step={1}
                    orientation="vertical"
                    className="h-28"
                    style={{
                      writingMode: "bt-lr", // For vertical orientation
                      WebkitAppearance: "slider-vertical",
                      width: "4px",
                    }}
                  />
                </div>
                <div className="text-xs text-center font-mono">
                  {settings[band.freq as keyof EQ10BandSettings] > 0 ? '+' : ''}{settings[band.freq as keyof EQ10BandSettings]}
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-center gap-4 mt-4">
            <button
              className="px-3 py-1 text-sm bg-secondary hover:bg-secondary/80 rounded"
              onClick={() => onChange(defaultEQ10Band)}
            >
              Reset
            </button>
            <button
              className="px-3 py-1 text-sm bg-primary text-primary-foreground hover:bg-primary/80 rounded"
              onClick={() => {
                // Preset de voz
                onChange({
                  "32": 2,
                  "64": 3,
                  "125": 1,
                  "250": -1,
                  "500": -2,
                  "1k": 0,
                  "2k": 2,
                  "4k": 3,
                  "8k": 2,
                  "16k": 1,
                });
              }}
            >
              Voz
            </button>
            <button
              className="px-3 py-1 text-sm bg-primary text-primary-foreground hover:bg-primary/80 rounded"
              onClick={() => {
                // Preset de música
                onChange({
                  "32": 4,
                  "64": 3,
                  "125": 2,
                  "250": 1,
                  "500": 0,
                  "1k": 0,
                  "2k": 1,
                  "4k": 2,
                  "8k": 3,
                  "16k": 4,
                });
              }}
            >
              Música
            </button>
          </div>
        </div>
      )}
    </Card>
  );
};
