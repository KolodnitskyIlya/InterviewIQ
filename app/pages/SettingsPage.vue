<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *">
      <StackLayout row="0" class="hero">
        <FlexboxLayout class="heroRow" alignItems="center">
          <GridLayout class="backButton" @tap="goBack">
            <Label text="←" class="backIcon" />
          </GridLayout>
          <Label text="Settings" class="heroTitle" />
        </FlexboxLayout>
      </StackLayout>

      <ScrollView row="1">
        <StackLayout class="content">
          <Label text="PREFERENCES" class="sectionLabel" />
          <StackLayout class="card">
            <GridLayout columns="auto, *, auto" class="row">
              <Label col="0" text="☾" class="rowIcon" />
              <Label col="1" text="Dark Mode" class="rowText" />
              <Switch col="2" v-model="darkMode" class="toggle" />
            </GridLayout>

            <StackLayout class="divider" />

            <GridLayout columns="auto, *, auto" class="row">
              <Label col="0" text="🔔" class="rowIcon" />
              <Label col="1" text="Push Notifications" class="rowText" />
              <Switch col="2" v-model="pushNotifications" class="toggle" />
            </GridLayout>

            <StackLayout class="divider" />

            <GridLayout columns="auto, *, auto, auto" class="row">
              <Label col="0" text="🌐" class="rowIcon" />
              <Label col="1" text="Language" class="rowText" />
              <Label col="2" text="English" class="rowValue" />
              <Label col="3" text="›" class="chevron" />
            </GridLayout>
          </StackLayout>

          <Label text="LEGAL" class="sectionLabel sectionSpacing" />
          <StackLayout class="card">
            <GridLayout columns="auto, *, auto" class="row">
              <Label col="0" text="🛡" class="rowIcon" />
              <Label col="1" text="Privacy Policy" class="rowText" />
              <Label col="2" text="›" class="chevron" />
            </GridLayout>

            <StackLayout class="divider" />

            <GridLayout columns="auto, *, auto" class="row">
              <Label col="0" text="🛡" class="rowIcon" />
              <Label col="1" text="Terms of Service" class="rowText" />
              <Label col="2" text="›" class="chevron" />
            </GridLayout>
          </StackLayout>

          <Label text="ACCOUNT" class="sectionLabel sectionSpacing" />
          <StackLayout class="card">
            <GridLayout columns="auto, *, auto" class="row">
              <Label col="0" text="🗑" class="rowIcon danger" />
              <Label col="1" text="Delete Account" class="rowText danger" />
              <Label col="2" text="›" class="chevron" />
            </GridLayout>
          </StackLayout>
        </StackLayout>
      </ScrollView>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

export default defineComponent({
  name: "SettingsPage",
  data() {
    return {
      darkMode: false,
      pushNotifications: true,
    };
  },
  methods: {
    goBack() {
      this.$navigateBack();
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
  padding-top: 70;
  padding-right: 24;
  padding-bottom: 22;
  padding-left: 24;
}

.heroRow {
  min-height: 56;
}

.backButton {
  width: 48;
  height: 48;
  border-radius: 24;
  background-color: rgba(99, 102, 241, 0.55);
  justify-content: center;
  align-items: center;
}

.backIcon {
  font-size: 30;
  color: #ffffff;
  text-align: center;
}

.heroTitle {
  margin-left: 14;
  font-size: 52;
  font-weight: 700;
  color: #ffffff;
  font-family: "Poppins";
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}

.sectionLabel {
  font-size: 13;
  font-weight: 700;
  color: #6b7280;
  font-family: "Poppins";
}

.sectionSpacing {
  margin-top: 26;
}

.card {
  margin-top: 8;
  background-color: #ffffff;
  border-radius: 24;
}

.row {
  height: 66;
  padding-top: 14;
  padding-right: 16;
  padding-bottom: 14;
  padding-left: 16;
}

.rowIcon {
  font-size: 24;
  color: #111827;
  vertical-align: middle;
}

.rowText {
  margin-left: 10;
  font-size: 20;
  font-weight: 500;
  color: #111827;
  font-family: "Poppins";
  vertical-align: middle;
}

.rowValue {
  font-size: 16;
  color: #6b7280;
  font-family: "Poppins";
  margin-right: 8;
  vertical-align: middle;
}

.toggle {
  vertical-align: middle;
}

.divider {
  height: 1;
  background-color: #e5e7eb;
}

.chevron {
  font-size: 28;
  color: #9ca3af;
  vertical-align: middle;
}

.danger {
  color: #ef4444;
}
</style>
