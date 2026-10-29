# Basic candidate deployment record

Date: 2026-10-29. File installation and hash verification only; no game execution of this candidate was performed.

## Backups made before deployment

Both original `SpeedRun` directories were copied, including their existing diagnostics backup files, and each copied file's SHA256 was verified against its source:

```text
backups/pre-basic-20261029/steam-SpeedRun
backups/pre-basic-20261029/save-SpeedRun
```

The original observer entry and metrics module remained unchanged in the repository and both live deployments. Inventory CSV contents were preserved. These backups are local recovery artifacts, not new active imports or a full game-save backup.

## Candidate destinations

```text
<game-install>/Stone Story_Data/StreamingAssets/Stonescript/SpeedRunBasic
<save-folder>/Stonescript/SpeedRunBasic
```

Both candidate destinations were absent before deployment. Five modules were copied into each and verified against repository sources. No existing unrelated files or Mind Stone text were overwritten. The exact root resolved by the game remains unisolated; installing identical candidate files in both roots avoids an intentionally inconsistent candidate version.

| Candidate-relative path | SHA256 |
|---|---|
| main.txt | 0D73A66BEE766B5E416067B05CFEE92C628A162BBD4B34D2123478C0BABA2B5B |
| config/Settings.txt | 9BBC4D78A9078329887D19F775465A7731FA1D82F396914D2479FD22CA6B9ACC |
| equipment/Catalog.txt | C0998A250E0E5642748A11D3EEE2F57D4E667C2430CAA8BF5180A9114B28A76D |
| locations/Dispatcher.txt | 2FBE3F332566CB3E325D0CC5B34ED7A14D39175D42C71881CD2A58803983C911 |
| combat/Generic.txt | 9C066053679F84D025E4527ACAA13E6E3AD94A161E65CA392522B7D2F8A175B4 |

Preserved observer entry SHA256: `A3CCD457DEBA302572F76AD4BED46CE5E49F1BA17E45F2DF92A213C184C9EA45`.

Preserved metrics SHA256: `6B5DCC9D5D12794BAA89456828884E02A4071B043C9DADB12CEE996A03BD8962`.

## Activation and rollback

To test, replace the old Mind Stone entry with `import SpeedRunBasic/main` and start a fresh manual run. Do not enable both entry points. Diagnostics are enabled, potion use is disabled. For rollback, restore `import SpeedRun/main`; original files remain available. See [BASIC_AUTOMATION.md](BASIC_AUTOMATION.md) for full instructions and [LOCATION_COVERAGE.md](LOCATION_COVERAGE.md) for all NOT RUN completion statuses.

Static checks passed on the source candidate; no native parser execution, combat completion, reliability, or timing accuracy is claimed. The prior user-reported loading/display pass applies only to the original observer.
