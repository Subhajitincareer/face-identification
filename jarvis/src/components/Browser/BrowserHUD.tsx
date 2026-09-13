import React from 'react';
import { BrowserRuntime } from '../../lib/jarvisStateMachine';
import { motion, AnimatePresence } from 'motion/react';

interface BrowserHUDProps {
  browser: BrowserRuntime;
}

export function BrowserHUD({ browser }: BrowserHUDProps) {
  // If the browser isn't doing anything active, we don't need a heavy HUD overlay
  const isExecuting = browser.state === 'navigating' || browser.state === 'interacting' || browser.state === 'reading';

  let actionText = '';
  switch (browser.state) {
    case 'navigating': actionText = 'NAVIGATING'; break;
    case 'interacting': actionText = 'INTERACTING'; break;
    case 'reading': actionText = 'READING PAGE'; break;
  }

  return (
    <AnimatePresence>
      {isExecuting && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 pointer-events-none flex flex-col items-center justify-center z-20"
        >
          {/* Subtle dark backdrop to make HUD readable */}
          <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px]" />
          
          <div className="relative z-30 flex flex-col items-center gap-4">
            {/* Pulsing indicator */}
            <div className="w-12 h-12 rounded-full border border-[var(--jarvis-cyan)] flex items-center justify-center">
              <motion.div 
                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="w-4 h-4 rounded-full bg-[var(--jarvis-cyan)]"
              />
            </div>

            {/* Status Panel */}
            <div className="bg-black/80 border border-[var(--jarvis-cyan)]/30 rounded px-6 py-4 flex flex-col items-center shadow-[0_0_20px_rgba(0,240,255,0.2)]">
              <span className="text-[var(--jarvis-cyan)] font-mono text-lg tracking-widest mb-2">
                {actionText}
              </span>
              
              <div className="flex flex-col w-full gap-1 border-t border-white/10 pt-2 font-mono text-[10px] text-white/60">
                <div className="flex justify-between gap-8">
                  <span>MCP TOOL</span>
                  <span className="text-white">{browser.activeTool}()</span>
                </div>
                {browser.action && (
                  <div className="flex justify-between gap-8 mt-1">
                    <span>ACTION</span>
                    <span className="text-white/80">{browser.action}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
