import { useEffect, useMemo, useState } from 'react';
import { Linking, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, useWindowDimensions, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { enableReminders, scheduleReminder } from '@/adapters/notifications';
import { loadGarage, saveGarage, saveSecret } from '@/adapters/storage';
import { captureReceipt, pickReceipt } from '@/adapters/upload';
import { starterGarage, type GarageSnapshot, type MaintenanceItem, type ManualTab, type Vehicle } from '@/domain/models';

const tabs: ManualTab[] = ['Due now', 'Upcoming', 'History', 'Recalls', 'Sources'];
const colors = { ink: '#15211c', muted: '#5d6b64', paper: '#f5f2e9', card: '#fffdf7', green: '#285f46', orange: '#c65d2e', line: '#d9d5c9', blue: '#315f7d' };

function Button({ label, onPress, secondary = false }: { label: string; onPress: () => void; secondary?: boolean }) {
  return <Pressable accessibilityRole="button" onPress={onPress} style={({ pressed }) => [styles.button, secondary && styles.buttonSecondary, pressed && styles.pressed]}><Text style={[styles.buttonText, secondary && styles.buttonTextSecondary]}>{label}</Text></Pressable>;
}

function Metric({ value, label, warning }: { value: number; label: string; warning?: boolean }) {
  return <View style={styles.metric}><Text style={[styles.metricValue, warning && { color: colors.orange }]}>{value}</Text><Text style={styles.metricLabel}>{label}</Text></View>;
}

function ItemCard({ item }: { item: MaintenanceItem }) {
  return <View style={styles.itemCard} accessibilityLabel={`${item.title}, ${item.due}`}>
    <View style={styles.row}><Text style={styles.itemTitle}>{item.title}</Text><Text style={[styles.pill, item.state === 'due' && styles.pillDue]}>{item.state}</Text></View>
    <Text style={styles.due}>{item.due}</Text><Text style={styles.note}>{item.note}</Text>
    <Text style={styles.source}>{item.source} · {item.confidence} confidence</Text>
  </View>;
}

export default function GarageScreen() {
  const { width } = useWindowDimensions();
  const wide = width >= 820;
  const [garage, setGarage] = useState<GarageSnapshot>(starterGarage);
  const [selected, setSelected] = useState<string | null>(starterGarage.vehicles[0].id);
  const [tab, setTab] = useState<ManualTab>('Due now');
  const [online, setOnline] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [identity, setIdentity] = useState('');
  const [vin, setVin] = useState('');
  const [mileage, setMileage] = useState('');
  const [status, setStatus] = useState('Saved garage is available offline.');

  useEffect(() => { loadGarage(starterGarage).then(setGarage); }, []);
  const vehicle = garage.vehicles.find((candidate) => candidate.id === selected) ?? garage.vehicles[0];
  const dueCount = garage.vehicles.flatMap((v) => v.items).filter((i) => i.state === 'due').length;
  const upcomingCount = garage.vehicles.flatMap((v) => v.items).filter((i) => i.state === 'upcoming').length;
  const visibleItems = useMemo(() => {
    if (!vehicle) return [];
    if (tab === 'Due now') return vehicle.items.filter((i) => i.state === 'due' || i.state === 'unknown');
    if (tab === 'Upcoming') return vehicle.items.filter((i) => i.state === 'upcoming');
    if (tab === 'History') return vehicle.items.filter((i) => i.state === 'completed');
    return [];
  }, [vehicle, tab]);

  async function persist(next: GarageSnapshot) { setGarage(next); await saveGarage(next); }
  async function addVehicle() {
    if (!identity.trim() || !Number.isFinite(Number(mileage)) || Number(mileage) < 0) { setStatus('Enter a vehicle and a non-negative mileage.'); return; }
    const nextVehicle: Vehicle = { id: `vehicle-${Date.now()}`, nickname: 'My vehicle', identity: identity.trim(), vinLast4: vin.slice(-4) || undefined, mileage: Number(mileage), severeUse: false, items: [] };
    if (vin) await saveSecret(`vin.${nextVehicle.id}`, vin.toUpperCase());
    await persist({ vehicles: [...garage.vehicles, nextVehicle], updatedAt: new Date().toISOString(), pendingSync: online ? 0 : garage.pendingSync + 1 });
    setSelected(nextVehicle.id); setShowAdd(false); setIdentity(''); setVin(''); setMileage(''); setStatus('Vehicle added. Exact trim and equipment still need owner confirmation.');
  }
  async function updateMileage() {
    if (!vehicle) return;
    const next = vehicle.mileage + 500;
    await persist({ ...garage, updatedAt: new Date().toISOString(), pendingSync: online ? 0 : garage.pendingSync + 1, vehicles: garage.vehicles.map((v) => v.id === vehicle.id ? { ...v, mileage: next } : v) });
    setStatus(`Mileage updated to ${next.toLocaleString()} mi${online ? '.' : ' and queued for sync.'}`);
  }
  async function addReceipt(camera: boolean) {
    const asset = camera ? await captureReceipt() : await pickReceipt();
    setStatus(asset ? `${asset.name} selected. Upload is queued until the authenticated API is configured.` : 'No receipt selected or permission was declined.');
  }
  async function reminders() {
    const permission = await enableReminders();
    if (permission === 'granted') await scheduleReminder(vehicle?.identity ?? 'Maintenance');
    setStatus(permission === 'granted' ? 'Reminder scheduled for a one-minute device smoke test.' : permission === 'web' ? 'Web reminders require a server push subscription; in-app reminders remain available.' : 'Notifications remain off. You can enable them in system settings.');
  }

  return <View style={styles.page}><SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.scroll}>
    <View style={styles.header}><View><Text style={styles.eyebrow}>BURNOUTBOYZ</Text><Text style={styles.heading}>Your garage, explained.</Text><Text style={styles.subheading}>Evidence-backed maintenance without fear or upsells.</Text></View><View style={[styles.connection, !online && styles.offline]}><Text style={styles.connectionText}>{online ? '● Online' : '● Offline cache'}</Text></View></View>
    <View style={styles.metrics}><Metric value={garage.vehicles.length} label="vehicles"/><Metric value={dueCount} label="review now" warning/><Metric value={upcomingCount} label="upcoming"/></View>
    <View style={[styles.main, wide && styles.mainWide]}>
      <View style={[styles.sidebar, wide && styles.sidebarWide]}><View style={styles.sectionHeader}><Text style={styles.sectionTitle}>Garage</Text><Button label="+ Add" onPress={() => setShowAdd(!showAdd)} secondary/></View>
        {showAdd && <View style={styles.form}><Text style={styles.formTitle}>Add by VIN or manually</Text><TextInput accessibilityLabel="Year make model and trim" placeholder="2019 Honda Civic EX" value={identity} onChangeText={setIdentity} style={styles.input}/><TextInput accessibilityLabel="VIN optional" placeholder="VIN (optional, stored securely on device)" autoCapitalize="characters" value={vin} onChangeText={setVin} style={styles.input}/><TextInput accessibilityLabel="Current mileage" placeholder="Current mileage" keyboardType="numeric" value={mileage} onChangeText={setMileage} style={styles.input}/><Text style={styles.legal}>Decoded VIN data identifies possibilities, not proof of installed equipment.</Text><Button label="Save vehicle" onPress={addVehicle}/></View>}
        {garage.vehicles.map((v) => <Pressable key={v.id} onPress={() => setSelected(v.id)} style={[styles.vehicleCard, selected === v.id && styles.vehicleSelected]} accessibilityRole="button"><Text style={styles.vehicleNickname}>{v.nickname}</Text><Text style={styles.vehicleIdentity}>{v.identity}</Text><Text style={styles.vehicleMeta}>{v.mileage.toLocaleString()} mi{v.vinLast4 ? ` · VIN •${v.vinLast4}` : ''}</Text></Pressable>)}
      </View>
      {vehicle && <View style={styles.manual}><View style={styles.manualTop}><View><Text style={styles.eyebrow}>DIGITAL OWNER MANUAL</Text><Text style={styles.manualTitle}>{vehicle.identity}</Text><Text style={styles.vehicleMeta}>{vehicle.mileage.toLocaleString()} miles · {vehicle.severeUse ? 'Severe-use schedule' : 'Standard schedule'}</Text></View><Button label="+500 mi" onPress={updateMileage} secondary/></View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.tabs}>{tabs.map((name) => <Pressable key={name} onPress={() => setTab(name)} style={[styles.tab, tab === name && styles.tabActive]}><Text style={[styles.tabText, tab === name && styles.tabTextActive]}>{name}</Text></Pressable>)}</ScrollView>
        {(tab === 'Due now' || tab === 'Upcoming' || tab === 'History') && <View style={styles.list}>{visibleItems.length ? visibleItems.map((item) => <ItemCard item={item} key={item.id}/>) : <View style={styles.empty}><Text style={styles.emptyTitle}>Nothing to show yet</Text><Text style={styles.note}>Add mileage or owner-confirmed records to sharpen the timeline.</Text></View>}</View>}
        {tab === 'Recalls' && <View style={styles.itemCard}><Text style={styles.itemTitle}>No model-level campaigns in the cached demo</Text><Text style={styles.note}>Model-level results are not VIN-specific proof. Confirm open status with NHTSA or the manufacturer.</Text><Button label="Open NHTSA VIN lookup" onPress={() => Linking.openURL('https://www.nhtsa.gov/recalls')} secondary/></View>}
        {tab === 'Sources' && <View style={styles.itemCard}><Text style={styles.itemTitle}>Source & confidence drill-down</Text><Text style={styles.note}>Every interval must identify its provider, version, assumptions, license class, and confidence. Demo entries are not vehicle advice.</Text>{vehicle.items.map((item) => <Text key={item.id} style={styles.source}>• {item.title}: {item.source} ({item.confidence})</Text>)}</View>}
        <View style={styles.actions}><Button label={Platform.OS === 'web' ? 'Choose receipt' : 'Receipt photo'} onPress={() => addReceipt(Platform.OS !== 'web')}/><Button label="Choose PDF" onPress={() => addReceipt(false)} secondary/><Button label="Enable reminder" onPress={reminders} secondary/></View>
        <View style={styles.consent}><Text style={styles.formTitle}>Connected car (optional)</Text><Text style={styles.note}>Manual mileage always works. Connecting a provider uses OAuth PKCE through the burnoutboyz://oauth/callback deep link and requests only odometer, oil-life, and DTC signals. Consent can be revoked and tokens cleared.</Text><Button label="Review consent" onPress={() => setStatus('No provider is configured. No data or consent was sent.')} secondary/></View>
      </View>}
    </View>
    <Pressable onPress={() => setOnline(!online)} accessibilityRole="button" style={styles.status}><Text accessibilityLiveRegion="polite" style={styles.statusText}>{status} · Tap to simulate {online ? 'offline' : 'online'}.</Text></Pressable>
    <Text style={styles.footer}>Planning guidance only — not diagnosis, repair proof, or a substitute for the exact owner manual and a qualified technician.</Text>
  </ScrollView></SafeAreaView></View>;
}

