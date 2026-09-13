import React from 'react';
import { useJarvisContext } from '../context/JarvisRuntimeContext';
import { AmbientBackground } from './AmbientBackground';
import { SystemStatus } from './SystemStatus';
import { AIOrb } from './AIOrb';
import { ActivityPanel } from './ActivityPanel';
import { LiveBrowserView } from './Browser/LiveBrowserView';
import { MCPPanel } from './MCPPanel';
import { Mic, MicOff, Power } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export function JarvisShell() {
  const { toggleJarvis, isJarvisActive, state, visualState } = useJarvisContext();

  return (
    <main className="relative flex min-h-screen w-full bg-transparent overflow-hidden">
      <AmbientBackground />
      
      {/* Central Visual Component */}
      <div className="absolute inset-0 flex flex-col items-center justify-center z-10 pointer-events-none">
        <AIOrb />
        
        {/* Toggle Button */}
        <div className="mt-16 pointer-events-auto">
          <button 
            onClick={toggleJarvis}
            className={`p-4 rounded-full backdrop-blur-md transition-colors border border-white/5 shadow-xl 
              ${isJarvisActive 
                ? 'bg-[var(--jarvis-error)]/20 text-[var(--jarvis-error)] hover:bg-[var(--jarvis-error)]/40' 
                : 'bg-white/10 text-white/60 hover:bg-white/20'}`}
          >
            {isJarvisActive ? <Mic className="w-6 h-6" /> : <Power className="w-6 h-6" />}
          </button>
        </div>

        {/* Global Error Display */}
        <AnimatePresence>
          {state.lastError && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-8 text-[var(--jarvis-error)] tech-text tracking-normal"
            >
              [ERROR: {state.lastError.source}] {state.lastError.message}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Floating Side Panels */}
      <div className="relative z-20 w-full h-full flex justify-between p-8 pointer-events-none">
        {/* Left Side: Diagnostics */}
        <div className="flex flex-col gap-4">
          <ActivityPanel />
          <MCPPanel />
        </div>

        {/* Right Side: Browsing context */}
        <div className="flex flex-col gap-4 items-end">
          <LiveBrowserView />
        </div>
      </div>

      {/* System Status Footer */}
      <SystemStatus />
    </main>
  );
}
