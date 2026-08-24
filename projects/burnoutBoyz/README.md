# BurnoutBoyz

A data-backed maintenance owner's manual for every car owner.

Enter or decode your vehicle, current mileage, vehicle age, driving conditions, and maintenance history. BurnoutBoyz explains what maintenance should have occurred, what is confirmed, what is unknown or overdue, and what is coming next.

See [`PRODUCT_DIRECTION.md`](PRODUCT_DIRECTION.md) for the product contract, data strategy, and safety boundaries. The evidence-backed [`HONDA_PRIOR_ART_MIGRATION.md`](HONDA_PRIOR_ART_MIGRATION.md) records which legacy planner/UI patterns may migrate, which claims must not, and the Git/deployment recovery anchors.

## Current stage

Production research and migration planning. The previous Honda Tech Upgrade MVP is prior art, not the final product.

## Initial official data sources

- NHTSA vPIC: https://www.nhtsa.gov/cars/rules/manufacture
- NHTSA datasets and recalls APIs: https://www.nhtsa.gov/nhtsa-datasets-and-apis
- FuelEconomy.gov web services: https://www.fueleconomy.gov/feg/ws/

A complete OEM maintenance schedule will require licensed schedule data, manufacturer-authorized sources, or user-supplied manual data. BurnoutBoyz must label the source and confidence of every interval.
