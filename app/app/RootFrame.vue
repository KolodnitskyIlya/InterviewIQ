<template>
  <Frame>
    <WelcomePage />
  </Frame>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import WelcomePage from "@/pages/welcome";

export default defineComponent({
  name: "RootFrame",
  components: {
    WelcomePage,
  },
});
</script>
