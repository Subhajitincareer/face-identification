import React, { useEffect, useRef, useState } from 'react';

interface BrowserScreenshotCanvasProps {
  canvasRef: React.RefObject<HTMLCanvasElement | null>;
  isActive: boolean;
}

export function BrowserScreenshotCanvas({ canvasRef, isActive }: BrowserScreenshotCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Use ResizeObserver to ensure the canvas matches its container accurately
  useEffect(() => {
    if (!containerRef.current || !canvasRef.current) return;
    
    const container = containerRef.current;
    const canvas = canvasRef.current;
    
    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        // We set internal canvas resolution
        // You could multiply by window.devicePixelRatio for high-DPI, but 1x is fine for preview performance
        canvas.width = width;
        canvas.height = height;
      }
    });
    
    resizeObserver.observe(container);
    return () => resizeObserver.disconnect();
  }, [canvasRef]);

  return (
    <div 
      ref={containerRef} 
      className={`relative w-full h-full overflow-hidden bg-black/80 transition-opacity duration-300 ${isActive ? 'opacity-100' : 'opacity-20'}`}
    >
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full object-contain" 
      />
      
      {/* Scanline overlay for cinematic effect */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]"
        style={{ backgroundImage: 'linear-gradient(transparent 50%, rgba(0,0,0,1) 50%)', backgroundSize: '100% 4px' }}
      />
    </div>
  );
}
