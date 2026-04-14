import { useRef, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Activity } from "lucide-react";

interface CompressorVUMeterProps {
  compressorNode?: any;
  enabled: boolean;
  size?: "sm" | "md" | "lg";
}

export const CompressorVUMeter: React.FC<CompressorVUMeterProps> = ({
  compressorNode,
  enabled,
  size = "md",
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const sizeMap = {
    sm: { width: 40, height: 20 },
    md: { width: 60, height: 30 },
    lg: { width: 80, height: 40 },
  };

  const { width, height } = sizeMap[size];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Draw background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    if (enabled) {
      // Draw VU meter bars (mock animation)
      const barCount = 5;
      const barWidth = width / barCount - 2;
      const barHeight = height - 4;

      for (let i = 0; i < barCount; i++) {
        const intensity = Math.random() * 0.8 + 0.2; // Mock random values
        const barHeightActual = barHeight * intensity;
        
        // Green to yellow to red gradient
        let color = '#00ff00';
        if (i >= 3) color = '#ffff00';
        if (i >= 4) color = '#ff0000';
        
        ctx.fillStyle = color;
        ctx.fillRect(
          i * (barWidth + 2) + 1,
          height - barHeightActual - 2,
          barWidth,
          barHeightActual
        );
      }
    } else {
      // Draw disabled state
      ctx.fillStyle = '#333';
      ctx.fillRect(2, 2, width - 4, height - 4);
    }

  }, [enabled, width, height]);

  if (size === "sm") {
    return (
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className="inline-block"
      />
    );
  }

  return (
    <Card className="p-2 bg-card border-border">
      <div className="flex items-center gap-2">
        <Activity className="w-4 h-4" />
        <span className="text-xs text-muted-foreground">Compressor</span>
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          className="inline-block"
        />
      </div>
    </Card>
  );
};
