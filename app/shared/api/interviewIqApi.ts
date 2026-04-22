import { request } from "./client";
import type {
  AuthMeResponse,
  AuthResponse,
  OnboardingOptionsResponse,
  OnboardingStateResponse,
  OnboardingUpdateRequest,
  UserProfileResponse,
} from "./types";

export interface SignInRequest {
  email: string;
  password: string;
}

export interface SignUpRequest {
  full_name: string;
  email: string;
  password: string;
}

export const interviewIqApi = {
  signIn(payload: SignInRequest) {
    return request<AuthResponse>("/auth/sign-in", {
      method: "POST",
      body: payload,
    });
  },
  signUp(payload: SignUpRequest) {
    return request<AuthResponse>("/auth/sign-up", {
      method: "POST",
      body: payload,
    });
  },
  getAuthMe() {
    return request<AuthMeResponse>("/auth/me", {
      auth: true,
    });
  },
  getOnboardingOptions() {
    return request<OnboardingOptionsResponse>("/onboarding/options");
  },
  saveOnboarding(payload: OnboardingUpdateRequest) {
    return request<OnboardingStateResponse>("/users/me/onboarding", {
      method: "PUT",
      auth: true,
      body: payload,
    });
  },
  getProfile() {
    return request<UserProfileResponse>("/users/me/profile", {
      auth: true,
    });
  },
};
