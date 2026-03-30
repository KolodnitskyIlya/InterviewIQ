<template>
  <GridLayout columns="*, *, *, *" class="bottomNav">
    <GridLayout
      col="0"
      rows="auto, auto"
      class="tabItem"
      :class="activeTab === 'home' ? 'activeTab' : ''"
      @tap="$emit('home')"
    >
      <Label
        row="0"
        text="⌂"
        class="tabIcon"
        :class="activeTab === 'home' ? 'activeTabIcon' : ''"
      />
      <Label
        row="1"
        text="Home"
        class="tabLabel"
        :class="activeTab === 'home' ? 'activeTabLabel' : ''"
      />
    </GridLayout>

    <GridLayout
      col="1"
      rows="auto, auto"
      class="tabItem"
      :class="activeTab === 'practice' ? 'activeTab' : ''"
      @tap="$emit('practice')"
    >
      <Label
        row="0"
        text="◎"
        class="tabIcon"
        :class="activeTab === 'practice' ? 'activeTabIcon' : ''"
      />
      <Label
        row="1"
        text="Practice"
        class="tabLabel"
        :class="activeTab === 'practice' ? 'activeTabLabel' : ''"
      />
    </GridLayout>

    <GridLayout
      col="2"
      rows="auto, auto"
      class="tabItem"
      :class="activeTab === 'analytics' ? 'activeTab' : ''"
      @tap="$emit('analytics')"
    >
      <Label
        row="0"
        text="▥"
        class="tabIcon"
        :class="activeTab === 'analytics' ? 'activeTabIcon' : ''"
      />
      <Label
        row="1"
        text="Analytics"
        class="tabLabel"
        :class="activeTab === 'analytics' ? 'activeTabLabel' : ''"
      />
    </GridLayout>

    <GridLayout
      col="3"
      rows="auto, auto"
      class="tabItem"
      :class="activeTab === 'profile' ? 'activeTab' : ''"
      @tap="$emit('profile')"
    >
      <Label
        row="0"
        text="◯"
        class="tabIcon"
        :class="activeTab === 'profile' ? 'activeTabIcon' : ''"
      />
      <Label
        row="1"
        text="Profile"
        class="tabLabel"
        :class="activeTab === 'profile' ? 'activeTabLabel' : ''"
      />
    </GridLayout>
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

type NavigationTab = "home" | "practice" | "analytics" | "profile";

export default defineComponent({
  name: "BottomNavigation",
  props: {
    activeTab: {
      type: String as PropType<NavigationTab>,
      required: true,
    },
  },
  emits: ["home", "practice", "analytics", "profile"],
});
</script>

<style scoped>
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
