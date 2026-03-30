<template>
  <StackLayout>
    <Label text="Time Per Answer" class="sectionTitle" />

    <GridLayout columns="*, auto" class="dropdownField" @tap="toggleOptions">
      <Label
        col="0"
        :text="selectedTime || 'Choose time limit'"
        class="dropdownText"
      />
      <Label col="1" text="⌄" class="dropdownIcon" />
    </GridLayout>

    <StackLayout v-if="showOptions" class="timeList">
      <Label
        v-for="option in options"
        :key="option"
        :text="option"
        class="timeOption"
        @tap="selectOption(option)"
      />
    </StackLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

const defaultOptions = ["30 sec", "45 sec", "60 sec", "90 sec", "120 sec"];

export default defineComponent({
  name: "TimerPicker",
  emits: ["select"],
  props: {
    selectedTime: {
      type: String,
      default: "",
    },
    options: {
      type: Array as PropType<string[]>,
      default: () => defaultOptions,
    },
  },
  data() {
    return {
      showOptions: false,
    };
  },
  methods: {
    toggleOptions() {
      this.showOptions = !this.showOptions;
    },
    selectOption(option: string) {
      this.$emit("select", option);
      this.showOptions = false;
    },
  },
});
</script>

<style scoped>
.sectionTitle {
  margin-top: 24;
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.dropdownField {
  margin-top: 12;
  min-height: 78;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 20;
  background-color: #f8fafc;
  padding-top: 22;
  padding-right: 24;
  padding-bottom: 22;
  padding-left: 24;
}

.dropdownText {
  font-size: 20;
  color: #111827;
  font-family: "Poppins";
}

.dropdownIcon {
  font-size: 22;
  color: #9ca3af;
  margin-left: 8;
}

.timeList {
  margin-top: 8;
  border-radius: 16;
  border-width: 1;
  border-color: #d1d5db;
  background-color: #ffffff;
}

.timeOption {
  min-height: 48;
  padding-top: 14;
  padding-right: 20;
  padding-bottom: 14;
  padding-left: 20;
  font-size: 18;
  color: #111827;
  font-family: "Poppins";
  border-bottom-width: 1;
  border-bottom-color: #e5e7eb;
}

.timeOption:last-child {
  border-bottom-width: 0;
}
</style>
