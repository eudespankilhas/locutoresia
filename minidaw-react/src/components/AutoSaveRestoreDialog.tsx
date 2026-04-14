import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Clock, Restore, Trash2 } from "lucide-react";

interface AutoSaveData {
  projectName: string;
  tracks: Array<{ id: string; name: string; type: string }>;
  savedAt: string;
}

interface AutoSaveRestoreDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  autoSaveData: AutoSaveData | null;
  onRestore: () => void;
  onDiscard: () => void;
}

export const AutoSaveRestoreDialog: React.FC<AutoSaveRestoreDialogProps> = ({
  open,
  onOpenChange,
  autoSaveData,
  onRestore,
  onDiscard,
}) => {
  if (!autoSaveData) return null;

  const savedDate = new Date(autoSaveData.savedAt);
  const timeAgo = new Date().getTime() - savedDate.getTime();
  const hoursAgo = Math.floor(timeAgo / (1000 * 60 * 60));
  const minutesAgo = Math.floor((timeAgo % (1000 * 60 * 60)) / (1000 * 60));

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            Auto-save Encontrado
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <Card className="p-4 bg-muted/50">
            <div className="space-y-2">
              <h3 className="font-medium">{autoSaveData.projectName}</h3>
              <p className="text-sm text-muted-foreground">
                Salvo há {hoursAgo > 0 ? `${hoursAgo}h` : ''}{minutesAgo}min
              </p>
              <p className="text-sm text-muted-foreground">
                {autoSaveData.tracks.length} tracks
              </p>
            </div>
          </Card>

          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">
              Um auto-save foi encontrado. Deseja restaurar este projeto ou começar novo?
            </p>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={onDiscard}>
              <Trash2 className="w-4 h-4 mr-2" />
              Descartar
            </Button>
            <Button onClick={onRestore}>
              <Restore className="w-4 h-4 mr-2" />
              Restaurar
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
