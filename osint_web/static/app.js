const $=s=>document.querySelector(s);
let current={};
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function toast(t){const e=$('#toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),2600)}
async function api(path,opt){const r=await fetch(path,opt);const j=await r.json();if(!r.ok)throw new Error(j.error||r.statusText);return j}
function metric(label,value,note,trend=''){return `<div class="metric"><span>${esc(label)}</span>${trend?`<span class="trend">${esc(trend)}</span>`:''}<strong>${esc(value)}</strong><small>${esc(note)}</small></div>`}
function renderOverview(d){
  current=d;
  const m=d.metrics||{};
  $('#metricCards').innerHTML=[
    metric('Search hits',m.search_hits_total||0,'observed across current reports'),
    metric('Downloaded',m.downloaded_total||0,'local payloads with provenance'),
    metric('Payload reuse',m.payload_reused_total||0,'deduplicated by SHA-256'),
    metric('Bibliography',m.bibliography_availability_ratio!=null?Math.round(m.bibliography_availability_ratio*100)+'%':'—','Telegram availability / 20 targets')
  ].join('');
  const ns=(d.network||{}).route_state||((d.network||{}).direct_telegram_tcp?'DIRECT_REACHABLE':'UNKNOWN');
  $('#networkState').textContent=ns;
  const streams=d.streams||[];
  $('#streams').innerHTML=streams.map(s=>`<div class="stream"><div class="stream-id">${esc(s.stream_id)}</div><div><b>${esc(s.name)}</b><small>${esc((s.roles||[]).join(' · '))}</small></div><div class="stream-status">READY</div></div>`).join('')||'<div class="empty">Нет данных по потокам</div>';
  const b=d.bibliography||{};
  const pct=b.availability_ratio!=null?Math.round(b.availability_ratio*100):0;
  $('#biblioGauge').style.setProperty('--pct',pct+'%');
  $('#biblioGauge .gauge-value').textContent=b.targets_total?pct+'%':'—';
  $('#biblioStats').innerHTML=`<div class="mini"><b>${b.found_candidate_total??0}</b><small>FOUND</small></div><div class="mini"><b>${b.not_found_total??0}</b><small>GAP</small></div><div class="mini"><b>${b.errors_total??0}</b><small>ERRORS</small></div>`;
  renderJobs(d.jobs||[]);
  renderTraces(d.trace_events||[]);
}
function renderJobs(rows){
  $('#jobs').innerHTML=(rows.slice().reverse().slice(0,9).map(j=>`<div class="job"><b>${esc(j.kind)}</b><span class="state-${esc(j.state)}">${esc(j.state)}</span><small>${esc(j.role||j.query||'')}</small><small>${esc(j.command_id||'')}</small></div>`).join(''))||'<div class="empty">Задачи из UI ещё не запускались</div>';
}
function renderTraces(rows){
  const target=$('#traces');
  if(!target)return;
  target.innerHTML=(rows.slice().reverse().slice(0,12).map(t=>`<div class="job"><b>${esc(t.command_name||t.command_id)}</b><span class="state-${esc(t.status)}">${esc(t.status)}</span><small>${esc(t.actor_role||'')} → ${esc(t.executor||'')}</small><small>${esc(t.state_before||'')} → ${esc(t.state_after||'')}</small><small>${esc(t.command_id||'')} · ${esc(t.task_id||'')}</small></div>`).join(''))||'<div class="empty">Трассировка появится после первого запуска действия из UI</div>';
}
async function refresh(){try{renderOverview(await api('/api/overview'));await refreshSearches()}catch(e){toast('Ошибка: '+e.message)}}
async function refreshSearches(){
  const d=await api('/api/search-results');
  const searches=d.searches||[];
  if(!searches.length)return;
  const last=searches[0],rows=last.results||[];
  $('#resultCount').textContent=rows.length;
  $('#searchState').style.display='none';
  $('#results').innerHTML=rows.slice(0,30).map(r=>`<div class="result"><div class="result-top"><b>${esc(r.chat_title||r.chat_username||r.chat_id)}</b><small>${r.has_file?'FILE':'MESSAGE'}</small></div><p>${esc(r.text||r.file_name||'')}</p><small>${esc(r.file_name||'')} ${r.file_size?(' · '+Math.round(r.file_size/1024)+' KB'):''}</small></div>`).join('');
}
async function action(payload){
  try{
    const r=await api('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    toast('Запущено: '+r.job.kind+' · '+r.job.command_id);
    setTimeout(refresh,700);
  }catch(e){toast('Не запущено: '+e.message)}
}
$('#searchBtn').onclick=()=>{const q=$('#queryInput').value.trim();if(q)action({action:'TELEGRAM_QUERY_PROBE',query:q});};
$('#queryInput').addEventListener('keydown',e=>{if(e.key==='Enter')$('#searchBtn').click()});
$('#refreshBtn').onclick=refresh;
$('#probeBtn').onclick=()=>action({action:'PROGRAMMER_BIBLIOGRAPHY_PROBE'});
$('#planBtn').onclick=()=>action({action:'PROGRAMMER_BIBLIOGRAPHY_PLAN'});
$('#remainingBtn').onclick=()=>action({action:'REMAINING_P0_WINDOWS'});
setInterval(refresh,5000);
refresh();