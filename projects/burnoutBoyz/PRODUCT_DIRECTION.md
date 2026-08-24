# BurnoutBoyz

> Your car's maintenance history, what should have happened, and what comes next.

BurnoutBoyz is a maintenance owner's manual for **all car owners**, not a Honda-only upgrade planner.

A user adds a vehicle by VIN or year/make/model/trim, enters current mileage, vehicle purchase/in-service date, driving conditions, and known maintenance records. BurnoutBoyz builds an evidence-backed maintenance timeline showing:

- Services that should already have occurred
- How many recurring service intervals have elapsed
- What the user confirms was actually completed
- Overdue or unknown maintenance
- What is coming next by mileage **or time**, whichever applies
- Active safety recalls
- Vehicle-specific fluids, parts, procedures, and source confidence when licensed data is available

## Important accuracy rule

Mileage alone is not enough. Manufacturer schedules can vary by engine, transmission, trim, region, time, and normal-versus-severe use. BurnoutBoyz must identify the vehicle as precisely as possible and show the source, schedule version, assumptions, and confidence. Generic fallback intervals must be labeled as general guidance, never presented as an OEM schedule.

## Data-source strategy

### Free official foundation

- NHTSA vPIC for VIN decoding and manufacturer-reported vehicle identity
- NHTSA Recalls API for safety recalls by year/make/model
- FuelEconomy.gov for EPA vehicle variants, fuel economy, emissions, and fuel characteristics

These sources do **not** provide a complete universal OEM maintenance schedule.

### Maintenance schedule candidates requiring commercial/license review

- MOTOR maintenance schedules
- Vehicle Databases Maintenance API
- Other OEM-authorized/licensed schedule providers discovered during research

The application needs a provider adapter and provenance registry so it can combine licensed OEM schedules, official recalls/specifications, manual imports, and carefully labeled generic fallback rules without silently blending them.

### Optional connected-car enhancement

Connected-car APIs such as Smartcar may provide current odometer, oil-life, diagnostics, or other data for compatible vehicles after owner authorization. Coverage varies by manufacturer, model, year, region, and endpoint. Manual mileage entry must always remain available.

## Core product flow

1. Create an account or use a privacy-preserving local trial.
2. Add a vehicle by VIN or year/make/model/trim.
3. Confirm the decoded configuration.
4. Enter mileage, in-service/purchase date, usage severity, and existing service records.
5. Review the maintenance timeline:
   - expected count
   - confirmed count
   - overdue/unknown count
   - next due mileage/date
6. Add receipts, notes, costs, parts, service location, and odometer evidence.
7. Receive configurable reminders.
8. Recheck recalls and update mileage over time.
9. Export or permanently delete the garage and service history.

## Production boundaries

- Never guarantee mechanical safety or replace a qualified mechanic.
- Never infer that a service was completed merely because an interval elapsed.
- Distinguish `expected`, `confirmed`, `unknown`, `overdue`, and `not applicable`.
- Cite every schedule source and license.
- Preserve schedule versions so historical recommendations do not silently change.
- Protect VINs, location, service records, receipts, and connected-car tokens as sensitive personal data.
- No ads or repair-shop recommendations disguised as maintenance requirements.

## Legacy migration

Useful deterministic planner/UI work from `/opt/data/HeRmEz/projects/honda-tech-upgrade` and its prior Vercel MVP may be migrated. Honda-specific branding and generic unsupported maintenance claims must not survive the production rebuild.
