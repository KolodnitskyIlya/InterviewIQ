<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto, auto, *" class="container">
      <GridLayout
        row="1"
        class="square"
        horizontalAlignment="center"
        verticalAlignment="middle"
      >
        <Label
          :text="'⭐'"
          class="star"
          horizontalAlignment="right"
          verticalAlignment="top"
        />
        <Label
          :text="'🧠'"
          class="brain"
          horizontalAlignment="center"
          verticalAlignment="middle"
        />
      </GridLayout>

      <StackLayout row="2" class="textBlock" horizontalAlignment="center">
        <Label text="InterviewIQ" class="title" />
        <Label :text="'Prepare • Practice • Perform'" class="subtitle" />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import HowItWorksPage from "@/pages/how-it-works";

export default defineComponent({
  name: "WelcomePage",
  mounted() {
    setTimeout(() => {
      this.$navigateTo(HowItWorksPage);
    }, 3000);
  },
});
</script>

<style scoped>
.page {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

.container {
  width: 100%;
  height: 100%;
}

.square {
  width: 200;
  height: 200;
  background-color: white;
  border-radius: 30;
}

.brain {
  font-size: 90;
}

.star {
  font-size: 20;
  margin: 10;
}

.textBlock {
  margin-top: 20;
}

.title {
  font-size: 26;
  font-weight: 600;
  color: white;
  font-family: "Poppins";
  text-align: center;
}

.subtitle {
  font-size: 14;
  color: #e5e7eb;
  font-family: "Poppins";
  text-align: center;
}
</style>
