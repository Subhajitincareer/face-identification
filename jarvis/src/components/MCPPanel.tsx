import React from 'react';
import { useJarvisContext } from '../context/JarvisRuntimeContext';
import { motion, AnimatePresence } from 'motion/react';

export function MCPPanel() {
  const { state } = useJarvisContext();
  const { activeToolCall, tool } = state;

  if (tool === 'idle' && !activeToolCall) return null;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="glass-panel w-[350px] overflow-hidden"
      >
        <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
          <span className="tech-text">MCP SYSTEM</span>
          <span className="tech-text text-[var(--jarvis-alert)] animate-pulse">{tool.toUpperCase()}</span>
        </div>
        
        {activeToolCall && (
          <div className="p-4 space-y-2 font-mono text-[11px] text-white/80">
            <div className="flex">
              <span className="w-16 text-white/40">TOOL</span>
              <span className="flex-1">{activeToolCall.name}()</span>
            </div>
            <div className="flex">
              <span className="w-16 text-white/40">CALL ID</span>
              <span className="flex-1 text-[var(--jarvis-cyan)] truncate">{activeToolCall.id}</span>
            </div>
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
