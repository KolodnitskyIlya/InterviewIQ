<template>
  <Page class="page">
    <GridLayout rows="auto,*,auto" class="container">
      <!-- Заголовок -->
      <Label text="How it Works" class="title" row="0" />

      <!-- Шаги -->
      <GridLayout row="1" rows="*,*,*" class="steps" columns="*">
        <FlexboxLayout class="step" orientation="row" row="0" column="0" alignItems="center">
          <StackLayout class="emojiBox step1">
            <Label text="💬" class="icon"/>
          </StackLayout>
          <StackLayout class="textBox">
            <Label text="Get AI Questions" class="stepTitle" textWrap="true"/>
            <Label text="Receive personalized interview questions based on your role and experience" class="stepSubtitle" textWrap="true"/>
          </StackLayout>
        </FlexboxLayout>

        <FlexboxLayout class="step" orientation="row" row="1" column="0" alignItems="center">
          <StackLayout class="emojiBox step2">
            <Label text="🎤" class="icon"/>
          </StackLayout>
          <StackLayout class="textBox">
            <Label text="Record Your Answer" class="stepTitle" textWrap="true"/>
            <Label text="Practice with timed responses just like a real interview" class="stepSubtitle" textWrap="true"/>
          </StackLayout>
        </FlexboxLayout>

        <FlexboxLayout class="step" orientation="row" row="2" column="0" alignItems="center">
          <StackLayout class="emojiBox step3">
            <Label text="✅" class="icon"/>
          </StackLayout>
          <StackLayout class="textBox">
            <Label text="Receive Instant Feedback" class="stepTitle" textWrap="true"/>
            <Label text="Get detailed insights on your performance and areas to improve" class="stepSubtitle" textWrap="true"/>
          </StackLayout>
        </FlexboxLayout>
      </GridLayout>

      <!-- Кнопка Continue -->
      <StackLayout row="2" class="bottomButton">
        <Button text="Continue" class="continueButton" @tap="goNext"/>
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import { Frame } from "@nativescript/core";

export default defineComponent({
  name: "HowItWorks",
  methods: {
    goNext() {
      // Навигация на экран персонализации
      Frame.topmost().navigate(() => require("./PersonalizeExperience").default);
    }
  }
});
</script>

<style scoped>
.page {
  background-color: #F9FAFB;
}

.container {
  width: 100%;
  height: 100%;
  padding: 30;
}

.title {
  font-size: 28;
  font-weight: 700;
  text-align: center;
  color: #111827;
  margin-bottom: 10;
}

.steps {
  row-gap: 25;
}

.step {
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}

.emojiBox {
  width: 60;
  height: 60;
  min-width: 60;
  min-height: 60;
  border-radius: 18;
  justify-content: center;
  align-items: center;
  padding: 10;
  margin-right: 15;
}

.step1 { background-color: #4F46E5; }
.step2 { background-color: #7C3AED; }
.step3 { background-color: #10B981; }

.icon {
  font-size: 28;
  color: white;
  text-align: center;
}

.textBox {
  flex: 1;
  min-width: 100;
}

.stepTitle {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  text-wrap: true;
}

.stepSubtitle {
  font-size: 14;
  color: #4B5563;
  margin-top: 4;
  text-wrap: true;
}

.bottomButton {
  padding-top: 20;
}

.continueButton {
  padding: 15;
  border-radius: 20;
  background: linear-gradient(90deg, #4F46E5, #7C3AED);
  color: white;
  font-size: 18;
  font-weight: 600;
  width: 100%;
}
</style>
