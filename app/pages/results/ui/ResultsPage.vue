<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto" class="container">
      <StackLayout row="0" class="hero">
        <Label text="Your score" class="heroLabel" />
        <Label :text="String(score)" class="scoreValue" />
        <Label text="Answer analysis" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <StackLayout class="card radarCard">
            <Label text="Performance Breakdown" class="cardTitle" />
            <StackLayout class="breakdownList">
              <StackLayout
                v-for="item in breakdownScores"
                :key="item.label"
                class="breakdownItem"
              >
                <GridLayout columns="*, auto" class="breakdownHeader">
                  <Label col="0" :text="item.label" class="axisLabel" />
                  <Label col="1" :text="item.value + '%'" class="axisValue" />
                </GridLayout>
                <GridLayout class="breakdownTrack">
                  <StackLayout
                    :width="breakdownWidth(item.value)"
                    class="breakdownFill"
                    horizontalAlignment="left"
                  />
                </GridLayout>
              </StackLayout>
            </StackLayout>
          </StackLayout>

          <StackLayout class="card strengthsCard">
            <Label text="Strengths" class="cardTitle successTitle" />
            <Label
              v-for="item in strengths"
              :key="item"
              :text="'• ' + item"
              class="cardItem successItem"
              textWrap="true"
            />
          </StackLayout>

          <StackLayout class="card improveCard">
            <Label text="Suggestion for improvement" class="cardTitle warningTitle" />
            <Label
              v-for="item in improvements"
              :key="item"
              :text="'• ' + item"
              class="cardItem warningItem"
              textWrap="true"
            />
          </StackLayout>
        </StackLayout>
      </ScrollView>

      <StackLayout row="2" class="bottomActions">
        <Button
          v-if="!isLastQuestion"
          text="Next question"
          class="primaryButton"
          @tap="nextQuestion"
        />
        <Button
          :text="isFinishing ? 'Finishing...' : 'Finish Session'"
          class="secondaryButton"
          @tap="finishSession"
        />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";
import { createActor, type ActorRefFrom } from "xstate";

import type { BreakdownScore } from "@/entities/session";
import { defaultBreakdownScores } from "@/entities/session";
import { resultsFlowMachine } from "@/features/finish-session";
import AnalyticsPage from "@/pages/analytics";
import QuestionsPage from "@/pages/questions";
import SignInPage from "@/pages/sign-in";
import { ApiError, interviewIqApi, type AnswerAnalysisResponse } from "@/shared";

type ResultsFlowActor = ActorRefFrom<typeof resultsFlowMachine>;

function toPercent(value: number): number {
  return Math.round(Math.max(0, Math.min(1, value)) * 100);
}

