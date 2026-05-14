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

export interface CreateSessionRequest {
  category: string;
  difficulty: string;
  time_limit_sec: number;
  question_count: number;
}

export interface SessionStateResponse {
  id: string;
  status: string;
  category: string;
  difficulty: string;
  time_limit_sec: number;
  question_count: number;
  current_question_index: number;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}

export interface QuestionItemResponse {
  id: string;
  category: string;
  difficulty: string;
  title: string;
  description: string;
}

export interface SessionQuestionResponse {
  session_id: string;
  current_question_index: number;
  total_questions: number;
  question: QuestionItemResponse | null;
}

export interface SubmitAnswerRequest {
  question_id: string;
  answer_text?: string | null;
  audio_url?: string | null;
  audio_id?: string | null;
}

export interface SubmitAnswerResponse {
  answer_id: string;
  session_id: string;
  question_id: string;
  status: string;
  transcript: string | null;
}

export interface AudioUploadRequest {
  question_id: string;
  file_name: string;
  content_type: string;
  audio_base64: string;
}

export interface AudioUploadResponse {
  audio_id: string;
  audio_url: string;
  content_type: string;
}

export interface AnswerAnalysisResponse {
  answer_id: string;
  overall_score: number;
  scores_by_category: Record<string, number>;
  strengths: string[];
  to_improve: string[];
  quick_tips: string[];
  ideal_answer_example: string;
  explanation?: string | null;
  provider?: string | null;
  rubric_version?: string | null;
  error_message?: string | null;
  latency_ms?: number | null;
  transcript?: string | null;
}

export interface SessionResultItem {
  answer_id: string;
  question_id: string;
  question_title: string;
  score: number;
}

export interface SessionResultsResponse {
  session_id: string;
  status: string;
  average_score: number;
  questions_answered: number;
  question_results: SessionResultItem[];
  finished_at: string | null;
}

export interface DeviceTokenRegisterRequest {
  token: string;
  platform: string;
  provider: string;
  app_version?: string | null;
  device_id?: string | null;
}

export interface DeviceTokenResponse {
  id: string;
  token: string;
  platform: string;
  provider: string;
  app_version: string | null;
  device_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReminderTestResponse {
  sent: number;
  failed: number;
  results: Array<{
    token_id: string;
    provider: string;
    success: boolean;
    message_id: string | null;
    error: string | null;
  }>;
}

export interface AnalyticsOverviewResponse {
  readiness_score: number;
  average_score: number;
  trend_percent: number;
}

export interface AnalyticsSkillItemResponse {
  name: string;
  score: number;
  change: number;
}

export interface AnalyticsSkillsResponse {
  items: AnalyticsSkillItemResponse[];
}

export interface AnalyticsWeeklyPointResponse {
  day: string;
  score: number;
}

export interface AnalyticsWeeklyProgressResponse {
  points: AnalyticsWeeklyPointResponse[];
}

export interface AnalyticsSessionItemResponse {
  session_id: string;
  category: string;
  score: number;
  completed_at: string | null;
  questions_count: number;
  duration_min: number;
}

export interface AnalyticsSessionsResponse {
  items: AnalyticsSessionItemResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface HomeDashboardResponse {
  progress_card: {
    value: number;
    trend: string;
    subtitle: string;
  };
  areas_to_improve: Array<{
    skill: string;
    score: number;
  }>;
  recent_sessions: AnalyticsSessionItemResponse[];
  resume_session: {
    session_id: string;
    question_index: number;
    total_questions: number;
  } | null;
}
