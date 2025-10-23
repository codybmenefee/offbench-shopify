import { mutation } from "../_generated/server";
import { v } from "convex/values";

export const createDocument = mutation({
  args: {
    projectId: v.id("projects"),
    name: v.string(),
    type: v.string(),
    uploadDate: v.number(),
    size: v.number(),
    status: v.union(
      v.literal("processed"),
      v.literal("processing"),
      v.literal("pending")
    ),
    sourceLink: v.optional(v.string()),
    metadata: v.optional(v.any()),
    // New fields for integration-based storage
    externalId: v.optional(v.string()),
    externalUrl: v.optional(v.string()),
    integrationId: v.optional(v.string()),
    summary: v.optional(v.string()),
    source: v.union(
      v.literal("upload"),
      v.literal("integration"),
      v.literal("local")
    ),
  },
  handler: async (ctx, args) => {
    const documentId = await ctx.db.insert("documents", args);
    return documentId;
  },
});

export const updateDocumentSummary = mutation({
  args: {
    documentId: v.id("documents"),
    summary: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.documentId, { summary: args.summary });
    return args.documentId;
  },
});

export const syncDocuments = mutation({
  args: {
    projectId: v.id("projects"),
    documents: v.array(
      v.object({
        name: v.string(),
        type: v.string(),
        uploadDate: v.number(),
        size: v.string(),
        status: v.union(
          v.literal("processed"),
          v.literal("processing"),
          v.literal("pending")
        ),
        sourceLink: v.optional(v.string()),
        metadata: v.optional(v.any()),
      })
    ),
  },
  handler: async (ctx, args) => {
    const documentIds: string[] = [];

    for (const documentData of args.documents) {
      const documentId = await ctx.db.insert("documents", {
        projectId: args.projectId,
        ...documentData,
      });
      documentIds.push(documentId);
    }

    return { documentIds, count: documentIds.length };
  },
});

export const updateDocumentStatus = mutation({
  args: {
    documentId: v.id("documents"),
    status: v.union(
      v.literal("processed"),
      v.literal("processing"),
      v.literal("pending")
    ),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.documentId, {
      status: args.status,
    });
    return args.documentId;
  },
});

export const deleteDocument = mutation({
  args: {
    documentId: v.id("documents"),
  },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.documentId);
    return { success: true };
  },
});

