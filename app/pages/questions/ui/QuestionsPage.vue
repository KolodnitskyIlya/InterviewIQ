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
        <TextView
          :text="answerText"
          hint="Type your answer..."
          class="answerInput"
          editable="true"
          @textChange="onAnswerTextChange"
        />

        <Button
          :text="recordButtonText"
          class="voiceButton"
          @tap="toggleRecording"
        />

        <Button
          :text="isSubmitting ? 'Submitting...' : 'Submit answer'"
          class="recordButton"
          :isEnabled="canSubmit"
          :class="canSubmit ? '' : 'submitButtonDisabled'"
          @tap="submitCurrentAnswer"
        />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";

import {
  cancelAudioRecording,
  startAudioRecording,
  stopAudioRecording,
  type RecordedAudio,
} from "@/features/submit-answer";
import PracticePage from "@/pages/practice";
import ResultsPage from "@/pages/results";
import SignInPage from "@/pages/sign-in";
import { ApiError, interviewIqApi, type QuestionItemResponse } from "@/shared";

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
    timeLimitSec: {
      type: Number,
      default: 60,
    },
    sessionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      questionData: null as QuestionItemResponse | null,
      answerText: "",
      recordedAudio: null as RecordedAudio | null,
      isRecording: false,
      isLoading: false,
      isSubmitting: false,
      remainingSeconds: this.timeLimitSec,
      timerInterval: null as ReturnType<typeof setInterval> | null,
      hasNavigatedToResults: false,
    };
  },
  mounted() {
    void this.loadCurrentQuestion();
    this.startTicking();
  },
  beforeUnmount() {
    this.stopTicking();
    if (this.isRecording) {
      cancelAudioRecording();
    }
  },
  computed: {
    question(): QuestionItemResponse {
      return (
        this.questionData ?? {
          id: "",
          category: this.selectedCategory,
          difficulty: "",
          title: this.isLoading ? "Loading question..." : "Question unavailable",
          description: this.isLoading ? "Please wait." : "Try going back and starting a new session.",
        }
      );
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
    canSubmit(): boolean {
      return Boolean(this.questionData?.id) && !this.isSubmitting;
    },
    recordButtonText(): string {
      if (this.isRecording) {
        return "Stop voice answer";
      }
      return this.recordedAudio ? "Record again" : "Record voice answer";
    },
  },
  methods: {
    async loadCurrentQuestion() {
      this.isLoading = true;
      try {
        const response = await interviewIqApi.getCurrentQuestion(this.sessionId);
        this.questionData = response.question;
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
          return;
        }

        await alert({
          title: "Failed to load question",
          message: error instanceof ApiError ? error.message : "Please try again.",
          okButtonText: "OK",
        });
      } finally {
        this.isLoading = false;
      }
    },
    startTicking() {
      if (this.timerInterval) {
        return;
      }
      this.timerInterval = setInterval(() => {
        this.remainingSeconds = Math.max(0, this.remainingSeconds - 1);
        if (this.remainingSeconds === 0) {
          void this.submitCurrentAnswer();
        }
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
    onAnswerTextChange(args: { value?: string; object?: { text?: string } }) {
      this.answerText = args.value ?? args.object?.text ?? "";
    },
    async toggleRecording() {
      if (this.isSubmitting) {
        return;
      }

      try {
        if (!this.isRecording) {
          startAudioRecording();
          this.recordedAudio = null;
          this.isRecording = true;
          return;
        }

        this.recordedAudio = stopAudioRecording();
        this.isRecording = false;
      } catch (error) {
        this.isRecording = false;
        await alert({
          title: "Voice recording unavailable",
          message: error instanceof Error ? error.message : "Please use text answer for now.",
          okButtonText: "OK",
        });
      }
    },
    async submitCurrentAnswer() {
      if (!this.questionData || this.isSubmitting || this.hasNavigatedToResults) {
        return;
      }

      this.isSubmitting = true;
      this.stopTicking();

      try {
        let audioUrl: string | null = null;
        let audioId: string | null = null;

        if (this.isRecording) {
          this.recordedAudio = stopAudioRecording();
          this.isRecording = false;
        }

        if (this.recordedAudio) {
          const upload = await interviewIqApi.uploadAnswerAudio(this.sessionId, {
            question_id: this.questionData.id,
            file_name: this.recordedAudio.fileName,
            content_type: this.recordedAudio.contentType,
            audio_base64: this.recordedAudio.audioBase64,
          });
          audioUrl = upload.audio_url;
          audioId = upload.audio_id;
        }

        const answer = await interviewIqApi.submitAnswer(this.sessionId, {
          question_id: this.questionData.id,
          answer_text: this.answerText.trim() || null,
          audio_url: audioUrl,
          audio_id: audioId,
        });
        const analysis = await interviewIqApi.getAnswerAnalysis(this.sessionId, answer.answer_id);
        this.goToResults(answer.answer_id, analysis.overall_score);
      } catch (error) {
        this.startTicking();
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
          return;
        }

        await alert({
          title: "Failed to submit answer",
          message: error instanceof ApiError ? error.message : "Please try again.",
          okButtonText: "OK",
        });
      } finally {
        this.isSubmitting = false;
      }
    },
    goToResults(answerId: string, score: number) {
      if (this.hasNavigatedToResults) {
        return;
      }
      this.hasNavigatedToResults = true;
      this.stopTicking();
      this.$navigateTo(ResultsPage, {
        clearHistory: true,
        props: {
          sessionId: this.sessionId,
          answerId,
          currentQuestionIndex: this.currentQuestionIndex,
          totalQuestions: this.totalQuestions,
          score,
          timeLimitSec: this.timeLimitSec,
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

.answerInput {
  height: 120;
  border-radius: 20;
  border-width: 1;
  border-color: #d1d5db;
  background-color: #ffffff;
  padding-top: 14;
  padding-right: 16;
  padding-bottom: 14;
  padding-left: 16;
  font-size: 16;
  color: #111827;
  font-family: "Poppins";
}

.recordButton {
  margin-top: 12;
  height: 72;
  border-radius: 26;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 20;
  font-weight: 600;
  font-family: "Poppins";
}

.voiceButton {
  margin-top: 10;
  height: 54;
  border-radius: 20;
  background-color: #ffffff;
  border-width: 1;
  border-color: #c7d2fe;
  color: #4f46e5;
  font-size: 17;
  font-weight: 600;
  font-family: "Poppins";
}

.submitButtonDisabled {
  opacity: 0.55;
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
