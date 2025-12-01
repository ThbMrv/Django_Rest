const apiBase = '/api';

function el(id){ return document.getElementById(id); }

async function fetchConcessions(){
  el('concession-list').textContent = 'Chargement...';
  try{
    const res = await fetch(`${apiBase}/concessionnaires/`);
    if(!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    renderConcessionList(data);
  }catch(e){ el('concession-list').textContent = 'Erreur : '+e.message }
}

function renderConcessionList(list){
  const container = el('concession-list');
  container.innerHTML = '';
  if(!list.length){ container.textContent = 'Aucun concessionnaire.'; return }
  list.forEach(c => {
    const d = document.createElement('div');
    d.className = 'item';
    d.innerHTML = `<div class="title">${escapeHtml(c.nom)}</div><div class="muted">id: ${c.id}</div>`;
    d.onclick = ()=> loadConcession(c.id);
    container.appendChild(d);
  })
}

// handle create concessionnaire form and create vehicule form
document.addEventListener('DOMContentLoaded', ()=>{
  // fetch CSRF token (this sets the CSRF cookie via the server)
  fetch(`${apiBase}/csrf/`, {credentials: 'same-origin'})
    .then(r => r.json())
    .then(j => { window._csrftoken = j.csrf })
    .catch(()=>{ window._csrftoken = null });

  // Auth UI handlers
  const authInfo = document.getElementById('auth-info');
  const btnShowLogin = document.getElementById('btn-show-login');
  const btnLogout = document.getElementById('btn-logout');

  function updateAuthUI(){
    const user = localStorage.getItem('username');
    const token = localStorage.getItem('access');
    if(user && token){
      authInfo.textContent = `Connecté: ${user}`;
      btnShowLogin.style.display = 'none';
      btnLogout.style.display = '';
    }else{
      authInfo.textContent = '';
      btnShowLogin.style.display = '';
      btnLogout.style.display = 'none';
    }
  }

  btnLogout?.addEventListener('click', ()=>{
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
    updateAuthUI();
  });

  btnShowLogin?.addEventListener('click', ()=>{
    // toggle the inline auth forms
    const forms = document.getElementById('auth-forms');
    if(forms.style.display === 'none' || !forms.style.display) forms.style.display = 'block';
    else forms.style.display = 'none';
  });

  updateAuthUI();

  async function register(username, password){
    try{
      const res = await fetch(`${apiBase}/users/`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, email: '', password})
      });
      if(!res.ok){
        const err = await res.json().catch(()=>null);
        throw new Error(err?.detail || 'Erreur création utilisateur');
      }
      alert('Utilisateur créé, vous pouvez maintenant vous connecter');
    }catch(e){ alert(e.message) }
  }

  async function login(username, password){
    try{
      const res = await fetch(`${apiBase}/token/`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, password})
      });
      if(!res.ok){
        const err = await res.json().catch(()=>null);
        throw new Error(err?.detail || 'Identifiants invalides');
      }
      const data = await res.json();
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);
      localStorage.setItem('username', username);
      updateAuthUI();
      alert('Connecté');
    }catch(e){ alert(e.message) }
  }

  // wire the new inline forms
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  if(loginForm){
    loginForm.addEventListener('submit', (e)=>{
      e.preventDefault();
      const u = document.getElementById('login-username').value.trim();
      const p = document.getElementById('login-password').value;
      if(!u || !p) return alert('Remplissez les champs');
      login(u, p);
    })
  }
  if(registerForm){
    registerForm.addEventListener('submit', (e)=>{
      e.preventDefault();
      const u = document.getElementById('reg-username').value.trim();
      const em = document.getElementById('reg-email').value.trim();
      const p = document.getElementById('reg-password').value;
      if(!u || !p) return alert('Remplissez les champs');
      // call register with email
      try{
        fetch(`${apiBase}/users/`, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({username: u, email: em, password: p})
        }).then(async res=>{
          if(!res.ok){
            const err = await res.json().catch(()=>null);
            throw new Error(err?.detail || 'Erreur création utilisateur');
          }
          alert('Compte créé — utilisez la connexion');
          document.getElementById('reg-username').value = '';
          document.getElementById('reg-email').value = '';
          document.getElementById('reg-password').value = '';
        }).catch(e=> alert(e.message));
      }catch(e){ alert(e.message) }
    })
  }

  const form = document.getElementById('create-concession-form');
  if(form){
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const name = document.getElementById('new-concession-nom').value.trim();
      const msg = document.getElementById('create-concession-msg');
      msg.textContent = '';
      try{
        const headers = {'Content-Type':'application/json'};
        if(window._csrftoken){ headers['X-CSRFToken'] = window._csrftoken }
        const access = localStorage.getItem('access');
        if(access){ headers['Authorization'] = 'Bearer ' + access }
        const payload = {nom: name};
        const res = await fetch(`${apiBase}/concessionnaires/`, {
          method: 'POST',
          credentials: 'same-origin',
          headers,
          body: JSON.stringify(payload)
        });
        if(!res.ok){
          const err = await res.json().catch(()=>({detail:res.statusText}));
          throw new Error(err.detail || JSON.stringify(err));
        }
        const data = await res.json();
        msg.textContent = 'Concessionnaire créé (id: '+data.id+')';
        document.getElementById('new-concession-nom').value = '';
        fetchConcessions();
      }catch(e){ msg.textContent = 'Erreur: '+e.message }
    })
  }

  const vform = document.getElementById('create-vehicule-form');
  if(vform){
    vform.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const marque = document.getElementById('veh-marque').value.trim();
      const type = document.getElementById('veh-type').value;
      const chevaux = parseInt(document.getElementById('veh-chevaux').value, 10);
      const prix = parseFloat(document.getElementById('veh-prix').value);
      const msg = document.getElementById('create-vehicule-msg');
      msg.textContent = '';
      if(!window._currentConcessionId){ msg.textContent = 'Sélectionnez d\u2019abord un concessionnaire.'; return }
      try{
        const headers = {'Content-Type':'application/json'};
        if(window._csrftoken){ headers['X-CSRFToken'] = window._csrftoken }
        const access = localStorage.getItem('access');
        if(access){ headers['Authorization'] = 'Bearer ' + access }
        const res = await fetch(`${apiBase}/concessionnaires/${window._currentConcessionId}/vehicules/`, {
          method: 'POST',
          credentials: 'same-origin',
          headers,
          body: JSON.stringify({marque, type, chevaux, prix_ht: prix})
        });
        if(!res.ok){
          const err = await res.json().catch(()=>({detail:res.statusText}));
          throw new Error(err.detail || JSON.stringify(err));
        }
        const data = await res.json();
        msg.textContent = 'Véhicule créé (id: '+data.id+')';
        // clear fields
        document.getElementById('veh-marque').value = '';
        document.getElementById('veh-chevaux').value = '';
        document.getElementById('veh-prix').value = '';
        loadVehicules(window._currentConcessionId);
      }catch(e){ msg.textContent = 'Erreur: '+e.message }
    })
  }
})

