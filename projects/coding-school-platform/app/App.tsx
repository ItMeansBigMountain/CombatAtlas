import { StatusBar } from 'expo-status-bar';
import { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator, Alert, Platform, Pressable, SafeAreaView, ScrollView,
  StyleSheet, Text, TextInput, View,
} from 'react-native';
import { CodeRunner } from './src/CodeRunner';
import { lessons, safeHints } from './src/curriculum';
import { loadSubmissions, saveSubmissions, Submission } from './src/storage';

type Role = 'learner' | 'teacher' | 'admin';

export default function App() {
  const [role, setRole] = useState<Role>('learner');
  const [selectedId, setSelectedId] = useState(lessons[0].id);
  const [code, setCode] = useState(lessons[0].starterCode);
  const [reflection, setReflection] = useState('');
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [hintIndex, setHintIndex] = useState(-1);
  const selected = useMemo(() => lessons.find(item => item.id === selectedId) ?? lessons[0], [selectedId]);

  useEffect(() => {
    loadSubmissions().then(setSubmissions).finally(() => setLoading(false));
  }, []);

  const selectLesson = (lessonId: string) => {
    const lesson = lessons.find(item => item.id === lessonId) ?? lessons[0];
    setSelectedId(lesson.id);
    setCode(lesson.starterCode);
    setReflection('');
    setHintIndex(-1);
  };

  const submit = async () => {
    if (!reflection.trim()) {
      Alert.alert('Reflection needed', 'Tell your teacher what you tried or learned.');
      return;
    }
    const item: Submission = { lessonId: selected.id, code, reflection: reflection.trim(), status: 'pending', queuedAt: new Date().toISOString() };
    const next = [item, ...submissions.filter(previous => previous.lessonId !== selected.id)];
    setSubmissions(next);
    await saveSubmissions(next);
    Alert.alert('Saved offline', 'Your evidence is queued for teacher review.');
  };

  const review = async (lessonId: string, status: Submission['status']) => {
    const next = submissions.map(item => item.lessonId === lessonId ? { ...item, status } : item);
    setSubmissions(next);
    await saveSubmissions(next);
  };

  if (loading) return <SafeAreaView style={styles.loading}><ActivityIndicator color="#2563eb" /><Text>Opening your offline classroom…</Text></SafeAreaView>;

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="dark" />
      <View style={styles.header}>
        <View><Text style={styles.eyebrow}>ALGORITHM ACADEMY</Text><Text style={styles.heading}>Learn by building</Text></View>
        <View style={styles.roleSwitch}>
          {(['learner', 'teacher', 'admin'] as Role[]).map(item => (
            <Pressable key={item} accessibilityRole="button" accessibilityLabel={`Switch to ${item} demo view`} accessibilityState={{ selected: role === item }} onPress={() => setRole(item)} style={[styles.roleButton, role === item && styles.roleButtonActive]}>
              <Text style={[styles.roleText, role === item && styles.roleTextActive]}>{item === 'learner' ? 'Learner' : item === 'teacher' ? 'Teacher' : 'Admin'}</Text>
            </Pressable>
          ))}
        </View>
      </View>
      {role === 'learner' ? (
        <ScrollView contentContainerStyle={styles.page} keyboardShouldPersistTaps="handled">
          <View style={styles.banner}><Text style={styles.bannerTitle}>Keep your streak alive</Text><Text style={styles.bannerText}>{submissions.length} lesson{submissions.length === 1 ? '' : 's'} completed · {submissions.filter(item => item.status === 'approved').length} teacher-approved</Text></View>
          <Text style={styles.section}>Modules</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.lessonRow}>
            {lessons.map((lesson, index) => (
              <Pressable key={lesson.id} accessibilityRole="button" accessibilityLabel={`Open ${lesson.title} lesson`} onPress={() => selectLesson(lesson.id)} style={[styles.lessonCard, selected.id === lesson.id && styles.lessonCardActive]}>
                <Text style={styles.cardStep}>{index + 1}</Text><Text style={styles.cardTitle}>{lesson.title}</Text><Text style={styles.cardMeta}>{lesson.module}</Text>
              </Pressable>
            ))}
          </ScrollView>
          <View style={styles.panel}>
            <Text style={styles.module}>{selected.module}</Text><Text style={styles.title}>{selected.title}</Text><Text style={styles.body}>{selected.description}</Text>
            {selected.rubric.map(item => <Text key={item} style={styles.check}>□ {item}</Text>)}
            <Text style={styles.label}>Your code draft</Text>
            <TextInput accessibilityLabel="Code draft" multiline autoCapitalize="none" autoCorrect={false} value={code} onChangeText={setCode} style={styles.editor} />
            <CodeRunner code={code} />
            <Pressable style={styles.hintButton} onPress={() => setHintIndex((hintIndex + 1) % safeHints.length)}><Text style={styles.hintButtonText}>Ask the safe AI coach for a hint</Text></Pressable>
            {hintIndex >= 0 && <Text style={styles.hint}>Hint only — no answer: {safeHints[hintIndex]}</Text>}
            <Text style={styles.label}>Reflection</Text>
            <TextInput accessibilityLabel="Lesson reflection" multiline value={reflection} onChangeText={setReflection} placeholder="What did you try? What will you change next?" placeholderTextColor="#64748b" style={styles.reflection} />
            <Pressable style={styles.primary} onPress={submit}><Text style={styles.primaryText}>Save evidence for teacher review</Text></Pressable>
          </View>
          <Text style={styles.offline}>Offline-ready reading and drafts · Demo learner data only · No private profile fields</Text>
        </ScrollView>
      ) : role === 'teacher' ? (
        <ScrollView contentContainerStyle={styles.page}>
          <View style={styles.banner}><Text style={styles.bannerTitle}>Teacher review queue</Text><Text style={styles.bannerText}>{submissions.filter(item => item.status === 'pending').length} pending · Review evidence before mastery or badges are awarded.</Text></View>
          {submissions.length === 0 ? <View style={styles.empty}><Text style={styles.title}>Nothing to review yet</Text><Text style={styles.body}>Switch to Learner and submit a reflection to test the full offline loop.</Text></View> : submissions.map(item => {
            const lesson = lessons.find(entry => entry.id === item.lessonId);
            return <View key={item.lessonId} style={styles.reviewCard}>
              <Text style={styles.module}>{lesson?.module}</Text><Text style={styles.title}>{lesson?.title}</Text>
              <Text style={styles.body}>Learner reflection: {item.reflection}</Text><Text style={styles.status}>Status: {item.status}</Text>
              <View style={styles.actions}><Pressable style={styles.approve} onPress={() => review(item.lessonId, 'approved')}><Text style={styles.actionText}>Approve mastery</Text></Pressable><Pressable style={styles.revise} onPress={() => review(item.lessonId, 'needs-revision')}><Text style={styles.reviseText}>Request revision</Text></Pressable></View>
            </View>;
          })}
        </ScrollView>
      ) : (
        <ScrollView contentContainerStyle={styles.page}>
          <View style={styles.banner}><Text style={styles.bannerTitle}>Admin release console</Text><Text style={styles.bannerText}>Demo-only operational view for safe rollout readiness across learner and teacher workflows.</Text></View>
          <View style={styles.adminGrid}>
            <View style={styles.metricCard}><Text style={styles.metricNumber}>0</Text><Text style={styles.metricLabel}>real student records</Text></View>
            <View style={styles.metricCard}><Text style={styles.metricNumber}>3</Text><Text style={styles.metricLabel}>demo roles available</Text></View>
            <View style={styles.metricCard}><Text style={styles.metricNumber}>{submissions.filter(item => item.status === 'pending').length}</Text><Text style={styles.metricLabel}>missing check-ins</Text></View>
            <View style={styles.metricCard}><Text style={styles.metricNumber}>{lessons.length}</Text><Text style={styles.metricLabel}>curriculum missions</Text></View>
          </View>
          <View style={styles.panel}>
            <Text style={styles.title}>Operational gates</Text>
            <Text style={styles.check}>☑ Teacher-reviewed mastery is separate from completion.</Text>
            <Text style={styles.check}>☑ Safe AI stays hint-only and does not generate answers.</Text>
            <Text style={styles.check}>☑ Parent-safe progress export avoids private profile fields.</Text>
            <Text style={styles.check}>☑ Signed iOS and Android releases require owner Apple/Google credentials.</Text>
          </View>
        </ScrollView>
      )}
      {Platform.OS !== 'web' && <Text style={styles.nativeNote}>Native exercise mode protects drafts and keeps execution teacher-approved.</Text>}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#f8fafc' }, loading: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12 },
  header: { paddingHorizontal: 20, paddingVertical: 14, backgroundColor: '#fff', borderBottomWidth: 1, borderColor: '#e2e8f0', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 12 },
  eyebrow: { color: '#2563eb', fontSize: 11, fontWeight: '800', letterSpacing: 1.2 }, heading: { color: '#0f172a', fontSize: 20, fontWeight: '800' },
  roleSwitch: { flexDirection: 'row', backgroundColor: '#e2e8f0', borderRadius: 12, padding: 3, flexWrap: 'wrap' }, roleButton: { paddingHorizontal: 10, paddingVertical: 8, borderRadius: 9 }, roleButtonActive: { backgroundColor: '#fff' }, roleText: { color: '#475569', fontWeight: '700' }, roleTextActive: { color: '#1d4ed8' },
  page: { width: '100%', maxWidth: 980, alignSelf: 'center', padding: 20, gap: 16 }, banner: { backgroundColor: '#1d4ed8', borderRadius: 20, padding: 20 }, bannerTitle: { color: '#fff', fontSize: 22, fontWeight: '800' }, bannerText: { color: '#dbeafe', marginTop: 6, lineHeight: 20 }, section: { color: '#0f172a', fontSize: 18, fontWeight: '800' }, lessonRow: { gap: 10, paddingRight: 20 },
  lessonCard: { width: 170, minHeight: 120, padding: 14, borderRadius: 16, backgroundColor: '#fff', borderWidth: 1, borderColor: '#e2e8f0' }, lessonCardActive: { borderColor: '#2563eb', borderWidth: 2 }, cardStep: { color: '#2563eb', fontWeight: '800' }, cardTitle: { color: '#0f172a', fontSize: 16, fontWeight: '800', marginTop: 8 }, cardMeta: { color: '#64748b', marginTop: 5 },
  panel: { backgroundColor: '#fff', borderRadius: 20, padding: 20, gap: 12, borderWidth: 1, borderColor: '#e2e8f0' }, module: { color: '#2563eb', fontWeight: '800', fontSize: 12, textTransform: 'uppercase' }, title: { color: '#0f172a', fontSize: 20, fontWeight: '800' }, body: { color: '#475569', lineHeight: 21 }, check: { color: '#334155' }, label: { color: '#0f172a', fontWeight: '800', marginTop: 6 }, editor: { minHeight: 180, backgroundColor: '#0f172a', color: '#d1fae5', padding: 16, borderRadius: 16, fontFamily: 'monospace', textAlignVertical: 'top' }, reflection: { minHeight: 100, borderWidth: 1, borderColor: '#cbd5e1', borderRadius: 14, padding: 14, color: '#0f172a', textAlignVertical: 'top' },
  hintButton: { alignSelf: 'flex-start', padding: 10 }, hintButtonText: { color: '#1d4ed8', fontWeight: '800' }, hint: { backgroundColor: '#eff6ff', color: '#1e40af', padding: 12, borderRadius: 12, lineHeight: 20 }, primary: { backgroundColor: '#2563eb', borderRadius: 14, padding: 15, alignItems: 'center' }, primaryText: { color: '#fff', fontWeight: '800' }, offline: { color: '#64748b', textAlign: 'center', fontSize: 12 },
  empty: { backgroundColor: '#fff', padding: 24, borderRadius: 18, gap: 8 }, reviewCard: { backgroundColor: '#fff', borderRadius: 18, padding: 18, gap: 10, borderWidth: 1, borderColor: '#e2e8f0' }, status: { color: '#475569', fontWeight: '700' }, actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 }, approve: { backgroundColor: '#15803d', borderRadius: 12, padding: 12 }, revise: { borderColor: '#dc2626', borderWidth: 1, borderRadius: 12, padding: 12 }, actionText: { color: '#fff', fontWeight: '800' }, reviseText: { color: '#b91c1c', fontWeight: '800' }, adminGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 }, metricCard: { flexGrow: 1, minWidth: 150, backgroundColor: '#fff', borderRadius: 18, padding: 18, borderWidth: 1, borderColor: '#e2e8f0' }, metricNumber: { color: '#1d4ed8', fontSize: 28, fontWeight: '900' }, metricLabel: { color: '#475569', fontWeight: '700', marginTop: 4 }, nativeNote: { backgroundColor: '#e0f2fe', color: '#075985', padding: 8, textAlign: 'center', fontSize: 11 },
});
