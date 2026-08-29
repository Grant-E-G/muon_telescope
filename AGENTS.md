# Agent Instructions

Before doing work in this repository, read the top-level `README.md`.

Follow the coding guidelines documented there for any code changes.

For hardware work, also read `docs/design.md`, `docs/build-and-debug.md`, and
`CONTRIBUTING.md`. Preserve these rules:

- Treat `docs/design.md` as the reviewed design intent. Update it in the same
  change when connectivity, component values, timing, pin assignments, or
  scientific scope changes.
- Use KiCad 9.0.9. Do not migrate KiCad files to another version implicitly.
- Do not guess a symbol pin number, footprint pad, connector orientation, or
  manufacturer part number. Check the current primary-source datasheet.
- For every selected part with a public datasheet, drawing, manual, or similar
  primary documentation, keep an unmodified local copy under
  `docs/datasheets/` and map its exact manufacturer number, source URL, and
  retrieval date in `docs/datasheets/README.md`. Add or replace the document in
  the same change as the part selection; do not silently retain stale files. If
  the manufacturer publishes only a maintained web page, record that URL and
  the lack of a static document in the index.
- Do not hand-edit, format, or mechanically rewrite KiCad source files.
- Do not approve manufacturing output without the release gates in
  `docs/build-and-debug.md` and an independent visual review.
- Keep the repository minimal. Extend an existing document or module when that
  keeps closely related work together.
