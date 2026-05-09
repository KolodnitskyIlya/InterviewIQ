import { ApplicationSettings, isAndroid } from "@nativescript/core";

import { clearAuthSession, getAccessToken } from "./authSession";

const API_BASE_URL_SETTING_KEY = "interviewiq.api.baseUrl";

const DEFAULT_API_BASE_URL = isAndroid
  ? "http://10.0.2.2:8000/api/v1"
  : "http://127.0.0.1:8000/api/v1";

export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(message: string, status: number, data: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

export function getApiBaseUrl(): string {
  return ApplicationSettings.getString(API_BASE_URL_SETTING_KEY, DEFAULT_API_BASE_URL);
}

export interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  auth?: boolean;
}

function formatValidationDetail(detail: unknown): string | null {
  if (typeof detail === "string") {
    return detail;
  }

  if (!Array.isArray(detail)) {
    return null;
  }

  const messages = detail
    .map((item) => {
      if (typeof item !== "object" || item === null) {
        return null;
      }

      const issue = item as { loc?: unknown; msg?: unknown };
      const field = Array.isArray(issue.loc)
        ? issue.loc.filter((part) => part !== "body").join(".")
        : "";
      const message = typeof issue.msg === "string" ? issue.msg : "";

      if (!message) {
        return null;
      }

      return field ? `${field}: ${message}` : message;
    })
    .filter((message): message is string => Boolean(message));

  return messages.length > 0 ? messages.join("\n") : null;
}

export async function request<T>(
  path: string,
  { method = "GET", body, auth = false }: RequestOptions = {},
): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
  };

  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  if (auth) {
    const token = getAccessToken();
    if (!token) {
      throw new ApiError("Authorization token is missing", 401, null);
    }
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  let payload: unknown = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    if (response.status === 401 && auth) {
      clearAuthSession();
    }

    const detail =
      typeof payload === "object" && payload !== null && "detail" in payload
        ? formatValidationDetail((payload as { detail?: unknown }).detail)
        : null;

    throw new ApiError(detail ?? `Request failed with status ${response.status}`, response.status, payload);
  }

  return payload as T;
}
