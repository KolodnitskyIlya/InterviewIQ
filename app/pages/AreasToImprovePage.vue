<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto">
      <ScrollView row="0">
        <StackLayout class="content">
          <FlexboxLayout class="titleRow" alignItems="center">
            <StackLayout class="warningCircle">
              <Label text="!" class="warningText" />
            </StackLayout>
            <Label text="Areas to improve" class="title" />
          </FlexboxLayout>

          <StackLayout class="improvementCard">
            <StackLayout class="metric">
              <FlexboxLayout class="metricHeader" justifyContent="space-between">
                <Label text="Technical Depth" class="metricLabel" />
                <Label text="68%" class="metricValue" />
              </FlexboxLayout>
              <GridLayout columns="68*, 32*" class="progressBar">
                <StackLayout col="0" class="progressFill" />
                <StackLayout col="1" class="progressRest" />
              </GridLayout>
            </StackLayout>

            <StackLayout class="metric">
              <FlexboxLayout class="metricHeader" justifyContent="space-between">
                <Label text="Communication" class="metricLabel" />
                <Label text="72%" class="metricValue" />
              </FlexboxLayout>
              <GridLayout columns="72*, 28*" class="progressBar">
                <StackLayout col="0" class="progressFill" />
                <StackLayout col="1" class="progressRest" />
              </GridLayout>
            </StackLayout>

            <StackLayout class="metric">
              <FlexboxLayout class="metricHeader" justifyContent="space-between">
                <Label text="Confidence" class="metricLabel" />
                <Label text="75%" class="metricValue" />
              </FlexboxLayout>
              <GridLayout columns="75*, 25*" class="progressBar">
                <StackLayout col="0" class="progressFill" />
                <StackLayout col="1" class="progressRest" />
              </GridLayout>
            </StackLayout>
          </StackLayout>

          <Label text="Recent Session" class="sectionTitle" />

          <GridLayout columns="*, auto" class="sessionCard">
            <StackLayout col="0" class="sessionMain">
              <Label text="Behavioral Questions" class="sessionTitle" />
              <Label text="2 days ago" class="sessionDate" />
            </StackLayout>
            <StackLayout col="1" class="scoreBlock">
              <Label text="82" class="scoreValue" />
              <Label text="Score" class="scoreLabel" />
            </StackLayout>
          </GridLayout>

          <GridLayout columns="*, auto" class="sessionCard">
            <StackLayout col="0" class="sessionMain">
              <Label text="Technical Round" class="sessionTitle" />
              <Label text="2 days ago" class="sessionDate" />
            </StackLayout>
            <StackLayout col="1" class="scoreBlock">
              <Label text="76" class="scoreValue" />
              <Label text="Score" class="scoreLabel" />
            </StackLayout>
          </GridLayout>
        </StackLayout>
      </ScrollView>

      <GridLayout row="1" columns="*, *, *, *" class="bottomNav">
        <StackLayout col="0" class="tabItem activeTab" @tap="goHome">
          <Label text="⌂" class="tabIcon activeTabIcon" />
          <Label text="Home" class="tabLabel activeTabLabel" />
        </StackLayout>
        <StackLayout col="1" class="tabItem">
          <Label text="◎" class="tabIcon" />
          <Label text="Practice" class="tabLabel" />
        </StackLayout>
        <StackLayout col="2" class="tabItem">
          <Label text="▥" class="tabIcon" />
          <Label text="Analytics" class="tabLabel" />
        </StackLayout>
        <StackLayout col="3" class="tabItem">
          <Label text="◯" class="tabIcon" />
          <Label text="Profile" class="tabLabel" />
        </StackLayout>
      </GridLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "AreasToImprovePage",
  methods: {
    goHome() {
      this.$navigateBack();
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

.titleRow {
  margin-bottom: 20;
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

.title {
  font-size: 22;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
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
  margin-bottom: 18;
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

.sectionTitle {
  margin-top: 28;
  font-size: 24;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionCard {
  margin-top: 16;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 18;
  padding-right: 20;
  padding-bottom: 18;
  padding-left: 20;
}

.sessionMain {
  vertical-align: middle;
}

.sessionTitle {
  font-size: 22;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionDate {
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
  align-items: center;
  justify-content: center;
}

.activeTab {
  background-color: #ddd6fe;
}

.tabIcon {
  font-size: 24;
  color: #6b7280;
  text-align: center;
}

.activeTabIcon {
  color: #6366f1;
}

.tabLabel {
  margin-top: 2;
  font-size: 14;
  color: #6b7280;
  font-family: "Poppins";
}

.activeTabLabel {
  color: #4f46e5;
}
</style>
