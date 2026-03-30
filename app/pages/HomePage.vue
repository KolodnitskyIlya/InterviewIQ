<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto">
      <ScrollView row="0">
        <StackLayout class="content">
          <StackLayout class="hero">
            <Label text="Good evening," class="greeting" />
            <Label
              text="Danil Kolbasenko 👋"
              class="userName"
              textWrap="true"
            />

            <GridLayout columns="auto, *" class="readinessCard">
              <StackLayout
                col="0"
                class="progressContainer"
                horizontalAlignment="center"
                verticalAlignment="center"
              >
                <GridLayout class="progressOuter">
                  <GridLayout class="progressTrack" />
                  <GridLayout class="progressArc" />
                  <GridLayout class="progressInner">
                    <Label
                      text="78%"
                      class="progressValue"
                      horizontalAlignment="center"
                      verticalAlignment="center"
                    />
                  </GridLayout>
                </GridLayout>
              </StackLayout>

              <StackLayout col="1" class="readinessInfo">
                <Label
                  text="Interview Readiness"
                  class="cardTitle"
                  textWrap="true"
                />
                <Label
                  text="You're doing great! Keep practicing."
                  class="cardSubtitle"
                  textWrap="true"
                />
                <FlexboxLayout class="growthRow" alignItems="center">
                  <Label text="↗" class="growthArrow" />
                  <Label text="+8% this week" class="cardGrowth" />
                </FlexboxLayout>
              </StackLayout>
            </GridLayout>
          </StackLayout>

          <StackLayout class="body">
            <Button
              text="▷ Start Practice Session"
              class="startButton"
              @tap="openPractice"
            />
            <Label text="Continue where you left off" class="sectionTitle" />

            <GridLayout columns="auto, *" class="sessionCard">
              <GridLayout col="0" class="sessionIcon">
                <Label
                  text="🕒"
                  class="sessionIconText"
                  horizontalAlignment="center"
                  verticalAlignment="center"
                />
              </GridLayout>

              <StackLayout col="1" class="sessionInfo">
                <Label
                  text="System Design Practice"
                  class="sessionTitle"
                  textWrap="true"
                />
                <Label
                  text="Question 7 of 10 • 15 min left"
                  class="sessionMeta"
                  textWrap="true"
                />
              </StackLayout>
            </GridLayout>

            <StackLayout class="improvementSection">
              <FlexboxLayout class="improvementRow" alignItems="center">
                <StackLayout class="warningCircle">
                  <Label text="!" class="warningText" />
                </StackLayout>
                <Label text="Areas to improve" class="improvementTitle" />
              </FlexboxLayout>

              <StackLayout class="improvementCard">
                <StackLayout class="metric">
                  <FlexboxLayout
                    class="metricHeader"
                    justifyContent="space-between"
                  >
                    <Label text="Technical Depth" class="metricLabel" />
                    <Label text="68%" class="metricValue" />
                  </FlexboxLayout>
                  <GridLayout columns="68*, 32*" class="progressBar">
                    <StackLayout col="0" class="progressFill" />
                    <StackLayout col="1" class="progressRest" />
                  </GridLayout>
                </StackLayout>

                <StackLayout class="metric">
                  <FlexboxLayout
                    class="metricHeader"
                    justifyContent="space-between"
                  >
                    <Label text="Communication" class="metricLabel" />
                    <Label text="72%" class="metricValue" />
                  </FlexboxLayout>
                  <GridLayout columns="72*, 28*" class="progressBar">
                    <StackLayout col="0" class="progressFill" />
                    <StackLayout col="1" class="progressRest" />
                  </GridLayout>
                </StackLayout>

                <StackLayout class="metric">
                  <FlexboxLayout
                    class="metricHeader"
                    justifyContent="space-between"
                  >
                    <Label text="Confidence" class="metricLabel" />
                    <Label text="75%" class="metricValue" />
                  </FlexboxLayout>
                  <GridLayout columns="75*, 25*" class="progressBar">
                    <StackLayout col="0" class="progressFill" />
                    <StackLayout col="1" class="progressRest" />
                  </GridLayout>
                </StackLayout>
              </StackLayout>

              <Label text="Recent Session" class="improvementSectionTitle" />

              <GridLayout columns="*, auto" class="scoreCard">
                <StackLayout col="0" class="scoreMain">
                  <Label text="Behavioral Questions" class="scoreTitle" />
                  <Label text="2 days ago" class="scoreDate" />
                </StackLayout>
                <StackLayout col="1" class="scoreBlock">
                  <Label text="82" class="scoreValue" />
                  <Label text="Score" class="scoreLabel" />
                </StackLayout>
              </GridLayout>

              <GridLayout columns="*, auto" class="scoreCard">
                <StackLayout col="0" class="scoreMain">
                  <Label text="Technical Round" class="scoreTitle" />
                  <Label text="2 days ago" class="scoreDate" />
                </StackLayout>
                <StackLayout col="1" class="scoreBlock">
                  <Label text="76" class="scoreValue" />
                  <Label text="Score" class="scoreLabel" />
                </StackLayout>
              </GridLayout>
            </StackLayout>
          </StackLayout>
        </StackLayout>
      </ScrollView>

      <GridLayout row="1" columns="*, *, *, *" class="bottomNav">
        <GridLayout col="0" rows="auto, auto" class="tabItem activeTab">
          <Label row="0" text="⌂" class="tabIcon activeTabIcon" />
          <Label row="1" text="Home" class="tabLabel activeTabLabel" />
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
import PracticePage from "./PracticePage.vue";
import ProfilePage from "./ProfilePage.vue";

