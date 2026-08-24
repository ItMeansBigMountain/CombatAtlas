ALTER TABLE interval_rules ADD COLUMN recurrence TEXT NOT NULL DEFAULT 'repeating' CHECK(recurrence IN ('repeating','one_time'));
ALTER TABLE interval_rules ADD COLUMN mileage_tolerance INTEGER NOT NULL DEFAULT 0 CHECK(mileage_tolerance >= 0);
ALTER TABLE interval_rules ADD COLUMN time_tolerance_days INTEGER NOT NULL DEFAULT 0 CHECK(time_tolerance_days >= 0);
