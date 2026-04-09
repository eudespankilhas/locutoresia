import React from 'react';
import { Play, Pause, Volume2, Scissors, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';

interface TrackControlsProps {
  volume: number;
  fadeIn: number;
  fadeOut: number;
  zoom: number;
  pan: number;
  playbackRate: number;
  onVolumeChange: (value: number[]) => void;
  onFadeInChange: (value: number) => void;
  onFadeOutChange: (value: number) => void;
  onZoomChange: (value: number) => void;
  onPanChange: (value: number) => void;
  onPlaybackRateChange: (value: number) => void;
  onTrim: () => void;
  onDuplicate: () => void;
}

const TrackControls: React.FC<TrackControlsProps> = ({
  volume,
  fadeIn,
  fadeOut,
  zoom,
  pan,
  playbackRate,
  onVolumeChange,
  onFadeInChange,
  onFadeOutChange,
  onZoomChange,
  onPanChange,
  onPlaybackRateChange,
  onTrim,
  onDuplicate
}) => {
  return (
    <div className="space-y-3 p-4 bg-gray-800 rounded-lg">
      {/* Volume Control */}
      <div className="flex items-center gap-3">
        <Volume2 className="w-4 h-4 text-gray-400" />
        <span className="text-sm text-gray-300 w-12">Vol</span>
        <Slider
          value={[volume]}
          onValueChange={onVolumeChange}
          min={0}
          max={200}
          className="flex-1"
        />
        <span className="text-sm text-gray-300 w-12 text-right">{volume}%</span>
      </div>

      {/* Fade Controls */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-xs text-gray-400">Fade In</label>
          <Slider
            value={[fadeIn]}
            onValueChange={(value) => onFadeInChange(value[0])}
            min={0}
            max={5}
            step={0.1}
          />
          <span className="text-xs text-gray-300 text-center">{fadeIn.toFixed(1)}s</span>
        </div>
        
        <div className="space-y-2">
          <label className="text-xs text-gray-400">Fade Out</label>
          <Slider
            value={[fadeOut]}
            onValueChange={(value) => onFadeOutChange(value[0])}
            min={0}
            max={5}
            step={0.1}
          />
          <span className="text-xs text-gray-300 text-center">{fadeOut.toFixed(1)}s</span>
        </div>
      </div>

      {/* Advanced Controls */}
      <div className="space-y-3">
        {/* Zoom */}
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-300 w-12">Zoom</span>
          <Slider
            value={[zoom]}
            onValueChange={(value) => onZoomChange(value[0])}
            min={0.5}
            max={4}
            step={0.25}
            className="flex-1"
          />
          <span className="text-sm text-gray-300 w-12 text-right">{zoom.toFixed(2)}x</span>
        </div>

        {/* Pan */}
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-300 w-12">Pan</span>
          <Slider
            value={[pan * 100 + 100]}
            onValueChange={(value) => onPanChange((value[0] - 100) / 100)}
            min={0}
            max={200}
            step={1}
            className="flex-1"
          />
          <span className="text-sm text-gray-300 w-12 text-right">
            {pan < 0 ? 'L' : pan > 0 ? 'R' : 'C'}
          </span>
        </div>

        {/* Playback Rate */}
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-300 w-12">Speed</span>
          <Slider
            value={[playbackRate * 100]}
            onValueChange={(value) => onPlaybackRateChange(value[0] / 100)}
            min={50}
            max={200}
            step={5}
            className="flex-1"
          />
          <span className="text-sm text-gray-300 w-12 text-right">{playbackRate.toFixed(2)}x</span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2 pt-2 border-t border-gray-700">
        <Button variant="outline" size="sm" onClick={onTrim} className="flex-1">
          <Scissors className="w-3 h-3 mr-1" />
          Trim
        </Button>
        <Button variant="outline" size="sm" onClick={onDuplicate} className="flex-1">
          <Copy className="w-3 h-3 mr-1" />
          Duplicate
        </Button>
      </div>
    </div>
  );
};

export default TrackControls;
