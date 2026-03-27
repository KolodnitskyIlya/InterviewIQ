<template>
  <Page actionBarHidden="true" class="page">
    <StackLayout class="container">
      <Label text="Personalize Your Experience" class="title" textWrap="true" />
      <Label
        text="Tell us about yourself to get tailored interview questions"
        class="subtitle"
        textWrap="true"
      />

      <Label text="Select Job Role" class="label" />
      <Button
        :text="
          selectedRoleIndex >= 0 ? roles[selectedRoleIndex] : 'Select role'
        "
        class="dropdownButton"
        @tap="toggleRoleList"
      />
      <StackLayout v-if="showRoleList" class="dropdownList">
        <Button
          v-for="(role, index) in roles"
          :key="index"
          :text="role"
          class="optionButton dropdownOptionButton"
          @tap="selectRole(index)"
        />
      </StackLayout>

      <Label text="Experience Level" class="label experienceLabel" />
      <StackLayout class="experienceOptions">
        <Button
          text="Junior (0-2 years)"
          :class="
            selectedExperience === 'Junior'
              ? 'selectedButton experienceButton'
              : 'optionButton experienceButton'
          "
          @tap="selectExperience('Junior')"
        />
        <Button
          text="Middle (3-5 years)"
          :class="
            selectedExperience === 'Middle'
              ? 'selectedButton experienceButton'
              : 'optionButton experienceButton'
          "
          @tap="selectExperience('Middle')"
        />
        <Button
          text="Senior (6+ years)"
          :class="
            selectedExperience === 'Senior'
              ? 'selectedButton experienceButton'
              : 'optionButton experienceButton'
          "
          @tap="selectExperience('Senior')"
        />
      </StackLayout>

      <Button text="Continue" class="continueButton" @tap="goNext" />
    </StackLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import SignInPage from "./SignInPage.vue";

export default defineComponent({
  name: "PersonalizeExperiencePage",
  data() {
    return {
      roles: [
        "Frontend Developer",
        "Backend Developer",
        "Fullstack Developer",
        "QA Engineer",
      ],
      selectedRoleIndex: -1,
      showRoleList: false,
      selectedExperience: "",
    };
  },
  methods: {
    toggleRoleList() {
      this.showRoleList = !this.showRoleList;
    },
    selectRole(index: number) {
      this.selectedRoleIndex = index;
      this.showRoleList = false;
    },
    selectExperience(level: string) {
      this.selectedExperience = level;
    },
    goNext() {
      this.$navigateTo(SignInPage);
    },
  },
});
</script>

<style scoped>
.page {
  background-color: #f9fafb;
}

.container {
  padding: 30;
  justify-content: center;
}

.title {
  font-size: 28;
  font-weight: 700;
  color: #111827;
  margin-bottom: 50;
}

.subtitle {
  font-size: 16;
  color: #6b7280;
  margin-bottom: 20;
}

.label {
  font-size: 14;
  font-weight: 600;
  color: #111827;
  margin-bottom: 10;
}

.dropdownButton {
  background-color: #ffffff;
  padding: 12;
  border-radius: 12;
  font-size: 16;
  text-align: left;
  color: #111827;
}

.dropdownList {
  background-color: #ffffff;
  border-radius: 12;
  padding: 5;
  margin-top: 8;
}

.optionButton {
  background-color: #ffffff;
  border-radius: 12;
  padding: 10;
  color: #111827;
  font-size: 16;
  text-align: left;
}

.dropdownOptionButton {
  margin-bottom: 8;
}

.dropdownOptionButton:last-child {
  margin-bottom: 0;
}

.selectedButton {
  background-color: #7c3aed;
  color: white;
  border-radius: 12;
  padding: 12;
  font-size: 16;
  text-align: left;
}

.experienceLabel {
  margin-top: 20;
}

.experienceButton {
  margin-bottom: 10;
}

.experienceButton:last-child {
  margin-bottom: 0;
}

.continueButton {
  margin-top: 20;
  padding: 15;
  border-radius: 20;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: white;
  font-size: 18;
  font-weight: 600;
}
</style>
