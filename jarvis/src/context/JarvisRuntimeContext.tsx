import React, { createContext, useContext } from 'react';
import { useJarvisRuntime } from '../hooks/useJarvisRuntime';
import { JarvisRuntimeState, initialJarvisState } from '../lib/jarvisStateMachine';
import { deriveJarvisVisualState, JarvisVisualState } from '../hooks/useJarvisVisualState';

type JarvisContextValue = {
  state: JarvisRuntimeState;
  visualState: JarvisVisualState;
  toggleJarvis: () => Promise<void>;
  isJarvisActive: boolean;
};

const JarvisContext = createContext<JarvisContextValue>({
  state: initialJarvisState,
  visualState: 'IDLE',
  toggleJarvis: async () => {},
  isJarvisActive: false
});

export function JarvisRuntimeProvider({ children }: { children: React.ReactNode }) {
  const { state, toggleJarvis, isJarvisActive } = useJarvisRuntime();
  const visualState = deriveJarvisVisualState(state);

  return (
    <JarvisContext.Provider value={{ state, visualState, toggleJarvis, isJarvisActive }}>
      {children}
    </JarvisContext.Provider>
  );
}

export function useJarvisContext() {
  return useContext(JarvisContext);
}
