import React, { useEffect, useMemo, useState } from 'react';
import { Image, Linking, Modal, Platform, Pressable, SafeAreaView, ScrollView, StyleSheet, Switch, Text, TextInput, View, useWindowDimensions } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { StatusBar } from 'expo-status-bar';
import { drills, getArtProfile, getDrillMedia, martialArts, searchAll } from './src/data/combatData.js';
import { getArtMedia, getDrillThemeMedia, mediaAttribution, normalizeVisualTheme, visualThemes } from './src/data/themeMedia.js';
import { defaultPreferences, developmentAdAdapter } from './src/monetization.js';

const PREFS_KEY = 'combatatlas.preferences.v1';
const THEME_PREF_KEY = 'combatatlas.visualTheme.v1';

export default function App() {
  const { width } = useWindowDimensions();
  const compact = width < 680;
  const [query, setQuery] = useState('');
  const [artId, setArtId] = useState(null);
  const [drill, setDrill] = useState(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [visualTheme, setVisualTheme] = useState(() => normalizeVisualTheme());
  const [preferences, setPreferences] = useState(defaultPreferences);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(PREFS_KEY).then((stored) => {
      if (stored) setPreferences({ ...defaultPreferences, ...JSON.parse(stored) });
    }).finally(() => setLoaded(true));
    AsyncStorage.getItem(THEME_PREF_KEY).then((stored) => setVisualTheme(normalizeVisualTheme(stored)));
  }, []);

  async function savePreferences(next) {
    setPreferences(next);
    await AsyncStorage.setItem(PREFS_KEY, JSON.stringify(next));
  }

  async function saveVisualTheme(themeId) {
    const next = normalizeVisualTheme(themeId);
    setVisualTheme(next);
    await AsyncStorage.setItem(THEME_PREF_KEY, next);
  }

  const results = useMemo(() => searchAll(query), [query]);
  const selectedArt = useMemo(() => artId ? getArtProfile(artId) : null, [artId]);
  const arts = query.trim() ? results.arts : martialArts;
  const matchingDrills = query.trim() ? results.drills.slice(0, 12) : [];

  function home() { setArtId(null); setDrill(null); setQuery(''); }
  function chooseArt(id) { setArtId(id); setDrill(null); }

  return <SafeAreaView style={styles.safe}>
    <StatusBar style="dark" />
    <ScrollView contentContainerStyle={styles.page} keyboardShouldPersistTaps="handled">
      <View style={styles.topbar}>
        <Pressable accessibilityRole="button" onPress={home}><Text style={styles.brand}>CombatAtlas</Text></Pressable>
        <View style={styles.topActions}>
          <ThemeSelector value={visualTheme} onChange={saveVisualTheme} />
          <Pressable accessibilityRole="button" onPress={() => setSettingsOpen(true)} style={styles.utility}><Text style={styles.utilityText}>Privacy & ads</Text></Pressable>
        </View>
      </View>

      {!drill && <View style={styles.hero}>
        <Text style={styles.kicker}>Find your next training session</Text>
        <Text style={[styles.title, compact && styles.titleCompact]}>Martial arts drills, kept simple.</Text>
        <TextInput accessibilityLabel="Search martial arts or drills" value={query} onChangeText={setQuery} placeholder="Search martial arts or drills" placeholderTextColor="#8b847b" style={styles.search} />
        <Text style={styles.count}>{martialArts.length} arts · {drills.length} drills · offline atlas</Text>
      </View>}

      {drill ? <DrillDetail drill={drill} visualTheme={visualTheme} onBack={() => setDrill(null)} /> : selectedArt ?
        <ArtDetail art={selectedArt} visualTheme={visualTheme} compact={compact} onBack={() => setArtId(null)} onDrill={setDrill} /> :
        <Home arts={arts} matchingDrills={matchingDrills} visualTheme={visualTheme} compact={compact} hasQuery={Boolean(query.trim())} onArt={chooseArt} onDrill={setDrill} />}

      {loaded && preferences.consent === 'accepted' && !preferences.removeAds && <View accessibilityLabel="Test advertisement" style={styles.testAd}>
        <Text style={styles.testAdText}>TEST AD · {developmentAdAdapter.bannerUnitId}</Text>
      </View>}
    </ScrollView>
    {loaded && preferences.consent === 'unset' && <Consent preferences={preferences} onSave={savePreferences} />}
    <Settings visible={settingsOpen} preferences={preferences} onClose={() => setSettingsOpen(false)} onSave={savePreferences} />
  </SafeAreaView>;
}

