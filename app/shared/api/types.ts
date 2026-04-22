export type ExperienceLevel = "junior" | "middle" | "senior";

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthUser {
  id: string;
  full_name: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  user: AuthUser;
  tokens: AuthTokens;
}

export interface AuthMeResponse {
  id: string;
  full_name: string;
  email: string;
  target_role: string | null;
  experience_level: ExperienceLevel | null;
  created_at: string;
}

export interface OnboardingOptionsResponse {
  roles: string[];
  experience_levels: ExperienceLevel[];
  categories: string[];
}

export interface OnboardingUpdateRequest {
  role: string;
  experience_level: ExperienceLevel;
}

export interface OnboardingStateResponse {
  role: string | null;
  experience_level: ExperienceLevel | null;
  updated_at: string;
}

export interface UserProfileResponse {
  id: string;
  full_name: string;
  email: string;
  target_role: string | null;
  experience_level: ExperienceLevel | null;
  created_at: string;
  updated_at: string;
}

export interface UpdateProfileRequest {
  full_name?: string;
  target_role?: string;
  experience_level?: ExperienceLevel;
}
