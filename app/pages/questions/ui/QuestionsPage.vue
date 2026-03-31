<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto" class="container">
      <StackLayout row="0" class="topBar">
        <GridLayout columns="42, *, 48" class="headerRow">
          <GridLayout col="0" class="closeButton" @tap="closePage">
            <Label text="×" class="closeIcon" />
          </GridLayout>

          <Label
            col="1"
            :text="progressLabel"
            class="progressLabel"
            horizontalAlignment="center"
          />

          <Label
            col="2"
            :text="timerText"
            class="timerLabel"
            horizontalAlignment="right"
          />
        </GridLayout>

        <GridLayout class="progressTrack">
          <StackLayout
            :width="progressWidth"
            class="progressFill"
            horizontalAlignment="left"
          />
        </GridLayout>
      </StackLayout>

      <StackLayout row="1" class="questionSection" verticalAlignment="middle">
        <Label :text="question.category" class="categoryBadge" />
        <StackLayout class="questionCard">
          <Label :text="question.title" class="questionTitle" textWrap="true" />
          <Label
            :text="question.description"
            class="questionSubtitle"
            textWrap="true"
          />
        </StackLayout>
      </StackLayout>

      <StackLayout row="2" class="bottomArea">
        <Button
          v-if="!isRecording"
          text="Start Recording"
          class="recordButton"
          @tap="startRecording"
        />

        <StackLayout v-else class="recordingCard">
          <Label text="Recording..." class="recordingTitle" />
          <Label text="~ ~ ~ ~ ~" class="waveText" />
        </StackLayout>

        <Button
          v-if="isRecording"
          text="Stop answer"
          class="stopButton"
          @tap="stopRecording"
        />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import { createActor, type ActorRefFrom } from "xstate";

import { questionSessionMachine } from "@/features/submit-answer";
import PracticePage from "@/pages/practice";
import ResultsPage from "@/pages/results";

const QUESTIONS = [
  {
    category: "Technical",
    title: "Explain the difference between REST and GraphQL APIs",
    description:
      "Provide a comprehensive answer discussing the key differences, use cases, and trade-offs.",
  },
  {
    category: "Behavioral",
    title: "Tell me about a time you had a conflict in your team",
    description:
      "Describe the situation, your actions, and what changed after your intervention.",
  },
  {
    category: "System Design",
    title: "How would you design a notification service for a mobile app?",
    description:
      "Focus on architecture, scaling, delivery guarantees, and monitoring.",
  },
];

type QuestionSessionActor = ActorRefFrom<typeof questionSessionMachine>;

