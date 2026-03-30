<template>
  <GridLayout columns="auto, *, auto" class="row">
    <Label col="0" :text="icon" class="rowIcon" />
    <Label col="1" :text="label" class="rowText" />
    <Switch
      col="2"
      :checked="modelValue"
      class="toggle"
      @checkedChange="onCheckedChange"
    />
  </GridLayout>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";

type CheckedChangeEvent = {
  value?: boolean;
  object?: {
    checked?: boolean;
  };
};

export default defineComponent({
  name: "ToggleSettingRow",
  emits: ["update:modelValue"],
  props: {
    icon: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    onCheckedChange(event: CheckedChangeEvent) {
      const nextValue =
        typeof event.value === "boolean"
          ? event.value
          : Boolean(event.object?.checked);
      this.$emit("update:modelValue", nextValue);
    },
  },
});
</script>

<style scoped>
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

.toggle {
  vertical-align: middle;
}
</style>
