import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import {
  computeMaintenancePlan,
  createSampleProfile,
  formatMiles,
  normalizeProfile,
  serviceEvents,
  vehicles,
} from './planner.js';

const STORAGE_KEY = 'honda-tech-upgrade-profile';

function loadInitialProfile() {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return stored ? normalizeProfile(JSON.parse(stored)) : createSampleProfile();
  } catch {
    return createSampleProfile();
  }
}

function StatusBadge({ status }) {
  return <span className={`badge ${status.replace(' ', '-')}`}>{status}</span>;
}

function App() {
  const [profile, setProfile] = useState(loadInitialProfile);
  const plan = useMemo(() => computeMaintenancePlan(profile), [profile]);

  function updateProfile(field, value) {
    const next = normalizeProfile({ ...profile, [field]: value });
    setProfile(next);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  }

  function loadSample() {
    const sample = createSampleProfile();
    setProfile(sample);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(sample));
  }

  function resetBlank() {
    const blank = normalizeProfile({ vehicle: 'Civic', mileage: 0, serviceEvent: 'Oil Change', serviceMileage: 0 });
    setProfile(blank);
    window.localStorage.removeItem(STORAGE_KEY);
  }

  return (
    <main className="shell" aria-labelledby="page-title">
      <section className="hero" aria-labelledby="page-title">
        <p className="eyebrow">Honda owner workflow · local demo</p>
        <h1 id="page-title">Plan the next maintenance move for your Honda</h1>
        <p className="lede">
          Enter a vehicle, mileage, and recent service event to get an instant ownership plan. This demo uses only local browser state — no accounts, credentials, VIN lookup, paid APIs, or private data.
        </p>
      </section>

      <section id="demo" className="planner" aria-label="Honda maintenance planner">
        <form className="card form-card" onSubmit={(event) => event.preventDefault()}>
          <h2>Vehicle snapshot</h2>
          <label htmlFor="vehicle">Vehicle</label>
          <select id="vehicle" value={profile.vehicle} onChange={(event) => updateProfile('vehicle', event.target.value)}>
            {vehicles.map((vehicle) => <option key={vehicle} value={vehicle}>Honda {vehicle}</option>)}
          </select>

          <label htmlFor="mileage">Current mileage</label>
          <input id="mileage" type="number" min="0" step="100" inputMode="numeric" value={profile.mileage} onChange={(event) => updateProfile('mileage', event.target.value)} />

          <label htmlFor="serviceEvent">Recent service event</label>
          <select id="serviceEvent" value={profile.serviceEvent} onChange={(event) => updateProfile('serviceEvent', event.target.value)}>
            {serviceEvents.map((service) => <option key={service} value={service}>{service}</option>)}
          </select>

          <label htmlFor="serviceMileage">Mileage at that service</label>
          <input id="serviceMileage" type="number" min="0" step="100" inputMode="numeric" value={profile.serviceMileage} onChange={(event) => updateProfile('serviceMileage', event.target.value)} />

          <div className="actions">
            <button type="button" onClick={() => updateProfile('mileage', profile.mileage)}>Build maintenance plan</button>
            <button type="button" className="secondary" onClick={loadSample}>Load sample data</button>
            <button type="button" className="ghost" onClick={resetBlank}>Reset blank</button>
          </div>
        </form>

        <section className="results card" aria-live="polite">
          <p className="eyebrow">Next ownership action</p>
          <h2>{plan.primary.service}</h2>
          <p className="lede">{plan.summary}</p>
          <p>{plan.planningNote}</p>

          <ol className="timeline">
            {plan.timeline.map((item) => (
              <li key={item.service}>
                <StatusBadge status={item.status} />
                <strong>{item.service}</strong>
                <span>{item.summary} Next target: {formatMiles(item.nextDue)}.</span>
              </li>
            ))}
          </ol>

          <p className="local-note">Saved locally in this browser only. Use “Load sample data” to restore the demo or “Reset blank” to clear it.</p>
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
