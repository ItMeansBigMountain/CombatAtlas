const intervals = {
  Civic: {
    'Oil Change': 5000,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000
  },
  Accord: {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000
  },
  CRV: {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000
  }
};

function computeSuggestions(vehicle, mileage, lastService) {
  const intv = intervals[vehicle] || intervals.Civic;
  const results = [];
  for (const [service, interval] of Object.entries(intv)) {
    const nextDue = lastService + interval;
    if (mileage >= nextDue) {
      results.push({service, status: 'OVERDUE', nextDue, milesOver: mileage - nextDue});
    } else {
      results.push({service, status: 'UPCOMING', nextDue, milesLeft: nextDue - mileage});
    }
  }
  return results;
}

function renderResults(results) {
  const out = document.getElementById('output');
  out.innerHTML = '<h2>Maintenance Suggestion</h2>';
  if (!results || results.length === 0) {
    out.innerHTML += '<p class="info">No data.</p>';
    return;
  }
  const ul = document.createElement('ul');
  results.forEach(r => {
    const li = document.createElement('li');
    if (r.status === 'OVERDUE') {
      li.className = 'warning';
      li.textContent = `${r.service}: OVERDUE by ${r.milesOver} mi (due at ${r.nextDue} mi)`;
    } else {
      li.className = 'info';
      li.textContent = `${r.service}: Due in ${r.milesLeft} mi (at ${r.nextDue} mi)`;
    }
    ul.appendChild(li);
  });
  out.appendChild(ul);
}

function loadSample() {
  document.getElementById('vehicle').value = 'Civic';
  document.getElementById('mileage').value = 45000;
  document.getElementById('lastService').value = 40000;
  handleSubmit();
}

function handleSubmit() {
  const vehicle = document.getElementById('vehicle').value;
  const mileage = parseInt(document.getElementById('mileage').value) || 0;
  const lastService = parseInt(document.getElementById('lastService').value) || 0;
  const results = computeSuggestions(vehicle, mileage, lastService);
  renderResults(results);
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('submit').addEventListener('click', handleSubmit);
  document.getElementById('reset').addEventListener('click', loadSample);
});