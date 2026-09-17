import { useState, useEffect, useCallback, useRef } from 'react';

export function useAutoHide(initialVisibility = true, timeoutMs = 3000) {
  const [isVisible, setIsVisible] = useState(initialVisibility);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const hide = useCallback(() => {
    setIsVisible(false);
  }, []);

  const show = useCallback(() => {
    setIsVisible(true);
    resetTimeout();
  }, []);

  const toggle = useCallback(() => {
    if (isVisible) {
      hide();
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    } else {
      show();
    }
  }, [isVisible, hide, show]);

  const resetTimeout = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      setIsVisible(false);
    }, timeoutMs);
  }, [timeoutMs]);

  useEffect(() => {
    if (isVisible) {
      resetTimeout();
    }
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [isVisible, resetTimeout]);

  return {
    isVisible,
    show,
    hide,
    toggle,
    resetTimeout,
  };
}
