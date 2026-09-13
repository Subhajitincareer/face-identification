import { useEffect, useRef, useState, useCallback } from 'react';
import { BrowserRuntime } from '../lib/jarvisStateMachine';
import { eventBus } from '../lib/eventBus';

interface UseBrowserStreamProps {
  canvasRef: React.RefObject<HTMLCanvasElement | null>;
  browserState: BrowserRuntime;
}

export function useBrowserStream({ canvasRef, browserState }: UseBrowserStreamProps) {
  const isCapturingRef = useRef(false);
  const [streamStatus, setStreamStatus] = useState<BrowserRuntime['preview']['status']>('unavailable');
  
  const fetchScreenshot = useCallback(async () => {
    if (isCapturingRef.current || !canvasRef.current || browserState.state === 'disconnected') {
      return;
    }

    isCapturingRef.current = true;
    
    try {
      const res = await fetch('/api/mcp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ toolName: 'take_screenshot', args: {} })
      });
      
      const data = await res.json();
      
      if (data.error || (data.result && data.result.error)) {
        setStreamStatus('error');
        isCapturingRef.current = false;
        return;
      }
      
      // Usually MCP result has content array or string
      let base64String = '';
      if (Array.isArray(data.result?.content)) {
        // e.g. [{ type: "text", text: "..." }]
        const textContent = data.result.content.find((c: any) => c.type === 'text');
        if (textContent) {
            base64String = textContent.text;
        }
      } else if (typeof data.result === 'string') {
        base64String = data.result;
      }

      if (!base64String || base64String.startsWith('Error:')) {
          if (base64String.startsWith('Error:')) {
            setStreamStatus('error');
          }
          isCapturingRef.current = false;
          return;
      }

      const img = new Image();
      img.onload = () => {
        if (!canvasRef.current) return;
        
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        
        // Draw image, matching object-fit: contain logic if necessary
        // Simple scale to fit for now, let CSS handle the responsive resizing of canvas element
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Compute aspect ratio preserving dimensions
        const canvasRatio = canvas.width / canvas.height;
        const imgRatio = img.width / img.height;
        
        let drawWidth, drawHeight, x, y;
        
        if (imgRatio > canvasRatio) {
          drawWidth = canvas.width;
          drawHeight = canvas.width / imgRatio;
          x = 0;
          y = (canvas.height - drawHeight) / 2;
        } else {
          drawHeight = canvas.height;
          drawWidth = canvas.height * imgRatio;
          y = 0;
          x = (canvas.width - drawWidth) / 2;
        }
        
        ctx.drawImage(img, x, y, drawWidth, drawHeight);
        setStreamStatus('live');
        
        // Emit a specific event so ActivityPanel can track when screenshots happen
        eventBus.emit({
          type: 'SCREENSHOT_CAPTURED',
          source: 'Chrome',
          status: 'SUCCESS'
        });
      };
      
      img.onerror = () => {
        setStreamStatus('error');
      };
      
      img.src = `data:image/png;base64,${base64String}`;
      
    } catch (err) {
      console.error("Screenshot stream error:", err);
      setStreamStatus('error');
    } finally {
      isCapturingRef.current = false;
    }
  }, [browserState.state, canvasRef]);

  useEffect(() => {
    // Only stream if the browser is "open" or actively doing something
    if (browserState.state === 'disconnected' || browserState.state === 'launching') {
      setStreamStatus('unavailable');
      return;
    }

    if (streamStatus === 'unavailable') {
      setStreamStatus('loading');
    }

    // 2 FPS polling
    const intervalId = setInterval(fetchScreenshot, 500);
    
    // Initial fetch
    fetchScreenshot();

    return () => {
      clearInterval(intervalId);
    };
  }, [browserState.state, fetchScreenshot, streamStatus]);

  return { streamStatus };
}
