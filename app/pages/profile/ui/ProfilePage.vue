<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, auto, auto, *, auto">
      <ProfileSummary row="0" :profile="profileData" :stats="statsData" />
      <JobInformation row="1" :items="jobInfoData" />
      <ProfileActions
        row="2"
        @openSettings="openSettings"
        @logout="logout"
      />

      <BottomNavigation
        row="4"
        activeTab="profile"
        @home="openHome"
        @practice="openPractice"
        @analytics="openAnalytics"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";

import type { JobInfoItem, ProfileStat, UserProfile } from "@/entities/user";
import { ApiError, clearAuthSession, getAccessToken, interviewIqApi } from "@/shared";
import AnalyticsPage from "@/pages/analytics";
import HomePage from "@/pages/home";
import PracticePage from "@/pages/practice";
import SettingsPage from "@/pages/settings";
import SignInPage from "@/pages/sign-in";
import BottomNavigation from "@/widgets/bottom-navigation";
import JobInformation from "@/widgets/job-information";
import ProfileActions from "@/widgets/profile-actions";
import ProfileSummary from "@/widgets/profile-summary";

const defaultProfile: UserProfile = {
  firstName: "User",
  lastName: "",
  email: "user@example.com",
  avatarLetter: "U",
};

const defaultStats: ProfileStat[] = [
  { value: "0", label: "Questions" },
  { value: "0", label: "Sessions" },
  { value: "0%", label: "Avg Score" },
];

const defaultJobInfo: JobInfoItem[] = [
  { label: "Target Role", value: "-" },
  { label: "Experience Level", value: "-" },
];

function experienceLabel(level: string | null): string {
  if (!level) {
    return "-";
  }

  if (level === "junior") {
    return "Junior";
  }

  if (level === "middle") {
    return "Middle";
  }

  if (level === "senior") {
    return "Senior";
  }

  return level;
}

function toUserProfile(fullName: string, email: string): UserProfile {
  const parts = fullName.trim().split(/\s+/).filter(Boolean);
  const firstName = parts[0] || "User";
  const lastName = parts.slice(1).join(" ");
  const avatarLetter = firstName[0]?.toUpperCase() || "U";

  return {
    firstName,
    lastName,
    email,
    avatarLetter,
  };
}

export default defineComponent({
  name: "ProfilePage",
  components: {
    BottomNavigation,
    ProfileSummary,
    JobInformation,
    ProfileActions,
  },
  data() {
    return {
      profileData: defaultProfile as UserProfile,
      statsData: defaultStats as ProfileStat[],
      jobInfoData: defaultJobInfo as JobInfoItem[],
    };
  },
  mounted() {
    void this.loadProfile();
  },
  methods: {
    async loadProfile() {
      if (!getAccessToken()) {
        this.$navigateTo(SignInPage, { clearHistory: true });
        return;
      }

      try {
        const [profile, overview, sessions] = await Promise.all([
          interviewIqApi.getProfile(),
          interviewIqApi.getAnalyticsOverview(),
          interviewIqApi.getAnalyticsSessions(1, 100),
        ]);

        this.profileData = toUserProfile(profile.full_name, profile.email);
        this.statsData = [
          {
            value: String(
              sessions.items.reduce(
                (total, session) => total + session.questions_count,
                0,
              ),
            ),
            label: "Questions",
          },
          { value: String(sessions.total), label: "Sessions" },
          { value: `${overview.average_score}%`, label: "Avg Score" },
        ];
        this.jobInfoData = [
          { label: "Target Role", value: profile.target_role || "-" },
          {
            label: "Experience Level",
            value: experienceLabel(profile.experience_level),
          },
        ];
      } catch (error) {
        await alert({
          title: "Failed to load profile",
          message: error instanceof ApiError ? error.message : "Please try again.",
          okButtonText: "OK",
        });

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
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openPractice() {
      this.$navigateTo(PracticePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openAnalytics() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openSettings() {
      this.$navigateTo(SettingsPage, {
        transition: {
          name: "slideLeft",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
    logout() {
      clearAuthSession();
      this.$navigateTo(SignInPage, {
        clearHistory: true,
        transition: {
          name: "fade",
          duration: 220,
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
</style>