function ThemeSelector({ value, onChange }) {
  return <View accessibilityRole="radiogroup" accessibilityLabel="Visual theme" style={styles.themeSelector}>
    {visualThemes.map((theme) => <Pressable key={theme.id} accessibilityRole="radio" accessibilityState={{ checked: value === theme.id }} accessibilityLabel={`${theme.label}: ${theme.description}`} onPress={() => onChange(theme.id)} style={[styles.themeButton, value === theme.id && styles.themeButtonActive]}><Text style={[styles.themeText, value === theme.id && styles.themeTextActive]}>{theme.shortLabel}</Text></Pressable>)}
  </View>;
}

function Home({ arts, matchingDrills, visualTheme, compact, hasQuery, onArt, onDrill }) {
  return <View>
    {matchingDrills.length > 0 && <><SectionTitle title="Matching drills" subtitle={`${matchingDrills.length} shown`} /><CardGrid compact={compact}>{matchingDrills.map((item) => <DrillCard key={item.id} drill={item} visualTheme={visualTheme} onPress={() => onDrill(item)} />)}</CardGrid></>}
    <SectionTitle title={hasQuery ? 'Martial arts' : 'Choose a martial art'} subtitle={hasQuery ? `${arts.length} matches` : 'Tap an art to browse drills'} />
    <CardGrid compact={compact}>{arts.map((art) => <ArtCard key={art.id} art={art} visualTheme={visualTheme} onPress={() => onArt(art.id)} />)}</CardGrid>
    {hasQuery && arts.length === 0 && matchingDrills.length === 0 && <Text style={styles.empty}>No matches. Try boxing, armbar, footwork, or kick.</Text>}
  </View>;
}

function CardGrid({ children, compact }) { return <View style={styles.grid}>{React.Children.map(children, (child) => <View style={[styles.gridCell, compact && styles.gridCellCompact]}>{child}</View>)}</View>; }
function SectionTitle({ title, subtitle }) { return <View style={styles.sectionTitle}><Text style={styles.h2}>{title}</Text><Text style={styles.muted}>{subtitle}</Text></View>; }

function ArtCard({ art, visualTheme, onPress }) { const media = getArtMedia(art, visualTheme); return <Pressable accessibilityRole="button" onPress={onPress} style={styles.card}><Image accessibilityLabel={media.imageAlt} source={{ uri: media.imageUrl }} style={styles.cardImage} /><Text style={styles.cardTitle}>{art.name}</Text><Text style={styles.cardMeta}>{art.origin}</Text></Pressable>; }
function DrillCard({ drill, visualTheme, onPress }) { const art = martialArts.find((item) => drill.martialArts?.includes(item.id)) || martialArts[0]; const media = getDrillThemeMedia(drill, art, visualTheme, getDrillMedia(drill)); return <Pressable accessibilityRole="button" onPress={onPress} style={styles.card}><Image accessibilityLabel={media.imageAlt} source={{ uri: media.imageUrl }} style={styles.cardImage} /><Text numberOfLines={2} style={styles.cardTitle}>{drill.title}</Text><Text style={styles.cardMeta}>{drill.difficulty} · {drill.contactLevel}</Text></Pressable>; }

function ArtDetail({ art, visualTheme, compact, onBack, onDrill }) { const media = getArtMedia(art, visualTheme); return <View><Back label="All arts" onPress={onBack} /><View style={[styles.artHero, compact && styles.artHeroCompact]}><Image accessibilityLabel={media.imageAlt} source={{ uri: media.imageUrl }} style={[styles.artImage, compact && styles.artImageCompact]} /><View style={styles.artCopy}><Text style={styles.kicker}>{art.origin}</Text><Text style={styles.h1}>{art.name}</Text><Text style={styles.body}>{art.description}</Text><Text style={styles.attribution}>{mediaAttribution(media)}</Text></View></View><SectionTitle title="Drills" subtitle={`${art.drills.length} options`} /><CardGrid compact={compact}>{art.drills.map((item) => <DrillCard key={item.id} drill={item} visualTheme={visualTheme} onPress={() => onDrill(item)} />)}</CardGrid></View>; }
function DrillDetail({ drill, visualTheme, onBack }) { const art = martialArts.find((item) => drill.martialArts?.includes(item.id)) || martialArts[0]; const media = getDrillThemeMedia(drill, art, visualTheme, getDrillMedia(drill)); return <View><Back label="Back to drills" onPress={onBack} /><Image accessibilityLabel={media.imageAlt} source={{ uri: media.imageUrl }} style={styles.detailImage} /><Text style={styles.kicker}>{drill.difficulty} · {drill.contactLevel}</Text><Text style={styles.h1}>{drill.title}</Text><Text style={styles.body}>{drill.summary}</Text><Pressable onPress={() => Linking.openURL(media.youtubeUrl)} style={styles.primary}><Text style={styles.primaryText}>Watch a demonstration</Text></Pressable><Text style={styles.attribution}>{mediaAttribution(media)}</Text><Text style={styles.h3}>How to practice</Text>{drill.instructions.slice(0, 4).map((step, i) => <Text key={i} style={styles.list}>{i + 1}. {step}</Text>)}<Text style={styles.h3}>Keep in mind</Text>{drill.coachingCues.slice(0, 3).map((cue, i) => <Text key={i} style={styles.list}>• {cue}</Text>)}</View>; }
function Back({ label, onPress }) { return <Pressable accessibilityRole="button" onPress={onPress} style={styles.back}><Text style={styles.backText}>‹ {label}</Text></Pressable>; }

