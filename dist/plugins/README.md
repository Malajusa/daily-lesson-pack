# Reviewed maths candidate

These are prepared, unactivated plugin 0.2.1 candidates for Daily Lesson Pack resource version 3.10.0-rc.5. The candidate report records exact archive checksums and the required prior release guard. The full archive preserves the existing renderer and HTML QA overlay; the update archive contains only the reviewed byte delta. Do not activate either automatically.

The connected GitHub service published snapshot commit `10e0c82e6eab86bab7a661a37e9e8d7b9f28347c`, with tree `41af24f7c8e502a55ed1837514979be3baefda00`, byte-identical to local reviewed handoff `ec9881a586a71b0c26504b6a3e71cc05179343c5`. CLI authentication was unavailable, so published commit IDs differ from the original focused commits.

`maths-calibration-reviewed-history.bundle` preserves those original commits, including tested source `67c85b32a5be9a78dc0edb1ed047f5e3b72b91c7`. It requires base `18aa531182e359e29833f63f5327d506c8451d4d`, already in main. From a clone of this repository:

```sh
git bundle verify dist/plugins/maths-calibration-reviewed-history.bundle
git fetch dist/plugins/maths-calibration-reviewed-history.bundle refs/heads/codex/maths-calibration-progression-20261015:refs/remotes/reviewed-local/maths-calibration-progression
```

This restores the original source identities referenced by the candidate manifests and independent audit. It does not merge the branch or activate a plugin. Full-slide rendering, actual slideshow playback and classroom confirmation remain pending. See the implementation report and independent review under `docs/implementation/`.
