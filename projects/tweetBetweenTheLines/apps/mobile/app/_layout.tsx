import { Stack } from 'expo-router'
import Head from 'expo-router/head'

export default function RootLayout() {
  return (
    <>
      <Head>
        <title>tweetBetweenTheLines</title>
        <meta name="theme-color" content="#153d36" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="BetweenLines" />
        <link rel="manifest" href="/manifest.webmanifest" />
        <link rel="apple-touch-icon" href="/icon-192.png" />
      </Head>
      <Stack screenOptions={{ headerShown: false }} />
    </>
  )
}
