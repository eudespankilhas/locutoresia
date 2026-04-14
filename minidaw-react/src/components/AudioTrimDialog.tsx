import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Scissors } from "lucide-react";

interface AudioTrimDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  audioUrl: string;
  trackName: string;
  onTrimApply: (startTime: number, endTime: number, saveAsCopy: boolean) => void;
}

export const AudioTrimDialog: React.FC<AudioTrimDialogProps> = ({
  open,
  onOpenChange,
  audioUrl,
  trackName,
  onTrimApply,
}) => {
  const [startTime, setStartTime] = useState(0);
  const [endTime, setEndTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [saveAsCopy, setSaveAsCopy] = useState(false);

  const handleApply = () => {
    if (startTime >= 0 && endTime > startTime && endTime <= duration) {
      onTrimApply(startTime, endTime, saveAsCopy);
      onOpenChange(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Scissors className="w-4 h-4" />
            Cortar Áudio - {trackName}
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="start-time">Início</Label>
            <Input
              id="start-time"
              type="number"
              value={startTime}
              onChange={(e) => setStartTime(Number(e.target.value))}
              min={0}
              step={0.1}
              placeholder="0.0"
            />
            <span className="text-sm text-muted-foreground">
              {formatTime(startTime)}
            </span>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="end-time">Fim</Label>
            <Input
              id="end-time"
              type="number"
              value={endTime}
              onChange={(e) => setEndTime(Number(e.target.value))}
              min={0}
              step={0.1}
              placeholder="0.0"
            />
            <span className="text-sm text-muted-foreground">
              {formatTime(endTime)}
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="save-as-copy"
              checked={saveAsCopy}
              onChange={(e) => setSaveAsCopy(e.target.checked)}
            />
            <Label htmlFor="save-as-copy">Salvar como cópia</Label>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
            <Button onClick={handleApply}>
              Aplicar Corte
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
