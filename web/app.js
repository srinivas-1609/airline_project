/* SkyLine — frontend logic for the Airline Reservation System */

let TOKEN = localStorage.getItem('skyline_token') || '';
let ME = null;

/* ---------------- tiny helpers ---------------- */

async function api(path, opts = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (TOKEN) headers.Authorization = 'Bearer ' + TOKEN;
  const res = await fetch('/api' + path, { ...opts, headers });
  const data = await res.json().catch(() => ({ detail: 'Unexpected server response' }));
  if (!res.ok) {
    if (res.status === 401 && TOKEN) { setSession('', null); refreshAuthUI(); showSection('home'); }
    throw new Error(typeof data.detail === 'string' ? data.detail : 'Request failed');
  }
  return data;
}

function $(id) { return document.getElementById(id); }

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function toast(msg, isError = false) {
  const t = $('toast');
  t.textContent = msg;
  t.className = 'toast' + (isError ? ' error' : '');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.add('hidden'), 3800);
}

function openModal(id) { $(id).classList.remove('hidden'); }
function closeModal(id) { $(id).classList.add('hidden'); }
function overlayClose(e, id) { if (e.target === $(id)) closeModal(id); }

function inr(n) { return '₹' + Number(n).toLocaleString('en-IN'); }

function setSession(token, user) {
  TOKEN = token;
  ME = user;
  if (token) localStorage.setItem('skyline_token', token);
  else localStorage.removeItem('skyline_token');
}

/* ---------------- auth ---------------- */

async function doLogin(e) {
  e.preventDefault();
  $('login-error').classList.add('hidden');
  try {
    const data = await api('/login', {
      method: 'POST',
      body: JSON.stringify({ username: $('login-username').value.trim(), password: $('login-password').value })
    });
    setSession(data.token, data.user);
    closeModal('modal-login');
    refreshAuthUI();
    toast(`Welcome back, ${data.user.name}!`);
    showSection(data.user.role === 'admin' ? 'admin' : 'home');
  } catch (err) {
    const box = $('login-error');
    box.textContent = err.message;
    box.classList.remove('hidden');
  }
}

async function doRegister(e) {
  e.preventDefault();
  $('register-error').classList.add('hidden');
  try {
    await api('/register', {
      method: 'POST',
      body: JSON.stringify({
        name: $('reg-name').value.trim(),
        username: $('reg-username').value.trim(),
        password: $('reg-password').value
      })
    });
    closeModal('modal-register');
    toast('Account created! Please sign in.');
    $('login-username').value = $('reg-username').value;
    openModal('modal-login');
  } catch (err) {
    const box = $('register-error');
    box.textContent = err.message;
    box.classList.remove('hidden');
  }
}

async function logout() {
  try { await api('/logout', { method: 'POST' }); } catch (_) {}
  setSession('', null);
  refreshAuthUI();
  showSection('home');
  toast('You have been logged out.');
}

function refreshAuthUI() {
  const logged = !!ME;
  $('auth-buttons').classList.toggle('hidden', logged);
  $('user-chip').classList.toggle('hidden', !logged);
  $('nav-bookings').classList.toggle('hidden', !logged);
  $('nav-admin').classList.toggle('hidden', !(logged && ME.role === 'admin'));
  if (logged) {
    $('user-name').textContent = ME.name;
    $('user-initial').textContent = ME.name.charAt(0).toUpperCase();
  }
}

/* ---------------- sections ---------------- */

function showSection(name) {
  if (name === 'bookings' && !ME) { openModal('modal-login'); return; }
  if (name === 'admin') {
    if (!ME) { openModal('modal-login'); return; }
    if (ME.role !== 'admin') { toast('Admin access required.', true); return; }
  }
  ['home', 'route', 'bookings', 'admin'].forEach(s => {
    $('section-' + s).classList.toggle('hidden', s !== name);
  });
  window.scrollTo(0, 0);
  if (name === 'home') loadFlights();
  if (name === 'bookings') loadBookings();
  if (name === 'admin') loadAdmin();
}

/* ---------------- flights ---------------- */

function swapStations() {
  const a = $('search-from'), b = $('search-to');
  const tmp = a.value; a.value = b.value; b.value = tmp;
}

