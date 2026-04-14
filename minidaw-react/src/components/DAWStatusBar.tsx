import { Card } from "@/components/ui/card";
import { Activity, Music, Clock } from "lucide-react";

interface DAWStatusBarProps {
  bpm?: number | null;
  compressorEnabled: boolean;
  crossfadeEnabled: boolean;
  crossfadeDuration: number;
  trackCount: number;
  totalDuration: number;
}

export const DAWStatusBar: React.FC<DAWStatusBarProps> = ({
  bpm,
  compressorEnabled,
  crossfadeEnabled,
  crossfadeDuration,
  trackCount,
  totalDuration,
}) => {
  return (
    <Card className="p-2 bg-card border-border">
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Music className="w-3 h-3" />
            <span>{trackCount} tracks</span>
          </div>
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>{totalDuration.toFixed(1)}s</span>
          </div>
          {bpm && (
            <div className="flex items-center gap-1">
              <Activity className="w-3 h-3" />
              <span>{bpm} BPM</span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-4">
          {compressorEnabled && (
            <span className="flex items-center gap-1">
              <Activity className="w-3 h-3" />
              Comp ON
            </span>
          )}
          {crossfadeEnabled && (
            <span className="flex items-center gap-1">
              <Activity className="w-3 h-3" />
              Crossfade {crossfadeDuration}s
            </span>
          )}
        </div>
      </div>
    </Card>
  );
};
