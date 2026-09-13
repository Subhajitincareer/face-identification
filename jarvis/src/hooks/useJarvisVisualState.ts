import { JarvisRuntimeState } from '../lib/jarvisStateMachine';

export type JarvisVisualState = 
  | 'OFFLINE'
  | 'IDLE'
  | 'LISTENING'
  | 'THINKING'
  | 'SPEAKING'
  | 'EXECUTING'
  | 'SUCCESS'
  | 'ERROR';

export function deriveJarvisVisualState(state: JarvisRuntimeState): JarvisVisualState {
  // 1. Connection failures supersede everything (OFFLINE)
  if (
    state.connections.gemini === 'disconnected' || 
    state.connections.gemini === 'error' ||
    state.model === 'disconnected' || 
    state.model === 'error'
  ) {
    return 'OFFLINE';
  }

  // 2. Error states
  if (state.tool === 'failed' || state.lastError) {
    return 'ERROR';
  }

  // 3. Executing tools (High Priority Visual)
  if (state.tool === 'calling') {
    return 'EXECUTING';
  }

  // 4. Voice and Model Activity
  if (state.model === 'speaking') {
    return 'SPEAKING';
  }

  if (state.model === 'generating') {
    return 'THINKING';
  }

  if (state.voice === 'user-speaking') {
    return 'LISTENING';
  }

  // 5. Success states (transient)
  if (state.tool === 'success') {
    return 'SUCCESS';
  }

  // Default Fallback
  return 'IDLE';
}
