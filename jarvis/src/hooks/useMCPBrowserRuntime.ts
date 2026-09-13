import { useEffect, useState } from 'react';
import { BrowserRuntime } from '../lib/jarvisStateMachine';
import { eventBus, JarvisEvent } from '../lib/eventBus';

export function useMCPBrowserRuntime(): BrowserRuntime {
  const [browser, setBrowser] = useState<BrowserRuntime>({ 
    state: 'disconnected',
    preview: { available: false, status: 'unavailable' }
  });

  useEffect(() => {
    const handleEvent = (event: JarvisEvent) => {
      if (event.type === 'MCP_REQUEST_SENT') {
        const toolName = event.metadata?.toolName;
        if (toolName === 'navigate') {
          setBrowser(prev => ({ ...prev, state: 'navigating', action: 'Navigating', activeTool: toolName }));
        } else if (toolName === 'get_page_source') {
          setBrowser(prev => ({ ...prev, state: 'reading', action: 'Reading page', activeTool: toolName }));
        } else if (toolName === 'click' || toolName === 'type_text') {
          setBrowser(prev => ({ ...prev, state: 'interacting', action: 'Interacting', activeTool: toolName }));
        }
      } else if (event.type === 'MCP_RESPONSE_RECEIVED') {
        if (event.status === 'SUCCESS') {
          setBrowser(prev => ({ ...prev, state: 'open', action: 'Idle', activeTool: undefined }));
        } else {
          setBrowser(prev => ({ ...prev, state: 'error', action: 'Tool Failed', activeTool: undefined }));
        }
      }
    };

    const unsubscribe = eventBus.subscribe(handleEvent);
    return () => unsubscribe();
  }, []);

  return browser;
}