function Consent({ preferences, onSave }) { return <View style={styles.consent}><Text style={styles.consentTitle}>Your privacy, your choice</Text><Text style={styles.consentBody}>CombatAtlas stores preferences on this device. Development uses test ads only. Choose whether to allow ads; personalization stays off unless you enable it later.</Text><View style={styles.consentActions}><Pressable style={styles.secondary} onPress={() => onSave({ ...preferences, consent: 'declined', personalizedAds: false })}><Text>Use without ads</Text></Pressable><Pressable style={styles.primary} onPress={() => onSave({ ...preferences, consent: 'accepted', personalizedAds: false })}><Text style={styles.primaryText}>Allow non-personalized ads</Text></Pressable></View></View>; }

function Settings({ visible, preferences, onClose, onSave }) {
  async function restore() { await onSave({ ...preferences, removeAds: false }); if (Platform.OS === 'web') globalThis.alert?.('No verified purchase found.'); }
  return <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}><SafeAreaView style={styles.modal}><View style={styles.modalTop}><Text style={styles.h2}>Privacy & ads</Text><Pressable onPress={onClose}><Text style={styles.done}>Done</Text></Pressable></View><Text style={styles.body}>Ads are disabled until consent. Development builds use test inventory only. Interstitials are capped at 3 per session, at least 8 actions and 10 minutes apart.</Text><View style={styles.setting}><View style={styles.settingCopy}><Text style={styles.settingTitle}>Allow ads</Text><Text style={styles.muted}>Non-personalized by default</Text></View><Switch value={preferences.consent === 'accepted'} onValueChange={(value) => onSave({ ...preferences, consent: value ? 'accepted' : 'declined', personalizedAds: false })} /></View><View style={styles.setting}><View style={styles.settingCopy}><Text style={styles.settingTitle}>Personalized ads</Text><Text style={styles.muted}>Requires explicit opt-in</Text></View><Switch disabled={preferences.consent !== 'accepted'} value={preferences.personalizedAds} onValueChange={(value) => onSave({ ...preferences, personalizedAds: value })} /></View><Pressable style={styles.primary} onPress={() => onSave({ ...preferences, removeAds: true })}><Text style={styles.primaryText}>Development: simulate Remove Ads</Text></Pressable><Pressable style={styles.secondary} onPress={restore}><Text>Restore ad-free purchase</Text></Pressable><Text style={styles.finePrint}>Production purchase and restore calls pass through a receipt-verifying billing boundary. No purchase is granted from an unverified receipt.</Text></SafeAreaView></Modal>;
}