async function loadConcession(id){
  el('concession-detail').textContent = 'Chargement...';
  el('vehicule-list').textContent = '';
  el('vehicule-detail').textContent = '';
  try{
    const res = await fetch(`${apiBase}/concessionnaires/${id}/`);
    if(!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    el('concession-detail').innerHTML = `<div class="card"><strong>${escapeHtml(data.nom)}</strong><div class="muted">id: ${data.id}</div></div>`;
    el('concession-detail').innerHTML = `<div class="card"><strong>${escapeHtml(data.nom)}</strong><div class="muted">id: ${data.id}</div></div>`;
    window._currentConcessionId = id;
    loadVehicules(id);
  }catch(e){ el('concession-detail').textContent = 'Erreur : '+e.message }
}

async function loadVehicules(concessionId){
  el('vehicule-list').textContent = 'Chargement...';
  try{
    const res = await fetch(`${apiBase}/concessionnaires/${concessionId}/vehicules/`);
    if(!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    renderVehiculeList(concessionId, data);
  }catch(e){ el('vehicule-list').textContent = 'Erreur : '+e.message }
}

function renderVehiculeList(concessionId, list){
  const container = el('vehicule-list');
  container.innerHTML = '';
  if(!list.length){ container.textContent = 'Aucun véhicule.'; return }
  list.forEach(v=>{
    const d = document.createElement('div');
    d.className = 'item';
    d.innerHTML = `<div class="title">${escapeHtml(v.marque)} (${escapeHtml(v.type)})</div>
                   <div class="muted">id: ${v.id} — ${v.chevaux} ch — ${v.prix_ht} € HT</div>`;
    d.onclick = ()=> loadVehicule(concessionId, v.id);
    container.appendChild(d);
  })
}

async function loadVehicule(concessionId, vehId){
  el('vehicule-detail').textContent = 'Chargement...';
  try{
    const res = await fetch(`${apiBase}/concessionnaires/${concessionId}/vehicules/${vehId}/`);
    if(!res.ok) throw new Error(res.statusText);
    const v = await res.json();
    el('vehicule-detail').innerHTML = `<div class="card"><strong>${escapeHtml(v.marque)}</strong>
      <div class="muted">id: ${v.id} — type: ${escapeHtml(v.type)}</div>
      <div>Chevaux: ${v.chevaux}</div>
      <div>Prix HT: ${v.prix_ht} €</div>
      <div class="muted">Concessionnaire id: ${v.concessionnaire}</div>
      </div>`;
  }catch(e){ el('vehicule-detail').textContent = 'Erreur : '+e.message }
}

function escapeHtml(s){ if(s==null) return ''; return String(s).replace(/[&<>"']/g, c=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
})[c]) }

fetchConcessions();
