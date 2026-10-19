# Information Propagation Intelligence — FATHER OSINT

Status: architecture / planned; no live propagation data collected.

## Scope
Study dissemination of public information across Telegram channels, websites, media and other lawful public sources. Distinguish direct forwards, citations, links, near-duplicates and inferred relationships.

## Workspace tabs
- Timeline: first observed publication, edits, forwards, peaks, delayed waves.
- Propagation Waves: publication counts per configurable time bucket (minute/hour/day), by platform, source and topic.
- Source Lineage: earliest observed source vs verified origin; distinguish observation time from publication time.
- Cascade Graph: nodes=messages/sources, edges=forward/quote/link/similarity; provenance, evidence and confidence per edge.
- Screenshots & Media: capture metadata, hashes, thumbnails, perceptual hashes, OCR as optional enrichment, screenshot-to-source links.
- Comparisons: channel-to-channel ratios, lag, amplification, citation rate, original-vs-repost rate, overlap and coverage.
- Events: burst detection, change points, recurring waves, cross-platform migration.
- Evidence: immutable acquisition record, capture time, source URL/message ID, SHA-256, timezone, collection run and method.
- Analyst Review: hypotheses, counter-evidence, confidence and human confirmation.

## Core schema
Publication(id, platform, source_id, native_id, published_at_utc, edited_at_utc?, observed_at_utc, permalink?, text_hash, media_hashes[], acquisition_id)
PropagationEdge(from_publication_id, to_publication_id, type, evidence_refs[], confidence, observed_at_utc)
Screenshot(id, publication_id?, captured_at_utc, source_url?, sha256, storage_ref, capture_method, viewport, provenance)
Wave(event_id, bucket_start_utc, bucket_size_seconds, source_id?, platform?, publications, forwards, quotations, unique_sources)
EventCluster(id, normalized_claim, earliest_observed_at_utc, origin_status, review_state)
Comparison(event_id, source_a, source_b, overlap, median_lag_seconds, amplification_ratio, evidence_count)

## Important analytical constraints
- Earliest observed != true origin. Collection gaps, deletions, private channels, timezones and late indexing distort history.
- Screenshots are supporting evidence, not proof of authenticity without corroboration.
- Similarity is not evidence of coordination, common ownership or malicious activity.
- Track original publication time and capture/observation time separately.
- Avoid fabricating reach, views, missing posts or causal relationships.
- Public authorized data only, respect platform access limits and rate limits.
- Network collection must pass configured VPN security policy; fail closed on policy failure.

## UI design
Top: event selector + time range + source filters.
Center: synchronized timeline and propagation-wave chart.
Left: sources and channel cohorts.
Right: selected publication, screenshot, provenance, links, ALINA assessment.
Bottom: cascade graph, comparison matrix, evidence table.

## Gates
1. UI demo using explicitly synthetic events.
2. Import public post metadata from collector with provenance.
3. Normalize timestamps, reposts, citations and links.
4. Implement clustering, deduplication and wave aggregation.
5. Implement cascade graph and source comparison.
6. Screenshot evidence capture with hashing and review.
7. Quality evaluation and ALINA integration.
