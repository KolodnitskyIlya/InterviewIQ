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
import { defineComponent } from "nativescript-vue";

import type { JobInfoItem, ProfileStat, UserProfile } from "@/entities/user";
import { jobInfo, profile, stats } from "@/entities/user";
import AnalyticsPage from "@/pages/analytics";
import HomePage from "@/pages/home";
import PracticePage from "@/pages/practice";
import SettingsPage from "@/pages/settings";
import SignInPage from "@/pages/sign-in";
import BottomNavigation from "@/widgets/bottom-navigation";
import JobInformation from "@/widgets/job-information";
import ProfileActions from "@/widgets/profile-actions";
import ProfileSummary from "@/widgets/profile-summary";

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
      profileData: profile as UserProfile,
      statsData: stats as ProfileStat[],
      jobInfoData: jobInfo as JobInfoItem[],
    };
  },
  methods: {
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
