import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectConflicts = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("open"), v.literal("in-progress"), v.literal("resolved"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("conflicts")
        .withIndex("by_project_status", (q) =>
          q.eq("projectId", args.projectId).eq("status", args.status)
        )
        .collect();
    }
    return await ctx.db
      .query("conflicts")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

export const getConflictById = query({
  args: {
    conflictId: v.id("conflicts"),
  },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.conflictId);
  },
});

