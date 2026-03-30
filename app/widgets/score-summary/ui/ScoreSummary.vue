<template>
  <StackLayout>
    <GridLayout columns="*, auto" class="card readinessCard">
      <StackLayout col="0">
        <Label :text="summary.label" class="sectionLabel" />
        <Label :text="`${summary.value}%`" class="bigValue" />
      </StackLayout>
      <StackLayout col="1" horizontalAlignment="right">
        <Label text="↗" class="trendIcon" />
        <Label :text="summary.trend" class="trendValue" />
        <Label :text="summary.caption" class="trendCaption" />
      </StackLayout>
    </GridLayout>

    <StackLayout class="card chartCard">
      <Label text="Weekly Progress" class="sectionLabel" />
      <FlexboxLayout
        class="lineChart"
        justifyContent="space-between"
        alignItems="flex-end"
      >
        <StackLayout
          v-for="point in weeklyProgress"
          :key="point.day"
          class="lineBar"
          :height="barHeight(point.value)"
        />
      </FlexboxLayout>
      <FlexboxLayout class="weekLabels" justifyContent="space-between">
        <Label
          v-for="point in weeklyProgress"
          :key="`${point.day}-label`"
          :text="point.day"
          class="axisText"
        />
      </FlexboxLayout>
    </StackLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { ReadinessSummary, WeeklyProgressPoint } from "@/entities/analytics";

const defaultSummary: ReadinessSummary = {
  label: "Overall Readiness",
  value: 78,
  trend: "+12%",
  caption: "vs last week",
};

const defaultWeekly: WeeklyProgressPoint[] = [
  { day: "Mon", value: 38 },
  { day: "Tue", value: 46 },
  { day: "Wed", value: 52 },
  { day: "Thu", value: 58 },
  { day: "Fri", value: 56 },
  { day: "Sat", value: 62 },
];

export default defineComponent({
  name: "ScoreSummary",
  props: {
    summary: {
      type: Object as PropType<ReadinessSummary>,
      default: () => defaultSummary,
    },
    weeklyProgress: {
      type: Array as PropType<WeeklyProgressPoint[]>,
      default: () => defaultWeekly,
    },
  },
  methods: {
    barHeight(value: number): number {
      const safe = Math.max(0, Math.min(100, value));
      return 24 + Math.round((safe / 100) * 56);
    },
  },
});
</script>

<style scoped>
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
}

.lineBar {
  width: 14;
  border-radius: 7;
  background: linear-gradient(180deg, #818cf8, #4f46e5);
}

.weekLabels {
  margin-top: 10;
}

.axisText {
  font-size: 11;
  color: #9ca3af;
  font-family: "Poppins";
}
</style>
