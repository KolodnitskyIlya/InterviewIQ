<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto">
      <ScrollView row="0">
        <StackLayout class="content">
          <StackLayout class="hero">
            <Label text="Hello," class="greeting" />
            <Label :text="userGreeting" class="userName" textWrap="true" />
            <ProgressCard
              :value="progressValue"
              :subtitle="progressSubtitle"
              :trend="progressTrend"
            />
          </StackLayout>

          <StackLayout class="body">
            <Button
              text="Start Practice Session"
              class="startButton"
              @tap="openPractice"
            />

            <Label
              v-if="resumeSession"
              text="Continue where you left off"
              class="sectionTitle"
            />

            <GridLayout
              v-if="resumeSession"
              columns="auto, *"
              class="sessionCard"
              @tap="resumePractice"
            >
              <GridLayout col="0" class="sessionIcon">
                <Label
                  text=">"
                  class="sessionIconText"
                  horizontalAlignment="center"
                  verticalAlignment="center"
                />
              </GridLayout>

              <StackLayout col="1" class="sessionInfo">
                <Label
                  text="Active practice session"
                  class="sessionTitle"
                  textWrap="true"
                />
                <Label :text="resumeMeta" class="sessionMeta" textWrap="true" />
              </StackLayout>
            </GridLayout>

            <StackLayout class="improvementSection">
              <ImprovementList
                :metrics="improvementMetrics"
                :sessions="recentSessionScores"
              />
            </StackLayout>
          </StackLayout>
        </StackLayout>
      </ScrollView>

      <BottomNavigation
        row="1"
        activeTab="home"
        @practice="openPractice"
        @analytics="openAnalytics"
        @profile="openProfile"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type {
  HomeDashboardResponse,
  AnalyticsSessionItemResponse,
} from "@/shared";
import { registerPushToken } from "@/features/register-push-token";
import {
  ApiError,
  getAccessToken,
  getAuthSession,
  interviewIqApi,
} from "@/shared";
import type { ImprovementMetric, SessionScore } from "@/entities/analytics";
import AnalyticsPage from "@/pages/analytics";
import PracticePage from "@/pages/practice";
import ProfilePage from "@/pages/profile";
import QuestionsPage from "@/pages/questions";
import SignInPage from "@/pages/sign-in";
import BottomNavigation from "@/widgets/bottom-navigation";
import ImprovementList from "@/widgets/improvement-list";
import ProgressCard from "@/widgets/progress-card";

function getFirstName(fullName: string): string {
  return fullName.trim().split(/\s+/).filter(Boolean)[0] || "User";
}

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
  name: "HomePage",
  components: {
    BottomNavigation,
    ProgressCard,
    ImprovementList,
  },
  data() {
    const session = getAuthSession();

    return {
      userName: session?.user.full_name
        ? getFirstName(session.user.full_name)
        : "User",
      progressValue: 0,
      progressTrend: "0% this week",
      progressSubtitle: "Complete a session to build your readiness score.",
      improvementMetrics: [] as ImprovementMetric[],
      recentSessionScores: [] as SessionScore[],
      resumeSession: null as HomeDashboardResponse["resume_session"],
    };
  },
  computed: {
    userGreeting(): string {
      return `${this.userName}`;
    },
    resumeMeta(): string {
      if (!this.resumeSession) {
        return "";
      }

      return `Question ${this.resumeSession.question_index} of ${this.resumeSession.total_questions}`;
    },
  },
  mounted() {
    void this.loadUserProfile();
    void this.loadDashboard();
    void registerPushToken();
  },
  methods: {
    async loadUserProfile() {
      if (!getAccessToken()) {
        this.$navigateTo(SignInPage, { clearHistory: true });
        return;
      }

      try {
        const profile = await interviewIqApi.getProfile();
        this.userName = getFirstName(profile.full_name);
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
        }
      }
    },
    async loadDashboard() {
      if (!getAccessToken()) {
        return;
      }

      try {
        const dashboard = await interviewIqApi.getHomeDashboard();
        this.progressValue = dashboard.progress_card.value;
        this.progressTrend = dashboard.progress_card.trend;
        this.progressSubtitle = dashboard.progress_card.subtitle;
        this.improvementMetrics = dashboard.areas_to_improve.map((item) => ({
          label: item.skill,
          value: item.score,
        }));
        this.recentSessionScores = dashboard.recent_sessions.map((session) => ({
          title: sessionTitle(session),
          date: formatSessionDate(session.completed_at),
          score: session.score,
        }));
        this.resumeSession = dashboard.resume_session;
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
        }
      }
    },
    async resumePractice() {
      if (!this.resumeSession) {
        return;
      }

      try {
        const session = await interviewIqApi.startPracticeSession(
          this.resumeSession.session_id,
        );
        this.$navigateTo(QuestionsPage, {
          clearHistory: true,
          props: {
            sessionId: session.id,
            currentQuestionIndex: session.current_question_index,
            totalQuestions: session.question_count,
            timeLimitSec: session.time_limit_sec,
          },
          transition: {
            name: "slideLeft",
            duration: 280,
            curve: "easeInOut",
          },
        });
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
        }
      }
    },
    openPractice() {
      this.$navigateTo(PracticePage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openAnalytics() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openProfile() {
      this.$navigateTo(ProfilePage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
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

.content {
  padding-bottom: 24;
}

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 44;
  border-bottom-left-radius: 44;
  padding-top: 72;
  padding-right: 24;
  padding-bottom: 26;
  padding-left: 24;
}

.greeting {
  font-size: 24;
  font-weight: 500;
  color: #f3f4f6;
  font-family: "Poppins";
}

.userName {
  margin-top: 8;
  font-size: 40;
  font-weight: 600;
  color: #ffffff;
  font-family: "Poppins";
}

.startButton {
  margin-top: 22;
  height: 68;
  border-radius: 24;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 24;
  font-weight: 600;
  font-family: "Poppins";
}

.body {
  padding-top: 24;
  padding-right: 24;
  padding-bottom: 0;
  padding-left: 24;
}

.sectionTitle {
  margin-top: 22;
  font-size: 22;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionCard {
  margin-top: 18;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 20;
  padding-right: 20;
  padding-bottom: 20;
  padding-left: 20;
}

.sessionIcon {
  width: 72;
  height: 72;
  border-radius: 22;
  background: linear-gradient(180deg, #4f46e5, #7c3aed);
  margin-right: 16;
}

.sessionIconText {
  font-size: 28;
  color: #ffffff;
  text-align: center;
}

.sessionInfo {
  vertical-align: middle;
}

.sessionTitle {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionMeta {
  margin-top: 8;
  font-size: 15;
  color: #4b5563;
  font-family: "Poppins";
}

.improvementSection {
  margin-top: 26;
}
</style>
