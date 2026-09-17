import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Slider from '@react-native-community/slider';
import { useState, useEffect } from 'react';

const PRESET_SPEEDS = [0.25, 0.5, 1, 1.25, 1.5, 2, 4];

interface SpeedSelectorProps {
  currentSpeed: number;
  onSpeedSelect: (speed: number) => void;
}

export function SpeedSelector({ currentSpeed, onSpeedSelect }: SpeedSelectorProps) {
  const [localSpeed, setLocalSpeed] = useState(currentSpeed);

  // Sync localSpeed when currentSpeed prop changes (e.g. from preset buttons)
  useEffect(() => {
    setLocalSpeed(currentSpeed);
  }, [currentSpeed]);

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Playback Speed</Text>
      
      <View style={styles.sliderContainer}>
        <View style={styles.sliderTextContainer}>
          <Text style={styles.currentSpeedText}>{localSpeed.toFixed(2)}×</Text>
        </View>
        <View style={styles.sliderRow}>
          <Text style={styles.rangeText}>0.25×</Text>
          <Slider
            style={styles.slider}
            minimumValue={0.25}
            maximumValue={4}
            step={0.05}
            value={localSpeed}
            onValueChange={setLocalSpeed}
            onSlidingComplete={onSpeedSelect}
            minimumTrackTintColor="#FFFFFF"
            maximumTrackTintColor="#555555"
            thumbTintColor="#FFFFFF"
          />
          <Text style={styles.rangeText}>4×</Text>
        </View>
      </View>

      <View style={styles.presetsContainer}>
        {PRESET_SPEEDS.map((speed) => {
          const isActive = currentSpeed === speed;
          return (
            <TouchableOpacity
              key={speed}
              style={[styles.speedButton, isActive && styles.speedButtonActive]}
              onPress={() => onSpeedSelect(speed)}
              accessibilityRole="button"
              accessibilityState={{ selected: isActive }}
              accessibilityLabel={`Playback speed ${speed}x`}
            >
              <Text style={[styles.speedText, isActive && styles.speedTextActive]}>
                {speed}×
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 16,
  },
  label: {
    color: '#aaa',
    fontSize: 14,
    marginBottom: 12,
    paddingHorizontal: 24,
  },
  sliderContainer: {
    paddingHorizontal: 24,
    marginBottom: 24,
  },
  sliderTextContainer: {
    alignItems: 'center',
    marginBottom: 8,
  },
  currentSpeedText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  sliderRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  rangeText: {
    color: '#aaa',
    fontSize: 12,
  },
  slider: {
    flex: 1,
    marginHorizontal: 12,
    height: 40,
  },
  presetsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    paddingHorizontal: 8,
  },
  speedButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginHorizontal: 6,
    marginBottom: 12,
    backgroundColor: '#333',
  },
  speedButtonActive: {
    backgroundColor: '#fff',
  },
  speedText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  speedTextActive: {
    color: '#000',
  },
});
