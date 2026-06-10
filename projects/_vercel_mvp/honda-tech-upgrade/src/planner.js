export const SERVICE_INTERVALS = {
  Civic: {
    'Oil Change': 5000,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
  Accord: {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
  'CR-V': {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
};

export const serviceEvents = Object.keys(SERVICE_INTERVALS.Civic);
export const vehicles = Object.keys(SERVICE_INTERVALS);

function toMileage(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

export function createSampleProfile() {
  return {
    vehicle: 'CR-V',
    mileage: 68400,
    serviceEvent: 'Tire Rotation',
    serviceMileage: 60000,
  };
}

export function normalizeProfile(input = {}) {
  const vehicle = SERVICE_INTERVALS[input.vehicle] ? input.vehicle : 'Civic';
  const serviceEvent = SERVICE_INTERVALS[vehicle][input.serviceEvent] ? input.serviceEvent : 'Oil Change';
  const mileage = toMileage(input.mileage);
  const serviceMileage = Math.min(toMileage(input.serviceMileage), mileage || Number.MAX_SAFE_INTEGER);

  return {
    vehicle,
    mileage,
    serviceEvent,
    serviceMileage,
  };
}

export function formatMiles(miles) {
  return `${Number(miles).toLocaleString('en-US')} miles`;
}

function buildTimeline(profile) {
  return Object.entries(SERVICE_INTERVALS[profile.vehicle]).map(([service, interval]) => {
    const knownServiceMileage = service === profile.serviceEvent ? profile.serviceMileage : 0;
    const cycleDue = (Math.floor(profile.mileage / interval) + 1) * interval;
    const nextDue = knownServiceMileage > 0 ? knownServiceMileage + interval : cycleDue;
    const milesUntilDue = nextDue - profile.mileage;

    if (milesUntilDue <= 0) {
      return {
        service,
        interval,
        nextDue,
        status: 'overdue',
        milesOver: Math.abs(milesUntilDue),
        summary: `${service} is overdue by ${formatMiles(Math.abs(milesUntilDue))}.`,
      };
    }

    return {
      service,
      interval,
      nextDue,
      status: milesUntilDue <= 1500 ? 'due soon' : 'planned',
      milesLeft: milesUntilDue,
      summary: `${service} is due in ${formatMiles(milesUntilDue)}.`,
    };
  }).sort((a, b) => {
    const aDistance = a.status === 'overdue' ? -a.milesOver : a.milesLeft;
    const bDistance = b.status === 'overdue' ? -b.milesOver : b.milesLeft;
    return aDistance - bDistance;
  });
}

export function computeMaintenancePlan(rawProfile) {
  const profile = normalizeProfile(rawProfile);
  const timeline = buildTimeline(profile);
  const primary = timeline.find((item) => item.service === profile.serviceEvent) || timeline[0];
  const planned = timeline.find((item) => item.status === 'planned');

  return {
    profile,
    primary,
    timeline,
    summary: `${profile.vehicle} at ${formatMiles(profile.mileage)}: ${primary.summary}`,
    planningNote: planned
      ? `Plan ahead for ${planned.service} around ${formatMiles(planned.nextDue)}.`
      : 'All tracked services need attention soon; prioritize a maintenance visit.',
  };
}
