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
            :isEnabled="canStartPractice"
            :class="canStartPractice ? '' : 'startButtonDisabled'"
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
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";
import { createActor, type ActorRefFrom } from "xstate";

import type { PracticeCategory, PracticeDifficulty } from "@/entities/practice";
import {
  practiceSetupMachine,
  type PracticeSetupContext,
} from "@/features/start-practice";
import AnalyticsPage from "@/pages/analytics";
import HomePage from "@/pages/home";
import ProfilePage from "@/pages/profile";
import QuestionsPage from "@/pages/questions";
import SignInPage from "@/pages/sign-in";
import { ApiError, interviewIqApi } from "@/shared";
import BottomNavigation from "@/widgets/bottom-navigation";
import CategoryPicker from "@/widgets/category-picker";
import DifficultyPicker from "@/widgets/difficulty-picker";
import TimerPicker from "@/widgets/timer-picker";

type PracticeSetupActor = ActorRefFrom<typeof practiceSetupMachine>;

function parseTimeLimitToSeconds(timeLimit: string): number {
  const match = timeLimit.match(/\d+/);
  if (!match) {
    return 60;
  }
  const parsed = Number.parseInt(match[0], 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 60;
}

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
      selectedCategory: "" as PracticeSetupContext["selectedCategory"],
      selectedDifficulty: "" as PracticeSetupContext["selectedDifficulty"],
      selectedTime: "",
      canStartPractice: false,
      isStarting: false,
      timeOptions: ["30 sec", "45 sec", "60 sec", "90 sec", "120 sec"],
      practiceActor: null as PracticeSetupActor | null,
      practiceSubscription: null as { unsubscribe: () => void } | null,
    };
  },
  mounted() {
    const actor = createActor(practiceSetupMachine);
    this.practiceActor = actor;
    this.practiceSubscription = actor.subscribe((snapshot) => {
      this.selectedCategory = snapshot.context.selectedCategory;
      this.selectedDifficulty = snapshot.context.selectedDifficulty;
      this.selectedTime = snapshot.context.selectedTime;
      this.canStartPractice = snapshot.matches("ready");
    });
    actor.start();
  },
  beforeUnmount() {
    this.practiceSubscription?.unsubscribe();
    this.practiceActor?.stop();
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
      this.practiceActor?.send({ type: "SELECT_CATEGORY", category });
    },
    selectDifficulty(level: PracticeDifficulty) {
      this.practiceActor?.send({ type: "SELECT_DIFFICULTY", difficulty: level });
    },
    selectTime(option: string) {
      this.practiceActor?.send({ type: "SELECT_TIME", time: option });
    },
    async startPractice() {
      if (!this.canStartPractice || this.isStarting) {
        return;
      }

      this.isStarting = true;
      try {
        const timeLimitSec = parseTimeLimitToSeconds(this.selectedTime || "60 sec");
        const created = await interviewIqApi.createPracticeSession({
          category: this.selectedCategory || "technical",
          difficulty: this.selectedDifficulty || "easy",
          time_limit_sec: timeLimitSec,
          question_count: 3,
        });
        const started = await interviewIqApi.startPracticeSession(created.id);

        this.$navigateTo(QuestionsPage, {
          clearHistory: true,
          props: {
            sessionId: started.id,
            currentQuestionIndex: started.current_question_index,
            totalQuestions: started.question_count,
            timeLimitSec: started.time_limit_sec,
          },
          transition: {
            name: "slideLeft",
            duration: 280,
            curve: "easeInOut",
          },
        });
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
          return;
        }

        await alert({
          title: "Failed to start practice",
          message: error instanceof ApiError ? error.message : "Please try again.",
          okButtonText: "OK",
        });
      } finally {
        this.isStarting = false;
      }
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

.startButtonDisabled {
  opacity: 0.55;
}
</style>
