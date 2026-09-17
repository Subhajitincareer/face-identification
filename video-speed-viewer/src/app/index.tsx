import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useVideoStore } from '../store/useVideoStore';
import { mediaService } from '../services/mediaService';

export default function HomeScreen() {
  const router = useRouter();
  const setSelectedVideoUri = useVideoStore((state) => state.setSelectedVideoUri);

  const handleChooseVideo = async () => {
    const uri = await mediaService.pickVideo();
    if (uri) {
      setSelectedVideoUri(uri);
      router.push('/player');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.emptyState}>
        <Ionicons name="film-outline" size={80} color="#555" />
        <Text style={styles.title}>No video selected</Text>
        <Text style={styles.subtitle}>
          Choose a video from your gallery{'\n'}and control its playback speed.
        </Text>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={handleChooseVideo}
        activeOpacity={0.8}
        accessibilityRole="button"
        accessibilityLabel="Choose Video"
        accessibilityHint="Opens your photo library to select a video"
      >
        <Ionicons name="play" size={24} color="#000" style={styles.buttonIcon} />
        <View>
          <Text style={styles.buttonText}>Choose Video</Text>
          <Text style={styles.buttonSubText}>Select a video from your device</Text>
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyState: {
    alignItems: 'center',
    marginBottom: 60,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 24,
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
    lineHeight: 24,
  },
  button: {
    backgroundColor: '#fff',
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#fff',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 5,
  },
  buttonIcon: {
    marginRight: 16,
  },
  buttonText: {
    color: '#000',
    fontSize: 18,
    fontWeight: 'bold',
  },
  buttonSubText: {
    color: '#555',
    fontSize: 12,
    marginTop: 4,
  },
});