function flightCard(f) {
  const full = f.available_seats <= 0;
  const seatsLabel = full ? 'Full — waitlist open' : `${f.available_seats} seats left`;
  return `
  <article class="flight-card">
    <div class="flight-top">
      <div class="airline"><span class="airline-badge">${esc(f.airline.charAt(0))}</span>
        <div><strong>${esc(f.airline)}</strong><span class="muted small">${esc(f.flight_number)}</span></div>
      </div>
      <span class="price">${inr(f.price)}</span>
    </div>
    <div class="flight-route">
      <div class="stop"><span class="code">${esc(f.source)}</span><span class="time">${esc(f.dep_time)}</span></div>
      <div class="line"><span class="dot"></span><span class="plane">✈</span><span class="dot"></span></div>
      <div class="stop right"><span class="code">${esc(f.destination)}</span><span class="time">${esc(f.arr_time)}</span></div>
    </div>
    <div class="flight-bottom">
      <span class="muted small">📅 ${esc(f.flight_date)}</span>
      <span class="seats ${full ? 'full' : ''}">${seatsLabel}</span>
      <button class="btn primary sm" ${full ? 'onclick="bookFlight(\'' + esc(f.flight_number) + '\', true)"' : 'onclick="bookFlight(\'' + esc(f.flight_number) + '\')"'}>${full ? 'Join waitlist' : 'Book now'}</button>
    </div>
  </article>`;
}

async function loadFlights() {
  const from = $('search-from').value, to = $('search-to').value, d = $('search-date').value;
  const qs = new URLSearchParams();
  if (from) qs.set('source', from);
  if (to) qs.set('destination', to);
  try {
    const data = await api('/flights?' + qs.toString());
    let flights = data.flights;
    if (d) flights = flights.filter(f => f.flight_date === d);
    $('results-count').textContent = `${flights.length} flight${flights.length === 1 ? '' : 's'} found`;
    $('results-title').textContent = (from || to || d) ? 'Search results' : 'All available flights';
    $('flight-grid').innerHTML = flights.length
      ? flights.map(flightCard).join('')
      : '<p class="empty">No flights match your search. Try a different route or date.</p>';
  } catch (err) { toast(err.message, true); }
}

function searchFlights() { showSection('home'); loadFlights(); }

/* ---------------- passenger-details booking flow ---------------- */

let pendingBooking = null; // { flightNumber, waitlist }

function openPassengerModal(flightNumber, waitlist) {
  pendingBooking = { flightNumber, waitlist };
  $('pd-flight-label').textContent = (waitlist ? 'Joining waitlist for ' : 'Booking ') +
    flightNumber + (ME && ME.name ? ' — ' + ME.name : '');
  // prefill name/email from the signed-in account
  if (ME) {
    $('pd-name').value = ME.name || '';
    $('pd-email').value = ME.username.includes('@') ? ME.username : '';
  }
  $('pd-error').classList.add('hidden');
  openModal('modal-passenger');
}

async function submitPassengerDetails(e) {
  e.preventDefault();
  if (!pendingBooking) return;
  const payload = {
    flight_number: pendingBooking.flightNumber,
    passenger: {
      full_name: $('pd-name').value.trim(),
      age: $('pd-age').value ? parseInt($('pd-age').value, 10) : null,
      gender: $('pd-gender').value,
      phone: $('pd-phone').value.trim(),
      email: $('pd-email').value.trim(),
      address: $('pd-address').value.trim()
    }
  };
  const submitBtn = $('pd-submit');
  submitBtn.disabled = true;
  try {
    const data = await api('/bookings', { method: 'POST', body: JSON.stringify(payload) });
    closeModal('modal-passenger');
    toast(data.message);
    loadFlights();
  } catch (err) {
    const box = $('pd-error');
    box.textContent = err.message;
    box.classList.remove('hidden');
  } finally {
    submitBtn.disabled = false;
  }
}

async function bookFlight(flightNumber, waitlist = false) {
  if (!ME) { toast('Please sign in to book a flight.', true); openModal('modal-login'); return; }
  openPassengerModal(flightNumber, waitlist);
}

/* ---------------- bookings ---------------- */

