import test from 'node:test';
import assert from 'node:assert/strict';
import {
  computeMaintenancePlan,
  createSampleProfile,
  normalizeProfile,
} from './planner.js';

test('normalizes a credential-free Honda owner profile', () => {
  assert.deepEqual(normalizeProfile({
    vehicle: 'Accord',
    mileage: '48250',
    serviceEvent: 'Oil Change',
    serviceMileage: '43000',
  }), {
    vehicle: 'Accord',
    mileage: 48250,
    serviceEvent: 'Oil Change',
    serviceMileage: 43000,
  });
});

test('computes the next service suggestion from selected event and mileage', () => {
  const plan = computeMaintenancePlan({
    vehicle: 'Civic',
    mileage: 45200,
    serviceEvent: 'Oil Change',
    serviceMileage: 40000,
  });

  assert.equal(plan.primary.service, 'Oil Change');
  assert.equal(plan.primary.status, 'overdue');
  assert.equal(plan.primary.nextDue, 45000);
  assert.equal(plan.primary.milesOver, 200);
  assert.match(plan.summary, /Civic at 45,200 miles/);
  assert.ok(plan.timeline.some((item) => item.service === 'Tire Rotation'));
});

test('provides sample profile data that can be loaded or reset without credentials', () => {
  const sample = createSampleProfile();
  assert.equal(sample.vehicle, 'CR-V');
  assert.equal(sample.mileage, 68400);
  assert.equal(sample.serviceEvent, 'Tire Rotation');
  assert.equal(sample.serviceMileage, 60000);

  const plan = computeMaintenancePlan(sample);
  assert.equal(plan.primary.status, 'overdue');
});
