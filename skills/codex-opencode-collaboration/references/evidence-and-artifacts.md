# Evidence and generated artifacts

Read this when a task depends on a PDF, image, video frame, generated page, dataset export, or other derived artifact. Apply only the checks needed for the claim; ordinary copy edits do not require a new forensic workflow.

## Pin the object being reviewed

Record the source revision or hash, generation command/settings relevant to reproduction, output hash, and exact page/frame/region or rendered URL and locale. Keep this in the task's existing verification record rather than publishing private source material. If the source or output changes, revalidate affected claims. Unchanged portions may retain prior evidence when hashes or an inspected diff establish that they are unchanged.

State what was actually inspected: original file, rendered page/image, extracted text, OCR, supplied excerpt, or summary. A review of OCR is not a visual inspection of the source; a summary is not the original. A tool-call count or generic evidence grade does not establish that the requested page or region was examined.

## Choose a check that can settle the claim

- Content: inspect the authoritative field or artifact region, including the requested language and placement. A matching word elsewhere does not verify the requirement.
- Appearance: open the actual rendered artifact at a useful scale. Check the relevant crop, page, or viewport; report any uninspected region. Do not imply that an agent has vision merely because it accepted a path.
- Derived data: compare against an independently obtained expected value or source sample. Agreement between two outputs of the same pipeline can preserve the same error.
- Release: tie the observed deployed page or download to the released source/artifact, then exercise the user-facing entry point.

Concrete observations such as a quoted label or pixel location are useful supporting evidence, not standalone proof of access. When reviewers disagree, return to the source and an independent probe; do not settle correctness by majority vote. Preserve the original evidence and frozen deliverables, and distinguish a suggested fix from a regenerated and inspected output.
