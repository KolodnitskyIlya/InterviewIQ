<template>
  <StackLayout>
    <Label :text="title" class="recentTitle" />

    <GridLayout
      v-for="session in sessions"
      :key="session.title"
      columns="*, auto"
      class="sessionCard"
    >
      <StackLayout col="0">
        <Label :text="session.title" class="sessionTitle" textWrap="true" />
        <Label :text="session.date" class="sessionDate" />
        <Label :text="session.meta" class="sessionMeta" />
      </StackLayout>
      <Label col="1" :text="`${session.score}`" class="sessionScore" />
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { DetailedSession } from "@/entities/analytics";

const defaultSessions: DetailedSession[] = [
  {
    title: "Technical Round",
    date: "Feb 25, 2026",
    meta: "10 questions • 25 min",
    score: 82,
  },
  {
    title: "Behavioral Questions",
    date: "Feb 20, 2026",
    meta: "8 questions • 20 min",
    score: 78,
  },
];

export default defineComponent({
  name: "RecentSessions",
  props: {
    title: {
      type: String,
      default: "Recent Session",
    },
    sessions: {
      type: Array as PropType<DetailedSession[]>,
      default: () => defaultSessions,
    },
  },
});
</script>

<style scoped>
.recentTitle {
  margin-top: 4;
  margin-bottom: 10;
  font-size: 20;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
}

.sessionCard {
  margin-bottom: 14;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 18;
  padding-right: 18;
  padding-bottom: 18;
  padding-left: 18;
}

.sessionTitle {
  font-size: 18;
  font-weight: 600;
  color: #111827;
  font-family: "Poppins";
}

.sessionDate {
  margin-top: 6;
  font-size: 13;
  color: #6b7280;
  font-family: "Poppins";
}

.sessionMeta {
  margin-top: 4;
  font-size: 12;
  color: #9ca3af;
  font-family: "Poppins";
}

.sessionScore {
  font-size: 28;
  font-weight: 700;
  color: #4f46e5;
  vertical-align: middle;
  font-family: "Poppins";
}
</style>
