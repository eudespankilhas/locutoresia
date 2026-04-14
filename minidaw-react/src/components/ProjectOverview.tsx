import { Card } from "@/components/ui/card";
import { Music, Mic, Clock } from "lucide-react";

interface TrackInfo {
  id: string;
  name: string;
  type: "voiceover" | "music";
  duration: number;
  color: string;
  hasAudio: boolean;
}

interface ProjectOverviewProps {
  tracks: TrackInfo[];
  totalDuration: number;
  currentTime: number;
  onSeek: (time: number) => void;
  onSelectTrack: (trackId: string) => void;
}

export const ProjectOverview: React.FC<ProjectOverviewProps> = ({
  tracks,
  totalDuration,
  currentTime,
  onSeek,
  onSelectTrack,
}) => {
  return (
    <Card className="p-4 bg-card border-border">
      <h3 className="font-semibold text-foreground mb-4">Visão Geral do Projeto</h3>
      
      <div className="space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span>Duração Total:</span>
          <span className="font-mono">{totalDuration.toFixed(1)}s</span>
        </div>
        
        <div className="flex items-center justify-between text-sm">
          <span>Tracks:</span>
          <span>{tracks.length}</span>
        </div>
        
        <div className="space-y-2">
          <div className="text-sm font-medium">Tracks:</div>
          {tracks.map((track) => (
            <div
              key={track.id}
              className="flex items-center justify-between p-2 bg-muted rounded cursor-pointer hover:bg-muted/80"
              onClick={() => onSelectTrack(track.id)}
            >
              <div className="flex items-center gap-2">
                {track.type === "voiceover" ? (
                  <Mic className="w-3 h-3" />
                ) : (
                  <Music className="w-3 h-3" />
                )}
                <span className="text-sm">{track.name}</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{track.duration.toFixed(1)}s</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
};
