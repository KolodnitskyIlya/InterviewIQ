<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto">
      <StackLayout row="0" class="hero">
        <Label text="Practice Setup" class="heroTitle" />
        <Label text="Customize your practice session" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <Label text="Select Category" class="sectionTitle" />
          <CategoryPicker
            :selectedCategory="selectedCategory"
            @select="selectCategory"
          />

          <Label text="Select Difficulty" class="sectionTitle difficultyTitle" />
          <DifficultyPicker
            :selectedDifficulty="selectedDifficulty"
            @select="selectDifficulty"
          />

          <TimerPicker
            :selectedTime="selectedTime"
            :options="timeOptions"
            class="timePicker"
            @select="selectTime"
          />

          <Button
            text="▷ Start Practice"
            class="startButton"
            @tap="startPractice"
          />
        </StackLayout>
      </ScrollView>

      <BottomNavigation
        row="2"
        activeTab="practice"
        @home="goHome"
        @analytics="openAnalytics"
        @profile="openProfile"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type { PracticeCategory, PracticeDifficulty } from "@/entities/practice";
import AnalyticsPage from "@/pages/analytics";
import HomePage from "@/pages/home";
import ProfilePage from "@/pages/profile";
import QuestionsPage from "@/pages/questions";
import BottomNavigation from "@/widgets/bottom-navigation";
import CategoryPicker from "@/widgets/category-picker";
import DifficultyPicker from "@/widgets/difficulty-picker";
import TimerPicker from "@/widgets/timer-picker";

export default defineComponent({
  name: "PracticePage",
  components: {
    BottomNavigation,
    CategoryPicker,
    DifficultyPicker,
    TimerPicker,
  },
  data() {
    return {
      selectedCategory: "" as PracticeCategory | "",
      selectedDifficulty: "" as PracticeDifficulty | "",
      selectedTime: "",
      timeOptions: ["30 sec", "45 sec", "60 sec", "90 sec", "120 sec"],
    };
  },
  methods: {
    goHome() {
      this.$navigateTo(HomePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openProfile() {
      this.$navigateTo(ProfilePage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openAnalytics() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    selectCategory(category: PracticeCategory) {
      this.selectedCategory = category;
    },
    selectDifficulty(level: PracticeDifficulty) {
      this.selectedDifficulty = level;
    },
    selectTime(option: string) {
      this.selectedTime = option;
    },
    startPractice() {
      this.$navigateTo(QuestionsPage, {
        clearHistory: true,
        props: {
          currentQuestionIndex: 0,
          totalQuestions: 3,
          selectedCategory: this.selectedCategory || "technical",
        },
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
  },
});
</script>

<style scoped>
.page {
  background-color: #f3f4f6;
}

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 52;
  border-bottom-left-radius: 52;
  padding-top: 64;
  padding-right: 28;
  padding-bottom: 30;
  padding-left: 28;
}

.heroTitle {
  font-size: 44;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}

.heroSubtitle {
  margin-top: 6;
  font-size: 15;
  font-weight: 600;
  color: #e5e7eb;
  font-family: "Poppins";
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.sectionTitle {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.difficultyTitle {
  margin-top: 18;
}

.timePicker {
  margin-top: 8;
}

.startButton {
  margin-top: 22;
  height: 68;
  border-radius: 24;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 24;
  font-weight: 600;
  font-family: "Poppins";
}
</style>
