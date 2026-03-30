<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto" class="container">
      <StackLayout row="0" class="hero">
        <Label text="Your score" class="heroLabel" />
        <Label :text="String(score)" class="scoreValue" />
        <Label text="Great performance!" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <StackLayout v-if="showBreakdown" class="card radarCard">
            <Label text="Performance Breakdown" class="cardTitle" />
            <GridLayout
              columns="*, *, *, *"
              rows="auto, auto"
              class="radarGrid"
            >
              <Label
                row="0"
                col="0"
                text="Examples"
                class="axisLabel leftLabel"
              />
              <Label
                row="0"
                col="1"
                text="Confidence"
                class="axisLabel topLabel"
              />
              <Label
                row="0"
                col="3"
                text="Clarity"
                class="axisLabel rightLabel"
              />
              <Label
                row="1"
                col="0"
                text="Technical"
                class="axisLabel bottomLeftLabel"
              />
              <Label
                row="1"
                col="3"
                text="Structure"
                class="axisLabel bottomRightLabel"
              />
            </GridLayout>
            <StackLayout class="radarShapeWrap">
              <Label text="◈" class="radarShape" />
            </StackLayout>
          </StackLayout>

          <StackLayout v-if="showBreakdown" class="card strengthsCard">
            <Label text="Strengths" class="cardTitle successTitle" />
            <Label
              text="• Clear articulation of key concept"
              class="cardItem successItem"
            />
            <Label
              text="• Good use of real-world examples"
              class="cardItem successItem"
            />
            <Label
              text="• Structured approach to answering"
              class="cardItem successItem"
            />
          </StackLayout>

          <StackLayout class="card improveCard">
            <Label
              text="Suggestion for improvement"
              class="cardTitle warningTitle"
            />
            <Label
              text="• Work on reducing filler words"
              class="cardItem warningItem"
            />
            <Label
              v-if="!isLastQuestion"
              text="• Consider providing more specific technical details"
              class="cardItem warningItem"
            />
            <Label
              v-if="!isLastQuestion"
              text="• Add comparison of trade-offs between options"
              class="cardItem warningItem"
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
          text="Finish Session"
          class="secondaryButton"
          @tap="finishSession"
        />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import AnalyticsPage from "./AnalyticsPage.vue";
import QuestionsPage from "./QuestionsPage.vue";

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
      default: 82,
    },
  },
  computed: {
    isLastQuestion(): boolean {
      return this.currentQuestionIndex >= this.totalQuestions - 1;
    },
    showBreakdown(): boolean {
      return this.currentQuestionIndex === 0;
    },
  },
  methods: {
    nextQuestion() {
      this.$navigateTo(QuestionsPage, {
        clearHistory: true,
        props: {
          currentQuestionIndex: this.currentQuestionIndex + 1,
          totalQuestions: this.totalQuestions,
        },
        transition: {
          name: "slideLeft",
          duration: 250,
          curve: "easeInOut",
        },
      });
    },
    finishSession() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
        transition: {
          name: "fade",
          duration: 220,
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

.radarGrid {
  margin-top: 10;
}

.axisLabel {
  font-size: 11;
  color: #9ca3af;
  font-family: "Poppins";
}

.leftLabel {
  horizontal-align: left;
}

.topLabel {
  horizontal-align: center;
}

.rightLabel {
  horizontal-align: right;
}

.bottomLeftLabel {
  margin-top: 74;
  horizontal-align: left;
}

.bottomRightLabel {
  margin-top: 74;
  horizontal-align: right;
}

.radarShapeWrap {
  align-items: center;
  margin-top: -8;
}

.radarShape {
  font-size: 128;
  color: #818cf8;
  text-align: center;
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
  line-height: 20;
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
