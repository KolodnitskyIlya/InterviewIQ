<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *, auto">
      <StackLayout row="0" class="hero">
        <Label text="Practice Setup" class="heroTitle" />
        <Label text="Customize your practice session" class="heroSubtitle" />
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <Label text="Select Category" class="sectionTitle" />

          <GridLayout columns="*, *" rows="auto, auto" class="categoryGrid">
            <StackLayout
              row="0"
              col="0"
              class="categoryCard categoryLeft categoryTop"
              :class="selectedCategory === 'hr' ? 'selectedCard' : ''"
              @tap="selectCategory('hr')"
            >
              <Label text="💼" class="categoryIcon" />
              <Label text="HR Questions" class="categoryText" />
            </StackLayout>

            <StackLayout
              row="0"
              col="1"
              class="categoryCard categoryRight categoryTop"
              :class="selectedCategory === 'technical' ? 'selectedCard' : ''"
              @tap="selectCategory('technical')"
            >
              <Label text="💻" class="categoryIcon" />
              <Label text="Technical" class="categoryText" />
            </StackLayout>

            <StackLayout
              row="1"
              col="0"
              class="categoryCard categoryLeft"
              :class="selectedCategory === 'behavioral' ? 'selectedCard' : ''"
              @tap="selectCategory('behavioral')"
            >
              <Label text="🗣" class="categoryIcon" />
              <Label text="Behavioral" class="categoryText" />
            </StackLayout>

            <StackLayout
              row="1"
              col="1"
              class="categoryCard categoryRight"
              :class="selectedCategory === 'system' ? 'selectedCard' : ''"
              @tap="selectCategory('system')"
            >
              <Label text="🗂" class="categoryIcon" />
              <Label text="System Design" class="categoryText" />
            </StackLayout>
          </GridLayout>

          <Label
            text="Select Difficulty"
            class="sectionTitle difficultyTitle"
          />
          <StackLayout>
            <GridLayout
              class="difficultyCard"
              :class="selectedDifficulty === 'Easy' ? 'selectedCard' : ''"
              @tap="selectDifficulty('Easy')"
            >
              <Label text="Easy" class="difficultyText" />
            </GridLayout>

            <GridLayout
              class="difficultyCard"
              :class="selectedDifficulty === 'Medium' ? 'selectedCard' : ''"
              @tap="selectDifficulty('Medium')"
            >
              <Label text="Medium" class="difficultyText" />
            </GridLayout>

            <GridLayout
              class="difficultyCard"
              :class="selectedDifficulty === 'Hard' ? 'selectedCard' : ''"
              @tap="selectDifficulty('Hard')"
            >
              <Label text="Hard" class="difficultyText" />
            </GridLayout>
          </StackLayout>

          <Label text="Time Per Answer" class="sectionTitle timeTitle" />
          <GridLayout
            columns="*, auto"
            class="dropdownField"
            @tap="toggleTimeList"
          >
            <Label
              col="0"
              :text="selectedTime || 'Choose time limit'"
              class="dropdownText"
            />
            <Label col="1" text="⌄" class="dropdownIcon" />
          </GridLayout>

          <StackLayout v-if="showTimeList" class="timeList">
            <Label
              v-for="option in timeOptions"
              :key="option"
              :text="option"
              class="timeOption"
              @tap="selectTime(option)"
            />
          </StackLayout>

          <Button
            text="▷ Start Practice"
            class="startButton"
            @tap="startPractice"
          />
        </StackLayout>
      </ScrollView>

      <GridLayout row="2" columns="*, *, *, *" class="bottomNav">
        <GridLayout col="0" rows="auto, auto" class="tabItem" @tap="goHome">
          <Label row="0" text="⌂" class="tabIcon" />
          <Label row="1" text="Home" class="tabLabel" />
        </GridLayout>
        <GridLayout col="1" rows="auto, auto" class="tabItem activeTab">
          <Label row="0" text="◎" class="tabIcon activeTabIcon" />
          <Label row="1" text="Practice" class="tabLabel activeTabLabel" />
        </GridLayout>
        <GridLayout
          col="2"
          rows="auto, auto"
          class="tabItem"
          @tap="openAnalytics"
        >
          <Label row="0" text="▥" class="tabIcon" />
          <Label row="1" text="Analytics" class="tabLabel" />
        </GridLayout>
        <GridLayout
          col="3"
          rows="auto, auto"
          class="tabItem"
          @tap="openProfile"
        >
          <Label row="0" text="◯" class="tabIcon" />
          <Label row="1" text="Profile" class="tabLabel" />
        </GridLayout>
      </GridLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import AnalyticsPage from "./AnalyticsPage.vue";
import HomePage from "./HomePage.vue";
import ProfilePage from "./ProfilePage.vue";
import QuestionsPage from "./QuestionsPage.vue";

