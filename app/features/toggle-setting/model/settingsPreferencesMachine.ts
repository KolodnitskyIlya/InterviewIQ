import { assign, setup } from "xstate";

export interface SettingsPreferencesContext {
  darkMode: boolean;
  pushNotifications: boolean;
}

export type SettingsPreferencesEvent =
  | { type: "SET_DARK_MODE"; value: boolean }
  | { type: "SET_PUSH_NOTIFICATIONS"; value: boolean }
  | { type: "RESET" };

const initialContext: SettingsPreferencesContext = {
  darkMode: false,
  pushNotifications: true,
};

export const settingsPreferencesMachine = setup({
  types: {
    context: {} as SettingsPreferencesContext,
    events: {} as SettingsPreferencesEvent,
  },
  actions: {
    applyChange: assign(({ context, event }) => {
      if (event.type === "SET_DARK_MODE") {
        return { ...context, darkMode: event.value };
      }
      if (event.type === "SET_PUSH_NOTIFICATIONS") {
        return { ...context, pushNotifications: event.value };
      }
      return initialContext;
    }),
  },
}).createMachine({
  id: "settingsPreferences",
  initial: "ready",
  context: initialContext,
  states: {
    ready: {
      on: {
        SET_DARK_MODE: { actions: "applyChange" },
        SET_PUSH_NOTIFICATIONS: { actions: "applyChange" },
        RESET: { actions: "applyChange" },
      },
    },
  },
});
