import { useRef, useEffect } from "react";

interface DAWTimelineProps {
  duration: number;
  currentTime: number;
  zoom: number;
  bpm?: number | null;
  snapEnabled?: boolean;
  onSeek: (time: number) => void;
}

export const DAWTimeline: React.FC<DAWTimelineProps> = ({
  duration,
  currentTime,
  zoom,
  bpm,
  snapEnabled,
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

    // Draw timeline background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    // Draw time markers
    ctx.fillStyle = '#666';
    ctx.font = '10px monospace';
    
    const interval = duration / 10; // 10 markers
    for (let i = 0; i <= 10; i++) {
      const x = (i / 10) * width;
      const time = (i / 10) * duration;
      
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.strokeStyle = '#333';
      ctx.stroke();
      
      ctx.fillText(`${time.toFixed(1)}s`, x + 2, height - 2);
    }

    // Draw playhead
    const playheadX = (currentTime / duration) * width;
    ctx.strokeStyle = '#ff0000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(playheadX, 0);
    ctx.lineTo(playheadX, height);
    ctx.stroke();

  }, [duration, currentTime, zoom, bpm, snapEnabled]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const time = (x / canvas.width) * duration;
    onSeek(time);
  };

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={40}
      onClick={handleClick}
      className="w-full h-10 cursor-pointer"
      style={{ width: '100%', height: '40px' }}
    />
  );
};
