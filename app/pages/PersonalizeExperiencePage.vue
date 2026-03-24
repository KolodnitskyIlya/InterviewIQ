<template>
  <Page class="page">
    <StackLayout class="container" spacing="20">

      <!-- Заголовок -->
      <Label text="Personalize Your Experience" class="title"/>
      <Label text="Tell us about yourself to get tailored interview questions" class="subtitle"/>

      <!-- Выпадающий список ролей -->
      <Label text="Select Job Role" class="label"/>
      <Button
        :text="selectedRoleIndex >= 0 ? roles[selectedRoleIndex] : 'Select role'"
        class="dropdownButton"
        @tap="toggleRoleList"
      />
      <StackLayout v-if="showRoleList" class="dropdownList" spacing="5">
        <Button
          v-for="(role, index) in roles"
          :key="index"
          :text="role"
          class="optionButton"
          @tap="selectRole(index)"
        />
      </StackLayout>

      <!-- Уровень опыта -->
      <Label text="Experience Level" class="label"/>
      <StackLayout class="experienceOptions" spacing="10">
        <Button
          text="Junior (0-2 years)"
          :class="selectedExperience === 'Junior' ? 'selectedButton' : 'optionButton'"
          @tap="selectExperience('Junior')"
        />
        <Button
          text="Middle (3-5 years)"
          :class="selectedExperience === 'Middle' ? 'selectedButton' : 'optionButton'"
          @tap="selectExperience('Middle')"
        />
        <Button
          text="Senior (6+ years)"
          :class="selectedExperience === 'Senior' ? 'selectedButton' : 'optionButton'"
          @tap="selectExperience('Senior')"
        />
      </StackLayout>

      <!-- Кнопка Continue -->
      <Button text="Continue" class="continueButton" @tap="goNext"/>
    </StackLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent, ref } from "nativescript-vue";

export default defineComponent({
  name: "PersonalizeExperience",
  setup() {
    const roles = ["Frontend Developer", "Backend Developer", "Fullstack Developer", "QA Engineer"];
    const selectedRoleIndex = ref(-1); // индекс выбранной роли
    const showRoleList = ref(false);   // показывает/скрывает список ролей
    const selectedExperience = ref(""); // уровень опыта

    const toggleRoleList = () => {
      showRoleList.value = !showRoleList.value;
    };

    const selectRole = (index: number) => {
      selectedRoleIndex.value = index;
      showRoleList.value = false; // скрываем список после выбора
    };

    const selectExperience = (level: string) => {
      selectedExperience.value = level;
    };

    const goNext = () => {
      console.log("Selected role:", selectedRoleIndex.value >= 0 ? roles[selectedRoleIndex.value] : "None");
      console.log("Selected experience:", selectedExperience.value || "None");
    };

    return {
      roles,
      selectedRoleIndex,
      showRoleList,
      selectedExperience,
      toggleRoleList,
      selectRole,
      selectExperience,
      goNext
    };
  }
});
</script>

<style scoped>
.page {
  background-color: #F9FAFB;
}

.container {
  padding: 30;
}

.title {
  font-size: 28;
  font-weight: 700;
  color: #111827;
}

.subtitle {
  font-size: 16;
  color: #6B7280;
  margin-bottom: 20;
}

.label {
  font-size: 14;
  font-weight: 600;
  color: #111827;
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
}

.optionButton {
  background-color: #ffffff;
  border-radius: 12;
  padding: 10;
  color: #111827;
  font-size: 16;
  text-align: left;
}

.selectedButton {
  background-color: #7C3AED;
  color: white;
  border-radius: 12;
  padding: 12;
  font-size: 16;
  text-align: left;
}

.experienceOptions Button.optionButton {
  background-color: #ffffff;
  border-radius: 12;
  padding: 12;
  color: #111827;
  font-size: 16;
  text-align: left;
}

.experienceOptions Button.selectedButton {
  background-color: #7C3AED;
  color: white;
  border-radius: 12;
  padding: 12;
  font-size: 16;
  text-align: left;
}

.continueButton {
  margin-top: 20;
  padding: 15;
  border-radius: 20;
  background: linear-gradient(90deg, #4F46E5, #7C3AED);
  color: white;
  font-size: 18;
  font-weight: 600;
}
</style>
