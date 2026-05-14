<template>
  <GridLayout columns="*, *" rows="auto, auto, auto, auto" class="categoryGrid">
    <StackLayout
      v-for="(category, index) in categories"
      :key="category.id"
      :row="Math.floor(index / 2)"
      :col="index % 2"
      class="categoryCard"
      :class="[
        index % 2 === 0 ? 'categoryLeft' : 'categoryRight',
        index < 6 ? 'categoryTop' : '',
        selectedCategory === category.id ? 'selectedCard' : '',
      ]"
      @tap="onSelect(category.id)"
    >
      <Label :text="category.icon" class="categoryIcon" />
      <Label :text="category.title" class="categoryText" textWrap="true" />
    </StackLayout>
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type { PracticeCategory } from "@/entities/practice";

type CategoryOption = {
  id: PracticeCategory;
  icon: string;
  title: string;
};

const categoryOptions: CategoryOption[] = [
  { id: "adaptability", icon: "A", title: "Adaptability" },
  { id: "career-goals", icon: "G", title: "Career Goals" },
  { id: "conflict-resolution", icon: "C", title: "Conflict Resolution" },
  { id: "culture-fit", icon: "F", title: "Culture Fit" },
  { id: "leadership", icon: "L", title: "Leadership" },
  { id: "motivation", icon: "M", title: "Motivation" },
  { id: "team-collaboration", icon: "T", title: "Team Collaboration" },
  { id: "work-style", icon: "W", title: "Work Style" },
];

export default defineComponent({
  name: "CategoryPicker",
  emits: ["select"],
  props: {
    selectedCategory: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      categories: categoryOptions,
    };
  },
  methods: {
    onSelect(category: PracticeCategory) {
      this.$emit("select", category);
    },
  },
});
</script>

<style scoped>
.categoryGrid {
  margin-top: 14;
}

.categoryCard {
  height: 104;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 20;
  background-color: #f8fafc;
  padding-top: 14;
  padding-right: 12;
  padding-bottom: 12;
  padding-left: 12;
}

.categoryLeft {
  margin-right: 8;
}

.categoryRight {
  margin-left: 8;
}

.categoryTop {
  margin-bottom: 12;
}

.selectedCard {
  border-color: #6366f1;
  background-color: #ede9fe;
}

.categoryIcon {
  width: 30;
  height: 30;
  border-radius: 15;
  background-color: #4f46e5;
  color: #ffffff;
  font-size: 15;
  font-weight: 700;
  text-align: center;
  font-family: "Poppins";
}

.categoryText {
  margin-top: 8;
  font-size: 15;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}
</style>
