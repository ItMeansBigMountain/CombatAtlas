import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import type { GarageSnapshot } from '@/domain/models';

const GARAGE_KEY = 'burnoutboyz.garage.v1';
const SECRET_PREFIX = 'burnoutboyz.secret.';

export async function loadGarage(fallback: GarageSnapshot): Promise<GarageSnapshot> {
  const value = await AsyncStorage.getItem(GARAGE_KEY);
  if (!value) return fallback;
  try { return JSON.parse(value) as GarageSnapshot; } catch { return fallback; }
}

export async function saveGarage(snapshot: GarageSnapshot): Promise<void> {
  await AsyncStorage.setItem(GARAGE_KEY, JSON.stringify(snapshot));
}

export async function saveSecret(name: string, value: string): Promise<void> {
  if (Platform.OS === 'web') {
    // Web secrets belong in server-managed HttpOnly sessions. Never persist VINs or OAuth tokens here.
    return;
  }
  await SecureStore.setItemAsync(`${SECRET_PREFIX}${name}`, value, {
    keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
  });
}

export async function clearSecret(name: string): Promise<void> {
  if (Platform.OS !== 'web') await SecureStore.deleteItemAsync(`${SECRET_PREFIX}${name}`);
}
