import React from 'react';
import { BrowserRuntime } from '../../lib/jarvisStateMachine';
import { motion, AnimatePresence } from 'motion/react';

interface BrowserActionOverlayProps {
  browser: BrowserRuntime;
}

export function BrowserActionOverlay({ browser }: BrowserActionOverlayProps) {
  // Currently, we don't have exact screen coordinates for elements from the MCP backend,
  // because the tool only receives a CSS selector (e.g., click(selector)).
  // In the future, if the backend returns bounding box coordinates, we can render a precise outline here.
  
  // For now, we will just render a subtle screen flash when an interaction happens.
  const isInteracting = browser.state === 'interacting';

  return (
    <AnimatePresence>
      {isInteracting && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 pointer-events-none z-15"
        >
          {/* Subtle edge glow to indicate active automation control over the page */}
          <div className="absolute inset-0 shadow-[inset_0_0_50px_rgba(0,255,136,0.2)] border-2 border-[var(--jarvis-success)]/30 transition-all duration-300" />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
