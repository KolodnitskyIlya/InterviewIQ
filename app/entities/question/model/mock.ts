import type { InterviewQuestion } from "./types";

export const mockQuestions: InterviewQuestion[] = [
  {
    category: "Technical",
    title: "Explain the difference between REST and GraphQL APIs",
    description:
      "Provide a comprehensive answer discussing the key differences, use cases, and trade-offs.",
  },
  {
    category: "Behavioral",
    title: "Tell me about a time you had a conflict in your team",
    description:
      "Describe the situation, your actions, and what changed after your intervention.",
  },
  {
    category: "System Design",
    title: "How would you design a notification service for a mobile app?",
    description:
      "Focus on architecture, scaling, delivery guarantees, and monitoring.",
  },
];
