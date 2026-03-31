import { assign, setup } from "xstate";

interface QuestionSessionInput {
  totalSeconds: number;
}

export interface QuestionSessionContext {
  totalSeconds: number;
  remainingSeconds: number;
  isRecording: boolean;
}

export type QuestionSessionEvent =
  | { type: "START_RECORDING" }
  | { type: "STOP_RECORDING" }
  | { type: "TICK" }
  | { type: "RESET_TIMER" };

export const questionSessionMachine = setup({
  types: {
    context: {} as QuestionSessionContext,
    events: {} as QuestionSessionEvent,
    input: {} as QuestionSessionInput,
  },
  actions: {
    beginRecording: assign(({ context }) => ({
      ...context,
      isRecording: true,
    })),
    endRecording: assign(({ context }) => ({
      ...context,
      isRecording: false,
    })),
    decrementTimer: assign(({ context }) => ({
      ...context,
      remainingSeconds: Math.max(0, context.remainingSeconds - 1),
    })),
    resetTimer: assign(({ context }) => ({
      ...context,
      remainingSeconds: context.totalSeconds,
      isRecording: false,
    })),
  },
  guards: {
    isTimedOut: ({ context }) => context.remainingSeconds <= 0,
  },
}).createMachine({
  id: "questionSession",
  initial: "idle",
  context: ({ input }) => ({
    totalSeconds: input.totalSeconds,
    remainingSeconds: input.totalSeconds,
    isRecording: false,
  }),
  states: {
    idle: {
      on: {
        START_RECORDING: {
          target: "recording",
          actions: "beginRecording",
        },
        RESET_TIMER: {
          actions: "resetTimer",
        },
      },
    },
    recording: {
      on: {
        TICK: {
          actions: "decrementTimer",
        },
        STOP_RECORDING: {
          target: "idle",
          actions: "endRecording",
        },
        RESET_TIMER: {
          target: "idle",
          actions: "resetTimer",
        },
      },
      always: {
        target: "timeout",
        guard: "isTimedOut",
      },
    },
    timeout: {
      entry: {
        type: "endRecording",
      },
      on: {
        START_RECORDING: {
          target: "recording",
          actions: ["resetTimer", "beginRecording"],
        },
        RESET_TIMER: {
          target: "idle",
          actions: "resetTimer",
        },
      },
    },
  },
});
