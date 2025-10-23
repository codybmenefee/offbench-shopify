import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const syncConflicts = mutation({
  args: {
    projectId: v.id("projects"),
    conflicts: v.array(
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
        conflictingStatements: v.array(v.string()),
        sources: v.array(v.string()),
        resolution: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    const conflictIds: string[] = [];

    for (const conflictData of args.conflicts) {
      const conflictId = await ctx.db.insert("conflicts", {
        projectId: args.projectId,
        ...conflictData,
      });
      conflictIds.push(conflictId);
    }

    return { conflictIds, count: conflictIds.length };
  },
});

export const updateConflictStatus = mutation({
  args: {
    conflictId: v.id("conflicts"),
    status: v.union(
      v.literal("open"),
      v.literal("in-progress"),
      v.literal("resolved")
    ),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.conflictId, {
      status: args.status,
    });
    return args.conflictId;
  },
});

export const updateConflictResolution = mutation({
  args: {
    conflictId: v.id("conflicts"),
    resolution: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.conflictId, {
      resolution: args.resolution,
      status: "resolved",
    });
    return args.conflictId;
  },
});

export const create = mutation({
  args: {
    projectId: v.id("projects"),
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
    conflictingStatements: v.array(v.string()),
    sources: v.array(v.string()),
    resolution: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const conflictId = await ctx.db.insert("conflicts", args);
    return conflictId;
  },
});

