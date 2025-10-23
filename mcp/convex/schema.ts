import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

/**
 * Convex Schema for Discovery Agent MCP
 * Matches frontend data structures exactly
 */

export default defineSchema({
  // Projects table - main project entities
  projects: defineTable({
    name: v.string(),
    scenarioId: v.string(),
    confidence: v.number(),
    gapsCount: v.number(),
    conflictsCount: v.number(),
    ambiguitiesCount: v.number(),
    documentsCount: v.number(),
    lastUpdated: v.number(),
    status: v.union(
      v.literal("active"),
      v.literal("archived"),
      v.literal("draft")
    ),
  }).index("by_scenarioId", ["scenarioId"])
    .index("by_status", ["status"])
    .index("by_lastUpdated", ["lastUpdated"]),

  // Gaps table - missing information
  gaps: defineTable({
    projectId: v.id("projects"),
    category: v.string(),
    description: v.string(),
    impact: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    priority: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    status: v.union(
      v.literal("open"),
      v.literal("in-progress"),
      v.literal("resolved")
    ),
    identifiedDate: v.number(),
    suggestedQuestion: v.optional(v.string()),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_priority", ["priority"])
    .index("by_project_status", ["projectId", "status"]),

  // Conflicts table - contradictions
  conflicts: defineTable({
    projectId: v.id("projects"),
    category: v.string(),
    description: v.string(),
    impact: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    priority: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    status: v.union(
      v.literal("open"),
      v.literal("in-progress"),
      v.literal("resolved")
    ),
    identifiedDate: v.number(),
    conflictingStatements: v.array(v.string()),
    sources: v.array(v.string()),
    resolution: v.optional(v.string()),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_priority", ["priority"])
    .index("by_project_status", ["projectId", "status"]),

  // Ambiguities table - unclear requirements
  ambiguities: defineTable({
    projectId: v.id("projects"),
    category: v.string(),
    description: v.string(),
    impact: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    clarificationNeeded: v.string(),
    clarification: v.optional(v.string()),
    status: v.union(
      v.literal("open"),
      v.literal("clarified"),
      v.literal("resolved")
    ),
    identifiedDate: v.number(),
    context: v.string(),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_project_status", ["projectId", "status"]),

  // Questions table - questions needing answers
  questions: defineTable({
    projectId: v.id("projects"),
    question: v.string(),
    category: v.string(),
    priority: v.union(
      v.literal("high"),
      v.literal("medium"),
      v.literal("low")
    ),
    status: v.union(
      v.literal("open"),
      v.literal("answered"),
      v.literal("deferred")
    ),
    askedDate: v.number(),
    answer: v.optional(v.string()),
    answeredDate: v.optional(v.number()),
    whyItMatters: v.optional(v.string()),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_priority", ["priority"])
    .index("by_project_status", ["projectId", "status"]),

  // Documents table - uploaded/ingested documents
  documents: defineTable({
    projectId: v.id("projects"),
    name: v.string(),
    type: v.string(),
    uploadDate: v.number(),
    size: v.number(), // Changed from string to number (bytes)
    status: v.union(
      v.literal("processed"),
      v.literal("processing"),
      v.literal("pending")
    ),
    sourceLink: v.optional(v.string()),
    metadata: v.optional(v.any()),
    // New fields for integration-based storage
    externalId: v.optional(v.string()), // Google Drive file ID
    externalUrl: v.optional(v.string()), // Direct link from Merge API
    integrationId: v.optional(v.string()), // Links to user's Google Drive integration
    summary: v.optional(v.string()), // AI-generated summary (from agent)
    source: v.union(
      v.literal("upload"),
      v.literal("integration"),
      v.literal("local")
    ),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_type", ["type"])
    .index("by_source", ["source"])
    .index("by_externalId", ["externalId"]),

  // Context Events table - activity timeline
  contextEvents: defineTable({
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
    timestamp: v.number(),
    metadata: v.optional(v.any()),
  }).index("by_project", ["projectId"])
    .index("by_timestamp", ["timestamp"])
    .index("by_project_timestamp", ["projectId", "timestamp"])
    .index("by_eventType", ["eventType"]),

  // Deliverables table - generated outputs
  deliverables: defineTable({
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
    generatedDate: v.number(),
    status: v.union(
      v.literal("draft"),
      v.literal("final"),
      v.literal("archived")
    ),
    fileType: v.string(),
    downloadUrl: v.optional(v.string()),
  }).index("by_project", ["projectId"])
    .index("by_status", ["status"])
    .index("by_type", ["type"]),

  // Auth Keys table - API keys for MCP authentication
  authKeys: defineTable({
    key: v.string(),
    name: v.string(),
    createdAt: v.number(),
    expiresAt: v.optional(v.number()),
    isActive: v.boolean(),
  }).index("by_key", ["key"])
    .index("by_isActive", ["isActive"]),
});

