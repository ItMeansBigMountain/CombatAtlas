# Honda Tech Upgrade implementation status

This file keeps developer-facing context that should not appear in the public demo UI.

## Current state

- The Vercel app is a static React/Vite product review shell.
- It presents the Honda owner value proposition, demo boundaries, and next integration plan.
- No VIN decoding, persistence, customer accounts, paid maintenance API, parts pricing, or service-history import is wired yet.

## Imported project signal

The original imported project notes described a Honda vehicle app for mileage logs, maintenance tracking, and service suggestions. They also included scaffold/backlog language and retired local machine paths from the import process. Those details are useful for triage, but they should remain in developer docs and not in customer-facing cards.

## Next implementation slice

1. Add a vehicle profile form that accepts VIN or manual year/make/model/trim entry.
2. Use NHTSA vPIC for free VIN decoding where VIN is provided.
3. Seed common Honda Civic/Accord interval data locally so the first planner works without paid APIs.
4. Abstract a maintenance provider interface before evaluating commercial OEM maintenance schedule providers.
5. Add saved vehicle profiles and service history only after the single-vehicle planner is useful.
