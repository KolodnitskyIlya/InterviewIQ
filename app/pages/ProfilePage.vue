<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, auto, auto, auto, *, auto">
      <StackLayout row="0" class="hero">
        <GridLayout class="avatar">
          <Label
            text="D"
            class="avatarText"
            horizontalAlignment="center"
            verticalAlignment="center"
          />
        </GridLayout>
        <Label text="Danil Kolbasenko" class="name" textWrap="true" />
        <Label text="danil.kolbasenko@email.com" class="email" />
      </StackLayout>

      <GridLayout row="1" columns="*, auto, *, auto, *" class="statsCard">
        <StackLayout col="0" class="statItem">
          <Label text="156" class="statValue" />
          <Label text="Questions" class="statLabel" />
        </StackLayout>
        <StackLayout col="1" class="statDivider" />

        <StackLayout col="2" class="statItem">
          <Label text="28" class="statValue" />
          <Label text="Sessions" class="statLabel" />
        </StackLayout>
        <StackLayout col="3" class="statDivider" />

        <StackLayout col="4" class="statItem">
          <Label text="78%" class="statValue" />
          <Label text="Avg Score" class="statLabel" />
        </StackLayout>
      </GridLayout>

      <StackLayout row="2" class="jobCard">
        <Label text="Job Information" class="cardTitle" />

        <GridLayout columns="*, auto" class="infoRow">
          <Label col="0" text="Target Role" class="infoLabel" />
          <Label
            col="1"
            text="ML Engineer"
            class="infoValue"
            horizontalAlignment="right"
          />
        </GridLayout>

        <GridLayout columns="*, auto" class="infoRow">
          <Label col="0" text="Experience Level" class="infoLabel" />
          <Label
            col="1"
            text="Senior (6+ years)"
            class="infoValue"
            horizontalAlignment="right"
          />
        </GridLayout>
      </StackLayout>

      <StackLayout row="3" class="actionsCard">
        <GridLayout
          columns="auto, *, auto"
          class="actionRow"
          @tap="openSettings"
        >
          <Label col="0" text="⚙" class="actionIcon" />
          <Label col="1" text="Settings" class="actionText" />
          <Label col="2" text="›" class="chevron" />
        </GridLayout>

        <StackLayout class="rowDivider" />

        <GridLayout columns="auto, *, auto" class="actionRow" @tap="logout">
          <Label col="0" text="⎋" class="logoutIcon" />
          <Label col="1" text="Logout" class="logoutText" />
          <Label col="2" text="›" class="chevron" />
        </GridLayout>
      </StackLayout>

      <GridLayout row="5" columns="*, *, *, *" class="bottomNav">
        <GridLayout col="0" rows="auto, auto" class="tabItem" @tap="openHome">
          <Label row="0" text="⌂" class="tabIcon" />
          <Label row="1" text="Home" class="tabLabel" />
        </GridLayout>
        <GridLayout
          col="1"
          rows="auto, auto"
          class="tabItem"
          @tap="openPractice"
        >
          <Label row="0" text="◎" class="tabIcon" />
          <Label row="1" text="Practice" class="tabLabel" />
        </GridLayout>
        <GridLayout col="2" rows="auto, auto" class="tabItem">
          <Label row="0" text="▥" class="tabIcon" />
          <Label row="1" text="Analytics" class="tabLabel" />
        </GridLayout>
        <GridLayout col="3" rows="auto, auto" class="tabItem activeTab">
          <Label row="0" text="◯" class="tabIcon activeTabIcon" />
          <Label row="1" text="Profile" class="tabLabel activeTabLabel" />
        </GridLayout>
      </GridLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import AnalyticsPage from "./AnalyticsPage.vue";
import HomePage from "./HomePage.vue";
import PracticePage from "./PracticePage.vue";
import SettingsPage from "./SettingsPage.vue";
import SignInPage from "./SignInPage.vue";

