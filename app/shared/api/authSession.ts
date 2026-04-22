import { ApplicationSettings } from "@nativescript/core";

import type { AuthResponse } from "./types";

const AUTH_SESSION_KEY = "interviewiq.auth.session";

export interface AuthSession {
  user: AuthResponse["user"];
  tokens: AuthResponse["tokens"];
}

export function saveAuthSession(session: AuthSession): void {
  ApplicationSettings.setString(AUTH_SESSION_KEY, JSON.stringify(session));
}

export function getAuthSession(): AuthSession | null {
  const raw = ApplicationSettings.getString(AUTH_SESSION_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as AuthSession;
  } catch {
    ApplicationSettings.remove(AUTH_SESSION_KEY);
    return null;
  }
}

export function getAccessToken(): string | null {
  return getAuthSession()?.tokens.access_token ?? null;
}

export function clearAuthSession(): void {
  ApplicationSettings.remove(AUTH_SESSION_KEY);
}
