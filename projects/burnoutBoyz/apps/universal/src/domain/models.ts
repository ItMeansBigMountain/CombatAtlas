export type Confidence = 'high' | 'medium' | 'unknown';
export type ManualTab = 'Due now' | 'Upcoming' | 'History' | 'Recalls' | 'Sources';

export type MaintenanceItem = {
  id: string;
  title: string;
  due: string;
  state: 'due' | 'upcoming' | 'completed' | 'unknown';
  source: string;
  confidence: Confidence;
  note: string;
};

export type Vehicle = {
  id: string;
  nickname: string;
  identity: string;
  vinLast4?: string;
  mileage: number;
  severeUse: boolean;
  items: MaintenanceItem[];
};

export type GarageSnapshot = { vehicles: Vehicle[]; updatedAt: string; pendingSync: number };

export const starterGarage: GarageSnapshot = {
  updatedAt: new Date().toISOString(),
  pendingSync: 0,
  vehicles: [{
    id: 'demo-civic', nickname: 'Daily', identity: '2019 Honda Civic EX', vinLast4: '1842', mileage: 68120, severeUse: false,
    items: [
      { id: 'oil', title: 'Engine oil & filter', due: 'Review now · 68,120 mi', state: 'due', source: 'Owner manual schedule · demo only', confidence: 'medium', note: 'Planning item, not a diagnosis. Add a record if already completed.' },
      { id: 'brake', title: 'Brake fluid', due: 'October 2026', state: 'upcoming', source: 'Owner manual schedule · demo only', confidence: 'medium', note: 'Time-based estimate. Confirm against the manual for this configuration.' },
      { id: 'tires', title: 'Tire rotation', due: 'Completed · 64,300 mi', state: 'completed', source: 'Owner-confirmed receipt', confidence: 'high', note: 'Confirmed by the owner; receipt attached.' },
    ],
  }],
};