export default defineComponent({
  name: "PracticePage",
  data() {
    return {
      selectedCategory: "",
      selectedDifficulty: "",
      selectedTime: "",
      showTimeList: false,
      timeOptions: ["30 sec", "45 sec", "60 sec", "90 sec", "120 sec"],
    };
  },
  methods: {
    goHome() {
      this.$navigateTo(HomePage, {
        clearHistory: true,
        transition: {
          name: "slideRight",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openProfile() {
      this.$navigateTo(ProfilePage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    openAnalytics() {
      this.$navigateTo(AnalyticsPage, {
        clearHistory: true,
        transition: {
          name: "slideLeft",
          duration: 280,
          curve: "easeInOut",
        },
      });
    },
    selectCategory(category: string) {
      this.selectedCategory = category;
    },
    selectDifficulty(level: string) {
      this.selectedDifficulty = level;
    },
    toggleTimeList() {
      this.showTimeList = !this.showTimeList;
    },
    selectTime(option: string) {
      this.selectedTime = option;
      this.showTimeList = false;
    },
    startPractice() {
      this.$navigateTo(QuestionsPage, {
        clearHistory: true,
        props: {
          currentQuestionIndex: 0,
          totalQuestions: 3,
          selectedCategory: this.selectedCategory || "technical",
        },
        transition: {
          name: "slideLeft",
          duration: 280,
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

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 52;
  border-bottom-left-radius: 52;
  padding-top: 64;
  padding-right: 28;
  padding-bottom: 30;
  padding-left: 28;
}

.heroTitle {
  font-size: 44;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}

.heroSubtitle {
  margin-top: 6;
  font-size: 15;
  font-weight: 600;
  color: #e5e7eb;
  font-family: "Poppins";
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.sectionTitle {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.categoryGrid {
  margin-top: 14;
}

.categoryCard {
  height: 116;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 22;
  background-color: #f8fafc;
  padding-top: 16;
  padding-right: 16;
  padding-bottom: 16;
  padding-left: 16;
}

.categoryLeft {
  margin-right: 8;
}

.categoryRight {
  margin-left: 8;
}

.categoryTop {
  margin-bottom: 12;
}

.selectedCard {
  border-color: #6366f1;
  background-color: #ede9fe;
}

.categoryIcon {
  font-size: 28;
}

.categoryText {
  margin-top: 8;
  font-size: 16;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.difficultyTitle {
  margin-top: 24;
}

.difficultyCard {
  margin-top: 10;
  height: 68;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 22;
  background-color: #f8fafc;
  padding-top: 20;
  padding-right: 20;
  padding-bottom: 20;
  padding-left: 20;
}

.difficultyCard.selectedCard {
  border-color: #6366f1;
  background-color: #ede9fe;
}

.difficultyText {
  font-size: 17;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.timeTitle {
  margin-top: 20;
}

.dropdownField {
  margin-top: 10;
  height: 68;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 22;
  background-color: #f8fafc;
  padding-top: 18;
  padding-right: 20;
  padding-bottom: 18;
  padding-left: 20;
}

.dropdownText {
  font-size: 17;
  color: #111827;
  font-weight: 500;
  font-family: "Poppins";
  vertical-align: middle;
}

.dropdownIcon {
  font-size: 20;
  color: #9ca3af;
  vertical-align: middle;
  horizontal-align: center;
}

.timeList {
  margin-top: 8;
  border-width: 1;
  border-color: #d1d5db;
  border-radius: 18;
  background-color: #ffffff;
  padding-top: 4;
  padding-bottom: 4;
}

.timeOption {
  padding-top: 12;
  padding-right: 16;
  padding-bottom: 12;
  padding-left: 16;
  font-size: 16;
  color: #111827;
  font-family: "Poppins";
}

.startButton {
  margin-top: 26;
  margin-bottom: 16;
  height: 72;
  border-radius: 24;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 20;
  font-weight: 600;
  font-family: "Poppins";
}

.bottomNav {
  border-top-width: 1;
  border-top-color: #d1d5db;
  background-color: #f8fafc;
  padding-top: 8;
  padding-right: 12;
  padding-bottom: 8;
  padding-left: 12;
}

.tabItem {
  height: 64;
  border-radius: 18;
  vertical-align: middle;
  horizontal-align: stretch;
  padding-top: 6;
  padding-bottom: 6;
}

.activeTab {
  background-color: #ddd6fe;
}

.tabIcon {
  font-size: 24;
  color: #6b7280;
  text-align: center;
  horizontal-align: center;
  vertical-align: middle;
}

.activeTabIcon {
  color: #6366f1;
}

.tabLabel {
  margin-top: 2;
  font-size: 14;
  color: #6b7280;
  font-family: "Poppins";
  text-align: center;
  horizontal-align: center;
  vertical-align: middle;
}

.activeTabLabel {
  color: #4f46e5;
}
</style>


