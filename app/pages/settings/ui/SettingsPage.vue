<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, *">
      <SettingsHeader row="0" @back="goBack" />

      <ScrollView row="1">
        <StackLayout class="content">
          <SettingsPreferences
            :darkMode="darkMode"
            :pushNotifications="pushNotifications"
            @update:darkMode="updateDarkMode"
            @update:pushNotifications="updatePushNotifications"
          />

          <SettingsLinks title="LEGAL" :items="legalData" />
          <SettingsLinks title="ACCOUNT" :items="accountData" />
        </StackLayout>
      </ScrollView>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

import type { SettingsLinkItem } from "@/entities/settings";
import { accountLinks, legalLinks } from "@/pages/settings/model/mock";
import SettingsHeader from "@/widgets/settings-header";
import SettingsLinks from "@/widgets/settings-links";
import SettingsPreferences from "@/widgets/settings-preferences";

export default defineComponent({
  name: "SettingsPage",
  components: {
    SettingsHeader,
    SettingsPreferences,
    SettingsLinks,
  },
  data() {
    return {
      darkMode: false,
      pushNotifications: true,
      legalData: legalLinks as SettingsLinkItem[],
      accountData: accountLinks as SettingsLinkItem[],
    };
  },
  methods: {
    goBack() {
      this.$navigateBack();
    },
    updateDarkMode(value: boolean) {
      this.darkMode = value;
    },
    updatePushNotifications(value: boolean) {
      this.pushNotifications = value;
    },
  },
});
</script>

<style scoped>
.page {
  background-color: #f3f4f6;
}

.content {
  padding-top: 18;
  padding-right: 24;
  padding-bottom: 24;
  padding-left: 24;
}
</style>
