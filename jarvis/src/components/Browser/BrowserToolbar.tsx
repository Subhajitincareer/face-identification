import React from 'react';
import { BrowserRuntime } from '../../lib/jarvisStateMachine';
import { Maximize2, Minimize2, X } from 'lucide-react';

interface BrowserToolbarProps {
  browser: BrowserRuntime;
  isExpanded: boolean;
  onToggleExpand: () => void;
}

export function BrowserToolbar({ browser, isExpanded, onToggleExpand }: BrowserToolbarProps) {
  let statusColor = 'text-white/30';
  if (browser.state === 'open' || browser.state === 'navigating' || browser.state === 'interacting' || browser.state === 'reading') {
    statusColor = 'text-[var(--jarvis-cyan)]';
  } else if (browser.state === 'error' || browser.preview.status === 'error') {
    statusColor = 'text-[var(--jarvis-error)]';
  } else if (browser.state === 'launching') {
    statusColor = 'text-[var(--jarvis-alert)] animate-pulse';
  }

  // Display text for the current status dot
  const statusText = browser.state === 'error' ? 'ERROR' 
    : browser.state === 'disconnected' ? 'DISCONNECTED'
    : browser.state === 'launching' ? 'LAUNCHING'
    : browser.preview.status === 'live' ? 'LIVE'
    : browser.preview.status === 'stale' ? 'STALE'
    : 'CONNECTED';

  return (
    <div className="flex items-center justify-between px-3 py-2 border-b border-white/5 bg-black/40 backdrop-blur-md z-10 shrink-0">
      <div className="flex items-center gap-3 overflow-hidden">
        <span className="tech-text text-white/80 shrink-0">CHROME</span>
        <div className={`flex items-center gap-1.5 tech-text ${statusColor} shrink-0`}>
          <div className="w-1.5 h-1.5 rounded-full bg-current" />
          <span>{statusText}</span>
        </div>
        
        {/* URL/Title */}
        {browser.title && (
          <>
            <div className="w-[1px] h-3 bg-white/10 shrink-0" />
            <span className="text-[10px] text-white/60 truncate font-mono max-w-[150px] sm:max-w-[300px]">
              {browser.title}
            </span>
          </>
        )}
      </div>

      <div className="flex items-center gap-2 ml-4 shrink-0 text-white/40">
        <button 
          onClick={onToggleExpand}
          className="p-1 hover:text-[var(--jarvis-cyan)] hover:bg-white/5 rounded transition-colors"
          title={isExpanded ? "Minimize" : "Expand"}
        >
          {isExpanded ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
        </button>
      </div>
    </div>
  );
}
