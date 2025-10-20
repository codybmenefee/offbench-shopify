import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectGaps = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("open"), v.literal("in-progress"), v.literal("resolved"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("gaps")
        .withIndex("by_project_status", (q) =>
          q.eq("projectId", args.projectId).eq("status", args.status)
        )
        .collect();
    }
    return await ctx.db
      .query("gaps")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

export const getGapById = query({
  args: {
    gapId: v.id("gaps"),
  },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.gapId);
  },
});

