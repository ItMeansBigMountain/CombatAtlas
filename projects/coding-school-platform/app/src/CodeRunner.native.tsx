import { StyleSheet, Text, View } from 'react-native';

export function CodeRunner({ code }: { code: string }) {
  return (
    <View style={styles.box} accessibilityLabel="Native coding exercise guidance">
      <Text style={styles.title}>Try it on your coding device</Text>
      <Text style={styles.text}>Your draft is saved offline. Run it in a teacher-approved Python workspace, then return here to submit evidence and reflection.</Text>
      <Text style={styles.preview} numberOfLines={5}>{code}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { backgroundColor: '#172554', borderRadius: 16, padding: 16, gap: 8 },
  title: { color: '#fff', fontSize: 16, fontWeight: '700' },
  text: { color: '#bfdbfe', lineHeight: 20 },
  preview: { color: '#d1fae5', fontFamily: 'monospace', fontSize: 12 },
});
