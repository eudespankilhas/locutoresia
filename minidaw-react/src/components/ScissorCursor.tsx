import { Scissors } from "lucide-react";

interface ScissorCursorProps {
  active: boolean;
}

export const ScissorCursor: React.FC<ScissorCursorProps> = ({ active }) => {
  if (!active) return null;

  return (
    <div className="fixed pointer-events-none z-50">
      <Scissors className="w-6 h-6 text-red-500" />
    </div>
  );
};
