export interface ImprovementMetric {
  label: string;
  value: number;
}

export interface SessionScore {
  title: string;
  date: string;
  score: number;
}

export interface ReadinessSummary {
  label: string;
  value: number;
  trend: string;
  caption: string;
}

export interface WeeklyProgressPoint {
  day: string;
  value: number;
}

export interface SkillMetric {
  label: string;
  value: number;
}

export interface DetailedSession {
  title: string;
  date: string;
  meta: string;
  score: number;
}
