import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectDeliverables = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("draft"), v.literal("final"), v.literal("archived"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("deliverables")
        .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
        .filter((q) => q.eq(q.field("status"), args.status))
        .collect();
    }
    return await ctx.db
      .query("deliverables")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