function toLabel(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default defineComponent({
  name: "ResultsPage",
  props: {
    currentQuestionIndex: {
      type: Number,
      default: 0,
    },
    totalQuestions: {
      type: Number,
      default: 3,
    },
    score: {
      type: Number,
      default: 0,
    },
    timeLimitSec: {
      type: Number,
      default: 60,
    },
    sessionId: {
      type: String,
      required: true,
    },
    answerId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      flowActor: null as ResultsFlowActor | null,
      flowSubscription: null as { unsubscribe: () => void } | null,
      isLastQuestion: this.currentQuestionIndex >= this.totalQuestions - 1,
      breakdownScores: [...defaultBreakdownScores] as BreakdownScore[],
      analysisData: null as AnswerAnalysisResponse | null,
      strengths: ["Relevant answer direction"] as string[],
      improvements: ["Add more measurable details"] as string[],
      isFinishing: false,
    };
  },
  mounted() {
    const actor = createActor(resultsFlowMachine, {
      input: {
        currentQuestionIndex: this.currentQuestionIndex,
        totalQuestions: this.totalQuestions,
      },
    });
    this.flowActor = actor;
    this.flowSubscription = actor.subscribe((snapshot) => {
      const index = snapshot.context.currentQuestionIndex;
      this.isLastQuestion = index >= snapshot.context.totalQuestions - 1;
    });
    actor.start();
    void this.loadAnalysis();
  },
  beforeUnmount() {
    this.flowSubscription?.unsubscribe();
    this.flowActor?.stop();
  },
  methods: {
    async loadAnalysis() {
      try {
        const analysis = await interviewIqApi.getAnswerAnalysis(this.sessionId, this.answerId);
        this.analysisData = analysis;
        this.strengths = analysis.strengths;
        this.improvements = analysis.to_improve;
        this.breakdownScores = Object.entries(analysis.scores_by_category).map(
          ([label, value]) => ({
            label: toLabel(label),
            value: toPercent(value),
          }),
        );
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
        }
      }
    },
    breakdownWidth(value: number) {
      return 180 * (Math.max(0, Math.min(100, value)) / 100);
    },
    async nextQuestion() {
      if (!this.flowActor) {
        return;
      }

      try {
        const next = await interviewIqApi.nextQuestion(this.sessionId);
        this.flowActor.send({ type: "NEXT_QUESTION" });
        this.$navigateTo(QuestionsPage, {
          clearHistory: true,
          props: {
            sessionId: this.sessionId,
            currentQuestionIndex: next.current_question_index,
            totalQuestions: next.total_questions,
            timeLimitSec: this.timeLimitSec,
          },
          transition: {
            name: "slideLeft",
            duration: 250,
            curve: "easeInOut",
          },
        });
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
          return;
        }

        await alert({
          title: "Failed to load next question",
          message: error instanceof ApiError ? error.message : "Please finish the session.",
          okButtonText: "OK",
        });
      }
    },
    async finishSession() {
      if (this.isFinishing) {
        return;
      }

      this.isFinishing = true;
      try {
        this.flowActor?.send({ type: "FINISH_SESSION" });
        await interviewIqApi.finishPracticeSession(this.sessionId);
        await interviewIqApi.getSessionResults(this.sessionId);
        this.$navigateTo(AnalyticsPage, {
          clearHistory: true,
          transition: {
            name: "fade",
            duration: 220,
            curve: "easeInOut",
          },
        });
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          this.$navigateTo(SignInPage, { clearHistory: true });
          return;
        }

        await alert({
          title: "Failed to finish session",
          message: error instanceof ApiError ? error.message : "Please try again.",
          okButtonText: "OK",
        });
      } finally {
        this.isFinishing = false;
      }
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
}

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 44;
  border-bottom-left-radius: 44;
  padding-top: 48;
  padding-right: 24;
  padding-bottom: 30;
  padding-left: 24;
  align-items: center;
}

.heroLabel {
  font-size: 14;
  color: #e5e7eb;
  font-family: "Poppins";
}

.scoreValue {
  margin-top: 8;
  font-size: 54;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}

.heroSubtitle {
  margin-top: 8;
  font-size: 18;
  font-weight: 600;
  color: #ffffff;
  font-family: "Poppins";
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.card {
  border-radius: 24;
  padding-top: 16;
  padding-right: 16;
  padding-bottom: 16;
  padding-left: 16;
  margin-bottom: 16;
}

.radarCard {
  background-color: #ffffff;
}

.cardTitle {
  font-size: 16;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.breakdownList {
  margin-top: 14;
}

.breakdownItem {
  margin-bottom: 12;
}

.breakdownHeader {
  margin-bottom: 6;
}

.axisLabel {
  font-size: 13;
  color: #6b7280;
  font-family: "Poppins";
}

.axisValue {
  font-size: 13;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
  text-align: right;
}

.breakdownTrack {
  width: 180;
  height: 10;
  border-radius: 5;
  background-color: #e5e7eb;
}

.breakdownFill {
  height: 10;
  border-radius: 5;
  background: linear-gradient(90deg, #818cf8, #6366f1);
}

.strengthsCard {
  background: linear-gradient(135deg, #d1fae5, #bbf7d0);
}

.successTitle {
  color: #065f46;
}

.successItem {
  color: #065f46;
}

.improveCard {
  background: linear-gradient(135deg, #fef3c7, #ffedd5);
  border-width: 1;
  border-color: #f59e0b;
}

.warningTitle {
  color: #92400e;
}

.warningItem {
  color: #92400e;
}

.cardItem {
  margin-top: 8;
  font-size: 14;
  line-height: 16;
  font-family: "Poppins";
}

.bottomActions {
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.primaryButton {
  height: 54;
  border-radius: 20;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 17;
  font-weight: 600;
  font-family: "Poppins";
}

.secondaryButton {
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
</style>
