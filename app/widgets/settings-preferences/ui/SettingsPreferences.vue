<template>
  <StackLayout>
    <Label text="PREFERENCES" class="sectionLabel" />
    <StackLayout class="card">
      <ToggleSettingRow
        icon="☾"
        label="Dark Mode"
        :modelValue="darkMode"
        @update:modelValue="$emit('update:darkMode', $event)"
      />

      <StackLayout class="divider" />

      <ToggleSettingRow
        icon="🔔"
        label="Push Notifications"
        :modelValue="pushNotifications"
        @update:modelValue="$emit('update:pushNotifications', $event)"
      />

      <StackLayout class="divider" />

      <GridLayout columns="auto, *, auto, auto" class="row">
        <Label col="0" text="🌐" class="rowIcon" />
        <Label col="1" text="Language" class="rowText" />
        <Label col="2" :text="language" class="rowValue" />
        <Label col="3" text="›" class="chevron" />
      </GridLayout>
    </StackLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import ToggleSettingRow from "@/features/toggle-setting";

export default defineComponent({
  name: "SettingsPreferences",
  components: {
    ToggleSettingRow,
  },
  emits: ["update:darkMode", "update:pushNotifications"],
  props: {
    darkMode: {
      type: Boolean,
      default: false,
    },
    pushNotifications: {
      type: Boolean,
      default: true,
    },
    language: {
      type: String,
      default: "English",
    },
  },
});
</script>

<style scoped>
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
</style>
