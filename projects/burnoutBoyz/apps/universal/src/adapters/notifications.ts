import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

export async function enableReminders(): Promise<'granted' | 'denied' | 'web'> {
  if (Platform.OS === 'web') return 'web';
  const current = await Notifications.getPermissionsAsync();
  const result = current.granted ? current : await Notifications.requestPermissionsAsync();
  if (!result.granted) return 'denied';
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('maintenance', {
      name: 'Maintenance reminders',
      importance: Notifications.AndroidImportance.DEFAULT,
    });
  }
  return 'granted';
}

export async function scheduleReminder(title: string): Promise<string | null> {
  if (Platform.OS === 'web') return null;
  return Notifications.scheduleNotificationAsync({
    content: { title: 'BurnoutBoyz reminder', body: `${title} is ready to review. This is a planning prompt, not a diagnosis.`, data: { href: '/' } },
    trigger: { type: Notifications.SchedulableTriggerInputTypes.TIME_INTERVAL, seconds: 60, channelId: 'maintenance' },
  });
}