const styles = StyleSheet.create({ page:{flex:1,backgroundColor:colors.paper},safe:{flex:1},scroll:{width:'100%',maxWidth:1180,alignSelf:'center',padding:20,gap:18},header:{flexDirection:'row',justifyContent:'space-between',alignItems:'flex-start',gap:16},eyebrow:{fontSize:12,fontWeight:'800',letterSpacing:1.8,color:colors.green},heading:{fontSize:34,fontWeight:'900',color:colors.ink,letterSpacing:-1},subheading:{fontSize:16,color:colors.muted,marginTop:4},connection:{backgroundColor:'#dceadf',paddingHorizontal:12,paddingVertical:8,borderRadius:99},offline:{backgroundColor:'#f7d9c9'},connectionText:{fontWeight:'700',color:colors.ink},metrics:{flexDirection:'row',backgroundColor:colors.card,borderRadius:18,borderWidth:1,borderColor:colors.line},metric:{flex:1,padding:16,alignItems:'center'},metricValue:{fontSize:25,fontWeight:'900',color:colors.ink},metricLabel:{fontSize:12,color:colors.muted,textTransform:'uppercase'},main:{gap:16},mainWide:{flexDirection:'row',alignItems:'flex-start'},sidebar:{gap:10},sidebarWide:{width:300},sectionHeader:{flexDirection:'row',justifyContent:'space-between',alignItems:'center'},sectionTitle:{fontSize:20,fontWeight:'900',color:colors.ink},form:{backgroundColor:colors.card,borderWidth:1,borderColor:colors.line,borderRadius:16,padding:14,gap:10},formTitle:{fontWeight:'800',fontSize:16,color:colors.ink},input:{minHeight:48,borderWidth:1,borderColor:colors.line,borderRadius:10,paddingHorizontal:12,backgroundColor:'white',color:colors.ink},legal:{fontSize:12,color:colors.muted,lineHeight:17},vehicleCard:{minHeight:90,backgroundColor:colors.card,borderWidth:1,borderColor:colors.line,borderRadius:15,padding:15},vehicleSelected:{borderColor:colors.green,borderWidth:2},vehicleNickname:{fontWeight:'800',fontSize:13,color:colors.green},vehicleIdentity:{fontWeight:'900',fontSize:17,color:colors.ink,marginTop:3},vehicleMeta:{color:colors.muted,marginTop:4},manual:{flex:1,minWidth:0,backgroundColor:colors.card,borderRadius:20,borderWidth:1,borderColor:colors.line,padding:18,gap:14},manualTop:{flexDirection:'row',justifyContent:'space-between',alignItems:'flex-start',gap:12},manualTitle:{fontSize:25,fontWeight:'900',color:colors.ink},tabs:{gap:6,borderBottomWidth:1,borderBottomColor:colors.line},tab:{minHeight:44,justifyContent:'center',paddingHorizontal:12},tabActive:{borderBottomWidth:3,borderBottomColor:colors.orange},tabText:{fontWeight:'700',color:colors.muted},tabTextActive:{color:colors.ink},list:{gap:10},itemCard:{backgroundColor:'#faf8f1',borderWidth:1,borderColor:colors.line,borderRadius:14,padding:15,gap:7},row:{flexDirection:'row',justifyContent:'space-between',gap:12},itemTitle:{fontSize:17,fontWeight:'900',color:colors.ink,flex:1},pill:{fontSize:11,fontWeight:'800',textTransform:'uppercase',color:colors.green,backgroundColor:'#dceadf',paddingHorizontal:8,paddingVertical:4,borderRadius:99,overflow:'hidden'},pillDue:{color:'#7c3217',backgroundColor:'#f7d9c9'},due:{fontSize:15,fontWeight:'800',color:colors.orange},note:{fontSize:14,color:colors.muted,lineHeight:20},source:{fontSize:12,color:colors.blue,lineHeight:18},empty:{padding:26,alignItems:'center',gap:4},emptyTitle:{fontSize:17,fontWeight:'800',color:colors.ink},actions:{flexDirection:'row',flexWrap:'wrap',gap:8},button:{minHeight:44,justifyContent:'center',backgroundColor:colors.green,paddingHorizontal:15,borderRadius:10},buttonSecondary:{backgroundColor:'transparent',borderWidth:1,borderColor:colors.green},buttonText:{fontWeight:'800',color:'white',textAlign:'center'},buttonTextSecondary:{color:colors.green},pressed:{opacity:.72},consent:{borderTopWidth:1,borderTopColor:colors.line,paddingTop:14,gap:8},status:{minHeight:44,justifyContent:'center',backgroundColor:'#e4e8e5',borderRadius:10,paddingHorizontal:14},statusText:{color:colors.ink,fontWeight:'600'},footer:{fontSize:12,color:colors.muted,textAlign:'center',paddingBottom:18,lineHeight:18} });