import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectAmbiguities = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("open"), v.literal("clarified"), v.literal("resolved"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("ambiguities")
        .withIndex("by_project_status", (q) =>
          q.eq("projectId", args.projectId).eq("status", args.status)
        )
        .collect();
    }
    return await ctx.db
      .query("ambiguities")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

