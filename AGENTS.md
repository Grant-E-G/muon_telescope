# Agent Instructions

Before doing work in this repository, read the top-level `README.md`.

Follow the coding guidelines documented there for any code changes.

For hardware work, also read `docs/design.md`, `docs/build-and-debug.md`, and
`CONTRIBUTING.md`. Preserve these rules:

- Treat `docs/design.md` as the reviewed design intent. Update it in the same
  change when connectivity, component values, timing, pin assignments, or
  scientific scope changes.
- Use KiCad 10.0.5. Do not migrate KiCad files to another version implicitly.
- Do not guess a symbol pin number, footprint pad, connector orientation, or
  manufacturer part number. Check the current primary-source datasheet.
- Do not hand-edit, format, or mechanically rewrite KiCad source files.
- Do not approve manufacturing output without the release gates in
  `docs/build-and-debug.md` and an independent visual review.
- Keep the repository minimal. Extend an existing document or module when that
  keeps closely related work together.
