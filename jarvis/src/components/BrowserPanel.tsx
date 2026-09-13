import React from 'react';
import { useJarvisContext } from '../context/JarvisRuntimeContext';
import { motion, AnimatePresence } from 'motion/react';

export function BrowserPanel() {
  const { state } = useJarvisContext();
  const { browser } = state;

  if (browser.state === 'disconnected') return null;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        className={`w-[400px] ${browser.activeTool ? 'glass-panel-active' : 'glass-panel'}`}
      >
        <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
          <span className="tech-text">CHROME BROWSER</span>
          <span className="tech-text text-[var(--jarvis-cyan)]">{browser.state.toUpperCase()}</span>
        </div>
        
        <div className="p-4 space-y-3 font-mono text-[11px] text-white/80">
          <div className="flex">
            <span className="w-20 text-white/40">ACTION</span>
            <span className="flex-1 truncate">{browser.action || 'Idle'}</span>
          </div>
          <div className="flex">
            <span className="w-20 text-white/40">URL</span>
            <span className="flex-1 truncate text-[var(--jarvis-cyan)]">{browser.url || '---'}</span>
          </div>
          {browser.activeTool && (
            <div className="flex mt-2 pt-2 border-t border-white/5">
              <span className="w-20 text-white/40">TOOL</span>
              <span className="flex-1 text-[var(--jarvis-alert)] animate-pulse">{browser.activeTool}()</span>
            </div>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
