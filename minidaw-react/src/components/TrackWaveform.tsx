import React, { useRef, useEffect, useState } from 'react';

interface TrackWaveformProps {
  audioUrl: string;
  color: string;
  currentTime: number;
  duration: number;
  zoom: number;
  fadeIn: number;
  fadeOut: number;
  onSeek: (time: number) => void;
}

const TrackWaveform: React.FC<TrackWaveformProps> = ({
  audioUrl,
  color,
  currentTime,
  duration,
  zoom,
  fadeIn,
  fadeOut,
  onSeek
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (!audioUrl || !canvasRef.current) return;

    const audio = new Audio(audioUrl);
    audioRef.current = audio;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    audio.addEventListener('loadedmetadata', () => {
      canvas.width = canvas.offsetWidth * zoom;
      canvas.height = 100;
      
      // Draw simple waveform visualization
      ctx.fillStyle = color.includes('blue') ? '#3b82f6' : '#a855f7';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw waveform pattern
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.beginPath();
      
      for (let i = 0; i < canvas.width; i += 4) {
        const height = Math.random() * 60 + 20;
        if (i === 0) {
          ctx.moveTo(i, canvas.height / 2);
        }
        ctx.lineTo(i, canvas.height / 2 - height / 2);
      }
      ctx.stroke();
    });

    audio.addEventListener('timeupdate', () => {
      setIsPlaying(!audio.paused);
    });

    audio.load();
  }, [audioUrl, zoom, color]);

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current || !duration) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const clickTime = (x / rect.width) * duration;
    onSeek(clickTime);
  };

  return (
    <div className="relative w-full h-24 bg-gray-900 rounded-lg overflow-hidden cursor-pointer">
      <canvas
        ref={canvasRef}
        onClick={handleCanvasClick}
        className="w-full h-full"
      />
      
      {/* Current time indicator */}
      {duration > 0 && (
        <div
          className="absolute top-0 bottom-0 w-0.5 bg-red-500"
          style={{
            left: `${(currentTime / duration) * 100}%`
          }}
        />
      )}
      
      {/* Fade indicators */}
      {fadeIn > 0 && (
        <div className="absolute left-0 top-0 bottom-0 w-8 bg-gradient-to-r from-green-500 to-transparent opacity-50" />
      )}
      
      {fadeOut > 0 && (
        <div className="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-orange-500 to-transparent opacity-50" />
      )}
      
      {/* Play/Pause indicator */}
      <div className="absolute top-2 right-2">
        {isPlaying ? (
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
        ) : (
          <div className="w-2 h-2 bg-gray-500 rounded-full" />
        )}
      </div>
    </div>
  );
};

export default TrackWaveform;
