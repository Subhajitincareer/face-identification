import { useEffect, useState } from 'react';
import { View, StyleSheet, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useEvent } from 'expo';
import { Ionicons } from '@expo/vector-icons';
import { useVideoStore } from '../store/useVideoStore';
import { SpeedSelector } from '../components/SpeedSelector';
import { VideoControls } from '../components/VideoControls';
import { useAutoHide } from '../hooks/useAutoHide';
import { mediaService } from '../services/mediaService';

export default function PlayerScreen() {
  const router = useRouter();
  const selectedVideoUri = useVideoStore((state) => state.selectedVideoUri);
  const setSelectedVideoUri = useVideoStore((state) => state.setSelectedVideoUri);
  const { isVisible: controlsVisible, toggle: toggleControls, resetTimeout } = useAutoHide(true, 3000);

  // If there's no video selected, go back to home
  useEffect(() => {
    if (!selectedVideoUri) {
      router.replace('/');
    }
  }, [selectedVideoUri, router]);

  const player = useVideoPlayer(selectedVideoUri || '', (p) => {
    p.loop = false;
    p.play();
  });

  const { isPlaying } = useEvent(player, 'playingChange', { isPlaying: player.playing });
  const { currentTime } = useEvent(player, 'timeUpdate', { currentTime: player.currentTime });
  // Duration is not directly part of an event in all versions, 
  // but it is available on player.duration
  const duration = player.duration || 0;
  // Playback rate
  const { playbackRate } = useEvent(player, 'playbackRateChange', { playbackRate: player.playbackRate });

  const handlePlayPause = () => {
    if (isPlaying) {
      player.pause();
    } else {
      // If the video has ended, restart it from the beginning
      if (duration > 0 && Math.abs(duration - currentTime) < 0.5) {
        player.currentTime = 0;
      }
      player.play();
    }
    resetTimeout();
  };

  const handleSeekBackward = () => {
    const newTime = Math.max(currentTime - 10, 0);
    player.currentTime = newTime;
    resetTimeout();
  };

  const handleSeekForward = () => {
    const newTime = Math.min(currentTime + 10, duration);
    player.currentTime = newTime;
    resetTimeout();
  };

  const handleSpeedSelect = (speed: number) => {
    player.playbackRate = speed;
    resetTimeout();
  };

  const handlePickVideo = async () => {
    resetTimeout();
    player.pause(); // pause current video while picking
    const uri = await mediaService.pickVideo();
    if (uri) {
      setSelectedVideoUri(uri);
    } else {
      player.play(); // resume if cancelled
    }
  };

  if (!selectedVideoUri) return null;

  return (
    <SafeAreaView style={styles.container}>
      <Pressable style={styles.videoContainer} onPressIn={toggleControls}>
        <VideoView
          style={styles.video}
          player={player}
          allowsFullscreen={false} // We will handle fullscreen logic later if needed
          allowsPictureInPicture={false}
          nativeControls={false} // We are building custom controls
          contentFit="contain"
        />
      </Pressable>

      {/* Header / Back Button */}
      {controlsVisible && (
        <View style={styles.header}>
          <Ionicons 
            name="chevron-down" 
            size={36} 
            color="#fff" 
            onPress={() => router.back()} 
            style={styles.headerButton}
          />
          <Ionicons 
            name="images-outline" 
            size={30} 
            color="#fff" 
            onPress={handlePickVideo} 
            style={styles.headerButton}
          />
        </View>
      )}

      {/* Controls Overlay */}
      {controlsVisible && (
        <View style={styles.controlsOverlay}>
          <VideoControls
            isPlaying={isPlaying}
            onPlayPause={handlePlayPause}
            onSeekBackward={handleSeekBackward}
            onSeekForward={handleSeekForward}
            currentTime={currentTime}
            duration={duration}
          />
          <View style={styles.speedSelectorContainer}>
            <SpeedSelector
              currentSpeed={playbackRate}
              onSpeedSelect={handleSpeedSelect}
            />
          </View>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  videoContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  video: {
    width: '100%',
    height: '100%',
  },
  header: {
    position: 'absolute',
    top: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    zIndex: 10,
  },
  headerButton: {
    padding: 8,
  },
  controlsOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(0,0,0,0.7)',
    paddingBottom: 20,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
  },
  speedSelectorContainer: {
    marginTop: 8,
  },
});
