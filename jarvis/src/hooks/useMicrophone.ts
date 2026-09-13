"use client";

import { useState, useEffect, useRef, useCallback } from 'react';

export function useMicrophone() {
  const [isRecording, setIsRecording] = useState(false);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const animationFrameRef = useRef<number>(0);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);

  const checkPermission = useCallback(async () => {
    try {
      // @ts-ignore
      const result = await navigator.permissions.query({ name: 'microphone' });
      if (result.state === 'granted') {
        setHasPermission(true);
      } else if (result.state === 'denied') {
        setHasPermission(false);
      } else {
        setHasPermission(null);
      }
      
      result.onchange = () => {
        if (result.state === 'granted') setHasPermission(true);
        else if (result.state === 'denied') setHasPermission(false);
      };
    } catch (e) {
      console.log("Permission query API not supported, fallback to manual request");
    }
  }, []);

  const requestPermission = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setHasPermission(true);
      stream.getTracks().forEach(track => track.stop());
    } catch (err) {
      console.error("Microphone permission denied", err);
      setHasPermission(false);
    }
  }, []);

  const startRecording = useCallback(async (onAudioData?: (data: Int16Array) => void) => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { channelCount: 1, sampleRate: 16000 } 
      });
      mediaStreamRef.current = stream;
      
      const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });
      
      await audioContextRef.current.audioWorklet.addModule('/audio-processor.js');
      const workletNode = new AudioWorkletNode(audioContextRef.current, 'pcm-processor');
      
      workletNode.port.onmessage = (event) => {
        if (onAudioData) onAudioData(event.data);
      };

      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256;

      sourceRef.current = audioContextRef.current.createMediaStreamSource(stream);
      sourceRef.current.connect(analyserRef.current);
      sourceRef.current.connect(workletNode);

      setIsRecording(true);
      setHasPermission(true);

      const updateVolume = () => {
        if (!analyserRef.current) return;
        const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
        analyserRef.current.getByteFrequencyData(dataArray);
        
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
        }
        const average = sum / dataArray.length;
        
        // Write directly to CSS variable on document root to avoid React re-renders!
        document.documentElement.style.setProperty('--mic-volume', average.toString());

        animationFrameRef.current = requestAnimationFrame(updateVolume);
      };

      updateVolume();
      return stream;
    } catch (err) {
      console.error("Error starting microphone", err);
      setHasPermission(false);
      return null;
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    if (sourceRef.current) sourceRef.current.disconnect();
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }
    setIsRecording(false);
    document.documentElement.style.setProperty('--mic-volume', '0');
  }, []);

  useEffect(() => {
    return () => {
      stopRecording();
    };
  }, [stopRecording]);

  return {
    isRecording,
    hasPermission,
    startRecording,
    stopRecording,
    requestPermission,
    checkPermission
  };
}
