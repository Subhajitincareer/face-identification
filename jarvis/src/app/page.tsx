"use client";

import { JarvisRuntimeProvider } from '../context/JarvisRuntimeContext';
import { JarvisShell } from '../components/JarvisShell';

export default function Jarvis() {
  return (
    <JarvisRuntimeProvider>
      <JarvisShell />
    </JarvisRuntimeProvider>
  );
}
