"use client"
import { createContext, useContext, useState, ReactNode } from 'react';


interface HwContextType {
  historyTrigger: number;
  refreshHistory: () => void;
  windowTrigger: number;
  refreshWindow: () => void;

}


const HwContext = createContext<HwContextType | null>(null);


interface HwProviderProps {
  children: ReactNode;
}

export function HwProvider({ children }: HwProviderProps) {

  const [historyTrigger, setHistoryTrigger] = useState<number>(50);
  const [windowTrigger, setWindowTrigger] = useState<number>(0);

  const refreshHistory = () => {

    setHistoryTrigger(prev => prev + 10);
  };
   const refreshWindow = () => {
    
    setWindowTrigger(prev => prev + 1);
  };

  const value: HwContextType = {
    historyTrigger,
    refreshHistory,
    windowTrigger,
    refreshWindow,
  };

  return (
    <HwContext.Provider value={value}>
      {children}
    </HwContext.Provider>
  );
}


export function useHw(): HwContextType {
  const context = useContext(HwContext);
  if (!context) {
    throw new Error('useHw должен использоваться внутри HwProvider');
  }
  return context;
}