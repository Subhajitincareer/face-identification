export type EventType = 
  | 'USER_AUDIO_STARTED'
  | 'USER_AUDIO_ENDED'
  | 'MODEL_TURN_STARTED'
  | 'MODEL_TURN_ENDED'
  | 'MODEL_AUDIO_STARTED'
  | 'MODEL_AUDIO_ENDED'
  | 'TOOL_CALL_STARTED'
  | 'MCP_REQUEST_SENT'
  | 'MCP_RESPONSE_RECEIVED'
  | 'BROWSER_NAVIGATION'
  | 'SCREENSHOT_CAPTURED'
  | 'ERROR_OCCURRED';

export interface JarvisEvent {
  eventId: string;
  timestamp: number;
  type: EventType;
  source: 'User' | 'Gemini' | 'MCP' | 'Chrome' | 'System';
  status: 'SUCCESS' | 'ERROR' | 'PENDING' | 'INFO';
  toolCallId?: string;
  durationMs?: number;
  metadata?: any;
}

type EventListener = (event: JarvisEvent) => void;

class EventBus {
  private listeners: EventListener[] = [];
  private eventHistory: JarvisEvent[] = [];

  subscribe(listener: EventListener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  emit(event: Omit<JarvisEvent, 'eventId' | 'timestamp'>) {
    const fullEvent: JarvisEvent = {
      ...event,
      eventId: `ev_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
    };
    
    this.eventHistory.push(fullEvent);
    
    // Keep history bounded to prevent memory leaks
    if (this.eventHistory.length > 1000) {
      this.eventHistory.shift();
    }

    this.listeners.forEach(listener => listener(fullEvent));
  }

  getHistory() {
    return [...this.eventHistory];
  }
}

export const eventBus = new EventBus();
