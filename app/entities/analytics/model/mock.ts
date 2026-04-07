import type {
  DetailedSession,
  ReadinessSummary,
  SkillMetric,
  WeeklyProgressPoint,
} from "./types";

export const readinessSummary: ReadinessSummary = {
  label: "Overall Readiness",
  value: 78,
  trend: "+12%",
  caption: "vs last week",
};

export const weeklyProgress: WeeklyProgressPoint[] = [
  { day: "Mon", value: 38 },
  { day: "Tue", value: 46 },
  { day: "Wed", value: 52 },
  { day: "Thu", value: 58 },
  { day: "Fri", value: 56 },
  { day: "Sat", value: 62 },
];

export const skillsBreakdown: SkillMetric[] = [
  { label: "Technical", value: 78 },
  { label: "Behavioral", value: 70 },
  { label: "HR", value: 62 },
  { label: "System Design", value: 58 },
];

export const recentSessions: DetailedSession[] = [
  {
    title: "Technical Round",
    date: "Feb 25, 2026",
    meta: "10 questions | 25 min",
    score: 82,
  },
  {
    title: "Behavioral Questions",
    date: "Feb 20, 2026",
    meta: "8 questions | 20 min",
    score: 78,
  },
];