export default defineComponent({
  name: "ProfilePage",
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

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 56;
  border-bottom-left-radius: 56;
  padding-top: 56;
  padding-right: 24;
  padding-bottom: 58;
  padding-left: 24;
  align-items: center;
}

.avatar {
  width: 114;
  height: 114;
  border-radius: 57;
  background-color: #ffffff;
  horizontal-align: center;
  vertical-align: middle;
}

.avatarText {
  font-size: 42;
  font-weight: 700;
  color: #4f46e5;
  font-family: "Poppins";
  text-align: center;
}

.name {
  margin-top: 14;
  font-size: 31;
  font-weight: 600;
  color: #ffffff;
  font-family: "Poppins";
  text-align: center;
  line-height: 34;
  margin-right: 18;
  margin-left: 18;
}

.email {
  margin-top: 2;
  font-size: 16;
  color: #f3f4f6;
  font-family: "Poppins";
  text-align: center;
}

.statsCard {
  margin-top: -34;
  margin-right: 24;
  margin-left: 24;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 12;
  padding-right: 10;
  padding-bottom: 12;
  padding-left: 10;
}

.statItem {
  align-items: center;
}

.statValue {
  font-size: 20;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
  text-align: center;
}

.statLabel {
  margin-top: 4;
  font-size: 12;
  color: #6b7280;
  font-family: "Poppins";
  text-align: center;
}

.statDivider {
  width: 1;
  background-color: #e5e7eb;
  margin-top: 12;
  margin-bottom: 12;
}

.jobCard {
  margin-top: 12;
  margin-right: 24;
  margin-left: 24;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 18;
  padding-right: 18;
  padding-bottom: 18;
  padding-left: 18;
}

.cardTitle {
  font-size: 20;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.infoRow {
  margin-top: 14;
}

.infoLabel {
  font-size: 16;
  color: #6b7280;
  font-family: "Poppins";
}

.infoValue {
  font-size: 16;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
  text-align: right;
}

.actionsCard {
  margin-top: 12;
  margin-right: 24;
  margin-left: 24;
  background-color: #ffffff;
  border-radius: 24;
}

.actionRow {
  height: 58;
  padding-top: 12;
  padding-right: 16;
  padding-bottom: 12;
  padding-left: 16;
}

.actionIcon {
  font-size: 24;
  color: #111827;
  vertical-align: middle;
}

.actionText {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  margin-left: 10;
  font-family: "Poppins";
  vertical-align: middle;
}

.rowDivider {
  height: 1;
  background-color: #e5e7eb;
}

.logoutIcon {
  font-size: 24;
  color: #ef4444;
  vertical-align: middle;
}

.logoutText {
  font-size: 18;
  font-weight: 600;
  color: #ef4444;
  margin-left: 10;
  font-family: "Poppins";
  vertical-align: middle;
}

.chevron {
  font-size: 28;
  color: #9ca3af;
  text-align: right;
  vertical-align: middle;
}

.bottomNav {
  border-top-width: 1;
  border-top-color: #d1d5db;
  background-color: #f8fafc;
  padding-top: 8;
  padding-right: 12;
  padding-bottom: 8;
  padding-left: 12;
}

.tabItem {
  height: 64;
  border-radius: 18;
  vertical-align: middle;
  horizontal-align: stretch;
  padding-top: 6;
  padding-bottom: 6;
}

.activeTab {
  background-color: #ddd6fe;
}

.tabIcon {
  font-size: 24;
  color: #6b7280;
  text-align: center;
  horizontal-align: center;
  vertical-align: middle;
}

.activeTabIcon {
  color: #6366f1;
}

.tabLabel {
  margin-top: 2;
  font-size: 14;
  color: #6b7280;
  font-family: "Poppins";
  text-align: center;
  horizontal-align: center;
  vertical-align: middle;
}

.activeTabLabel {
  color: #4f46e5;
}
</style>
