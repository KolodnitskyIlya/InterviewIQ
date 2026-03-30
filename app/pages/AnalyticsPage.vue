<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto">
      <StackLayout row="0" class="hero">
        <Label text="Analytics" class="heroTitle" />
        <Label text="Track your progress over time" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <GridLayout columns="*, auto" class="card readinessCard">
            <StackLayout col="0">
              <Label text="Overall Readiness" class="sectionLabel" />
              <Label text="78%" class="bigValue" />
            </StackLayout>
            <StackLayout col="1" horizontalAlignment="right">
              <Label text="↗" class="trendIcon" />
              <Label text="+12%" class="trendValue" />
              <Label text="vs last week" class="trendCaption" />
            </StackLayout>
          </GridLayout>

          <StackLayout class="card chartCard">
            <Label text="Weekly Progress" class="sectionLabel" />
            <GridLayout
              columns="auto, *, auto, *, auto, *, auto, *, auto, *, auto, *, auto"
              class="lineChart"
            >
              <StackLayout col="1" class="lineBar bar1" />
              <StackLayout col="3" class="lineBar bar2" />
              <StackLayout col="5" class="lineBar bar3" />
              <StackLayout col="7" class="lineBar bar4" />
              <StackLayout col="9" class="lineBar bar5" />
              <StackLayout col="11" class="lineBar bar6" />
            </GridLayout>
            <GridLayout columns="*, *, *, *, *, *" class="weekLabels">
              <Label col="0" text="Mon" class="axisText" />
              <Label col="1" text="Tue" class="axisText" />
              <Label col="2" text="Wed" class="axisText" />
              <Label col="3" text="Thu" class="axisText" />
              <Label col="4" text="Fri" class="axisText" />
              <Label col="5" text="Sat" class="axisText" />
            </GridLayout>
          </StackLayout>

          <StackLayout class="card skillsCard">
            <GridLayout columns="*, auto">
              <Label col="0" text="Skills Breakdown" class="sectionLabel" />
              <Label col="1" text="◎" class="cardIcon" />
            </GridLayout>

            <GridLayout columns="auto, *" class="skillRow">
              <Label col="0" text="Technical" class="skillLabel" />
              <GridLayout col="1" columns="78*, 22*" class="barTrack">
                <StackLayout col="0" class="barFill" />
                <StackLayout col="1" class="barRest" />
              </GridLayout>
            </GridLayout>

            <GridLayout columns="auto, *" class="skillRow">
              <Label col="0" text="Behavioral" class="skillLabel" />
              <GridLayout col="1" columns="70*, 30*" class="barTrack">
                <StackLayout col="0" class="barFill" />
                <StackLayout col="1" class="barRest" />
              </GridLayout>
            </GridLayout>

            <GridLayout columns="auto, *" class="skillRow">
              <Label col="0" text="HR" class="skillLabel" />
              <GridLayout col="1" columns="62*, 38*" class="barTrack">
                <StackLayout col="0" class="barFill" />
                <StackLayout col="1" class="barRest" />
              </GridLayout>
            </GridLayout>

            <GridLayout columns="auto, *" class="skillRow">
              <Label col="0" text="System Design" class="skillLabel" />
              <GridLayout col="1" columns="58*, 42*" class="barTrack">
                <StackLayout col="0" class="barFill" />
                <StackLayout col="1" class="barRest" />
              </GridLayout>
            </GridLayout>
          </StackLayout>

          <Label text="Recent Session" class="recentTitle" />

          <GridLayout columns="*, auto" class="sessionCard">
            <StackLayout col="0">
              <Label text="Technical Round" class="sessionTitle" />
              <Label text="Feb 25, 2026" class="sessionDate" />
              <Label text="10 questions • 25 min" class="sessionMeta" />
            </StackLayout>
            <Label col="1" text="82" class="sessionScore" />
          </GridLayout>

          <GridLayout columns="*, auto" class="sessionCard">
            <StackLayout col="0">
              <Label text="Behavioral Questions" class="sessionTitle" />
              <Label text="Feb 20, 2026" class="sessionDate" />
              <Label text="8 questions • 20 min" class="sessionMeta" />
            </StackLayout>
            <Label col="1" text="78" class="sessionScore" />
          </GridLayout>
        </StackLayout>
      </ScrollView>

      <GridLayout row="2" columns="*, *, *, *" class="bottomNav">
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
          <Label row="0" text="◉" class="tabIcon" />
          <Label row="1" text="Practice" class="tabLabel" />
        </GridLayout>
        <GridLayout col="2" rows="auto, auto" class="tabItem activeTab">
          <Label row="0" text="▥" class="tabIcon activeTabIcon" />
          <Label row="1" text="Analytics" class="tabLabel activeTabLabel" />
        </GridLayout>
        <GridLayout
          col="3"
          rows="auto, auto"
          class="tabItem"
          @tap="openProfile"
        >
          <Label row="0" text="◯" class="tabIcon" />
          <Label row="1" text="Profile" class="tabLabel" />
        </GridLayout>
      </GridLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import HomePage from "./HomePage.vue";
import PracticePage from "./PracticePage.vue";
import ProfilePage from "./ProfilePage.vue";

export default defineComponent({
  name: "AnalyticsPage",
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

.card {
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 16;
  padding-right: 16;
  padding-bottom: 16;
  padding-left: 16;
  margin-bottom: 16;
}

.sectionLabel {
  font-size: 16;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.bigValue {
  margin-top: 6;
  font-size: 34;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.trendIcon {
  font-size: 18;
  color: #10b981;
  text-align: right;
}

.trendValue {
  margin-top: 4;
  font-size: 16;
  font-weight: 700;
  color: #10b981;
  text-align: right;
  font-family: "Poppins";
}

.trendCaption {
  font-size: 11;
  color: #9ca3af;
  text-align: right;
  font-family: "Poppins";
}

.lineChart {
  margin-top: 16;
  height: 80;
  vertical-align: bottom;
}

.lineBar {
  width: 14;
  border-radius: 7;
  background: linear-gradient(180deg, #818cf8, #4f46e5);
  vertical-align: bottom;
  horizontal-align: center;
}

.bar1 {
  height: 38;
}
.bar2 {
  height: 46;
}
.bar3 {
  height: 52;
}
.bar4 {
  height: 58;
}
.bar5 {
  height: 56;
}
.bar6 {
  height: 62;
}

.weekLabels {
  margin-top: 10;
}

.axisText {
  font-size: 11;
  color: #9ca3af;
  text-align: center;
  font-family: "Poppins";
}

.cardIcon {
  color: #9ca3af;
  font-size: 16;
}

.skillRow {
  margin-top: 14;
}

.skillLabel {
  width: 90;
  font-size: 13;
  color: #6b7280;
  font-family: "Poppins";
}

.barTrack {
  height: 18;
  border-radius: 9;
  margin-left: 14;
}

.barFill {
  border-radius: 9;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

.barRest {
  border-radius: 9;
  background-color: #ede9fe;
}

.recentTitle {
  margin-top: 4;
  margin-bottom: 10;
  font-size: 20;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.sessionCard {
  margin-bottom: 14;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 18;
  padding-right: 18;
  padding-bottom: 18;
  padding-left: 18;
}

.sessionTitle {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionDate {
  margin-top: 6;
  font-size: 13;
  color: #6b7280;
  font-family: "Poppins";
}

.sessionMeta {
  margin-top: 4;
  font-size: 12;
  color: #9ca3af;
  font-family: "Poppins";
}

.sessionScore {
  font-size: 28;
  font-weight: 700;
  color: #4f46e5;
  vertical-align: middle;
  font-family: "Poppins";
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
