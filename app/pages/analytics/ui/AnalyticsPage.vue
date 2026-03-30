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
import HomePage from "@/pages/home";
import PracticePage from "@/pages/practice";
import ProfilePage from "@/pages/profile";
import {
  readinessSummary,
  recentSessions,
  skillsBreakdown,
  weeklyProgress,
} from "@/pages/analytics/model/mock";
import BottomNavigation from "@/widgets/bottom-navigation";
import RecentSessions from "@/widgets/recent-sessions";
import ScoreSummary from "@/widgets/score-summary";
import SkillsChart from "@/widgets/skills-chart";

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
      summary: readinessSummary as ReadinessSummary,
      weekly: weeklyProgress as WeeklyProgressPoint[],
      skills: skillsBreakdown as SkillMetric[],
      sessions: recentSessions as DetailedSession[],
    };
  },
  methods: {
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
