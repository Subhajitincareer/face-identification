import { useEffect, useReducer, useCallback } from 'react';
import { JarvisRuntimeState, initialJarvisState, jarvisStateReducer } from '../lib/jarvisStateMachine';
import { useMicrophone } from './useMicrophone';
import { useGeminiLive } from './useGeminiLive';
import { useMCPBrowserRuntime } from './useMCPBrowserRuntime';
import { eventBus, JarvisEvent } from '../lib/eventBus';

export function useJarvisRuntime() {
  const [state, dispatch] = useReducer(jarvisStateReducer, initialJarvisState);
  
  const mic = useMicrophone();
  const gemini = useGeminiLive();
  const browserRuntime = useMCPBrowserRuntime();

  // Sync Connections
  useEffect(() => {
    dispatch({
      type: 'UPDATE_CONNECTIONS',
      payload: {
        microphone: mic.hasPermission ? (mic.isRecording ? 'connected' : 'disconnected') : 'error',
        gemini: gemini.isConnected ? 'connected' : (gemini.errorMsg ? 'error' : 'disconnected'),
        mcp: 'disconnected', // Derived from first tool call success
        browser: browserRuntime.state === 'disconnected' ? 'disconnected' : 'connected'
      }
    });
  }, [mic.hasPermission, mic.isRecording, gemini.isConnected, gemini.errorMsg, browserRuntime.state]);

  // Sync Browser Runtime
  useEffect(() => {
    dispatch({ type: 'UPDATE_BROWSER', payload: browserRuntime });
  }, [browserRuntime]);

  // Event Bus Reducer
  useEffect(() => {
    const handleEvent = (event: JarvisEvent) => {
      switch (event.type) {
        case 'MODEL_TURN_STARTED':
          dispatch({ type: 'UPDATE_MODEL', payload: 'generating' });
          break;
        case 'MODEL_AUDIO_STARTED':
          dispatch({ type: 'UPDATE_MODEL', payload: 'speaking' });
          break;
        case 'TOOL_CALL_STARTED':
          dispatch({ type: 'UPDATE_TOOL', payload: 'calling' });
          dispatch({ 
            type: 'SET_ACTIVE_TOOL', 
            payload: { id: event.toolCallId!, name: event.metadata.toolName, startedAt: event.timestamp } 
          });
          // Optimistically set MCP connected if a tool runs
          dispatch({ type: 'UPDATE_CONNECTIONS', payload: { mcp: 'connected' } });
          break;
        case 'MCP_RESPONSE_RECEIVED':
          if (event.status === 'SUCCESS') {
            dispatch({ type: 'UPDATE_TOOL', payload: 'success' });
            setTimeout(() => dispatch({ type: 'UPDATE_TOOL', payload: 'idle' }), 2000);
          } else {
            dispatch({ type: 'UPDATE_TOOL', payload: 'failed' });
            dispatch({ 
              type: 'SET_ERROR', 
              payload: { source: 'MCP', message: event.metadata?.error || 'Unknown Error', timestamp: event.timestamp }
            });
          }
          break;
        case 'ERROR_OCCURRED':
          dispatch({ type: 'UPDATE_MODEL', payload: 'error' });
          dispatch({ 
            type: 'SET_ERROR', 
            payload: { source: event.source, message: event.metadata?.error || 'Unknown Error', timestamp: event.timestamp }
          });
          break;
      }
    };

    const unsubscribe = eventBus.subscribe(handleEvent);
    return () => unsubscribe();
  }, []);

  const toggleJarvis = useCallback(async () => {
    if (gemini.isConnected) {
      mic.stopRecording();
      gemini.disconnect();
      dispatch({ type: 'UPDATE_MODEL', payload: 'disconnected' });
    } else {
      if (mic.hasPermission !== true) {
        await mic.requestPermission();
        if (mic.hasPermission === false) return;
      }
      dispatch({ type: 'UPDATE_MODEL', payload: 'connecting' });
      await gemini.connect();
      await mic.startRecording((pcmData) => {
        gemini.sendAudio(pcmData);
      });
      dispatch({ type: 'UPDATE_MODEL', payload: 'ready' });
    }
  }, [mic, gemini]);

  return {
    state,
    toggleJarvis,
    isJarvisActive: gemini.isConnected
  };
}
