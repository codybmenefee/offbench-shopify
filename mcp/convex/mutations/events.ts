import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const logEvent = mutation({
  args: {
    projectId: v.id("projects"),
    eventType: v.union(
      v.literal("document_added"),
      v.literal("gap_identified"),
      v.literal("conflict_resolved"),
      v.literal("question_answered"),
      v.literal("confidence_updated"),
      v.literal("ambiguity_clarified"),
      v.literal("project_created"),
      v.literal("analysis_completed")
    ),
    description: v.string(),
    timestamp: v.optional(v.number()),
    metadata: v.optional(v.any()),
  },
  handler: async (ctx, args) => {
    const eventId = await ctx.db.insert("contextEvents", {
      projectId: args.projectId,
      eventType: args.eventType,
      description: args.description,
      timestamp: args.timestamp || Date.now(),
      metadata: args.metadata,
    });
    return eventId;
  },
});

