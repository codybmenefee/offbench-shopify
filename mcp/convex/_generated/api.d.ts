/* eslint-disable */
/**
 * Generated `api` utility.
 *
 * THIS CODE IS AUTOMATICALLY GENERATED.
 *
 * To regenerate, run `npx convex dev`.
 * @module
 */

import type * as mutations_ambiguities from "../mutations/ambiguities.js";
import type * as mutations_conflicts from "../mutations/conflicts.js";
import type * as mutations_deliverables from "../mutations/deliverables.js";
import type * as mutations_documents from "../mutations/documents.js";
import type * as mutations_events from "../mutations/events.js";
import type * as mutations_gaps from "../mutations/gaps.js";
import type * as mutations_projects from "../mutations/projects.js";
import type * as mutations_questions from "../mutations/questions.js";
import type * as queries_ambiguities from "../queries/ambiguities.js";
import type * as queries_conflicts from "../queries/conflicts.js";
import type * as queries_deliverables from "../queries/deliverables.js";
import type * as queries_documents from "../queries/documents.js";
import type * as queries_gaps from "../queries/gaps.js";
import type * as queries_projects from "../queries/projects.js";
import type * as queries_questions from "../queries/questions.js";

import type {
  ApiFromModules,
  FilterApi,
  FunctionReference,
} from "convex/server";

/**
 * A utility for referencing Convex functions in your app's API.
 *
 * Usage:
 * ```js
 * const myFunctionReference = api.myModule.myFunction;
 * ```
 */
declare const fullApi: ApiFromModules<{
  "mutations/ambiguities": typeof mutations_ambiguities;
  "mutations/conflicts": typeof mutations_conflicts;
  "mutations/deliverables": typeof mutations_deliverables;
  "mutations/documents": typeof mutations_documents;
  "mutations/events": typeof mutations_events;
  "mutations/gaps": typeof mutations_gaps;
  "mutations/projects": typeof mutations_projects;
  "mutations/questions": typeof mutations_questions;
  "queries/ambiguities": typeof queries_ambiguities;
  "queries/conflicts": typeof queries_conflicts;
  "queries/deliverables": typeof queries_deliverables;
  "queries/documents": typeof queries_documents;
  "queries/gaps": typeof queries_gaps;
  "queries/projects": typeof queries_projects;
  "queries/questions": typeof queries_questions;
}>;
declare const fullApiWithMounts: typeof fullApi;

export declare const api: FilterApi<
  typeof fullApiWithMounts,
  FunctionReference<any, "public">
>;
export declare const internal: FilterApi<
  typeof fullApiWithMounts,
  FunctionReference<any, "internal">
>;

export declare const components: {};
