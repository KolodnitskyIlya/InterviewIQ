import { ApplicationSettings, Device, isAndroid, isIOS } from "@nativescript/core";

import { interviewIqApi } from "@/shared";

const MOCK_PUSH_TOKEN_KEY = "interviewiq.mockPushToken";

function createToken(): string {
  const existing = ApplicationSettings.getString(MOCK_PUSH_TOKEN_KEY);
  if (existing) {
    return existing;
  }

  const token = `mock-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  ApplicationSettings.setString(MOCK_PUSH_TOKEN_KEY, token);
  return token;
}

function platform(): string {
  if (isAndroid) {
    return "android";
  }
  if (isIOS) {
    return "ios";
  }
  return "unknown";
}

export async function registerMockPushToken(): Promise<void> {
  const token = createToken();
  await interviewIqApi.registerDeviceToken({
    token,
    platform: platform(),
    provider: "mock",
    app_version: "1.0.0",
    device_id: Device.uuid,
  });
}
