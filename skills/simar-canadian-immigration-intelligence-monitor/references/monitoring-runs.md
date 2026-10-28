# Immigration monitoring runs

## Build a self-contained run prompt

Include:
- The exact programs, jurisdictions, communities or case alias to check.
- Primary sources and the topic boundaries.
- The prior successful check/baseline if actually accessible, or a defined lookback window.
- What constitutes a meaningful change and whether to remain quiet if nothing changed.
- The required evidence, dates, practical implications, language and destination.
- A rule to disclose source failures and avoid unsupported legal conclusions.

Do not assume persistent memory or a previous result is available to the scheduler. If no baseline is accessible, establish a clearly dated baseline or use the requested lookback period; do not invent “new since last time.” Deduplicate by source, event identifier, effective date and substantive content where the available run state permits.

Use accessible scheduling/run state or an expressly authorized persistent artifact for baselines. Do not create a hidden client database or silently edit skill instructions as a substitute for monitoring state.

## Official source map

Use links as starting points and open operative instructions, not just headlines.

| Topic | Starting source |
| --- | --- |
| IRCC policy and delivery instructions | https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/operational-bulletins-manuals.html |
| Express Entry rounds and category changes | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html |
| All provincial nominee jurisdictions | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/provincial-nominees.html |
| Alberta streams and notices | https://www.alberta.ca/aaip-application-streams |
| RCIP/FCIP and official community links | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/rural-franco-pilots.html |
| Work-permit instructions | https://www.canada.ca/en/immigration-refugees-citizenship/services/work-canada.html |
| LMIA and employer-side rules | https://www.canada.ca/en/employment-social-development/services/foreign-workers.html |
| Occupational classification | https://noc.esdc.gc.ca/ |

For an all-PNP request, follow every current provincial/territorial program in the IRCC directory and record coverage; do not treat an Alberta/Ontario scan as national coverage. Research Quebec and Nunavut separately when in scope. For RCIP/FCIP, verify the relevant community body's current priorities, intake and designated-employer information as well as federal instructions.

Distinguish rule changes from announcements, draw results, new occupations, application openings, allocations and employer vacancies. A designated-employer list is not a job vacancy list. A changed webpage timestamp alone is not a substantive immigration change.

## Run-prompt patterns

Adapt these to the actual request; they are not pre-enabled tasks.

**Immigration digest**
“Check official Canadian immigration sources for material changes affecting [scope] during [lookback]. Verify operative instructions and effective dates. Report each change, affected group, practical action and direct source. List sources or jurisdictions that could not be verified. Use [language] and keep the report concise. Do not predict draws or guarantee eligibility.”

**Opening or rule-change watch**
“Check whether [exact program/stream/community condition] has changed from [verified baseline or defined state]. Notify me only if the condition is verified from the responsible official source. State the application window, who is included, material exceptions and source. If verification fails, disclose the coverage failure instead of reporting that no change occurred.”

**Case reminder**
“Remind me about [action] for [case alias] using the confirmed date [date and governing timezone]. State whether the date was user-supplied or independently verified. Do not present an unverified reminder date as a legal deadline or perform the filing.”

**Authorized intake triage**
“When this run is triggered by the authorized [source], fetch the actual matching item, apply the user's semantic conditions, extract relevant dates and missing documents, and prepare a concise internal triage note. Use the available immigration workflow to flag urgent issues. Do not send a client response, submit anything or broaden the data scope beyond the authorization.”

## Report shape

Lead with an urgent verified change, if any. Otherwise group meaningful updates by the requested scope.

| Change / source | Published and effective dates | Who is affected | Required or suggested action |
| --- | --- | --- | --- |

State the check period, actual coverage and material failures. Keep operational suggestions distinct from legal requirements. For “notify only if changed,” do not send a routine no-change digest; follow the automation system's supported quiet behaviour.

Use one consolidated digest for a broad recurring request unless the user asks for separate tasks. Choose a polling frequency proportionate to the requested condition within tool limits; never promise real-time alerts for a periodic poll.
