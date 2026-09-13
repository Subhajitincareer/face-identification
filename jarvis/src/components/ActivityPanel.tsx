import React, { useEffect, useState, useRef } from 'react';
import { eventBus, JarvisEvent } from '../lib/eventBus';
import { motion, AnimatePresence } from 'motion/react';

export function ActivityPanel() {
  const [events, setEvents] = useState<JarvisEvent[]>([]);
  const [mode, setMode] = useState<'normal' | 'diagnostic'>('normal');
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initial load
    setEvents(eventBus.getHistory());
    
    // Subscribe to new events
    const unsubscribe = eventBus.subscribe((newEvent) => {
      setEvents(prev => [...prev, newEvent]);
    });
    
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    // Auto scroll to bottom
    if (endRef.current) {
      endRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [events, mode]);

  return (
    <div className="glass-panel w-[450px] max-h-[300px] flex flex-col overflow-hidden pointer-events-auto">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
        <span className="tech-text">ACTIVITY LOG</span>
        <button 
          onClick={() => setMode(m => m === 'normal' ? 'diagnostic' : 'normal')}
          className="tech-text text-white/30 hover:text-[var(--jarvis-cyan)] transition-colors"
        >
          {mode === 'normal' ? 'SHOW DIAGNOSTICS' : 'NORMAL MODE'}
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-[11px] text-white/70">
        <AnimatePresence initial={false}>
          {events.map((ev, i) => (
            <motion.div 
              key={ev.eventId}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-start gap-4"
            >
              <span className="text-white/30 shrink-0">
                {new Date(ev.timestamp).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
              
              {mode === 'normal' ? (
                <NormalEventView event={ev} />
              ) : (
                <DiagnosticEventView event={ev} />
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={endRef} />
      </div>
    </div>
  );
}

function NormalEventView({ event }: { event: JarvisEvent }) {
  let text = '';
  switch (event.type) {
    case 'USER_AUDIO_STARTED': text = 'Listening to user...'; break;
    case 'MODEL_TURN_STARTED': text = 'Analyzing request...'; break;
    case 'TOOL_CALL_STARTED': text = `Executing tool: ${event.metadata?.toolName}`; break;
    case 'MCP_RESPONSE_RECEIVED': 
      if (event.status === 'SUCCESS') text = `Tool completed successfully`;
      else text = `Tool execution failed`;
      break;
    case 'ERROR_OCCURRED': text = `System Error: ${event.metadata?.error}`; break;
    default: return null; // Hide obscure events in normal mode
  }

  return (
    <span className={event.status === 'ERROR' ? 'text-[var(--jarvis-error)]' : 'text-white/80'}>
      {text}
    </span>
  );
}

function DiagnosticEventView({ event }: { event: JarvisEvent }) {
  return (
    <div className="flex flex-col gap-1 w-full border-l border-white/10 pl-2">
      <div className="flex gap-4 w-full">
        <span className="w-24 text-[var(--jarvis-cyan)] truncate" title={event.eventId}>{event.eventId}</span>
        <span className="w-16 text-white/50">{event.source}</span>
        <span className="w-32 text-white/80 truncate">{event.type}</span>
        {event.status === 'SUCCESS' && <span className="text-[var(--jarvis-success)] ml-auto">✓</span>}
        {event.status === 'ERROR' && <span className="text-[var(--jarvis-error)] ml-auto">✗</span>}
      </div>
      {event.toolCallId && (
        <div className="text-white/40 flex gap-4">
          <span>Call: {event.toolCallId}</span>
          {event.durationMs && <span>{event.durationMs}ms</span>}
        </div>
      )}
      {event.metadata && (
        <div className="text-white/30 text-[9px] break-all">
          {JSON.stringify(event.metadata)}
        </div>
      )}
    </div>
  );
}