function parseTimeLimitToSeconds(timeLimit: string): number {
  const match = timeLimit.match(/\d+/);
  if (!match) {
    return 60;
  }
  const parsed = Number.parseInt(match[0], 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 60;
}

function formatSeconds(totalSeconds: number): string {
  const safe = Math.max(0, totalSeconds);
  const minutes = Math.floor(safe / 60);
  const seconds = safe % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

export default defineComponent({
  name: "QuestionsPage",
  props: {
    currentQuestionIndex: {
      type: Number,
      default: 0,
    },
    totalQuestions: {
      type: Number,
      default: 3,
    },
    selectedCategory: {
      type: String,
      default: "Technical",
    },
    timeLimit: {
      type: String,
      default: "60 sec",
    },
  },
  data() {
    return {
      isRecording: false,
      remainingSeconds: parseTimeLimitToSeconds(this.timeLimit),
      sessionActor: null as QuestionSessionActor | null,
      sessionSubscription: null as { unsubscribe: () => void } | null,
      timerInterval: null as ReturnType<typeof setInterval> | null,
      hasNavigatedToResults: false,
    };
  },
  mounted() {
    const actor = createActor(questionSessionMachine, {
      input: {
        totalSeconds: parseTimeLimitToSeconds(this.timeLimit),
      },
    });

    this.sessionActor = actor;
    this.sessionSubscription = actor.subscribe((snapshot) => {
      this.isRecording = snapshot.context.isRecording;
      this.remainingSeconds = snapshot.context.remainingSeconds;

      if (snapshot.matches("recording")) {
        this.startTicking();
      } else {
        this.stopTicking();
      }

      if (snapshot.matches("timeout")) {
        this.goToResults();
      }
    });

    actor.start();
  },
  beforeUnmount() {
    this.stopTicking();
    this.sessionSubscription?.unsubscribe();
    this.sessionActor?.stop();
  },
  computed: {
    question(): { category: string; title: string; description: string } {
      return QUESTIONS[this.currentQuestionIndex % QUESTIONS.length];
    },
    progressLabel(): string {
      return `Question ${this.currentQuestionIndex + 1} of ${this.totalQuestions}`;
    },
    progressWidth(): number {
      const maxWidth = 132;
      return maxWidth * ((this.currentQuestionIndex + 1) / this.totalQuestions);
    },
    timerText(): string {
      return formatSeconds(this.remainingSeconds);
    },
  },
  methods: {
    startTicking() {
      if (this.timerInterval) {
        return;
      }
      this.timerInterval = setInterval(() => {
        this.sessionActor?.send({ type: "TICK" });
      }, 1000);
    },
    stopTicking() {
      if (!this.timerInterval) {
        return;
      }
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    },
    closePage() {
      this.$navigateTo(PracticePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
    startRecording() {
      this.sessionActor?.send({ type: "START_RECORDING" });
    },
    stopRecording() {
      this.sessionActor?.send({ type: "STOP_RECORDING" });
      this.goToResults();
    },
    goToResults() {
      if (this.hasNavigatedToResults) {
        return;
      }
      this.hasNavigatedToResults = true;
      this.stopTicking();
      this.$navigateTo(ResultsPage, {
        clearHistory: true,
        props: {
          currentQuestionIndex: this.currentQuestionIndex,
          totalQuestions: this.totalQuestions,
          score: 82,
          timeLimit: this.timeLimit,
        },
        transition: {
          name: "slideLeft",
          duration: 250,
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

.container {
  width: 100%;
  height: 100%;
  padding-top: 54;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.topBar {
  margin-bottom: 12;
}

.headerRow {
  vertical-align: middle;
  align-items: center;
}

.closeButton {
  width: 42;
  height: 42;
  border-radius: 21;
  background-color: #ffffff;
  border-width: 1;
  border-color: #e5e7eb;
  justify-content: center;
  align-items: center;
}

.closeIcon {
  font-size: 24;
  color: #111827;
  text-align: center;
}

.progressLabel {
  font-size: 12;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
  text-align: center;
  padding-right: 8;
  padding-left: 8;
  vertical-align: middle;
}

.timerLabel {
  font-size: 12;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
  text-align: right;
  vertical-align: middle;
}

.progressTrack {
  margin-top: 12;
  height: 6;
  border-radius: 3;
  background-color: #e5e7eb;
}

.progressFill {
  height: 6;
  border-radius: 3;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

.questionSection {
  justify-content: center;
}

.categoryBadge {
  margin-bottom: 12;
  padding-top: 8;
  padding-right: 18;
  padding-bottom: 8;
  padding-left: 18;
  border-radius: 16;
  background-color: #6d4df5;
  color: #ffffff;
  font-size: 13;
  font-weight: 600;
  font-family: "Poppins";
  horizontal-align: center;
}

.questionCard {
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 30;
  padding-right: 24;
  padding-bottom: 28;
  padding-left: 24;
  border-width: 1;
  border-color: #e5e7eb;
}

.questionTitle {
  font-size: 28;
  font-weight: 600;
  color: #111827;
  text-align: center;
  font-family: "Poppins";
}

.questionSubtitle {
  margin-top: 50;
  font-size: 15;
  color: #6b7280;
  text-align: center;
  font-family: "Poppins";
}

.bottomArea {
  padding-top: 16;
}

.recordButton {
  height: 72;
  border-radius: 26;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 20;
  font-weight: 600;
  font-family: "Poppins";
}

.recordingCard {
  border-radius: 22;
  background-color: #e5e7eb;
  padding-top: 18;
  padding-right: 18;
  padding-bottom: 18;
  padding-left: 18;
}

.recordingTitle {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  text-align: center;
  font-family: "Poppins";
}

.waveText {
  margin-top: 12;
  font-size: 20;
  color: #6d4df5;
  text-align: center;
  font-family: "Poppins";
}

.stopButton {
  margin-top: 12;
  height: 56;
  border-radius: 20;
  background-color: #ffffff;
  border-width: 1;
  border-color: #c7d2fe;
  color: #4f46e5;
  font-size: 18;
  font-weight: 600;
  font-family: "Poppins";
}
</style>
