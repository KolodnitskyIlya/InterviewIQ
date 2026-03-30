<template>
  <GridLayout columns="auto, *, auto" class="actionRow" @tap="$emit('tap')">
    <Label col="0" text="⎋" class="logoutIcon" />
    <Label col="1" text="Logout" class="logoutText" />
    <Label col="2" text="›" class="chevron" />
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "LogoutAction",
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

.logoutIcon {
  font-size: 24;
  color: #ef4444;
  vertical-align: middle;
}

.logoutText {
  font-size: 18;
  font-weight: 600;
  color: #ef4444;
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