export default defineComponent({
  name: "HomePage",
  methods: {
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

.readinessCard {
  margin-top: 22;
  margin-right: 8;
  margin-left: 8;
  background-color: #ddd6fe;
  border-radius: 24;
  padding-top: 18;
  padding-right: 16;
  padding-bottom: 18;
  padding-left: 16;
}

.progressContainer {
  width: 112;
  margin-right: 14;
}

.progressOuter {
  width: 108;
  height: 108;
  border-radius: 54;
  justify-content: center;
  align-items: center;
}

.progressTrack {
  width: 108;
  height: 108;
  border-width: 7;
  border-color: #d1d5db;
  border-radius: 54;
}

.progressArc {
  width: 108;
  height: 108;
  border-width: 7;
  border-radius: 54;
  border-top-color: #14b8a6;
  border-right-color: #3b82f6;
  border-bottom-color: #4f46e5;
  border-left-color: transparent;
  rotate: -30;
  justify-content: center;
  align-items: center;
}

.progressInner {
  width: 82;
  height: 82;
  border-radius: 41;
  background-color: #ede9fe;
  justify-content: center;
  align-items: center;
}

.progressValue {
  font-size: 22;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.readinessInfo {
  vertical-align: middle;
}

.cardTitle {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  line-height: 22;
  font-family: "Poppins";
}

.cardSubtitle {
  margin-top: 6;
  font-size: 12;
  color: #4b5563;
  line-height: 16;
  font-family: "Poppins";
}

.growthRow {
  margin-top: 10;
}

.growthArrow {
  font-size: 16;
  color: #10b981;
  margin-right: 4;
  font-weight: 700;
  font-family: "Poppins";
}

.cardGrowth {
  font-size: 15;
  color: #111827;
  font-weight: 500;
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

.improvementRow {
  margin-top: 26;
  margin-bottom: 12;
}

.warningCircle {
  width: 30;
  height: 30;
  border-width: 2;
  border-color: #fb923c;
  border-radius: 15;
  justify-content: center;
  align-items: center;
  margin-right: 12;
}

.warningText {
  font-size: 19;
  color: #fb923c;
  font-weight: 600;
  text-align: center;
}

.improvementTitle {
  font-size: 21;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
}

.improvementSection {
  margin-bottom: 8;
}

.improvementCard {
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 16;
  padding-right: 16;
  padding-bottom: 16;
  padding-left: 16;
}

.metric {
  margin-bottom: 16;
}

.metric:last-child {
  margin-bottom: 0;
}

.metricHeader {
  margin-bottom: 8;
}

.metricLabel {
  font-size: 17;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
}

.metricValue {
  font-size: 17;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
}

.progressBar {
  height: 14;
  border-radius: 7;
}

.progressFill {
  border-top-left-radius: 7;
  border-bottom-left-radius: 7;
  border-top-right-radius: 7;
  border-bottom-right-radius: 7;
  background: linear-gradient(90deg, #f59e0b, #ef4444);
}

.progressRest {
  border-top-right-radius: 7;
  border-bottom-right-radius: 7;
  background-color: #d1d5db;
}

.improvementSectionTitle {
  margin-top: 24;
  font-size: 24;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.scoreCard {
  margin-top: 16;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 18;
  padding-right: 20;
  padding-bottom: 18;
  padding-left: 20;
}

.scoreMain {
  vertical-align: middle;
}

.scoreTitle {
  font-size: 22;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.scoreDate {
  margin-top: 10;
  font-size: 17;
  color: #6b7280;
  font-family: "Poppins";
}

.scoreBlock {
  margin-left: 12;
  horizontal-align: right;
  vertical-align: middle;
}

.scoreValue {
  font-size: 52;
  color: #10b981;
  font-weight: 600;
  text-align: right;
  font-family: "Poppins";
}

.scoreLabel {
  font-size: 17;
  color: #6b7280;
  text-align: right;
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
