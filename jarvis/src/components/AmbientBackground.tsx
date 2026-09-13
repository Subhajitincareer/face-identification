import React from 'react';

export function AmbientBackground() {
  return (
    <div className="fixed inset-0 w-full h-full -z-50 pointer-events-none bg-[var(--background)] overflow-hidden">
      {/* Central gradient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-[var(--jarvis-cyan)] opacity-[0.03] blur-[120px]" />
      
      {/* Technical grid */}
      <div 
        className="absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage: `
            linear-gradient(to right, #fff 1px, transparent 1px),
            linear-gradient(to bottom, #fff 1px, transparent 1px)
          `,
          backgroundSize: '100px 100px',
        }}
      />
      
      {/* Vignette edge darkening */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_40%,#000_100%)]" />
    </div>
  );
}
