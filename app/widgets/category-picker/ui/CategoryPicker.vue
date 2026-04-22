<template>
  <GridLayout columns="*, *" rows="auto, auto" class="categoryGrid">
    <StackLayout
      v-for="(category, index) in categories"
      :key="category.id"
      :row="Math.floor(index / 2)"
      :col="index % 2"
      class="categoryCard"
      :class="[
        index % 2 === 0 ? 'categoryLeft' : 'categoryRight',
        index < 2 ? 'categoryTop' : '',
        selectedCategory === category.id ? 'selectedCard' : '',
      ]"
      @tap="onSelect(category.id)"
    >
      <Label :text="category.icon" class="categoryIcon" />
      <Label :text="category.title" class="categoryText" />
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
  { id: "hr", icon: "💼", title: "HR Questions" },
  { id: "technical", icon: "💻", title: "Technical" },
  { id: "behavioral", icon: "🗣", title: "Behavioral" },
  { id: "system-design", icon: "🗂", title: "System Design" },
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
  height: 116;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 22;
  background-color: #f8fafc;
  padding-top: 16;
  padding-right: 16;
  padding-bottom: 16;
  padding-left: 16;
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
  font-size: 28;
}

.categoryText {
  margin-top: 8;
  font-size: 16;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
}
</style>

