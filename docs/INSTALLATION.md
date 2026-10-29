# Lifecycle and measurement observer

This guide describes the preserved observer-only `SpeedRun` entry. For the separate basic automation candidate, use [BASIC_AUTOMATION.md](BASIC_AUTOMATION.md) and its `SpeedRunBasic` import; do not enable both entry points.

Status: **loading/import execution and visible diagnostics verified in-game by the owner on 2026-10-29**. Lifecycle resets, timing accuracy, completion capture, and Ouroboros handling remain unverified. Exact game build and baseline target were not supplied. This observer issues no equipment, ability, potion, movement, pause, or persistent-storage commands. It observes the run driven by the game's existing behavior and any other script you choose to retain.

## Install

Paths below use portable placeholders instead of a local username or Steam account ID. Exact original local-path documents are retained in ignored backups.

Local path supplied by the owner (2026-10-29):

```text
<game-install>/Stone Story_Data/StreamingAssets/Stonescript
```

Both observer files were installed beneath this directory as `SpeedRun/main.txt` and `SpeedRun/metrics/RunMetrics.txt`. A matching deployment was also found under:

```text
<user-profile>/AppData/LocalLow/Martian Rex, Inc_/Stone Story/<steam-account-id>/Stonescript
```

Diagnostics are currently enabled in the working copies. The owner confirmed successful loading after adding `import SpeedRun/main`. Because both roots contain the scripts, that observation does not isolate which copy the game resolves. Do not reinstall, move, disable, or overwrite either deployment just to follow this guide; the existing deployment is working.

1. Back up the current Mind Stone text and any existing destination scripts.
2. Locate your game's actual save-file directory. Use the official manual's [external-script section](https://stonestoryrpg.com/stonescript/manual.html#import) and its save-folder link; do not assume the repository is the game's import folder. Platform/save layouts differ.
3. For an observer-only installation, create `SpeedRun` inside that save directory's `Stonescript` folder. Copy only `scripts/main.txt` and `scripts/metrics/RunMetrics.txt`, preserving these paths (the separate `scripts/basic` candidate uses a different import root):

   ```text
   Stonescript/SpeedRun/main.txt
   Stonescript/SpeedRun/metrics/RunMetrics.txt
   ```

4. For a new installation, ensure `showDiagnostics` is `true` for validation. It is already enabled in the current working deployment; no change is needed now.
5. Add exactly one line to the Mind Stone:

   ```stonescript
   import SpeedRun/main
   ```

6. Start a fresh run manually with the Mind Stone enabled. Verify imports and diagnostics before relying on any measurement. Retain other automation only if you deliberately want to measure it; record that configuration.

Deployment copies are separate from the repository. Recopy only when an update is deliberately requested, after identifying the resolved root and preserving local changes. After changing configuration or imports, start a fresh manual run; reload behavior should not be inferred from editing during play. This documentation update did not change either working deployment.

## Architecture and project helper interface

- `scripts/main.txt` owns lifecycle dispatch and the diagnostics switch. It creates a measurement object once. Fresh entry resets session results; Ouroboros loops start a new attempt while retaining the last completed result. First execution mid-run starts an explicitly partial observation.
- `scripts/metrics/RunMetrics.txt` defines the measurement object. `Begin(kind, fromBoundary)` resets attempt state; `Observe()` latches one positive leaderboard completion after observing zero; `ElapsedFrames()` returns the observed interval; `Draw(loops)` renders optional diagnostics. `ResetSession()` clears retained results.
- Future location dispatch belongs at the marked point in `main.txt`, after lifecycle and before observation. Handlers can receive the measurement object explicitly if needed. No handler registry, arbitration engine, or empty combat modules are introduced.

All helper names above are project functions. Native timing/lifecycle fields come from the official manual. No location-specific conditions exist.

## What the measurements mean

| Field | Meaning |
|---|---|
| `startKind` | `entry`, `loop`, or `attached`; identifies the observed boundary |
| Observed interval | `totaltime` minus the captured start frame; continues after boss defeat, so it is not a frozen completion score |
| Location / accumulated | Raw `time` and `totaltime` for diagnosing transitions |
| Current completion | Captured `lbtime` for this full attempt; `-1` means no eligible completion observed |
| Last completion | Latest eligible completion retained across observed loops, including failed/unfinished subsequent attempts; `-1` means none |
| Full completions seen | Count of captured results, not attempts, deaths, or reliability |
| Loops seen | Ouroboros boundaries observed since entry/initialization; not the game's absolute loop number after late attachment |

An attached interval never contributes a completion result. At the next observed loop it becomes eligible. A full attempt must observe `lbtime = 0` before a positive value is accepted. This conservative rule can omit a result if a boundary/reset is missed; it should not invent one. No failure detection, death counting, statistics, disk export, historical benchmark set, or wall-clock measurement is provided.

Diagnostics use advanced prints each enabled frame because display persistence is not assumed. With diagnostics disabled, there is no rendering or string-formatting work. Normal operation checks lifecycle flags and a small completion latch; there are no growing arrays, inventory scans, timers incremented each frame, or repeated state snapshots. Actual overhead remains unmeasured.

## In-game acceptance

Record game build/platform, script revision, location/difficulty, gear, retained Mind Stone logic, potion/resources, and results. Check recent Stonescript errors with the game's diagnostics (Tab on PC).

| Scenario | Expected result to verify |
|---|---|
| Fresh manual entry | `entry`, loops 0, no completion, count 0; interval begins at boundary |
| Normal progression and boss sub-location | Accumulated interval remains meaningful; lifecycle does not unexpectedly reset |
| Boss defeat | Score equals displayed leaderboard result; count increments once, never on subsequent result frames |
| Ouroboros loop, repeated twice | `loop`; interval restarts; current result clears; last result/count survive; no stale score capture |
| Leave and manually restart | Session count and last result reset |
| First install during a run | `attached`, interval starts at attachment, no full completion credited; next loop enables full measurement |
| Open/close Mind Stone without editing | No unintended lifecycle reset or duplicate completion |
| Disable/re-enable Mind Stone or miss a boundary | Record what actually happens; measurements spanning missed boundaries are invalid; restart manually |
| Failure/abandonment | No synthetic completion; no reliability claim inferred from count |
| Diagnostics false | No observer text; gameplay/equipment unchanged; compare timing against diagnostics-on and observer-absent runs |

Use a location that reports `lbtime` and can loop for completion tests. Zero-only `lbtime` locations will not yield a result. If the score is exposed only after script execution ends, the latch may miss it; verify on the installed build. Check small-screen overlay readability and overlap separately.

Loading/import execution and visible diagnostics have passed by user report. The scenarios above remain expected results, not recorded passes. Use [the structured acceptance checklist and failure template](OBSERVER_ACCEPTANCE.md) as the result-tracking document. Overall observer acceptance remains pending. Do not begin performance comparisons from a mid-run attachment or a run with missed boundaries.
