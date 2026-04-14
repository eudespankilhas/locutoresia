import { useRef, useEffect } from "react";

interface TrackClipHandlesProps {
  audioUrl: string;
  currentTime: number;
  duration: number;
  onSeek: (time: number) => void;
}

export const TrackClipHandles: React.FC<TrackClipHandlesProps> = ({
  audioUrl,
  currentTime,
  duration,
  onSeek,
}) => {
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

    // Draw clip background
    ctx.fillStyle = '#2a2a2a';
    ctx.fillRect(0, 0, width, height);

    // Draw handles
    const handleWidth = 10;
    
    // Left handle
    ctx.fillStyle = '#00ff00';
    ctx.fillRect(0, 0, handleWidth, height);
    
    // Right handle
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(width - handleWidth, 0, handleWidth, height);

    // Draw playhead
    const playheadX = (currentTime / duration) * width;
    ctx.strokeStyle = '#ffff00';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(playheadX, 0);
    ctx.lineTo(playheadX, height);
    ctx.stroke();

  }, [audioUrl, currentTime, duration]);

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={30}
      className="w-full h-8"
      style={{ width: '100%', height: '30px' }}
    />
  );
};
