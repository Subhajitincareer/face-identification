import React from 'react';
import { useJarvisContext } from '../context/JarvisRuntimeContext';

export function SystemStatus() {
  const { state } = useJarvisContext();
  const { connections } = state;

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-8 tech-text">
      <StatusItem label="MIC" status={connections.microphone} />
      <StatusItem label="MODEL" status={connections.gemini} />
      <StatusItem label="MCP" status={connections.mcp} />
      <StatusItem label="BROWSER" status={connections.browser} />
    </div>
  );
}

function StatusItem({ label, status }: { label: string, status: string }) {
  let color = 'text-white/50';
  if (status === 'connected') color = 'text-[var(--jarvis-cyan)] shadow-[var(--jarvis-cyan)]';
  if (status === 'error') color = 'text-[var(--jarvis-error)]';
  if (status === 'connecting') color = 'text-[var(--jarvis-alert)] animate-pulse';

  return (
    <div className="flex items-center gap-2">
      <span>{label}</span>
      <div className={`w-1.5 h-1.5 rounded-full bg-current ${color}`} />
    </div>
  );
}
