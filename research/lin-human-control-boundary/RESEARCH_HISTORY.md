# LIN Human-Control Boundary — Research Development History

Archive prepared: 2026-11-09 (record preparation date; not proof of original creation time).

## Purpose
Preserve both experimental software versions without overwriting either. This is an engineering research log, not a claim of clinical or formal mathematical validation.

## v0.1 — Baseline governance simulator
- Standalone Python simulator with explicit approval, rejection, revocation, unauthorized execution prevention, Freeze, and controlled recovery.
- Archived test output records 6 passing tests.
- Scope: simulated external permissions, not inference of human cognition or real-device control.

## v0.2 — Fault-injection extension
- Added explicit fault cases: disconnection, expired authorization, executor mismatch, and audit failure, with Freeze/recovery handling.
- Archived test output records 8 passing tests.
- Scope: single-process simulated control; no real hardware or deployed API.

## Evidence classification
- L: research propositions and governance requirements; not validated by these software tests.
- D: design choices in the two prototypes.
- P: executable Python prototype and archived test outputs.
- X: external empirical, hardware, neurological, or formal proof **not established**.

## Preservation rules
1. Do not overwrite v0.1 with v0.2; each ZIP is preserved byte-for-byte.
2. Any future version should have its own folder, tests, changelog and hashes.
3. Before publication, separately verify provenance of theoretical claims, original specifications, and test reproducibility.
4. No GitHub or Zenodo changes were made when this archive was assembled.

## Files and SHA-256
- `LIN_Human_Control_Boundary_MVP_v0_1.zip`: `b8ac27d3b207a6208fac001aa3ea15a0ec10f5e39c8e13a29d6929d1081eb27c`
- `LIN_Human_Control_Boundary_MVP_v0_2.zip`: `b128ca1eb9738e395d51f80641628d6e81ff6fe2b0555cc1cea7dd4d80f021ee`

## GitHub upload status
Research history text uploaded first. Binary version archives and source files must be uploaded separately before claiming a complete archive.