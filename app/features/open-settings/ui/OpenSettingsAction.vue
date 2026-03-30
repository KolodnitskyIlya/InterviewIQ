<template>
  <GridLayout columns="auto, *, auto" class="actionRow" @tap="$emit('tap')">
    <Label col="0" text="⚙" class="actionIcon" />
    <Label col="1" text="Settings" class="actionText" />
    <Label col="2" text="›" class="chevron" />
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "OpenSettingsAction",
  emits: ["tap"],
});
</script>

<style scoped>
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

.chevron {
  font-size: 28;
  color: #9ca3af;
  vertical-align: middle;
}
</style>
