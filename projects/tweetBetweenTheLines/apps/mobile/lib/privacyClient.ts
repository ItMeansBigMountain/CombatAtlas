import * as AuthSession from 'expo-auth-session'
import * as DocumentPicker from 'expo-document-picker'
import * as SecureStore from 'expo-secure-store'
import * as WebBrowser from 'expo-web-browser'
import { Platform } from 'react-native'

WebBrowser.maybeCompleteAuthSession()

export type ClientPlatform = 'web' | 'ios' | 'android'
export type SourceStatus = 'available' | 'connected' | 'importing' | 'revoked'
export type JobStatus = 'queued' | 'uploading' | 'analyzing' | 'completed' | 'failed'

export type SourceConnection = {
  id: string
  name: string
  coverage: string
  status: SourceStatus
  method: 'oauth' | 'archive'
}

export type ImportJob = {
  id: string
  fileName: string
  progress: number
  status: JobStatus
  message: string
}

export type PrivacyClient = {
  platform: ClientPlatform
  oauthRedirectUri: string
  storeSession(session: string): Promise<void>
  clearSession(): Promise<void>
  chooseArchive(): Promise<{ name: string; uri: string; size: number | null } | null>
}

const SESSION_KEY = 'tweet-between-the-lines.session'
let browserSession: string | null = null

function runtimePlatform(): ClientPlatform {
  if (Platform.OS === 'ios' || Platform.OS === 'android') return Platform.OS
  return 'web'
}

export function createPrivacyClient(): PrivacyClient {
  const platform = runtimePlatform()
  return {
    platform,
    oauthRedirectUri: AuthSession.makeRedirectUri({ scheme: 'tweetbetweenthelines', path: 'oauth/callback' }),
    async storeSession(session) {
      if (platform === 'web') {
        // Web access tokens must remain in server-set HttpOnly cookies. This only
        // keeps a non-secret, in-memory session hint for the current tab.
        browserSession = session
        return
      }
      await SecureStore.setItemAsync(SESSION_KEY, session, {
        keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
      })
    },
    async clearSession() {
      browserSession = null
      if (platform !== 'web') await SecureStore.deleteItemAsync(SESSION_KEY)
    },
    async chooseArchive() {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/zip', 'application/json'],
        copyToCacheDirectory: false,
        multiple: false,
      })
      if (result.canceled) return null
      const file = result.assets[0]
      return { name: file.name, uri: file.uri, size: file.size ?? null }
    },
  }
}

export function validateArchiveSelection(file: { name: string; size: number | null }): string | null {
  if (!/\.(zip|json)$/i.test(file.name)) return 'Choose an official .zip or .json archive.'
  if (file.size !== null && file.size > 250_000_000) return 'Archive exceeds the 250 MB upload limit.'
  return null
}
