import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';

export type UploadAsset = { uri: string; name: string; mimeType?: string | null; size?: number };

export async function pickReceipt(): Promise<UploadAsset | null> {
  const result = await DocumentPicker.getDocumentAsync({ type: ['image/*', 'application/pdf'], copyToCacheDirectory: true });
  if (result.canceled) return null;
  const asset = result.assets[0];
  return { uri: asset.uri, name: asset.name, mimeType: asset.mimeType, size: asset.size };
}

export async function captureReceipt(): Promise<UploadAsset | null> {
  const permission = await ImagePicker.requestCameraPermissionsAsync();
  if (!permission.granted) return null;
  const result = await ImagePicker.launchCameraAsync({ mediaTypes: ['images'], quality: 0.8 });
  if (result.canceled) return null;
  const asset = result.assets[0];
  return { uri: asset.uri, name: asset.fileName ?? `receipt-${Date.now()}.jpg`, mimeType: asset.mimeType, size: asset.fileSize };
}
