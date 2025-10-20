import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const upsertProject = mutation({
  args: {
    scenarioId: v.string(),
    name: v.string(),
    confidence: v.number(),
    gapsCount: v.number(),
    conflictsCount: v.number(),
    ambiguitiesCount: v.number(),
    documentsCount: v.number(),
    status: v.union(v.literal("active"), v.literal("archived"), v.literal("draft")),
  },
  handler: async (ctx, args) => {
    // Check if project with this scenarioId exists
    const existing = await ctx.db
      .query("projects")
      .withIndex("by_scenarioId", (q) => q.eq("scenarioId", args.scenarioId))
      .first();

    const projectData = {
      ...args,
      lastUpdated: Date.now(),
    };

    if (existing) {
      // Update existing project
      await ctx.db.patch(existing._id, projectData);
      return existing._id;
    } else {
      // Create new project
      return await ctx.db.insert("projects", projectData);
    }
  },
});

export const updateProjectStatus = mutation({
  args: {
    projectId: v.id("projects"),
    status: v.union(v.literal("active"), v.literal("archived"), v.literal("draft")),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.projectId, {
      status: args.status,
      lastUpdated: Date.now(),
    });
    return args.projectId;
  },
});

export const updateProjectCounts = mutation({
  args: {
    projectId: v.id("projects"),
    gapsCount: v.optional(v.number()),
    conflictsCount: v.optional(v.number()),
    ambiguitiesCount: v.optional(v.number()),
    documentsCount: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const { projectId, ...updates } = args;
    await ctx.db.patch(projectId, {
      ...updates,
      lastUpdated: Date.now(),
    });
    return projectId;
  },
});

export const updateProjectConfidence = mutation({
  args: {
    projectId: v.id("projects"),
    confidence: v.number(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.projectId, {
      confidence: args.confidence,
      lastUpdated: Date.now(),
    });
    return args.projectId;
  },
});

export const deleteProject = mutation({
  args: {
    projectId: v.id("projects"),
  },
  handler: async (ctx, args) => {
    // Delete project and all related data
    await ctx.db.delete(args.projectId);
    
    // Delete related gaps
    const gaps = await ctx.db
      .query("gaps")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const gap of gaps) {
      await ctx.db.delete(gap._id);
    }
    
    // Delete related conflicts
    const conflicts = await ctx.db
      .query("conflicts")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const conflict of conflicts) {
      await ctx.db.delete(conflict._id);
    }
    
    // Delete related ambiguities
    const ambiguities = await ctx.db
      .query("ambiguities")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const ambiguity of ambiguities) {
      await ctx.db.delete(ambiguity._id);
    }
    
    // Delete related questions
    const questions = await ctx.db
      .query("questions")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const question of questions) {
      await ctx.db.delete(question._id);
    }
    
    // Delete related documents
    const documents = await ctx.db
      .query("documents")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const document of documents) {
      await ctx.db.delete(document._id);
    }
    
    // Delete related events
    const events = await ctx.db
      .query("contextEvents")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const event of events) {
      await ctx.db.delete(event._id);
    }
    
    // Delete related deliverables
    const deliverables = await ctx.db
      .query("deliverables")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();
    for (const deliverable of deliverables) {
      await ctx.db.delete(deliverable._id);
    }
    
    return { success: true };
  },
});

