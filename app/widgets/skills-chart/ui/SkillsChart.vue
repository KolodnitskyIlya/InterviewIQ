<template>
  <StackLayout class="card skillsCard">
    <GridLayout columns="*, auto">
      <Label col="0" text="Skills Breakdown" class="sectionLabel" />
      <Label col="1" text="◎" class="cardIcon" />
    </GridLayout>

    <GridLayout
      v-for="skill in skills"
      :key="skill.label"
      columns="auto, *"
      class="skillRow"
    >
      <Label col="0" :text="skill.label" class="skillLabel" />
      <GridLayout col="1" :columns="barColumns(skill.value)" class="barTrack">
        <StackLayout col="0" class="barFill" />
        <StackLayout col="1" class="barRest" />
      </GridLayout>
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { SkillMetric } from "@/entities/analytics";

const defaultSkills: SkillMetric[] = [
  { label: "Technical", value: 78 },
  { label: "Behavioral", value: 70 },
  { label: "HR", value: 62 },
  { label: "System Design", value: 58 },
];

export default defineComponent({
  name: "SkillsChart",
  props: {
    skills: {
      type: Array as PropType<SkillMetric[]>,
      default: () => defaultSkills,
    },
  },
  methods: {
    barColumns(value: number): string {
      const safe = Math.max(0, Math.min(100, Math.round(value)));
      return `${safe}*, ${100 - safe}*`;
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
</style>
