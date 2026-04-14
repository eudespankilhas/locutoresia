import { useRef, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Volume2 } from "lucide-react";

interface LUFSMeterProps {
  analysers: AnalyserNode[];
  isPlaying: boolean;
}

export const LUFSMeter: React.FC<LUFSMeterProps> = ({ analysers, isPlaying }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Draw background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    // Draw LUFS scale
    ctx.fillStyle = '#666';
    ctx.font = '10px monospace';
    
    // LUFS levels from -24 to 0
    for (let i = -24; i <= 0; i += 6) {
      const y = ((i + 24) / 24) * height;
      ctx.fillText(`${i}`, 2, y + 3);
      
      ctx.beginPath();
      ctx.moveTo(25, y);
      ctx.lineTo(width, y);
      ctx.strokeStyle = '#333';
      ctx.stroke();
    }

    if (isPlaying && analysers.length > 0) {
      // Calculate LUFS (simplified)
      let sum = 0;
      let count = 0;
      
      analysers.forEach(analyser => {
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(dataArray);
        
        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
          count++;
        }
      });
      
      const average = count > 0 ? sum / count : 0;
      const lufs = -24 + (average / 255) * 24;
      
      // Draw LUFS meter
      const meterY = ((lufs + 24) / 24) * height;
      const meterHeight = height - meterY;
      
      // Color based on level
      let color = '#00ff00'; // Green
      if (lufs > -12) color = '#ffff00'; // Yellow
      if (lufs > -6) color = '#ff0000'; // Red
      
      ctx.fillStyle = color;
      ctx.fillRect(25, meterY, width - 25, meterHeight);
      
      // Draw current value
      ctx.fillStyle = '#fff';
      ctx.fillText(`${lufs.toFixed(1)} LUFS`, width - 60, 15);
    }

  }, [analysers, isPlaying]);

  return (
    <Card className="p-2 bg-card border-border">
      <div className="flex items-center gap-2">
        <Volume2 className="w-4 h-4" />
        <span className="text-xs text-muted-foreground">LUFS</span>
        <canvas
          ref={canvasRef}
          width={120}
          height={60}
          className="inline-block"
        />
      </div>
    </Card>
  );
};
