<template>
  <Page class="page">
    <GridLayout rows="*, auto, auto, *" class="container">
      <!-- квадрат -->
      <GridLayout row="1" class="square">
        <Label text="⭐" class="star" />
        <Label text="🧠" class="brain" />
      </GridLayout>

      <!-- текст -->
      <StackLayout row="2" class="textBlock">
        <Label text="InterviewIQ" class="title" />
        <Label text="Prepare • Practice • Perform" class="subtitle" />
      </StackLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "nativescript-vue";
import { Frame } from "@nativescript/core";

export default defineComponent({
  name: "Home",
  setup() {
    onMounted(() => {
      setTimeout(() => {
        const frame = Frame.topmost();
        if (frame) {
          // Переход на экран HowItWorks.vue
          frame.navigate(() => require("./HowItWorks").default);
        }
      }, 3000); // 3 секунды задержка
    });
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

/* квадрат */
.square {
  width: 200;
  height: 200;
  background-color: white;
  border-radius: 30;
  horizontal-align: center;
  vertical-align: middle;
}

/* мозг */
.brain {
  font-size: 90;
  horizontal-align: center;
  vertical-align: middle;
}

/* звезда */
.star {
  font-size: 20;
  horizontal-align: right;
  vertical-align: top;
  margin: 10;
}

/* текст */
.textBlock {
  margin-top: 20;
  horizontal-align: center;
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
