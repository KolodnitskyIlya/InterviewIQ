<template>
  <StackLayout class="hero">
    <FlexboxLayout class="heroRow" alignItems="center">
      <GridLayout class="backButton" @tap="$emit('back')">
        <Label text="←" class="backIcon" />
      </GridLayout>
      <Label text="Settings" class="heroTitle" />
    </FlexboxLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "SettingsHeader",
  emits: ["back"],
});
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  padding-top: 70;
  padding-right: 24;
  padding-bottom: 22;
  padding-left: 24;
}

.heroRow {
  min-height: 56;
}

.backButton {
  width: 48;
  height: 48;
  border-radius: 24;
  background-color: rgba(99, 102, 241, 0.55);
  justify-content: center;
  align-items: center;
}

.backIcon {
  font-size: 30;
  color: #ffffff;
  text-align: center;
}

.heroTitle {
  margin-left: 14;
  font-size: 52;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}
</style>
