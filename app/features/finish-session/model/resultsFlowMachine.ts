import { assign, setup } from "xstate";

interface ResultsFlowInput {
  currentQuestionIndex: number;
  totalQuestions: number;
}

export interface ResultsFlowContext {
  currentQuestionIndex: number;
  totalQuestions: number;
}

export type ResultsFlowEvent =
  | { type: "NEXT_QUESTION" }
  | { type: "FINISH_SESSION" };

export const resultsFlowMachine = setup({
  types: {
    context: {} as ResultsFlowContext,
    events: {} as ResultsFlowEvent,
    input: {} as ResultsFlowInput,
  },
  actions: {
    goToNextQuestion: assign(({ context }) => ({
      ...context,
      currentQuestionIndex: Math.min(
        context.totalQuestions - 1,
        context.currentQuestionIndex + 1,
      ),
    })),
  },
  guards: {
    hasNextQuestion: ({ context }) =>
      context.currentQuestionIndex < context.totalQuestions - 1,
  },
}).createMachine({
  id: "resultsFlow",
  initial: "reviewing",
  context: ({ input }) => ({
    currentQuestionIndex: input.currentQuestionIndex,
    totalQuestions: input.totalQuestions,
  }),
  states: {
    reviewing: {
      on: {
        NEXT_QUESTION: [
          {
            guard: "hasNextQuestion",
            actions: "goToNextQuestion",
          },
          {
            target: "completed",
          },
        ],
        FINISH_SESSION: {
          target: "completed",
        },
      },
    },
    completed: {
      type: "final",
    },
  },
});
