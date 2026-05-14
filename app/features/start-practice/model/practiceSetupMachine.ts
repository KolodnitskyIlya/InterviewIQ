import { assign, setup } from "xstate";

import type { PracticeCategory, PracticeDifficulty } from "@/entities/practice";

export interface PracticeSetupContext {
  selectedCategory: PracticeCategory | "";
  selectedDifficulty: PracticeDifficulty | "";
  selectedTime: string;
  selectedQuestionCount: number;
}

export type PracticeSetupEvent =
  | { type: "SELECT_CATEGORY"; category: PracticeCategory }
  | { type: "SELECT_DIFFICULTY"; difficulty: PracticeDifficulty }
  | { type: "SELECT_TIME"; time: string }
  | { type: "SELECT_QUESTION_COUNT"; count: number }
  | { type: "RESET" };

const initialContext: PracticeSetupContext = {
  selectedCategory: "",
  selectedDifficulty: "",
  selectedTime: "",
  selectedQuestionCount: 10,
};

export const practiceSetupMachine = setup({
  types: {
    context: {} as PracticeSetupContext,
    events: {} as PracticeSetupEvent,
  },
  actions: {
    applySelection: assign(({ context, event }) => {
      if (event.type === "SELECT_CATEGORY") {
        return { ...context, selectedCategory: event.category };
      }
      if (event.type === "SELECT_DIFFICULTY") {
        return { ...context, selectedDifficulty: event.difficulty };
      }
      if (event.type === "SELECT_TIME") {
        return { ...context, selectedTime: event.time };
      }
      if (event.type === "SELECT_QUESTION_COUNT") {
        return { ...context, selectedQuestionCount: event.count };
      }
      return initialContext;
    }),
  },
  guards: {
    isComplete: ({ context }) =>
      Boolean(
        context.selectedCategory &&
          context.selectedDifficulty &&
          context.selectedTime,
      ),
    isIncomplete: ({ context }) =>
      !(
        context.selectedCategory &&
        context.selectedDifficulty &&
        context.selectedTime
      ),
  },
}).createMachine({
  id: "practiceSetup",
  initial: "editing",
  context: initialContext,
  states: {
    editing: {
      on: {
        SELECT_CATEGORY: { actions: "applySelection" },
        SELECT_DIFFICULTY: { actions: "applySelection" },
        SELECT_TIME: { actions: "applySelection" },
        SELECT_QUESTION_COUNT: { actions: "applySelection" },
        RESET: { actions: "applySelection" },
      },
      always: {
        target: "ready",
        guard: "isComplete",
      },
    },
    ready: {
      on: {
        SELECT_CATEGORY: { actions: "applySelection" },
        SELECT_DIFFICULTY: { actions: "applySelection" },
        SELECT_TIME: { actions: "applySelection" },
        SELECT_QUESTION_COUNT: { actions: "applySelection" },
        RESET: { actions: "applySelection" },
      },
      always: {
        target: "editing",
        guard: "isIncomplete",
      },
    },
  },
});
