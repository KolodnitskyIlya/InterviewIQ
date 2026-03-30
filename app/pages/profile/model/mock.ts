import type { JobInfoItem, ProfileStat, UserProfile } from "@/entities/user";

export const profile: UserProfile = {
  firstName: "Danil",
  lastName: "Kolbasenko",
  email: "danil.kolbasenko@email.com",
  avatarLetter: "D",
};

export const stats: ProfileStat[] = [
  { value: "156", label: "Questions" },
  { value: "28", label: "Sessions" },
  { value: "78%", label: "Avg Score" },
];

export const jobInfo: JobInfoItem[] = [
  { label: "Target Role", value: "ML Engineer" },
  { label: "Experience Level", value: "Senior (6+ years)" },
];
