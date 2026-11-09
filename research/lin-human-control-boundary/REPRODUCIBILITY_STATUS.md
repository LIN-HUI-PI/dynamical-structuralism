# Reproducibility and provenance status (2026-11-09)

## Original local archives (not yet committed to GitHub)
- v0.1 ZIP SHA-256: `b8ac27d3b207a6208fac001aa3ea15a0ec10f5e39c8e13a29d6929d1081eb27c`
- v0.2 ZIP SHA-256: `b128ca1eb9738e395d51f80641628d6e81ff6fe2b0555cc1cea7dd4d80f021ee`
- Local extraction and retest of these **original archives** on 2026-11-09: v0.1 6/6 tests passed, v0.2 8/8 tests passed.
- Tests used Python unittest; results do not demonstrate real-world hardware safety or human cognitive sovereignty.

## Important provenance limitation
The Python source previously committed to `v0.1/` and `v0.2/` was reconstructed in chat and is **not verified byte-for-byte identical** to the ZIP archives above. GitHub Actions runs the **GitHub source**, not the archived originals. Do not cite CI results as reproducing the original archive until the source is reconciled.

## CI
`.github/workflows/lin-human-control-boundary.yml` runs two separate unittest jobs on GitHub. A committed workflow does not by itself establish a passing CI run; inspect the Actions tab for status.

## Remaining work
1. Upload the original ZIP archives unchanged.
2. Verify hashes after retrieval.
3. Compare committed sources to extracted originals and correct the repository using version-preserving commits.
4. Verify GitHub Actions jobs and preserve logs.
