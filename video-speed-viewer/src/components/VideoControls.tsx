import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { formatTime } from '../utils/formatTime';

interface VideoControlsProps {
  isPlaying: boolean;
  onPlayPause: () => void;
  onSeekBackward: () => void;
  onSeekForward: () => void;
  currentTime: number;
  duration: number;
}

export function VideoControls({
  isPlaying,
  onPlayPause,
  onSeekBackward,
  onSeekForward,
  currentTime,
  duration,
}: VideoControlsProps) {
  // A simple progress calculation for the timeline.
  // We'll improve the slider in a later phase, but for now we show a basic progress bar.
  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <View style={styles.container}>
      {/* Timeline */}
      <View style={styles.timelineContainer}>
        <Text style={styles.timeText}>{formatTime(currentTime)}</Text>
        <View style={styles.progressBarContainer}>
          <View style={styles.progressBarBackground}>
            <View style={[styles.progressBarFill, { width: `${progress}%` }]} />
            <View style={[styles.progressThumb, { left: `${progress}%` }]} />
          </View>
        </View>
        <Text style={styles.timeText}>{formatTime(duration)}</Text>
      </View>

      {/* Primary Controls */}
      <View style={styles.controlsRow}>
        <TouchableOpacity 
          style={styles.iconButton} 
          onPress={onSeekBackward}
          accessibilityLabel="Seek backward 10 seconds"
        >
          <Ionicons name="play-back" size={32} color="#fff" />
          <Text style={styles.seekText}>10s</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.playPauseButton} 
          onPress={onPlayPause}
          accessibilityLabel={isPlaying ? 'Pause video' : 'Play video'}
        >
          <Ionicons name={isPlaying ? 'pause' : 'play'} size={40} color="#000" />
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.iconButton} 
          onPress={onSeekForward}
          accessibilityLabel="Seek forward 10 seconds"
        >
          <Ionicons name="play-forward" size={32} color="#fff" />
          <Text style={styles.seekText}>10s</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 24,
    width: '100%',
  },
  timelineContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 32,
  },
  timeText: {
    color: '#fff',
    fontSize: 14,
    fontVariant: ['tabular-nums'],
    width: 48,
    textAlign: 'center',
  },
  progressBarContainer: {
    flex: 1,
    height: 20,
    justifyContent: 'center',
    marginHorizontal: 12,
  },
  progressBarBackground: {
    height: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderRadius: 2,
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#fff',
    borderRadius: 2,
    position: 'absolute',
    left: 0,
    top: 0,
  },
  progressThumb: {
    width: 16,
    height: 16,
    borderRadius: 8,
    backgroundColor: '#fff',
    position: 'absolute',
    top: -6,
    marginLeft: -8, // Center the thumb on the progress point
  },
  controlsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 40,
  },
  iconButton: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  playPauseButton: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  seekText: {
    color: '#aaa',
    fontSize: 12,
    marginTop: 4,
  },
});
