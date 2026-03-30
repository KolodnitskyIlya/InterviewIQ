<template>
  <StackLayout class="jobCard">
    <Label text="Job Information" class="cardTitle" />

    <GridLayout
      v-for="item in items"
      :key="item.label"
      columns="*, auto"
      class="infoRow"
    >
      <Label col="0" :text="item.label" class="infoLabel" />
      <Label
        col="1"
        :text="item.value"
        class="infoValue"
        horizontalAlignment="right"
      />
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { JobInfoItem } from "@/entities/user";

const defaultItems: JobInfoItem[] = [
  { label: "Target Role", value: "ML Engineer" },
  { label: "Experience Level", value: "Senior (6+ years)" },
];

export default defineComponent({
  name: "JobInformation",
  props: {
    items: {
      type: Array as PropType<JobInfoItem[]>,
      default: () => defaultItems,
    },
  },
});
</script>

<style scoped>
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
</style>
