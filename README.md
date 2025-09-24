# AmiBroker AFL Project

Private repository for AFL development (indicators + strategies).

## Structure
- `src/` AFL sources
  - `indicators/` domain indicators (prefix `ind_`)
  - `strategies/` entry/exit logic (prefix `strat_`)
  - `utils/` helper functions (prefix `util_`)
- `tests/` test data + snapshot outputs
- `tools/` dev utilities (linters, scripts)
- `docs/` design/API, ADRs