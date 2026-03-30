<template>
  <StackLayout class="actionsCard">
    <OpenSettingsAction @tap="$emit('openSettings')" />
    <StackLayout class="rowDivider" />
    <LogoutAction @tap="$emit('logout')" />
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import LogoutAction from "@/features/logout";
import OpenSettingsAction from "@/features/open-settings";

export default defineComponent({
  name: "ProfileActions",
  components: {
    OpenSettingsAction,
    LogoutAction,
  },
  emits: ["openSettings", "logout"],
});
</script>

<style scoped>
.actionsCard {
  margin-top: 12;
  margin-right: 24;
  margin-left: 24;
  background-color: #ffffff;
  border-radius: 24;
}

.rowDivider {
  height: 1;
  background-color: #e5e7eb;
}
</style>
