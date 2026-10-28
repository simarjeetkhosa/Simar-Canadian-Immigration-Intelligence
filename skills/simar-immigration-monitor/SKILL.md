---
name: simar-immigration-monitor
description: Set up and manage requested Canadian immigration automations for Simar, including IRCC/Express Entry and all-PNP digests, AAIP/RCIP/FCIP intake watches, NOC and work-permit policy changes, case-date reminders and explicitly authorized intake-event triage. Use when the user asks to check later, repeatedly, on a schedule or when a relevant change occurs, or asks to edit/pause those tasks. Do not create a running task merely because this skill is installed or requested for improvement; exclude unrelated automations.
---

# Simar Immigration Monitor

Turn a requested future check into a real, verified automation using the available scheduling tools. Never claim that a skill file runs on its own.

Copyright (c) 2026 Simarjeet Khosa; see LICENSE for the MIT software licence. On another AI platform, use that host's supported scheduler and discover its actual capabilities. An imported ZIP, MCP workflow server or connected account does not itself create a schedule. Do not transfer private case material or claim an automation was migrated without creating and verifying it in the target host.

## Establish the requested job

Identify the subject, geographic/program scope, relevant condition, output language, timing/timezone and delivery destination. Reuse already supplied preferences. Default user-facing times to the current user's established timezone. For Simar's personal installation this is America/Toronto unless updated by the user or session; do not apply this personal default to another professional's installation without establishing their timezone.

Distinguish these requests:
- **Skill capability:** Create or improve instructions only. Do not activate tasks.
- **Recurring digest:** Schedule the requested repeated delivery.
- **Condition watch:** Check for a specific change and notify only when it is verified.
- **Case reminder:** Remind about a user-confirmed date, or verify the legal date before presenting it as established.
- **Intake-event triage:** Use a supported event trigger for an explicitly authorized source and action; do not quietly scan unrelated inboxes or substitute polling for a requested event.

Ask only for missing information that changes the task materially. When a direct recurring request leaves routine timing details open, use the scheduling tool's supported defaults and clearly report the resulting schedule.

## Create or update the actual task

1. Discover and follow the current automation tools and schemas. Use private lookup to check for an existing relevant task; list tasks publicly only when requested.
2. Prepare a self-contained run prompt using [monitoring runs](references/monitoring-runs.md). Include scope, sources, change criteria, evidence requirements, output format and failure handling. Keep scheduling details in the schedule fields.
3. Use the actual create/update tool for an authorized schedule request. Choose exact timing for named clock times, flexible timing for dayparts, and a recurring condition watch for future-condition checks. Apply the tool's current frequency limits and event-trigger rules.
4. For supported mail/calendar/project events, verify the source identity and authorization with the appropriate connector; resolve people before person-directed actions. Do not invent webhook support or connection state.
5. Stop for an actual connection, approval or unsupported timing requirement. Do not create a task that depends on inaccessible data while claiming it will work later.
6. Preserve existing schedules and settings outside the requested change. Avoid duplicates. Do not run an existing task immediately unless the user asks for an immediate run.
7. Confirm success only from the returned result. State what is monitored, the schedule/timezone, notification condition and destination. Distinguish creation from a completed run.

## Execute a monitoring run

Use Simar Immigration Intelligence when available for immigration research, source verification and case analysis. Discover it by skill name rather than hardcoding a local path. If unavailable, follow the primary-source and verification requirements in the monitoring reference.

Perform read-only research by default. Do not submit applications, contact employers/clients, send drafts, change case records or alter this skill merely because a watcher detected a change. A separately authorized action may proceed within its scope.

Do not put client identifiers, full immigration files or private contact details in public searches or task titles. For case reminders, use a case alias and the minimum necessary date/context.

If no change is found after successful checks, respect the requested quiet/digest behaviour. If sources cannot be checked, report a coverage limitation when it could matter; do not translate a retrieval failure into “no change.” Never claim complete monitoring when some named sources were not checked.

## Maintain the task

Use current tools to inspect runs, update, pause, resume or delete only as requested. For a failed or missed run, identify the actual status and explain what remains uncertain. Keep the user informed without promising continuous or instantaneous monitoring beyond the schedule's real capabilities.
