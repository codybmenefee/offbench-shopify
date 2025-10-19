# Test Scenarios for Discovery Tool Prototype

This document outlines **five lightweight, realistic scenarios** for testing the Discovery → Implementation Confidence Tool. Each scenario is designed to generate believable discovery artifacts (emails, transcripts, branding guides) that the tool can process to create implementation plans.

The goal is to keep scenarios **simple, clear, and representative** — not to test full enterprise complexity, but to validate that the tool can systematically strengthen discovery and catch gaps.

---

## Scenario 1 – "CozyHome" Shopify + QuickBooks Integration

### Context
A small home décor retailer uses Shopify for online sales and **QuickBooks Online** for accounting. They want to stop manually re-entering orders and sync inventory automatically.

### Key Systems
Shopify, QuickBooks Online

### Integration Goals
* Sync orders (Shopify → QuickBooks invoices)
* Sync inventory quantities (QuickBooks → Shopify)
* Push daily sales summary to QuickBooks

### Discovery Inputs (to simulate)
* Email thread between store owner and accountant
* Call transcript about pain points ("I spend 3 hours a day reconciling orders")
* Branding guide (product SKUs, store tone)

### Tool Output Expectation
A simple implementation plan with:
* Integration overview
* System of record table
* Data flow summary (orders, inventory, daily sales)
* 3–4 open questions (e.g. "Should refunds sync automatically?")

---

## Scenario 2 – "BrewCrew Coffee" Shopify + Klaviyo CRM

### Context
A coffee subscription brand wants to improve customer engagement. Shopify manages sales; **Klaviyo** handles marketing and customer segmentation.

### Key Systems
Shopify, Klaviyo

### Integration Goals
* Sync customer and order data from Shopify to Klaviyo
* Segment by product and purchase frequency
* Trigger "reorder reminder" emails automatically

### Discovery Inputs (to simulate)
* Slack-style chat transcript between marketing lead and developer
* Email chain about "wishlist" features
* Brand tone guide ("friendly, artisan voice")

### Tool Output Expectation
* Simple plan with data flow (Shopify → Klaviyo contacts, events)
* Email trigger workflow summary
* 2–3 open questions (e.g. "Do we sync guest checkouts?")

---

## Scenario 3 – "PetPawz" Shopify + ShipStation Integration

### Context
A pet accessories startup uses Shopify for orders and **ShipStation** for fulfillment. They currently print labels manually and want automation.

### Key Systems
Shopify, ShipStation

### Integration Goals
* Automatically create shipments when orders are paid
* Send tracking info back to Shopify
* Handle returns smoothly

### Discovery Inputs (to simulate)
* Customer support call notes ("We ship ~100 orders/day")
* Email from operations lead ("Need faster shipping label creation")
* Screenshot of Shopify orders dashboard

### Tool Output Expectation
* Step-by-step fulfillment flow
* 2–3 integration risks (e.g. API rate limits)
* Open questions ("How do we handle preorders?")

---

## Scenario 4 – "FitFuel" Shopify + Inventory App (Stocky)

### Context
A small fitness brand with two retail stores and an online store wants unified inventory tracking. Uses **Stocky** (Shopify app) for purchasing.

### Key Systems
Shopify, Stocky

### Integration Goals
* Sync store and online inventory
* Generate low-stock alerts
* Centralize purchase orders

### Discovery Inputs (to simulate)
* Team chat log discussing inventory mismatches
* Internal SOP doc about restocking
* Screenshot or mockup of inventory spreadsheet

### Tool Output Expectation
* Basic workflow diagram (even in text)
* List of fields to sync
* 2–3 open questions ("Which location is source of truth?")

---

## Scenario 5 – "Bloom & Co." Shopify + Local POS

### Context
A flower shop uses Shopify for online orders and a simple POS system for in-store sales. They want unified daily sales and inventory visibility.

### Key Systems
Shopify, Local POS

### Integration Goals
* Sync daily sales totals between POS and Shopify
* Keep shared product inventory updated
* Generate combined end-of-day report

### Discovery Inputs (to simulate)
* Email from shop manager ("We keep overselling tulips!")
* Chat transcript between POS vendor and store tech
* Short process doc describing current closing routine

### Tool Output Expectation
* Implementation summary with clear goals
* Table of data fields (items, prices, totals)
* 3 follow-ups ("Do we reconcile tax data?", "Which system closes the day?")

---

## Why These Scenarios Work for Prototyping

* **Limited Complexity**: Each uses 2–3 systems max (no deep ERP complexity)
* **Realistic Context**: Relatable SMB scenarios for Shopify integrators
* **Natural Artifacts**: Generate authentic discovery documents (emails, call transcripts, chat logs)
* **Built-in Ambiguity**: Each offers enough gaps for the tool to raise intelligent follow-ups
* **Representative Coverage**: Covers different integration patterns (accounting, marketing, fulfillment, inventory, POS)

---

## Next Steps

For each scenario, create sample discovery artifacts such as:
* 1–2 email threads
* 1 call/chat transcript
* 1 supporting document (branding guide, SOP, screenshot notes)

These artifacts should contain the right mix of:
* Clear requirements (to test parsing)
* Ambiguous statements (to test gap detection)
* Conflicting information (to test ambiguity surfacing)
* Missing details (to test question generation)

