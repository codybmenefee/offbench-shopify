import { query } from "../_generated/server";
import { v } from "convex/values";

export const listProjects = query({
  args: {
    status: v.optional(
      v.union(v.literal("active"), v.literal("archived"), v.literal("draft"))
    ),
  },
  handler: async (ctx, args) => {
    if (args.status) {
      return await ctx.db
        .query("projects")
        .withIndex("by_status", (q) => q.eq("status", args.status))
        .order("desc")
        .collect();
    }
    return await ctx.db
      .query("projects")
      .withIndex("by_lastUpdated")
      .order("desc")
      .collect();
  },
});

export const getProjectDetails = query({
  args: {
    projectId: v.id("projects"),
  },
  handler: async (ctx, args) => {
    const project = await ctx.db.get(args.projectId);
    if (!project) return null;

    // Get counts of related entities
    const gaps = await ctx.db
      .query("gaps")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();

    const conflicts = await ctx.db
      .query("conflicts")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();

    const ambiguities = await ctx.db
      .query("ambiguities")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();

    const questions = await ctx.db
      .query("questions")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();

    const documents = await ctx.db
      .query("documents")
      .withIndex("by_project", (q) => q.eq("projectId", args.projectId))
      .collect();

    return {
      ...project,
      gaps,
      conflicts,
      ambiguities,
      questions,
      documents,
    };
  },
});

export const getProjectByScenarioId = query({
  args: {
    scenarioId: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("projects")
      .withIndex("by_scenarioId", (q) => q.eq("scenarioId", args.scenarioId))
      .first();
  },
});

export const getProjectTimeline = query({
  args: {
    projectId: v.id("projects"),
  },
  handler: async (ctx, args) => {
    const events = await ctx.db
      .query("contextEvents")
      .withIndex("by_project_timestamp", (q) => q.eq("projectId", args.projectId))
      .order("desc")
      .collect();

    return events;
  },
});

