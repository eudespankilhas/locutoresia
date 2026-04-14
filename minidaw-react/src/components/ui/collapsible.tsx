import * as React from "react"

interface CollapsibleProps {
  children: React.ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  disabled?: boolean;
}

interface CollapsibleTriggerProps {
  children: React.ReactNode;
  asChild?: boolean;
}

interface CollapsibleContentProps {
  children: React.ReactNode;
  forceMount?: boolean;
}

const CollapsibleContext = React.createContext<{
  open: boolean;
  onOpenChange: (open: boolean) => void;
} | null>(null);

const Collapsible: React.FC<CollapsibleProps> = ({ children, open = false, onOpenChange }) => {
  return (
    <CollapsibleContext.Provider value={{ open, onOpenChange: onOpenChange || (() => {}) }}>
      {children}
    </CollapsibleContext.Provider>
  );
};

const CollapsibleTrigger: React.FC<CollapsibleTriggerProps> = ({ children, asChild = false }) => {
  const context = React.useContext(CollapsibleContext);
  if (!context) throw new Error("CollapsibleTrigger must be used within a Collapsible");

  const { open, onOpenChange } = context;

  if (asChild) {
    return React.cloneElement(children as React.ReactElement, {
      onClick: () => onOpenChange(!open),
    });
  }

  return (
    <button onClick={() => onOpenChange(!open)}>
      {children}
    </button>
  );
};

const CollapsibleContent: React.FC<CollapsibleContentProps> = ({ children, forceMount }) => {
  const context = React.useContext(CollapsibleContext);
  if (!context) throw new Error("CollapsibleContent must be used within a Collapsible");

  const { open } = context;

  if (!forceMount && !open) return null;

  return <div>{children}</div>;
};

export { Collapsible, CollapsibleTrigger, CollapsibleContent };
