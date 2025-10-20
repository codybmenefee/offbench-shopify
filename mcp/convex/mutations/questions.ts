import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const syncQuestions = mutation({
  args: {
    projectId: v.id("projects"),
    questions: v.array(
      v.object({
        question: v.string(),
        category: v.string(),
        priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
        status: v.union(
          v.literal("open"),
          v.literal("answered"),
          v.literal("deferred")
        ),
        askedDate: v.number(),
        answer: v.optional(v.string()),
        answeredDate: v.optional(v.number()),
        whyItMatters: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    const questionIds: string[] = [];

    for (const questionData of args.questions) {
      const questionId = await ctx.db.insert("questions", {
        projectId: args.projectId,
        ...questionData,
      });
      questionIds.push(questionId);
    }

    return { questionIds, count: questionIds.length };
  },
});

export const answerQuestion = mutation({
  args: {
    questionId: v.id("questions"),
    answer: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.questionId, {
      answer: args.answer,
      answeredDate: Date.now(),
      status: "answered",
    });
    return args.questionId;
  },
});

export const updateQuestionStatus = mutation({
  args: {
    questionId: v.id("questions"),
    status: v.union(
      v.literal("open"),
      v.literal("answered"),
      v.literal("deferred")
    ),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.questionId, {
      status: args.status,
    });
    return args.questionId;
  },
});

