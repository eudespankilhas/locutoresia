import { useEffect, useCallback } from 'react';

interface KeyboardShortcutsProps {
  onPlayPause: () => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onIncreaseFade: () => void;
  onDecreaseFade: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onToggleScissor: () => void;
  onTimelineZoomIn: () => void;
  onTimelineZoomOut: () => void;
  onSelectAll: () => void;
  onDeleteSelected: () => void;
  onCopy: () => void;
  onPaste: () => void;
  onEscape: () => void;
}

export const useKeyboardShortcuts = ({
  onPlayPause,
  onZoomIn,
  onZoomOut,
  onIncreaseFade,
  onDecreaseFade,
  onUndo,
  onRedo,
  onToggleScissor,
  onTimelineZoomIn,
  onTimelineZoomOut,
  onSelectAll,
  onDeleteSelected,
  onCopy,
  onPaste,
  onEscape
}: KeyboardShortcutsProps) => {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    // Prevent default for our shortcuts
    if (event.ctrlKey || event.metaKey) {
      switch (event.key) {
        case 'z':
          event.preventDefault();
          onUndo();
          break;
        case 'y':
          event.preventDefault();
          onRedo();
          break;
        case 'c':
          event.preventDefault();
          onCopy();
          break;
        case 'v':
          event.preventDefault();
          onPaste();
          break;
        case 'a':
          event.preventDefault();
          onSelectAll();
          break;
        case '=':
        case '+':
          event.preventDefault();
          onTimelineZoomIn();
          break;
        case '-':
          event.preventDefault();
          onTimelineZoomOut();
          break;
      }
    } else {
      switch (event.key) {
        case ' ':
        case 'Spacebar':
          event.preventDefault();
          onPlayPause();
          break;
        case 'c':
          event.preventDefault();
          onToggleScissor();
          break;
        case 'Delete':
          event.preventDefault();
          onDeleteSelected();
          break;
        case 'Escape':
          event.preventDefault();
          onEscape();
          break;
        case 'ArrowUp':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            onZoomIn();
          }
          break;
        case 'ArrowDown':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            onZoomOut();
          }
          break;
        case 'ArrowLeft':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            onDecreaseFade();
          }
          break;
        case 'ArrowRight':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            onIncreaseFade();
          }
          break;
      }
    }
  }, [
    onPlayPause,
    onZoomIn,
    onZoomOut,
    onIncreaseFade,
    onDecreaseFade,
    onUndo,
    onRedo,
    onToggleScissor,
    onTimelineZoomIn,
    onTimelineZoomOut,
    onSelectAll,
    onDeleteSelected,
    onCopy,
    onPaste,
    onEscape
  ]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);
};
