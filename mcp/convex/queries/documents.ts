import { query } from "../_generated/server";
import { v } from "convex/values";

export const getProjectDocuments = query({
  args: {
    projectId: v.id("projects"),
    status: v.optional(
      v.union(v.literal("processed"), v.literal("processing"), v.literal("pending"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("documents")
        .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
        .filter((q) => q.eq(q.field("status"), args.status))
        .collect();
    }
    return await ctx.db
      .query("documents")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
  },
});

