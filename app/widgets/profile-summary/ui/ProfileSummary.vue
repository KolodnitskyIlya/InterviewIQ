<template>
  <StackLayout>
    <StackLayout class="hero">
      <GridLayout class="avatar">
        <Label
          :text="profile.avatarLetter"
          class="avatarText"
          horizontalAlignment="center"
          verticalAlignment="center"
        />
      </GridLayout>
      <Label :text="fullName" class="name" textWrap="true" />
      <Label :text="profile.email" class="email" />
    </StackLayout>

    <GridLayout row="1" columns="*, auto, *, auto, *" class="statsCard">
      <StackLayout col="0" class="statItem">
        <Label :text="statAt(0).value" class="statValue" />
        <Label :text="statAt(0).label" class="statLabel" />
      </StackLayout>
      <StackLayout col="1" class="statDivider" />

      <StackLayout col="2" class="statItem">
        <Label :text="statAt(1).value" class="statValue" />
        <Label :text="statAt(1).label" class="statLabel" />
      </StackLayout>
      <StackLayout col="3" class="statDivider" />

      <StackLayout col="4" class="statItem">
        <Label :text="statAt(2).value" class="statValue" />
        <Label :text="statAt(2).label" class="statLabel" />
      </StackLayout>
    </GridLayout>
  </StackLayout>
</template>

<script lang="ts">
import { defineComponent, PropType } from "nativescript-vue";

import type { ProfileStat, UserProfile } from "@/entities/user";

const defaultProfile: UserProfile = {
  firstName: "Danil",
  lastName: "Kolbasenko",
  email: "danil.kolbasenko@email.com",
  avatarLetter: "D",
};

const defaultStats: ProfileStat[] = [
  { value: "156", label: "Questions" },
  { value: "28", label: "Sessions" },
  { value: "78%", label: "Avg Score" },
];

export default defineComponent({
  name: "ProfileSummary",
  props: {
    profile: {
      type: Object as PropType<UserProfile>,
      default: () => defaultProfile,
    },
    stats: {
      type: Array as PropType<ProfileStat[]>,
      default: () => defaultStats,
    },
  },
  computed: {
    fullName(): string {
      return `${this.profile.firstName} ${this.profile.lastName}`;
    },
  },
  methods: {
    statAt(index: number): ProfileStat {
      return this.stats[index] || { value: "-", label: "" };
    },
  },
});
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-bottom-right-radius: 56;
  border-bottom-left-radius: 56;
  padding-top: 56;
  padding-right: 24;
  padding-bottom: 58;
  padding-left: 24;
  align-items: center;
}

.avatar {
  width: 114;
  height: 114;
  border-radius: 57;
  background-color: #ffffff;
  horizontal-align: center;
  vertical-align: middle;
}

.avatarText {
  font-size: 42;
  font-weight: 700;
  color: #4f46e5;
  font-family: "Poppins";
  text-align: center;
}

.name {
  margin-top: 14;
  font-size: 31;
  font-weight: 600;
  color: #ffffff;
  font-family: "Poppins";
  text-align: center;
  line-height: 34;
  margin-right: 18;
  margin-left: 18;
}

.email {
  margin-top: 2;
  font-size: 16;
  color: #f3f4f6;
  font-family: "Poppins";
  text-align: center;
}

.statsCard {
  margin-top: -34;
  margin-right: 24;
  margin-left: 24;
  background-color: #ffffff;
  border-radius: 24;
  padding-top: 12;
  padding-right: 10;
  padding-bottom: 12;
  padding-left: 10;
}

.statItem {
  align-items: center;
}

.statValue {
  font-size: 20;
  font-weight: 700;
  color: #111827;
  font-family: "Poppins";
  text-align: center;
}

.statLabel {
  margin-top: 4;
  font-size: 12;
  color: #6b7280;
  font-family: "Poppins";
  text-align: center;
}

.statDivider {
  width: 1;
  background-color: #e5e7eb;
  margin-top: 12;
  margin-bottom: 12;
}
</style>
