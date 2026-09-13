import React, { useRef, useState } from 'react';
import { useJarvisContext } from '../../context/JarvisRuntimeContext';
import { useBrowserStream } from '../../hooks/useBrowserStream';
import { BrowserScreenshotCanvas } from './BrowserScreenshotCanvas';
import { BrowserToolbar } from './BrowserToolbar';
import { BrowserHUD } from './BrowserHUD';
import { BrowserActionOverlay } from './BrowserActionOverlay';
import { motion, AnimatePresence } from 'motion/react';

export function LiveBrowserView() {
  const { state } = useJarvisContext();
  const { browser } = state;
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  // Custom hook that manages the 2FPS screenshot polling
  const { streamStatus } = useBrowserStream({
    canvasRef,
    browserState: browser
  });

  const [isExpanded, setIsExpanded] = useState(false);

  // If the browser is completely disconnected, hide the view entirely on small screens
  // On desktop it could be an empty placeholder, but hiding it is cleaner for the cinematic look.
  if (browser.state === 'disconnected') {
    return null;
  }

  return (
    <AnimatePresence>
      <motion.div
        layout
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className={`
          glass-panel flex flex-col overflow-hidden pointer-events-auto shadow-2xl
          ${isExpanded 
            ? 'fixed inset-4 md:inset-10 z-50' // Expanded cinematic mode
            : 'fixed bottom-24 right-4 md:bottom-8 md:right-8 w-[320px] h-[240px] sm:w-[480px] sm:h-[320px] z-40' // Floating mini-browser snapped to bottom-right
          }
        `}
      >
        <BrowserToolbar 
          browser={{ ...browser, preview: { ...browser.preview, status: streamStatus } }} 
          isExpanded={isExpanded}
          onToggleExpand={() => setIsExpanded(!isExpanded)}
        />
        
        <div className="relative flex-1 w-full bg-[#111]">
          {/* Main rendering canvas */}
          <BrowserScreenshotCanvas 
            canvasRef={canvasRef} 
            isActive={streamStatus === 'live' || streamStatus === 'stale'} 
          />

          {/* Execution HUD overlay */}
          <BrowserHUD browser={browser} />
          
          {/* Action markers/outlines */}
          <BrowserActionOverlay browser={browser} />

          {/* Fallback states */}
          <AnimatePresence>
            {(streamStatus === 'unavailable' || streamStatus === 'loading') && browser.state !== 'launching' && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-10"
              >
                <div className="tech-text text-white/40">
                  {streamStatus === 'loading' ? 'ESTABLISHING PREVIEW STREAM...' : 'PREVIEW UNAVAILABLE'}
                </div>
              </motion.div>
            )}

            {streamStatus === 'error' && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 flex flex-col items-center justify-center bg-black/90 z-10 border border-[var(--jarvis-error)]/20"
              >
                <div className="tech-text text-[var(--jarvis-error)] mb-2">LIVE PREVIEW ERROR</div>
                <div className="tech-text text-white/50 text-[8px]">Screenshot stream unavailable</div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
