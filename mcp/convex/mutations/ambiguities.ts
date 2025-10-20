import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const syncAmbiguities = mutation({
  args: {
    projectId: v.id("projects"),
    ambiguities: v.array(
      v.object({
        category: v.string(),
        description: v.string(),
        impact: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
        clarificationNeeded: v.string(),
        status: v.union(
          v.literal("open"),
          v.literal("clarified"),
          v.literal("resolved")
        ),
        identifiedDate: v.number(),
        context: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    const ambiguityIds: string[] = [];

    for (const ambiguityData of args.ambiguities) {
      const ambiguityId = await ctx.db.insert("ambiguities", {
        projectId: args.projectId,
        ...ambiguityData,
      });
      ambiguityIds.push(ambiguityId);
    }

    return { ambiguityIds, count: ambiguityIds.length };
  },
});

export const updateAmbiguityStatus = mutation({
  args: {
    ambiguityId: v.id("ambiguities"),
    status: v.union(
      v.literal("open"),
      v.literal("clarified"),
      v.literal("resolved")
    ),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.ambiguityId, {
      status: args.status,
    });
    return args.ambiguityId;
  },
});

