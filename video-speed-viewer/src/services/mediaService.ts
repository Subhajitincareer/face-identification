import * as ImagePicker from 'expo-image-picker';
import { Alert } from 'react-native';

export const mediaService = {
  /**
   * Opens the system media picker filtered to videos only.
   *
   * @returns {Promise<string | null>} URI of the selected video, or null if cancelled or error.
   */
  async pickVideo(): Promise<string | null> {
    try {
      const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permission.granted) {
        Alert.alert('Permission required', 'We need media library permission to select a video.');
        return null;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ['videos'],
        allowsEditing: false,
        quality: 1,
      });

      if (result.canceled) {
        return null;
      }

      const video = result.assets[0];
      if (!video || video.type !== 'video') {
        console.warn('Selected asset is not a video');
        Alert.alert('Error', 'The selected asset is not a valid video.');
        return null;
      }

      return video.uri;
    } catch (error) {
      console.error('Error picking video:', error);
      Alert.alert('Error', 'Could not open the video picker. Please try again.');
      return null;
    }
  },
};
