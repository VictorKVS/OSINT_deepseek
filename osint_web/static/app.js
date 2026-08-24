const $=s=>document.querySelector(s);
let current={};
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function toast(t){const e=$('#toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),2600)}
async function api(path,opt){const r=await fetch(path,opt);const j=await r.json();if(!r.ok)throw new Error(j.error||r.statusText);return j}
function fmtBytes(v){const n=Number(v||0);if(!n)return '0 B';const u=['B','KB','MB','GB'];let x=n,i=0;while(x>=1024&&i<u.length-1){x/=1024;i++}return (x>=100?x.toFixed(0):x>=10?x.toFixed(1):x.toFixed(2))+' '+u[i]}
function fmtSpeed(v){return v?fmtBytes(v)+'/s':'—'}
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
  renderDownloads(d.downloads||{});
  renderJobs(d.jobs||[]);
  renderTraces(d.trace_events||[]);
}
function renderDownloads(d){
  const live=d.live||[],history=d.history||[];
  const active=live.reduce((n,r)=>n+Number(r.downloading_total||0)+Number(r.hashing_total||0),0);
  const queued=live.reduce((n,r)=>n+Number(r.queued_total||0),0);
  const received=live.reduce((n,r)=>n+Number(r.bytes_received_total||0),0);
  const expected=live.reduce((n,r)=>n+Number(r.bytes_expected_total||0),0);
  $('#downloadSummary').innerHTML=[`<span class="chip on">Этап 1 · Acquisition</span>`,`<span class="chip">активно: ${active}</span>`,`<span class="chip">в очереди: ${queued}</span>`,`<span class="chip">${fmtBytes(received)} / ${fmtBytes(expected)}</span>`,`<span class="chip">история: ${history.length}</span>`].join('');
  const order={DOWNLOADING:0,HASHING:1,QUEUED:2,FAILED:3,DOWNLOADED:4,REUSED:5};
  $('#downloadsLive').innerHTML=live.map(role=>{
    const items=(role.items||[]).slice().sort((a,b)=>(order[a.status]??9)-(order[b.status]??9));
    const pct=Number(role.overall_progress_pct||0);
    const rows=items.slice(0,30).map(i=>{
      const ip=Number(i.progress_pct||0), received=Number(i.bytes_received||0), total=Number(i.total_bytes||0);
      return `<div class="download-row"><div><b>${esc(i.file_name||('message '+i.message_id))}</b><small>${esc(role.role_id||'')} · ${esc(i.chat_id||'')}</small></div><div class="download-status state-${esc(i.status||'QUEUED')}">${esc(i.status||'QUEUED')}</div><div><div class="progress-track"><div class="progress-fill" style="width:${Math.max(0,Math.min(100,ip))}%"></div></div><small>${ip.toFixed(1)}% · ${fmtBytes(received)} / ${fmtBytes(total)}</small></div><div><small>${fmtSpeed(i.speed_bytes_per_second)}</small></div></div>`;
    }).join('');
    return `<div class="download-role"><div class="download-role-head"><div><b>${esc(role.role_id||'UNKNOWN')}</b><small>${esc(role.stage||'STAGE_1_ACQUISITION')}</small></div><div><b>${pct.toFixed(1)}%</b><small>${esc(role.state||'')}</small></div></div><div class="progress-track" style="margin-bottom:10px"><div class="progress-fill" style="width:${Math.max(0,Math.min(100,pct))}%"></div></div>${rows||'<div class="empty">Файлы ещё не поставлены в очередь</div>'}</div>`;
  }).join('')||'<div class="empty">Живая телеметрия появится при следующем запуске ROLE_ACQUISITION после обновления кода.</div>';
  $('#downloadsHistory').innerHTML=history.slice().reverse().slice(0,40).map(i=>`<div class="download-row"><div><b>${esc(i.file_name||'file')}</b><small>${esc(i.role_id||'')} · ${esc(i.source_url||'')}</small></div><div class="download-status state-${esc(i.status||'DOWNLOADED')}">${esc(i.status||'DOWNLOADED')}</div><div><div class="progress-track"><div class="progress-fill" style="width:100%"></div></div><small>100% · ${fmtBytes(i.file_size)}</small></div><div><small class="mono">${esc((i.sha256||'').slice(0,12))}</small></div></div>`).join('')||'<div class="empty">История загрузок пока пуста</div>';
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
setInterval(refresh,2000);
refresh();