import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectQuestions = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("open"), v.literal("answered"), v.literal("deferred"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("questions")
        .withIndex("by_project_status", (q) =>
          q.eq("projectId", args.projectId).eq("status", args.status)
        )
        .collect();
    }
    return await ctx.db
      .query("questions")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

export const getOpenQuestions = query({
  args: {
    projectId: v.optional(v.id("projects")),
  },
  handler: async (ctx, args) => {
    if (args.projectId) {
      return await ctx.db
        .query("questions")
        .withIndex("by_project_status", (q) =>
          q.eq("projectId", args.projectId).eq("status", "open")
        )
        .collect();
    }
    return await ctx.db
      .query("questions")
      .withIndex("by_status", (q) => q.eq("status", "open"))
      .collect();
  },
});

