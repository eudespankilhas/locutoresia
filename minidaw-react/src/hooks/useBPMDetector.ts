import { useState, useCallback } from 'react';

export const useBPMDetector = () => {
  const [isDetecting, setIsDetecting] = useState(false);

  const detectBPM = useCallback(async (audioUrl: string): Promise<number> => {
    setIsDetecting(true);
    
    try {
      // Simple BPM detection using Web Audio API
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const response = await fetch(audioUrl);
      const arrayBuffer = await response.arrayBuffer();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer.slice(0));
      
      // Get audio data
      const channelData = audioBuffer.getChannelData(0);
      const sampleRate = audioBuffer.sampleRate;
      
      // Simple peak detection for BPM estimation
      const peaks: number[] = [];
      const threshold = 0.3;
      const minDistance = sampleRate * 0.3; // Minimum 300ms between beats
      
      for (let i = 0; i < channelData.length; i++) {
        if (Math.abs(channelData[i]) > threshold) {
          if (peaks.length === 0 || i - peaks[peaks.length - 1] > minDistance) {
            peaks.push(i);
          }
        }
      }
      
      // Calculate BPM from peaks
      if (peaks.length < 2) {
        return 120; // Default BPM
      }
      
      const intervals: number[] = [];
      for (let i = 1; i < peaks.length; i++) {
        intervals.push(peaks[i] - peaks[i - 1]);
      }
      
      const avgInterval = intervals.reduce((sum, interval) => sum + interval, 0) / intervals.length;
      const bpm = Math.round((60 * sampleRate) / avgInterval);
      
      // Clamp to reasonable BPM range
      return Math.max(60, Math.min(200, bpm));
      
    } catch (error) {
      console.error('BPM detection failed:', error);
      return 120; // Default BPM on error
    } finally {
      setIsDetecting(false);
    }
  }, []);

  return {
    detectBPM,
    isDetecting
  };
};
