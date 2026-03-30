<template>
  <StackLayout class="improvementList">
    <FlexboxLayout v-if="showHeader" class="improvementRow" alignItems="center">
      <StackLayout class="warningCircle">
        <Label text="!" class="warningText" />
      </StackLayout>
      <Label :text="title" class="improvementTitle" />
    </FlexboxLayout>

    <StackLayout class="improvementCard">
      <StackLayout
        v-for="metric in metrics"
        :key="metric.label"
        class="metric"
      >
        <FlexboxLayout class="metricHeader" justifyContent="space-between">
          <Label :text="metric.label" class="metricLabel" />
          <Label :text="`${metric.value}%`" class="metricValue" />
        </FlexboxLayout>
        <GridLayout :columns="metricColumns(metric.value)" class="progressBar">
          <StackLayout col="0" class="progressFill" />
          <StackLayout col="1" class="progressRest" />
        </GridLayout>
      </StackLayout>
    </StackLayout>

    <Label :text="recentTitle" class="improvementSectionTitle" />

    <GridLayout
      v-for="session in sessions"
      :key="session.title"
      columns="*, auto"
      class="scoreCard"
    >
      <StackLayout col="0" class="scoreMain">
        <Label :text="session.title" class="scoreTitle" textWrap="true" />
        <Label :text="session.date" class="scoreDate" />
      </StackLayout>
      <StackLayout col="1" class="scoreBlock">
        <Label :text="`${session.score}`" class="scoreValue" />
        <Label text="Score" class="scoreLabel" />
      </StackLayout>
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { ImprovementMetric, SessionScore } from "@/entities/analytics";

const defaultMetrics: ImprovementMetric[] = [
  { label: "Technical Depth", value: 68 },
  { label: "Communication", value: 72 },
  { label: "Confidence", value: 75 },
];

const defaultSessions: SessionScore[] = [
  { title: "Behavioral Questions", date: "2 days ago", score: 82 },
  { title: "Technical Round", date: "2 days ago", score: 76 },
];

export default defineComponent({
  name: "ImprovementList",
  props: {
    showHeader: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      default: "Areas to improve",
    },
    recentTitle: {
      type: String,
      default: "Recent Session",
    },
    metrics: {
      type: Array as PropType<ImprovementMetric[]>,
      default: () => defaultMetrics,
    },
    sessions: {
      type: Array as PropType<SessionScore[]>,
      default: () => defaultSessions,
    },
  },
  methods: {
    metricColumns(value: number): string {
      const safe = Math.max(0, Math.min(100, Math.round(value)));
      return `${safe}*, ${100 - safe}*`;
    },
  },
});
</script>

<style scoped>
.improvementList {
  margin-bottom: 8;
}

.improvementRow {
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
</style>
