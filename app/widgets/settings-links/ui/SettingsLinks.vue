<template>
  <StackLayout class="sectionSpacing">
    <Label :text="title" class="sectionLabel" />
    <StackLayout class="card">
      <StackLayout v-for="(item, index) in items" :key="item.id">
        <GridLayout columns="auto, *, auto, auto" class="row">
          <Label col="0" :text="item.icon" class="rowIcon" :class="dangerClass(item)" />
          <Label col="1" :text="item.label" class="rowText" :class="dangerClass(item)" />
          <Label col="2" :text="item.value || ''" class="rowValue" />
          <Label col="3" text="›" class="chevron" />
        </GridLayout>
        <StackLayout v-if="index < items.length - 1" class="divider" />
      </StackLayout>
    </StackLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { SettingsLinkItem } from "@/entities/settings";

export default defineComponent({
  name: "SettingsLinks",
  props: {
    title: {
      type: String,
      required: true,
    },
    items: {
      type: Array as PropType<SettingsLinkItem[]>,
      default: () => [],
    },
  },
  methods: {
    dangerClass(item: SettingsLinkItem): string {
      return item.danger ? "danger" : "";
    },
  },
});
</script>

<style scoped>
.sectionSpacing {
  margin-top: 26;
}

.sectionLabel {
  font-size: 13;
  font-weight: 700;
  color: #6b7280;
  font-family: "Poppins";
}

.card {
  margin-top: 8;
  background-color: #ffffff;
  border-radius: 24;
}

.row {
  height: 66;
  padding-top: 14;
  padding-right: 16;
  padding-bottom: 14;
  padding-left: 16;
}

.rowIcon {
  font-size: 24;
  color: #111827;
  vertical-align: middle;
}

.rowText {
  margin-left: 10;
  font-size: 20;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
  vertical-align: middle;
}

.rowValue {
  font-size: 16;
  color: #6b7280;
  font-family: "Poppins";
  margin-right: 8;
  vertical-align: middle;
}

.divider {
  height: 1;
  background-color: #e5e7eb;
}

.chevron {
  font-size: 28;
  color: #9ca3af;
  vertical-align: middle;
}

.danger {
  color: #ef4444;
}
</style>
