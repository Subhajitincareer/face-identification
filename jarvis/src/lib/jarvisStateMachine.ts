export type VoiceState = 'idle' | 'user-speaking' | 'user-silent';
export type ModelState = 'disconnected' | 'connecting' | 'ready' | 'generating' | 'speaking' | 'interrupted' | 'error';
export type ToolState = 'idle' | 'calling' | 'success' | 'failed';

export type BrowserRuntime = {
  state: 'disconnected' | 'launching' | 'open' | 'navigating' | 'interacting' | 'reading' | 'error';
  tabId?: string;
  url?: string;
  title?: string;
  action?: string;
  activeTool?: string;
  preview: {
    available: boolean;
    updatedAt?: number;
    status: 'unavailable' | 'loading' | 'live' | 'stale' | 'error';
  };
};

export type ConnectionState = {
  microphone: 'disconnected' | 'connected' | 'error';
  gemini: 'disconnected' | 'connecting' | 'connected' | 'error';
  mcp: 'disconnected' | 'connecting' | 'connected' | 'error';
  browser: 'disconnected' | 'launching' | 'connected' | 'error';
};

export type JarvisRuntimeState = {
  voice: VoiceState;
  model: ModelState;
  tool: ToolState;
  browser: BrowserRuntime;
  connections: ConnectionState;

  currentTask?: string;

  activeToolCall?: {
    id: string;
    name: string;
    startedAt: number;
  };

  lastError?: {
    source: string;
    message: string;
    timestamp: number;
  };
};

export const initialJarvisState: JarvisRuntimeState = {
  voice: 'idle',
  model: 'disconnected',
  tool: 'idle',
  browser: { state: 'disconnected', preview: { available: false, status: 'unavailable' } },
  connections: {
    microphone: 'disconnected',
    gemini: 'disconnected',
    mcp: 'disconnected',
    browser: 'disconnected'
  }
};

// Represents a partial update to the state
export type StateUpdateAction = 
  | { type: 'UPDATE_VOICE'; payload: VoiceState }
  | { type: 'UPDATE_MODEL'; payload: ModelState }
  | { type: 'UPDATE_TOOL'; payload: ToolState }
  | { type: 'UPDATE_BROWSER'; payload: Partial<BrowserRuntime> }
  | { type: 'UPDATE_CONNECTIONS'; payload: Partial<ConnectionState> }
  | { type: 'SET_ACTIVE_TOOL'; payload: JarvisRuntimeState['activeToolCall'] }
  | { type: 'SET_CURRENT_TASK'; payload: string }
  | { type: 'SET_ERROR'; payload: NonNullable<JarvisRuntimeState['lastError']> };

export function jarvisStateReducer(state: JarvisRuntimeState, action: StateUpdateAction): JarvisRuntimeState {
  switch (action.type) {
    case 'UPDATE_VOICE':
      return { ...state, voice: action.payload };
    case 'UPDATE_MODEL':
      return { ...state, model: action.payload };
    case 'UPDATE_TOOL':
      return { ...state, tool: action.payload };
    case 'UPDATE_BROWSER':
      return { ...state, browser: { ...state.browser, ...action.payload } };
    case 'UPDATE_CONNECTIONS':
      return { ...state, connections: { ...state.connections, ...action.payload } };
    case 'SET_ACTIVE_TOOL':
      return { ...state, activeToolCall: action.payload };
    case 'SET_CURRENT_TASK':
      return { ...state, currentTask: action.payload };
    case 'SET_ERROR':
      return { ...state, lastError: action.payload };
    default:
      return state;
  }
}