const styles = StyleSheet.create({
  safe:{flex:1,backgroundColor:'#f6f3ee'},page:{width:'100%',maxWidth:1120,alignSelf:'center',paddingHorizontal:16,paddingTop:18,paddingBottom:80},topbar:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',gap:10,marginBottom:34},brand:{fontSize:20,fontWeight:'900',letterSpacing:-.7,color:'#171717'},topActions:{flexDirection:'row',alignItems:'center',justifyContent:'flex-end',gap:8,flexWrap:'wrap',flexShrink:1},themeSelector:{flexDirection:'row',backgroundColor:'#fff',borderWidth:1,borderColor:'#ded7cc',borderRadius:999,padding:3,gap:2},themeButton:{paddingVertical:8,paddingHorizontal:10,borderRadius:999},themeButtonActive:{backgroundColor:'#171717'},themeText:{fontSize:12,fontWeight:'900',color:'#5f574d'},themeTextActive:{color:'#fff'},utility:{paddingVertical:10,paddingHorizontal:12,borderRadius:18,backgroundColor:'#fff'},utilityText:{fontWeight:'700',color:'#514d47'},hero:{maxWidth:760,width:'100%',alignSelf:'center',alignItems:'center',marginBottom:36},kicker:{color:'#8a5d2c',textTransform:'uppercase',letterSpacing:1.7,fontSize:12,fontWeight:'900',marginBottom:10},title:{fontSize:58,lineHeight:58,fontWeight:'900',letterSpacing:-3.6,textAlign:'center',color:'#111',marginBottom:24},titleCompact:{fontSize:42,lineHeight:42,letterSpacing:-2.7},search:{width:'100%',height:60,borderWidth:1,borderColor:'#ded7cc',backgroundColor:'#fff',borderRadius:30,paddingHorizontal:22,fontSize:17,color:'#111'},count:{marginTop:12,color:'#777067'},sectionTitle:{marginTop:24,marginBottom:14,flexDirection:'row',flexWrap:'wrap',gap:10,justifyContent:'space-between',alignItems:'flex-end'},h2:{fontSize:30,fontWeight:'900',letterSpacing:-1.4,color:'#111'},h1:{fontSize:40,lineHeight:42,fontWeight:'900',letterSpacing:-2,color:'#111',marginBottom:12},h3:{fontSize:19,fontWeight:'900',marginTop:26,marginBottom:10,color:'#171717'},muted:{color:'#726c64'},grid:{flexDirection:'row',flexWrap:'wrap',marginHorizontal:-7},gridCell:{width:'33.333%',padding:7},gridCellCompact:{width:'50%'},card:{backgroundColor:'#fff',borderWidth:1,borderColor:'#e2dbd0',borderRadius:22,overflow:'hidden',minHeight:225},cardImage:{width:'100%',height:140,backgroundColor:'#e9e1d6'},cardTitle:{fontSize:16,fontWeight:'900',letterSpacing:-.45,color:'#171717',paddingHorizontal:14,paddingTop:12},cardMeta:{fontSize:12,color:'#7f766b',textTransform:'capitalize',paddingHorizontal:14,paddingTop:4,paddingBottom:14},artHero:{flexDirection:'row',backgroundColor:'#fff',borderWidth:1,borderColor:'#e2dbd0',borderRadius:28,padding:16,alignItems:'center'},artHeroCompact:{flexDirection:'column',alignItems:'stretch'},artImage:{width:'48%',height:340,borderRadius:20,backgroundColor:'#e9e1d6'},artImageCompact:{width:'100%',height:230},artCopy:{flex:1,padding:24},body:{fontSize:17,lineHeight:27,color:'#625f58'},attribution:{fontSize:12,lineHeight:18,color:'#81776a',marginTop:10},detailImage:{width:'100%',height:300,borderRadius:26,backgroundColor:'#e9e1d6',marginBottom:24},list:{fontSize:16,lineHeight:25,color:'#625f58',marginBottom:8},back:{alignSelf:'flex-start',paddingVertical:10,marginBottom:12},backText:{fontWeight:'800',color:'#56524b'},primary:{backgroundColor:'#171717',borderRadius:18,paddingVertical:15,paddingHorizontal:18,alignItems:'center',marginTop:16},primaryText:{color:'#fff',fontWeight:'900'},secondary:{backgroundColor:'#fff',borderWidth:1,borderColor:'#d8d0c5',borderRadius:18,paddingVertical:14,paddingHorizontal:16,alignItems:'center',marginTop:10},empty:{padding:24,color:'#726c64'},testAd:{marginTop:36,minHeight:54,borderWidth:1,borderStyle:'dashed',borderColor:'#9b9489',alignItems:'center',justifyContent:'center',borderRadius:14},testAdText:{fontSize:11,fontWeight:'800',color:'#777067',letterSpacing:1},consent:{position:'absolute',left:12,right:12,bottom:12,backgroundColor:'#fff',borderRadius:24,padding:18,borderWidth:1,borderColor:'#ddd4c8',shadowColor:'#000',shadowOpacity:.18,shadowRadius:20,elevation:10},consentTitle:{fontSize:20,fontWeight:'900',color:'#111'},consentBody:{color:'#625f58',lineHeight:21,marginTop:7},consentActions:{marginTop:4},modal:{flex:1,backgroundColor:'#f6f3ee',padding:20},modalTop:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:20},done:{fontWeight:'900',color:'#8a5d2c',fontSize:17},setting:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',backgroundColor:'#fff',borderRadius:18,padding:16,marginTop:12},settingCopy:{flex:1,paddingRight:12},settingTitle:{fontSize:16,fontWeight:'800',color:'#171717'},finePrint:{fontSize:12,lineHeight:18,color:'#777067',marginTop:18}
});
