import { request } from "./client";
import type {
  AuthMeResponse,
  AuthResponse,
  AnswerAnalysisResponse,
  AudioUploadRequest,
  AudioUploadResponse,
  CreateSessionRequest,
  OnboardingOptionsResponse,
  OnboardingStateResponse,
  OnboardingUpdateRequest,
  SessionQuestionResponse,
  SessionResultsResponse,
  SessionStateResponse,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
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
  createPracticeSession(payload: CreateSessionRequest) {
    return request<SessionStateResponse>("/practice/sessions", {
      method: "POST",
      auth: true,
      body: payload,
    });
  },
  startPracticeSession(sessionId: string) {
    return request<SessionStateResponse>(`/practice/sessions/${sessionId}/start`, {
      method: "POST",
      auth: true,
    });
  },
  getPracticeSession(sessionId: string) {
    return request<SessionStateResponse>(`/practice/sessions/${sessionId}`, {
      auth: true,
    });
  },
  getCurrentQuestion(sessionId: string) {
    return request<SessionQuestionResponse>(`/practice/sessions/${sessionId}/questions/current`, {
      auth: true,
    });
  },
  nextQuestion(sessionId: string) {
    return request<SessionQuestionResponse>(`/practice/sessions/${sessionId}/questions/next`, {
      method: "POST",
      auth: true,
    });
  },
  submitAnswer(sessionId: string, payload: SubmitAnswerRequest) {
    return request<SubmitAnswerResponse>(`/practice/sessions/${sessionId}/answers`, {
      method: "POST",
      auth: true,
      body: payload,
    });
  },
  uploadAnswerAudio(sessionId: string, payload: AudioUploadRequest) {
    return request<AudioUploadResponse>(`/practice/sessions/${sessionId}/audio`, {
      method: "POST",
      auth: true,
      body: payload,
    });
  },
  getAnswerAnalysis(sessionId: string, answerId: string) {
    return request<AnswerAnalysisResponse>(
      `/practice/sessions/${sessionId}/answers/${answerId}/analysis`,
      { auth: true },
    );
  },
  finishPracticeSession(sessionId: string) {
    return request<SessionStateResponse>(`/practice/sessions/${sessionId}/finish`, {
      method: "POST",
      auth: true,
    });
  },
  getSessionResults(sessionId: string) {
    return request<SessionResultsResponse>(`/practice/sessions/${sessionId}/results`, {
      auth: true,
    });
  },
};
