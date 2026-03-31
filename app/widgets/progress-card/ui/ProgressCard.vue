<template>
  <GridLayout columns="auto, *" class="readinessCard">
    <StackLayout
      col="0"
      class="progressContainer"
      horizontalAlignment="center"
      verticalAlignment="center"
    >
      <StackLayout class="scorePanel">
        <Label :text="valueLabel" class="progressValue" />
        <GridLayout class="meterTrack">
          <StackLayout
            :width="meterWidth"
            class="meterFill"
            horizontalAlignment="left"
          />
        </GridLayout>
      </StackLayout>
    </StackLayout>

    <StackLayout col="1" class="readinessInfo">
      <Label :text="title" class="cardTitle" textWrap="true" />
      <Label :text="subtitle" class="cardSubtitle" textWrap="true" />
      <FlexboxLayout class="growthRow" alignItems="center">
        <Label text="↗" class="growthArrow" />
        <Label :text="trend" class="cardGrowth" />
      </FlexboxLayout>
    </StackLayout>
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "ProgressCard",
  props: {
    value: {
      type: Number,
      default: 78,
    },
    title: {
      type: String,
      default: "Interview Readiness",
    },
    subtitle: {
      type: String,
      default: "You're doing great! Keep practicing.",
    },
    trend: {
      type: String,
      default: "+8% this week",
    },
  },
  computed: {
    clampedValue(): number {
      return Math.max(0, Math.min(100, Math.round(this.value)));
    },
    valueLabel(): string {
      return `${this.clampedValue}%`;
    },
    meterWidth(): number {
      return 76 * (this.clampedValue / 100);
    },
  },
});
</script>

<style scoped>
.readinessCard {
  margin-top: 22;
  margin-right: 8;
  margin-left: 8;
  background-color: #ddd6fe;
  border-radius: 24;
  padding-top: 18;
  padding-right: 16;
  padding-bottom: 18;
  padding-left: 16;
}

.progressContainer {
  width: 112;
  margin-right: 14;
}

.scorePanel {
  width: 96;
  height: 96;
  border-radius: 28;
  background-color: #ede9fe;
  border-width: 2;
  border-color: #c4b5fd;
  padding-top: 20;
  padding-right: 10;
  padding-bottom: 16;
  padding-left: 10;
}

.progressValue {
  font-size: 24;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
  text-align: center;
}

.meterTrack {
  margin-top: 14;
  width: 76;
  height: 8;
  border-radius: 4;
  background-color: #d1d5db;
  horizontal-align: center;
}

.meterFill {
  height: 8;
  border-radius: 4;
  background: linear-gradient(90deg, #14b8a6, #3b82f6, #4f46e5);
}

.readinessInfo {
  vertical-align: middle;
}

.cardTitle {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  line-height: 22;
  font-family: "Poppins";
}

.cardSubtitle {
  margin-top: 6;
  font-size: 12;
  color: #4b5563;
  line-height: 16;
  font-family: "Poppins";
}

.growthRow {
  margin-top: 10;
}

.growthArrow {
  font-size: 16;
  color: #10b981;
  margin-right: 4;
  font-weight: 700;
  font-family: "Poppins";
}

.cardGrowth {
  font-size: 15;
  color: #111827;
  font-weight: 500;
  font-family: "Poppins";
}
</style>
