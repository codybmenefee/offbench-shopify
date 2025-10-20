import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const syncGaps = mutation({
  args: {
    projectId: v.id("projects"),
    gaps: v.array(
      v.object({
        category: v.string(),
        description: v.string(),
        impact: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
        priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
        status: v.union(
          v.literal("open"),
          v.literal("in-progress"),
          v.literal("resolved")
        ),
        identifiedDate: v.number(),
        suggestedQuestion: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    const gapIds: string[] = [];

    for (const gapData of args.gaps) {
      const gapId = await ctx.db.insert("gaps", {
        projectId: args.projectId,
        ...gapData,
      });
      gapIds.push(gapId);
    }

    return { gapIds, count: gapIds.length };
  },
});

export const updateGapStatus = mutation({
  args: {
    gapId: v.id("gaps"),
    status: v.union(
      v.literal("open"),
      v.literal("in-progress"),
      v.literal("resolved")
    ),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.gapId, {
      status: args.status,
    });
    return args.gapId;
  },
});