async function loadBookings() {
  try {
    const data = await api('/bookings');
    const list = $('bookings-list');
    if (!data.bookings.length) {
      list.innerHTML = '<p class="empty">No bookings yet. <a href="#" onclick="showSection(\'home\'); return false;">Browse flights →</a></p>';
      return;
    }
    list.innerHTML = data.bookings.map(b => {
      const f = b.flight || {};
      const cancelled = b.status === 'CANCELLED';
      return `
      <div class="booking-card ${cancelled ? 'cancelled' : ''}">
        <div class="booking-head">
          <div>
            <span class="booking-id">${esc(b.booking_id)}</span>
            <span class="status ${cancelled ? 'cancelled' : 'confirmed'}">${b.status}</span>
          </div>
          ${!cancelled ? `<button class="btn danger sm" onclick="cancelBooking('${esc(b.booking_id)}')">Cancel</button>` : ''}
        </div>
        <div class="booking-body">
          <div><span class="muted small">Flight</span><strong>${esc(f.flight_number || b.flight_number)}</strong></div>
          <div><span class="muted small">Route</span><strong>${esc(f.source || '?')} → ${esc(f.destination || '?')}</strong></div>
          <div><span class="muted small">Date</span><strong>${esc(f.flight_date || '—')}</strong></div>
          <div><span class="muted small">Times</span><strong>${esc(f.dep_time || '—')} – ${esc(f.arr_time || '—')}</strong></div>
          <div><span class="muted small">Booked</span><strong>${esc((b.booking_date || '').slice(0, 10))}</strong></div>
        </div>
        ${b.passenger ? `
        <div class="pax-strip">
          <span>👤 ${esc(b.passenger.full_name)}</span>
          ${b.passenger.age ? `<span>${esc(b.passenger.age)}y</span>` : ''}
          ${b.passenger.gender ? `<span>${esc(b.passenger.gender)}</span>` : ''}
          ${b.passenger.phone ? `<span>📞 ${esc(b.passenger.phone)}</span>` : ''}
          ${b.passenger.email ? `<span>✉️ ${esc(b.passenger.email)}</span>` : ''}
          ${b.passenger.address ? `<span class="pax-address">🏠 ${esc(b.passenger.address)}</span>` : ''}
        </div>` : ''}
      </div>`;
    }).join('');
  } catch (err) { toast(err.message, true); }
}

async function cancelBooking(bookingId) {
  if (!confirm(`Cancel booking ${bookingId}?`)) return;
  try {
    const data = await api('/bookings/' + encodeURIComponent(bookingId), { method: 'DELETE' });
    toast(data.message);
    loadBookings();
  } catch (err) { toast(err.message, true); }
}

/* ---------------- route finder ---------------- */

async function findRoute() {
  const from = $('route-from').value, to = $('route-to').value;
  const box = $('route-result');
  box.classList.remove('hidden');
  if (from === to) { box.innerHTML = '<p class="empty">Origin and destination are the same.</p>'; return; }
  try {
    const data = await api(`/route?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`);
    box.innerHTML = `
      <div class="route-path">
        ${data.path.map((p, i) => `
          <span class="route-node">${esc(p)}</span>
          ${i < data.path.length - 1 ? '<span class="route-arrow">→</span>' : ''}
        `).join('')}
      </div>
      <div class="route-meta">
        <div><span class="muted small">Total distance</span><strong>${data.total_distance_km.toLocaleString('en-IN')} km</strong></div>
        <div><span class="muted small">Layovers</span><strong>${data.stops}</strong></div>
      </div>`;
  } catch (err) { box.innerHTML = `<p class="empty">${esc(err.message)}</p>`; }
}

/* ---------------- admin ---------------- */

let adminTab = 'flights';

