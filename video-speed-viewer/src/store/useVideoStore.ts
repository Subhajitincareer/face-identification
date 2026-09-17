import { create } from 'zustand';

interface VideoState {
  selectedVideoUri: string | null;
  setSelectedVideoUri: (uri: string | null) => void;
}

export const useVideoStore = create<VideoState>((set) => ({
  selectedVideoUri: null,
  setSelectedVideoUri: (uri) => set({ selectedVideoUri: uri }),
}));
