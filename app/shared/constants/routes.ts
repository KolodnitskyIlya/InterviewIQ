export const APP_ROUTES = {
  welcome: "welcome",
  howItWorks: "how-it-works",
  personalizeExperience: "personalize-experience",
  signIn: "sign-in",
  signUp: "sign-up",
  home: "home",
  practice: "practice",
  questions: "questions",
  results: "results",
  analytics: "analytics",
  profile: "profile",
  settings: "settings",
} as const;

export type AppRoute = (typeof APP_ROUTES)[keyof typeof APP_ROUTES];
