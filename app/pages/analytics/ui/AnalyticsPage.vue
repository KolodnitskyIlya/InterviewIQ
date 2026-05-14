<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto">
      <StackLayout row="0" class="hero">
        <Label text="Analytics" class="heroTitle" />
        <Label text="Track your progress over time" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <ScoreSummary :summary="summary" :weeklyProgress="weekly" />
          <SkillsChart :skills="skills" />
          <RecentSessions :sessions="sessions" />
        </StackLayout>
      </ScrollView>

      <BottomNavigation
        row="2"
        activeTab="analytics"
        @home="openHome"
        @practice="openPractice"
        @profile="openProfile"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type {
  DetailedSession,
  ReadinessSummary,
  SkillMetric,
  WeeklyProgressPoint,
} from "@/entities/analytics";
import { ApiError, interviewIqApi, type AnalyticsSessionItemResponse } from "@/shared";
import HomePage from "@/pages/home";
import PracticePage from "@/pages/practice";
import ProfilePage from "@/pages/profile";
import SignInPage from "@/pages/sign-in";
import BottomNavigation from "@/widgets/bottom-navigation";
import RecentSessions from "@/widgets/recent-sessions";
import ScoreSummary from "@/widgets/score-summary";
import SkillsChart from "@/widgets/skills-chart";

function formatSessionDate(value: string | null): string {
  if (!value) {
    return "Recently";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Recently";
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function sessionTitle(session: AnalyticsSessionItemResponse): string {
  return session.category
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default defineComponent({
  name: "AnalyticsPage",
  components: {
    BottomNavigation,
    ScoreSummary,
    SkillsChart,
    RecentSessions,
  },
  data() {
    return {
      summary: {
        label: "Overall Readiness",
        value: 0,
        trend: "0%",
        caption: "vs previous session",
      } as ReadinessSummary,
      weekly: [] as WeeklyProgressPoint[],
      skills: [] as SkillMetric[],
      sessions: [] as DetailedSession[],
    };
  },
  mounted() {
    void this.loadAnalytics();
  },
  methods: {
    async loadAnalytics() {
      try {
        const [overview, weekly, skills, sessions] = await Promise.all([
          interviewIqApi.getAnalyticsOverview(),
          interviewIqApi.getAnalyticsWeeklyProgress(),
          interviewIqApi.getAnalyticsSkills(),
          interviewIqApi.getAnalyticsSessions(1, 10),
        ]);

        this.summary = {
          label: "Overall Readiness",
          value: overview.readiness_score,
          trend: `${overview.trend_percent >= 0 ? "+" : ""}${overview.trend_percent}%`,
          caption: "vs previous session",
        };
        this.weekly = weekly.points.map((point) => ({
          day: point.day,
          value: point.score,
        }));
        this.skills = skills.items.map((skill) => ({
          label: skill.name,
          value: skill.score,
        }));
        this.sessions = sessions.items.map((session) => ({
          title: sessionTitle(session),
          date: formatSessionDate(session.completed_at),
          meta: `${session.questions_count} questions | ${session.duration_min} min`,
          score: session.score,
        }));
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
        }
      }
    },
    openHome() {
      this.$navigateTo(HomePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
    openPractice() {
      this.$navigateTo(PracticePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
    openProfile() {
      this.$navigateTo(ProfilePage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
  },
});
</script>

<style scoped>
.page {
  background-color: #f3f4f6;
}

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 44;
  border-bottom-left-radius: 44;
  padding-top: 68;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.heroTitle {
  font-size: 34;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}

.heroSubtitle {
  margin-top: 6;
  font-size: 14;
  color: #e5e7eb;
  font-family: "Poppins";
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}
</style>
