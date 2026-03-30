<template>
  <GridLayout columns="auto, *" class="readinessCard">
    <StackLayout
      col="0"
      class="progressContainer"
      horizontalAlignment="center"
      verticalAlignment="center"
    >
      <GridLayout class="progressOuter">
        <GridLayout class="progressTrack" />
        <GridLayout class="progressArc" :style="`rotate: ${progressRotation};`" />
        <GridLayout class="progressInner">
          <Label
            :text="valueLabel"
            class="progressValue"
            horizontalAlignment="center"
            verticalAlignment="center"
          />
        </GridLayout>
      </GridLayout>
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
    progressRotation(): number {
      return -140 + this.clampedValue * 2.4;
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

.progressOuter {
  width: 108;
  height: 108;
  border-radius: 54;
  justify-content: center;
  align-items: center;
}

.progressTrack {
  width: 108;
  height: 108;
  border-width: 7;
  border-color: #d1d5db;
  border-radius: 54;
}

.progressArc {
  width: 108;
  height: 108;
  border-width: 7;
  border-radius: 54;
  border-top-color: #14b8a6;
  border-right-color: #3b82f6;
  border-bottom-color: #4f46e5;
  border-left-color: transparent;
  justify-content: center;
  align-items: center;
}

.progressInner {
  width: 82;
  height: 82;
  border-radius: 41;
  background-color: #ede9fe;
  justify-content: center;
  align-items: center;
}

.progressValue {
  font-size: 22;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
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
