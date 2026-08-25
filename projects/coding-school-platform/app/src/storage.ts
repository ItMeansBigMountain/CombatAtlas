import AsyncStorage from '@react-native-async-storage/async-storage';

export type Submission = {
  lessonId: string;
  code: string;
  reflection: string;
  status: 'pending' | 'approved' | 'needs-revision';
  queuedAt: string;
};

const KEY = 'algorithm-academy:demo-submissions:v1';

export async function loadSubmissions(): Promise<Submission[]> {
  const stored = await AsyncStorage.getItem(KEY);
  if (!stored) return [];
  try {
    const value: unknown = JSON.parse(stored);
    return Array.isArray(value) ? value as Submission[] : [];
  } catch {
    return [];
  }
}

export async function saveSubmissions(items: Submission[]) {
  await AsyncStorage.setItem(KEY, JSON.stringify(items));
}
