import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const createDeliverable = mutation({
  args: {
    projectId: v.id("projects"),
    name: v.string(),
    type: v.union(
      v.literal("implementation_plan"),
      v.literal("requirements_document"),
      v.literal("technical_specification"),
      v.literal("gap_analysis_report"),
      v.literal("risk_assessment"),
      v.literal("sow")
    ),
    generatedDate: v.optional(v.number()),
    status: v.union(v.literal("draft"), v.literal("final"), v.literal("archived")),
    fileType: v.string(),
    downloadUrl: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const deliverableId = await ctx.db.insert("deliverables", {
      projectId: args.projectId,
      name: args.name,
      type: args.type,
      generatedDate: args.generatedDate || Date.now(),
      status: args.status,
      fileType: args.fileType,
      downloadUrl: args.downloadUrl,
    });
    return deliverableId;
  },
});

export const updateDeliverableStatus = mutation({
  args: {
    deliverableId: v.id("deliverables"),
    status: v.union(v.literal("draft"), v.literal("final"), v.literal("archived")),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.deliverableId, {
      status: args.status,
    });
    return args.deliverableId;
  },
});