function switchTab(tab) {
  adminTab = tab;
  document.querySelectorAll('.admin-tabs .tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  ['flights', 'bookings', 'waitlist'].forEach(t => $('admin-' + t).classList.toggle('hidden', t !== tab));
}

async function loadAdmin() {
  try {
    const [stats, flights, bookings, waitlist] = await Promise.all([
      api('/admin/stats'), api('/flights'), api('/admin/bookings'), api('/admin/waitlist')
    ]);
    const s = stats;
    $('stats-grid').innerHTML = `
      <div class="stat"><span class="stat-num">${s.total_flights}</span><span>Flights</span></div>
      <div class="stat"><span class="stat-num">${s.confirmed_bookings}</span><span>Confirmed</span></div>
      <div class="stat"><span class="stat-num">${s.cancelled_bookings}</span><span>Cancelled</span></div>
      <div class="stat"><span class="stat-num">${s.waitlist_count}</span><span>Waitlisted</span></div>
      <div class="stat"><span class="stat-num">${inr(s.revenue)}</span><span>Est. revenue</span></div>`;

    $('admin-flights-table').querySelector('tbody').innerHTML = flights.flights.map(f => `
      <tr>
        <td><strong>${esc(f.flight_number)}</strong></td>
        <td>${esc(f.airline)}</td>
        <td>${esc(f.source)} → ${esc(f.destination)}</td>
        <td>${esc(f.flight_date)}</td>
        <td>${esc(f.dep_time)} – ${esc(f.arr_time)}</td>
        <td>${f.available_seats}/${f.total_seats}</td>
        <td>${inr(f.price)}</td>
        <td><button class="btn danger sm" onclick="deleteFlight('${esc(f.flight_number)}')">Delete</button></td>
      </tr>`).join('') || '<tr><td colspan="8" class="empty">No flights</td></tr>';

    $('admin-bookings-table').querySelector('tbody').innerHTML = bookings.bookings.map(b => {
      const f = b.flight || {};
      const p = b.passenger || {};
      return `<tr>
        <td>${esc(b.booking_id)}</td>
        <td>#${b.user_id}</td>
        <td>${esc(f.flight_number || b.flight_number)} (${esc(f.source || '?')}→${esc(f.destination || '?')})</td>
        <td>${p.full_name ? esc(p.full_name) : '<span class="muted">—</span>'}</td>
        <td>${p.phone ? esc(p.phone) : '<span class="muted">—</span>'}</td>
        <td><span class="status ${b.status === 'CANCELLED' ? 'cancelled' : 'confirmed'}">${b.status}</span></td>
        <td>${esc((b.booking_date || '').slice(0, 10))}</td>
      </tr>`;
    }).join('') || '<tr><td colspan="7" class="empty">No bookings</td></tr>';

    $('admin-waitlist-table').querySelector('tbody').innerHTML = waitlist.waitlist.map((w, i) => `
      <tr><td>${i + 1}</td><td>#${w.user_id}</td><td>${esc(w.flight_number)}</td><td>P${w.priority}</td></tr>
    `).join('') || '<tr><td colspan="4" class="empty">Waiting list is empty</td></tr>';
  } catch (err) { toast(err.message, true); }
}

async function addFlight(e) {
  e.preventDefault();
  try {
    const data = await api('/admin/flights', {
      method: 'POST',
      body: JSON.stringify({
        flight_number: $('af-number').value.trim(),
        airline: $('af-airline').value.trim(),
        source: $('af-source').value,
        destination: $('af-destination').value,
        flight_date: $('af-date').value,
        dep_time: $('af-dep').value,
        arr_time: $('af-arr').value,
        total_seats: parseInt($('af-seats').value, 10),
        price: parseFloat($('af-price').value)
      })
    });
    toast(data.message);
    $('add-flight-form').reset();
    loadAdmin();
  } catch (err) { toast(err.message, true); }
}

async function deleteFlight(fn) {
  if (!confirm(`Delete flight ${fn}?`)) return;
  try {
    const data = await api('/admin/flights/' + encodeURIComponent(fn), { method: 'DELETE' });
    toast(data.message);
    loadAdmin();
  } catch (err) { toast(err.message, true); }
}

/* ---------------- boot ---------------- */

async function boot() {
  // date input min = today
  const today = new Date().toISOString().slice(0, 10);
  $('search-date').min = today;
  $('af-date').min = today;

  try {
    const data = await api('/airports');
    for (const sel of ['search-from', 'search-to', 'route-from', 'route-to', 'af-source', 'af-destination']) {
      const el = $(sel);
      const keep = el.querySelector('option');
      el.innerHTML = '';
      if (keep && keep.value === '') el.appendChild(keep);
      data.airports.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a; opt.textContent = a;
        el.appendChild(opt);
      });
    }
  } catch (err) { console.error('Failed to load airports', err); }

  if (TOKEN) {
    try {
      const data = await api('/me');
      ME = data.user;
    } catch (_) { setSession('', null); }
  }
  refreshAuthUI();
  loadFlights();
}

boot();
