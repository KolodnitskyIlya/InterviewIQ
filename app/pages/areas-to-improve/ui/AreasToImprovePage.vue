<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto">
      <ScrollView row="0">
        <StackLayout class="content">
          <ImprovementList />
        </StackLayout>
      </ScrollView>

      <BottomNavigation
        row="1"
        activeTab="home"
        @home="goHome"
        @practice="openPractice"
        @analytics="openAnalytics"
        @profile="openProfile"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import AnalyticsPage from "@/pages/analytics";
import HomePage from "@/pages/home";
import PracticePage from "@/pages/practice";
import ProfilePage from "@/pages/profile";
import BottomNavigation from "@/widgets/bottom-navigation";
import ImprovementList from "@/widgets/improvement-list";

export default defineComponent({
  name: "AreasToImprovePage",
  components: {
    BottomNavigation,
    ImprovementList,
  },
  methods: {
    goHome() {
      this.$navigateTo(HomePage, {
        clearHistory: true,
      });
    },
    openPractice() {
      this.$navigateTo(PracticePage, {
        clearHistory: true,
      });
    },
    openAnalytics() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
      });
    },
    openProfile() {
      this.$navigateTo(ProfilePage, {
        clearHistory: true,
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
  padding-top: 82;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}
</style>
