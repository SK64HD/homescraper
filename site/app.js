const status = document.querySelector('#status');
const count = document.querySelector('#record-count');
const tbody = document.querySelector('#properties');
const search = document.querySelector('#search');

let properties = [];

function text(value) {
  return value === null || value === undefined || value === '' ? '—' : String(value);
}

function render(rows) {
  count.textContent = String(properties.length);
  tbody.replaceChildren();

  if (!rows.length) {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td colspan="5" class="empty">No matching records.</td>';
    tbody.appendChild(tr);
    return;
  }

  for (const property of rows) {
    const tr = document.createElement('tr');
    const address = [property.situs_address, property.city, property.zip].filter(Boolean).join(', ');
    tr.innerHTML = `
      <td>${text(address)}</td>
      <td>${text(property.pin)}</td>
      <td>${text(property.owner)}</td>
      <td>${text(property.assessed_value)}</td>
      <td>${text(property.source)}</td>
    `;
    tbody.appendChild(tr);
  }
}

async function load() {
  try {
    const response = await fetch('./data/properties.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    properties = Array.isArray(payload.properties) ? payload.properties : [];
    status.textContent = `Data loaded · ${properties.length} records`;
    render(properties);
  } catch (error) {
    status.textContent = 'Dashboard shell · data feed not published';
    count.textContent = 'Not loaded';
  }
}

search.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase();
  if (!query) return render(properties);
  render(properties.filter((property) => JSON.stringify(property).toLowerCase().includes(query)));
});

load();
