import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { History, RotateCcw } from "lucide-react";

interface HistoryState {
  tracks: any[];
  description: string;
}

interface HistoryPanelProps {
  history: HistoryState[];
  currentIndex: number;
  onJumpTo: (index: number) => void;
  onClear: () => void;
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({
  history,
  currentIndex,
  onJumpTo,
  onClear,
}) => {
  return (
    <Card className="p-4 bg-card border-border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-foreground flex items-center gap-2">
          <History className="w-4 h-4" />
          Histórico
        </h3>
        <Button variant="outline" size="sm" onClick={onClear}>
          Limpar
        </Button>
      </div>

      <div className="space-y-2 max-h-60 overflow-y-auto">
        {history.map((item, index) => (
          <div
            key={index}
            className={`p-2 rounded cursor-pointer transition-colors ${
              index === currentIndex
                ? "bg-primary text-primary-foreground"
                : "bg-muted hover:bg-muted/80"
            }`}
            onClick={() => onJumpTo(index)}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm">{item.description}</span>
              {index === currentIndex && (
                <RotateCcw className="w-3 h-3" />
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
