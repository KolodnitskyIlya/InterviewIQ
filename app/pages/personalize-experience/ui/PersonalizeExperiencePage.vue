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
        :text="selectedRole || 'Select role'"
        class="dropdownButton"
        @tap="toggleRoleList"
      />
      <StackLayout v-if="showRoleList" class="dropdownList">
        <Button
          v-for="role in roles"
          :key="role"
          :text="role"
          class="optionButton dropdownOptionButton"
          @tap="selectRole(role)"
        />
      </StackLayout>

      <Label text="Experience Level" class="label experienceLabel" />
      <StackLayout class="experienceOptions">
        <Button
          v-for="level in experienceLevels"
          :key="level"
          :text="experienceLabel(level)"
          :class="
            selectedExperience === level
              ? 'selectedButton experienceButton'
              : 'optionButton experienceButton'
          "
          @tap="selectExperience(level)"
        />
      </StackLayout>

      <Button
        :text="isSubmitting ? 'Saving...' : 'Continue'"
        class="continueButton"
        :isEnabled="!isLoadingOptions && !isSubmitting"
        @tap="goNext"
      />
    </StackLayout>
  </Page>
</template>

<script lang="ts">
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";
import {
  ApiError,
  getAccessToken,
  interviewIqApi,
  type ExperienceLevel,
} from "@/shared";
import HomePage from "@/pages/home";
import SignInPage from "@/pages/sign-in";

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message;
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return "Something went wrong. Please try again.";
}

export default defineComponent({
  name: "PersonalizeExperiencePage",
  data() {
    return {
      roles: [
        "ML Engineer",
        "Backend Engineer",
        "Data Scientist",
        "Product Analyst",
      ] as string[],
      selectedRole: "",
      showRoleList: false,
      experienceLevels: ["junior", "middle", "senior"] as ExperienceLevel[],
      selectedExperience: "" as ExperienceLevel | "",
      isLoadingOptions: false,
      isSubmitting: false,
    };
  },
  mounted() {
    void this.loadOptions();
  },
  methods: {
    async loadOptions() {
      if (!getAccessToken()) {
        this.$navigateTo(SignInPage, { clearHistory: true });
        return;
      }

      this.isLoadingOptions = true;

      try {
        const options = await interviewIqApi.getOnboardingOptions();
        this.roles = options.roles;
        this.experienceLevels = options.experience_levels;
      } catch (error) {
        await alert({
          title: "Failed to load options",
          message: errorMessage(error),
          okButtonText: "OK",
        });
      } finally {
        this.isLoadingOptions = false;
      }
    },
    toggleRoleList() {
      this.showRoleList = !this.showRoleList;
    },
    selectRole(role: string) {
      this.selectedRole = role;
      this.showRoleList = false;
    },
    selectExperience(level: ExperienceLevel) {
      this.selectedExperience = level;
    },
    experienceLabel(level: ExperienceLevel): string {
      if (level === "junior") {
        return "Junior";
      }

      if (level === "middle") {
        return "Middle";
      }

      return "Senior";
    },
    async goNext() {
      if (!getAccessToken()) {
        this.$navigateTo(SignInPage, { clearHistory: true });
        return;
      }

      if (!this.selectedRole || !this.selectedExperience) {
        await alert({
          title: "Validation error",
          message: "Please choose role and experience level.",
          okButtonText: "OK",
        });
        return;
      }

      if (this.isSubmitting) {
        return;
      }

      this.isSubmitting = true;

      try {
        await interviewIqApi.saveOnboarding({
          role: this.selectedRole,
          experience_level: this.selectedExperience,
        });

        this.$navigateTo(HomePage, {
          clearHistory: true,
        });
      } catch (error) {
        await alert({
          title: "Failed to save onboarding",
          message: errorMessage(error),
          okButtonText: "OK",
        });
      } finally {
        this.isSubmitting = false;
      }
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
