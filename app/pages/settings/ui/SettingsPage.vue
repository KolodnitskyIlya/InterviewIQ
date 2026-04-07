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
import { createActor, type ActorRefFrom } from "xstate";

import type { SettingsLinkItem } from "@/entities/settings";
import { accountLinks, legalLinks } from "@/entities/settings";
import { settingsPreferencesMachine } from "@/features/toggle-setting";
import SettingsHeader from "@/widgets/settings-header";
import SettingsLinks from "@/widgets/settings-links";
import SettingsPreferences from "@/widgets/settings-preferences";

type SettingsPreferencesActor = ActorRefFrom<typeof settingsPreferencesMachine>;

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
      preferencesActor: null as SettingsPreferencesActor | null,
      preferencesSubscription: null as { unsubscribe: () => void } | null,
    };
  },
  mounted() {
    const actor = createActor(settingsPreferencesMachine);
    this.preferencesActor = actor;
    this.preferencesSubscription = actor.subscribe((snapshot) => {
      this.darkMode = snapshot.context.darkMode;
      this.pushNotifications = snapshot.context.pushNotifications;
    });
    actor.start();
  },
  beforeUnmount() {
    this.preferencesSubscription?.unsubscribe();
    this.preferencesActor?.stop();
  },
  methods: {
    goBack() {
      this.$navigateBack();
    },
    updateDarkMode(value: boolean) {
      this.preferencesActor?.send({ type: "SET_DARK_MODE", value });
    },
    updatePushNotifications(value: boolean) {
      this.preferencesActor?.send({ type: "SET_PUSH_NOTIFICATIONS", value });
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
