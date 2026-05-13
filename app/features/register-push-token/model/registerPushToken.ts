import { ApplicationSettings, Device, isAndroid, isIOS } from "@nativescript/core";
import { firebase } from "@nativescript/firebase-core";
import "@nativescript/firebase-messaging";

import { interviewIqApi } from "@/shared";

const MOCK_PUSH_TOKEN_KEY = "interviewiq.mockPushToken";
let isFirebaseInitialized = false;

function platform(): string {
  if (isAndroid) {
    return "android";
  }
  if (isIOS) {
    return "ios";
  }
  return "unknown";
}

function createMockToken(): string {
  const existing = ApplicationSettings.getString(MOCK_PUSH_TOKEN_KEY);
  if (existing) {
    return existing;
  }

  const token = `mock-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  ApplicationSettings.setString(MOCK_PUSH_TOKEN_KEY, token);
  return token;
}

async function initializeFirebase(): Promise<void> {
  if (isFirebaseInitialized) {
    return;
  }

  await firebase().initializeApp();
  isFirebaseInitialized = true;
}

async function getFcmToken(): Promise<string> {
  await initializeFirebase();

  const messaging = firebase().messaging();
  await messaging.requestPermission();
  await messaging.registerDeviceForRemoteMessages();
  messaging.showNotificationsWhenInForeground = true;

  messaging.onMessage((remoteMessage) => {
    console.log("Foreground FCM message:", JSON.stringify(remoteMessage));
  });

  messaging.onToken((token) => {
    void registerToken(token, "fcm");
  });

  const token = await messaging.getToken();
  if (!token) {
    throw new Error("FCM token is empty");
  }
  return token;
}

async function registerToken(token: string, provider: "fcm" | "mock"): Promise<void> {
  await interviewIqApi.registerDeviceToken({
    token,
    platform: platform(),
    provider,
    app_version: "1.0.0",
    device_id: Device.uuid,
  });
}

export async function registerPushToken(): Promise<void> {
  try {
    const token = await getFcmToken();
    await registerToken(token, "fcm");
  } catch (error) {
    console.log("FCM token registration failed, using mock token:", error);
    await registerToken(createMockToken(), "mock");
  }
}
