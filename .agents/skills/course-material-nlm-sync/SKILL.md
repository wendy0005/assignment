---
name: course-material-nlm-sync
description: Add new or updated course learning materials to existing NotebookLM notebooks without duplicate uploads. Use in this assignment repo when the user says there are new course materials, asks to check existing NLM sources, or wants course uploads synced. Reuse each course's notebook rather than creating another notebook.
---

# Sync course materials to NotebookLM

Use this workflow for course-material updates in this repository. For authentication, source commands, and processing status, consult [the installed NLM skill](../nlm-skill/SKILL.md). Do not generate quizzes, podcasts, or other Studio artifacts as part of an upload request.

## Course and destination

- Read [the course notebook registry](references/course-notebooks.json). It records the existing Operating Systems and Algorithms notebooks, local download folders, and successful replacements for failed originals.
- Infer the course from the user's material path or course code. Ask only if it remains ambiguous.
- If the user supplies an LMS link, use the repository's current scraper workflow to collect the requested new materials into Downloads before syncing. Inspect its current instructions and implementation; a signed-in LMS URL is not a useful public NotebookLM source.
- Resolve `~/Downloads/Camu Materials/` for the current user. Keep original files in their course folders; do not move them into this skill or commit them.
- Verify the saved notebook ID with a live notebook read under the intended NLM account. If unavailable, list notebooks and match the course code/title. A missing notebook may mean the wrong account or stale registry; do not create a replacement automatically.
- For an unregistered course, look for an existing matching notebook first. If none exists, ask whether to create its first notebook. For a registered course, keep using its existing notebook unless the user explicitly requests another.

## Check before uploading

Read `~/Downloads/Camu Materials/notebooklm-upload-manifest.json` if present, then list the destination notebook's sources live. Local state alone does not establish that a source still exists or is ready.

1. Inventory actual learning files. Exclude `.DS_Store`, scraper JSON, upload receipts/manifests, README instructions, and generated import-copy folders. Include substantive lesson Markdown/text, but skip image-link-only Markdown when the linked images are already represented.
2. Compute SHA-256 for each original file. Use its path relative to `Camu Materials` as the manifest key and a descriptive course-relative path as the source title.
3. Match content hashes within this course, including files renamed or moved. When a manifest hash matches and its recorded source ID is live and ready, skip it.
4. Check live titles and known replacement IDs as well. If the current hash matches a registered replacement's `original_sha256` and its source ID is live and ready, skip the failed original and its import copies. If that hash differs, the replacement covers an older version; handle the file as revised material. Mark a title-only match as unverified content, not a verified hash match. If the user reports a revision or local evidence indicates change, inspect the existing source or resolve the ambiguity before deciding it is unchanged.
5. If a tracked file's hash changed, treat it as revised material. Upload the revision to the same notebook with a distinguishable title, such as a date plus a short hash. Retain the earlier source unless the user authorizes replacement/deletion. Do not upload a second revision if that hash is already represented by a ready source.
6. If the source ID is absent remotely, re-upload the missing material. If it is still processing, wait or check its status; do not upload another copy. If it failed, inspect and report the failure rather than treating its title as a successful duplicate check.

For files imported before hash tracking, a matching title is a candidate existing source. Read enough source content/metadata to establish whether it represents the material when needed. If comparison cannot establish whether a reported revision is new, ask a focused question rather than silently skipping it or uploading an uncertain duplicate. Never manufacture hashes for existing remote sources.

## Upload only missing or revised material

- Confirm the active account when multiple NLM profiles exist; use the chosen profile explicitly. Authenticate if credentials have expired. Keep credentials out of output and repo files.
- Fetch the live source list again before mutations if the earlier inventory is stale or other uploads occurred.
- Upload sequentially to the resolved notebook, allowing the NLM skill's recommended spacing between source operations. For CLI use, check current help for flags; the installed executable may require `~/.local/bin/nlm` when it is absent from PATH.
- Capture the source ID immediately, then verify processing. An accepted upload is not yet a ready source. If an upload command fails or times out, list live sources before any retry: it may already have created an entry.
- Record each result immediately and write the manifest atomically, preserving existing records and unrelated fields. Store original file hash, notebook ID, source ID, title, representation type, and processing status. Preserve existing `result.source_id` records when extending the earlier manifest format.
- For a transformed source, record both the original file hash and the replacement source ID/hash. This lets a later run recognize the original as already represented even if the failed original entry is removed.
- Bound recovery: after a confirmed failure, use one appropriate fallback if useful. Do not repeatedly upload the same bytes or cycle through formats without evidence. Report unresolved files and keep their original downloads.
- For scanned charts, use OCR or a searchable document and disclose any loss of layout/hierarchy. For video, verify whether it contains speech before transcribing; music-only material may need visual notes. Label sampled visual notes accurately. Do not automatically regenerate a fallback that already exists and is ready.
- Do not delete sources, clear failed entries, rename existing notebooks, or create another notebook as routine cleanup. Obtain explicit authorization for source deletion, following the NLM skill.

## Finish

Refresh the source list. Report the course notebook link, added/revised/skipped counts, processing failures, and any fallback limitations. Save the updated upload manifest in Downloads. Do not claim all materials are ready while some are still processing or failed. Do not commit, push, or upload unrelated local files as part of the sync.
