import AsyncStorage from '@react-native-async-storage/async-storage'
import * as SecureStore from 'expo-secure-store'
import { Platform } from 'react-native'
import type { JournalEntry, OfflineMutation } from '../../../frontend/journal-app/src/journalDomain'

const entriesKey = 'journal-ai.entries.v1'
const queueKey = 'journal-ai.offline-queue.v1'
const sessionKey = 'journal-ai.session.v1'

export async function loadEntries(): Promise<JournalEntry[]> {
  return JSON.parse((await AsyncStorage.getItem(entriesKey)) ?? '[]') as JournalEntry[]
}
export async function saveEntries(entries: JournalEntry[]) { await AsyncStorage.setItem(entriesKey, JSON.stringify(entries)) }
export async function loadQueue(): Promise<OfflineMutation[]> { return JSON.parse((await AsyncStorage.getItem(queueKey)) ?? '[]') as OfflineMutation[] }
export async function saveQueue(queue: OfflineMutation[]) { await AsyncStorage.setItem(queueKey, JSON.stringify(queue)) }
export async function saveSession(token: string) {
  if (Platform.OS === 'web') await AsyncStorage.setItem(sessionKey, token)
  else await SecureStore.setItemAsync(sessionKey, token, { requireAuthentication: false })
}
export async function clearAllPrivateData() {
  await AsyncStorage.multiRemove([entriesKey, queueKey, sessionKey])
  if (Platform.OS !== 'web') await SecureStore.deleteItemAsync(sessionKey)
}
