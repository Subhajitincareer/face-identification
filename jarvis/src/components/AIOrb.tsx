import React, { useEffect, useRef } from 'react';
import { motion, useAnimation } from 'motion/react';
import { useJarvisContext } from '../context/JarvisRuntimeContext';

export function AIOrb() {
  const { visualState } = useJarvisContext();
  const controls = useAnimation();
  const orbRef = useRef<HTMLDivElement>(null);

  // Animate based on discrete visual states
  useEffect(() => {
    switch (visualState) {
      case 'OFFLINE':
      case 'ERROR':
        controls.start({
          scale: 0.95,
          borderColor: 'rgba(255, 51, 51, 0.5)',
          boxShadow: '0 0 20px rgba(255, 51, 51, 0.2)',
          transition: { duration: 1 }
        });
        break;
      case 'IDLE':
        controls.start({
          scale: 1,
          borderColor: 'rgba(0, 240, 255, 0.2)',
          boxShadow: '0 0 30px rgba(0, 240, 255, 0.1)',
          transition: { duration: 2, repeat: Infinity, repeatType: 'reverse' }
        });
        break;
      case 'LISTENING':
        controls.start({
          scale: 1.05,
          borderColor: 'rgba(0, 240, 255, 0.6)',
          boxShadow: '0 0 60px rgba(0, 240, 255, 0.3)',
          transition: { duration: 0.3 }
        });
        break;
      case 'THINKING':
        controls.start({
          scale: [1, 1.1, 1],
          borderColor: 'rgba(0, 119, 255, 0.8)',
          boxShadow: '0 0 80px rgba(0, 119, 255, 0.4)',
          transition: { duration: 1.5, repeat: Infinity }
        });
        break;
      case 'SPEAKING':
        controls.start({
          scale: 1.1,
          borderColor: 'rgba(0, 240, 255, 0.9)',
          boxShadow: '0 0 100px rgba(0, 240, 255, 0.5)',
          transition: { duration: 0.2 }
        });
        break;
      case 'EXECUTING':
        controls.start({
          scale: 1.2,
          borderColor: 'rgba(0, 255, 136, 0.8)',
          boxShadow: '0 0 80px rgba(0, 255, 136, 0.4)',
          transition: { duration: 0.5, repeat: Infinity, repeatType: 'reverse' }
        });
        break;
      case 'SUCCESS':
        controls.start({
          scale: 1,
          borderColor: 'rgba(0, 255, 136, 0.4)',
          boxShadow: '0 0 40px rgba(0, 255, 136, 0.2)',
          transition: { duration: 0.5 }
        });
        break;
    }
  }, [visualState, controls]);

  // Audio reactivity via requestAnimationFrame reading CSS vars
  useEffect(() => {
    let animationId: number;
    const updateAudioReact = () => {
      if (orbRef.current && (visualState === 'LISTENING' || visualState === 'SPEAKING')) {
        // Read the global CSS variable set by useMicrophone
        const volStr = getComputedStyle(document.documentElement).getPropertyValue('--mic-volume');
        const vol = parseFloat(volStr) || 0;
        // Apply transform directly to avoid React render cycle
        const scale = 1 + (vol / 255) * 0.4;
        orbRef.current.style.transform = `scale(${scale})`;
      } else if (orbRef.current) {
        orbRef.current.style.transform = `scale(1)`;
      }
      animationId = requestAnimationFrame(updateAudioReact);
    };
    updateAudioReact();
    return () => cancelAnimationFrame(animationId);
  }, [visualState]);

  return (
    <div className="relative flex items-center justify-center w-[400px] h-[400px]">
      {/* Outer rotating ring */}
      <motion.div 
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        className="absolute inset-0 border border-white/5 rounded-full border-dashed"
      />
      
      {/* Inner rotating ring (reverse) */}
      <motion.div 
        animate={{ rotate: -360 }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
        className="absolute inset-8 border border-[var(--jarvis-cyan)]/20 rounded-full border-dotted"
      />

      {/* The Core Orb */}
      <motion.div
        ref={orbRef}
        animate={controls}
        className="relative z-10 w-32 h-32 rounded-full border-2 bg-black/50 backdrop-blur-xl flex items-center justify-center"
      >
        {/* Core center point */}
        <div className="w-8 h-8 rounded-full bg-white/10 blur-[2px]" />
      </motion.div>

      {/* Label layer */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 mt-32 tech-text text-[var(--jarvis-cyan)]">
        {visualState}
      </div>
    </div>
  );
}
