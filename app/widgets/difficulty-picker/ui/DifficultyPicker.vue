<template>
  <StackLayout>
    <GridLayout
      v-for="level in levels"
      :key="level.id"
      class="difficultyCard"
      :class="selectedDifficulty === level.id ? 'selectedCard' : ''"
      @tap="onSelect(level.id)"
    >
      <Label :text="level.label" class="difficultyText" />
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type { PracticeDifficulty } from "@/entities/practice";

type DifficultyOption = {
  id: PracticeDifficulty;
  label: string;
};

const difficultyLevels: DifficultyOption[] = [
  { id: "easy", label: "Easy" },
  { id: "medium", label: "Medium" },
  { id: "hard", label: "Hard" },
];

export default defineComponent({
  name: "DifficultyPicker",
  emits: ["select"],
  props: {
    selectedDifficulty: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      levels: difficultyLevels,
    };
  },
  methods: {
    onSelect(level: PracticeDifficulty) {
      this.$emit("select", level);
    },
  },
});
</script>

<style scoped>
.difficultyCard {
  margin-top: 10;
  min-height: 78;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 20;
  background-color: #f8fafc;
  padding-top: 22;
  padding-right: 24;
  padding-bottom: 22;
  padding-left: 24;
}

.difficultyText {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.selectedCard {
  border-color: #6366f1;
  background-color: #ede9fe;
}
</style>
