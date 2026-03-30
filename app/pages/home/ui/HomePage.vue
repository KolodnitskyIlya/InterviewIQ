<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="*, auto">
      <ScrollView row="0">
        <StackLayout class="content">
          <StackLayout class="hero">
            <Label text="Good evening," class="greeting" />
            <Label text="Danil Kolbasenko 👋" class="userName" textWrap="true" />
            <ProgressCard :value="78" />
          </StackLayout>

          <StackLayout class="body">
            <Button
              text="▷ Start Practice Session"
              class="startButton"
              @tap="openPractice"
            />
            <Label text="Continue where you left off" class="sectionTitle" />

            <GridLayout columns="auto, *" class="sessionCard">
              <GridLayout col="0" class="sessionIcon">
                <Label
                  text="🕒"
                  class="sessionIconText"
                  horizontalAlignment="center"
                  verticalAlignment="center"
                />
              </GridLayout>

              <StackLayout col="1" class="sessionInfo">
                <Label text="System Design Practice" class="sessionTitle" textWrap="true" />
                <Label text="Question 7 of 10 • 15 min left" class="sessionMeta" textWrap="true" />
              </StackLayout>
            </GridLayout>

            <StackLayout class="improvementSection">
              <ImprovementList />
            </StackLayout>
          </StackLayout>
        </StackLayout>
      </ScrollView>

      <BottomNavigation
        row="1"
        activeTab="home"
        @practice="openPractice"
        @analytics="openAnalytics"
        @profile="openProfile"
      />
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import AnalyticsPage from "@/pages/analytics";
import PracticePage from "@/pages/practice";
import ProfilePage from "@/pages/profile";
import BottomNavigation from "@/widgets/bottom-navigation";
import ImprovementList from "@/widgets/improvement-list";
import ProgressCard from "@/widgets/progress-card";

export default defineComponent({
  name: "HomePage",
  components: {
    BottomNavigation,
    ProgressCard,
    ImprovementList,
  },
  methods: {
    openPractice() {
      this.$navigateTo(PracticePage, {
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
  },
});
</script>

<style scoped>
.page {
  background-color: #f3f4f6;
}

.content {
  padding-bottom: 24;
}

.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 44;
  border-bottom-left-radius: 44;
  padding-top: 72;
  padding-right: 24;
  padding-bottom: 26;
  padding-left: 24;
}

.greeting {
  font-size: 24;
  font-weight: 500;
  color: #f3f4f6;
  font-family: "Poppins";
}

.userName {
  margin-top: 8;
  font-size: 40;
  font-weight: 600;
  color: #ffffff;
  font-family: "Poppins";
}

.startButton {
  margin-top: 22;
  height: 68;
  border-radius: 24;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #ffffff;
  font-size: 24;
  font-weight: 600;
  font-family: "Poppins";
}

.body {
  padding-top: 24;
  padding-right: 24;
  padding-bottom: 0;
  padding-left: 24;
}

.sectionTitle {
  margin-top: 22;
  font-size: 22;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionCard {
  margin-top: 18;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 20;
  padding-right: 20;
  padding-bottom: 20;
  padding-left: 20;
}

.sessionIcon {
  width: 72;
  height: 72;
  border-radius: 22;
  background: linear-gradient(180deg, #4f46e5, #7c3aed);
  margin-right: 16;
}

.sessionIconText {
  font-size: 28;
  color: #ffffff;
  text-align: center;
}

.sessionInfo {
  vertical-align: middle;
}

.sessionTitle {
  font-size: 20;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionMeta {
  margin-top: 8;
  font-size: 15;
  color: #4b5563;
  font-family: "Poppins";
}

.improvementSection {
  margin-top: 26;
}
</style>
