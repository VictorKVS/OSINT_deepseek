const $=s=>document.querySelector(s);
let current={};
let latestSearch=null;
let latestRows=[];

function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot',"'":'&#39;'}[c]))}
function toast(t){const e=$('#toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),3000)}
async function api(path,opt){const r=await fetch(path,opt);const j=await r.json();if(!r.ok)throw new Error(j.error||r.statusText);return j}
function fmtBytes(v){const n=Number(v||0);if(!n)return '0 B';const u=['B','KB','MB','GB'];let x=n,i=0;while(x>=1024&&i<u.length-1){x/=1024;i++}return (x>=100?x.toFixed(0):x>=10?x.toFixed(1):x.toFixed(2))+' '+u[i]}
function fmtSpeed(v){return v?fmtBytes(v)+'/s':'—'}
function metric(label,value,note,trend=''){return `<div class="metric"><span>${esc(label)}</span>${trend?`<span class="trend">${esc(trend)}</span>`:''}<strong>${esc(value)}</strong><small>${esc(note)}</small></div>`}

function catalogRole(){return (current.role_catalog||[]).find(r=>r.role_id===$('#roleSelect').value)||null}
function catalogTopic(){const r=catalogRole();return r?(r.topics||[]).find(t=>t.target_id===$('#topicSelect').value)||null:null}
function updateDestination(){const t=catalogTopic();$('#destinationPath').textContent=t?t.destination:'—'}
function renderCatalog(d){
  const roles=d.role_catalog||[];
  const select=$('#roleSelect');
  const previous=select.value;
  select.innerHTML=roles.map(r=>`<option value="${esc(r.role_id)}">${esc(r.role_id)} · ${esc(r.knowledge_base_id||'')}</option>`).join('');
  if(previous&&roles.some(r=>r.role_id===previous))select.value=previous;
  else if(roles.some(r=>r.role_id==='PROGRAMMER'))select.value='PROGRAMMER';

  const lib=$('#libraryRoleSelect');
  if(lib){
    const libPrevious=lib.value;
    lib.innerHTML=roles.map(r=>`<option value="${esc(r.role_id)}">${esc(r.role_id)} · ${esc(r.knowledge_base_id||'')} · RU:${esc(r.ru_regulatory_documents_total||0)}</option>`).join('');
    if(libPrevious&&roles.some(r=>r.role_id===libPrevious))lib.value=libPrevious;
    else if(roles.some(r=>r.role_id==='PROGRAMMER'))lib.value='PROGRAMMER';
  }
  renderTopics();
}
function renderTopics(){
  const role=catalogRole();
  const select=$('#topicSelect');
  const previous=select.value;
  const topics=role?.topics||[];
  select.innerHTML=topics.map(t=>`<option value="${esc(t.target_id)}">${esc(t.target_id)} · ${esc(t.label)}</option>`).join('');
  if(previous&&topics.some(t=>t.target_id===previous))select.value=previous;
  updateDestination();
}

const stageLabels={
  STAGE_0_RU_REGULATORY_BASELINE:'0 RU',
  STAGE_1_ACQUISITION:'1 Acquire',
  STAGE_1_COVERAGE:'1 Coverage',
  STAGE_2_DOCUMENT_COMPILER:'2 Compiler',
  STAGE_3_KNOWLEDGE_EXTRACTION:'3 Knowledge',
  STAGE_4_RELATIONS_AND_CONFLICTS:'4 Relations',
  STAGE_5_ANALYST_AND_CRITIC:'5 Analyst',
  STAGE_6_REVIEW:'6 Review',
  KB_READY:'KB Ready'
};
function renderLibraryOrders(rows){
  const target=$('#libraryOrders');if(!target)return;
  if(!rows.length){target.innerHTML='<div class="empty">Заказов пока нет. Выберите роль и нажмите «Заказать и запустить».</div>';return;}
  target.innerHTML=rows.slice(0,12).map(o=>{
    const stages=o.stages||{};
    const baseline=o.ru_regulatory_baseline||{};
    const docs=baseline.documents||[];
    const stageHtml=Object.keys(stageLabels).map(key=>{
      const st=stages[key]||{};
      return `<div class="library-stage"><b>${esc(stageLabels[key])}</b><small class="state-${esc(st.state||'PENDING')}">${esc(st.state||'PENDING')}</small></div>`;
    }).join('');
    const superseded=(baseline.known_superseded||[]).map(x=>`${x.designation}→${x.superseded_by}`).join(' · ');
    const gaps=(o.gaps||[]).length;
    const m=o.metrics||{};
    return `<div class="library-order-card"><div class="library-order-head"><div><b>${esc(o.role_id)} · ${esc(o.knowledge_base_id||'')}</b><small>${esc(o.order_id)} · target ${esc(o.maturity_target)} · ${esc(o.execution_mode||'')}</small></div><div><span class="state-${esc(o.state||'')}">${esc(o.state||'')}</span><small>${esc(o.current_stage||'')}</small></div></div><div class="library-regulatory"><b>🇷🇺 Нормативный слой РФ: ${esc(baseline.state||'RESEARCH_REQUIRED')} · документов ${docs.length}</b><small>${docs.slice(0,6).map(d=>`${d.designation} [${d.status}]`).join(' · ')||'нормативная база ещё не собрана'}</small>${superseded?`<small>Замены: ${esc(superseded)}</small>`:''}</div><div class="library-stage-row">${stageHtml}</div><div class="download-summary" style="margin-top:10px"><span class="chip">тем: ${esc(m.topics_covered||0)}/${esc((Number(m.topics_covered||0)+Number(m.topics_gap||0))||0)}</span><span class="chip">скачано: ${esc(m.downloaded_total||0)}</span><span class="chip">reuse: ${esc(m.reused_total||0)}</span><span class="chip">GAP: ${esc(gaps)}</span></div></div>`;
  }).join('');
}

function renderOverview(d){
  current=d;
  renderCatalog(d);
  renderLibraryOrders(d.library_orders||[]);
  const m=d.metrics||{};
  $('#metricCards').innerHTML=[
    metric('Search hits',m.search_hits_total||0,'по текущим acquisition-отчётам'),
    metric('Downloaded',m.downloaded_total||0,'локальные payload с provenance'),
    metric('Payload reuse',m.payload_reused_total||0,'дедупликация по SHA-256'),
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
  const failed=live.reduce((n,r)=>n+Number(r.failed_total||0),0);
  $('#downloadSummary').innerHTML=[
    `<span class="chip on">Этап 1 · Acquisition</span>`,
    `<span class="chip">активно: ${active}</span>`,
    `<span class="chip">в очереди: ${queued}</span>`,
    `<span class="chip">ошибок: ${failed}</span>`,
    `<span class="chip">${fmtBytes(received)} / ${fmtBytes(expected)}</span>`,
    `<span class="chip">история: ${history.length}</span>`
  ].join('');
  const order={DOWNLOADING:0,HASHING:1,QUEUED:2,FAILED:3,DOWNLOADED:4,REUSED:5};
  $('#downloadsLive').innerHTML=live.map(role=>{
    const items=(role.items||[]).slice().sort((a,b)=>(order[a.status]??9)-(order[b.status]??9));
    const pct=Number(role.overall_progress_pct||0);
    const ctx=role.context||{};
    const rows=items.slice(0,40).map(i=>{
      const ip=Number(i.progress_pct||0),received=Number(i.bytes_received||0),total=Number(i.total_bytes||0);
      return `<div class="download-row"><div><b>${esc(i.file_name||('message '+i.message_id))}</b><small>${esc(role.role_id||'')} · ${esc(i.target_id||ctx.target_id||'')} · ${esc(i.chat_id||'')}</small></div><div class="download-status state-${esc(i.status||'QUEUED')}">${esc(i.status||'QUEUED')}</div><div><div class="progress-track"><div class="progress-fill" style="width:${Math.max(0,Math.min(100,ip))}%"></div></div><small>${ip.toFixed(1)}% · ${fmtBytes(received)} / ${fmtBytes(total)}</small></div><div><small>${fmtSpeed(i.speed_bytes_per_second)}</small><br><small class="mono">${esc((i.sha256||'').slice(0,12))}</small></div></div>`;
    }).join('');
    return `<div class="download-role"><div class="download-role-head"><div><b>${esc(role.role_id||'UNKNOWN')}</b><small>${esc(ctx.topic||role.stage||'STAGE_1_ACQUISITION')} · ${esc(ctx.command_id||'')}</small></div><div><b>${pct.toFixed(1)}%</b><small>${esc(role.state||'')}</small></div></div><div class="progress-track" style="margin-bottom:10px"><div class="progress-fill" style="width:${Math.max(0,Math.min(100,pct))}%"></div></div>${rows||'<div class="empty">Файлы ещё не поставлены в очередь</div>'}</div>`;
  }).join('')||'<div class="empty">Очередь пуста. Найди файл выше и нажми «Скачать».</div>';
  $('#downloadsHistory').innerHTML=history.slice().reverse().slice(0,80).map(i=>`<div class="download-row"><div><b>${esc(i.file_name||'file')}</b><small>${esc(i.role_id||'')} · ${esc(i.target_id||i.topic||'')}<br>${esc(i.local_path||i.source_url||'')}</small></div><div class="download-status state-${esc(i.status||'DOWNLOADED')}">${esc(i.status||'DOWNLOADED')}</div><div><div class="progress-track"><div class="progress-fill" style="width:${i.status==='FAILED'?0:100}%"></div></div><small>${i.status==='FAILED'?'ошибка':('100% · '+fmtBytes(i.file_size))}</small></div><div><small class="mono">${esc((i.sha256||'').slice(0,12))}</small><br><small>${esc(i.command_id||'')}</small></div></div>`).join('')||'<div class="empty">История загрузок пока пуста</div>';
}

function renderJobs(rows){
  $('#jobs').innerHTML=(rows.slice().reverse().slice(0,12).map(j=>`<div class="job"><b>${esc(j.kind)}</b><span class="state-${esc(j.state)}">${esc(j.state)}</span><small>${esc(j.role||j.query||'')}</small><small>${esc(j.command_id||'')}</small></div>`).join(''))||'<div class="empty">Задачи из UI ещё не запускались</div>';
}
function renderTraces(rows){
  const target=$('#traces');if(!target)return;
  target.innerHTML=(rows.slice().reverse().slice(0,15).map(t=>`<div class="job"><b>${esc(t.command_name||t.command_id)}</b><span class="state-${esc(t.status)}">${esc(t.status)}</span><small>${esc(t.actor_role||'')} → ${esc(t.executor||'')}</small><small>${esc(t.state_before||'')} → ${esc(t.state_after||'')}</small><small>${esc(t.command_id||'')} · ${esc(t.task_id||'')}</small></div>`).join(''))||'<div class="empty">Трассировка появится после первого запуска действия из UI</div>';
}

function currentRoute(){return {role:$('#roleSelect').value,target_id:$('#topicSelect').value}}
function routeForSearch(){return {role:latestSearch?.role_id||$('#roleSelect').value,target_id:latestSearch?.target_id||$('#topicSelect').value}}
function updateDownloadSelectedState(){
  const checked=[...document.querySelectorAll('.result-check:checked')];
  const btn=$('#downloadSelectedBtn');
  btn.classList.toggle('disabled',checked.length===0);
  btn.textContent=checked.length?`⇩ Скачать отмеченные (${checked.length}/5)`:'⇩ Скачать отмеченные';
}
function downloadPayload(row){
  const route=routeForSearch();
  return {action:'TELEGRAM_DOWNLOAD',role:route.role,target_id:route.target_id,chat_id:row.chat_id,chat_username:row.chat_username||'',message_id:row.message_id,file_name:row.file_name||'',correlation_id:latestSearch?.correlation_id||undefined,parent_command_id:latestSearch?.command_id||undefined};
}
async function downloadRow(index){const row=latestRows[index];if(!row||!row.has_file)return;await action(downloadPayload(row))}

async function refresh(){
  try{renderOverview(await api('/api/overview'));await refreshSearches()}catch(e){toast('Ошибка: '+e.message)}
}
async function refreshSearches(){
  const d=await api('/api/search-results');
  const searches=d.searches||[];
  if(!searches.length)return;
  const last=searches[0];
  if(last.status!=='PASS'){
    $('#searchState').style.display='block';
    $('#searchState').textContent='Последний поиск завершился ошибкой: '+(last.error||last.status);
    return;
  }
  latestSearch=last;
  latestRows=last.results||[];
  $('#resultCount').textContent=latestRows.length;
  $('#searchContextBadge').textContent=`${last.role_id||'—'} · ${last.target_id||'—'} · файлов ${last.files_total||0}`;
  $('#searchState').style.display=latestRows.length?'none':'block';
  if(!latestRows.length)$('#searchState').textContent='По этому запросу результатов нет.';
  $('#results').innerHTML=latestRows.slice(0,50).map((r,i)=>{
    const downloadable=r.has_file&&r.message_id&&r.chat_id;
    return `<div class="result"><div class="result-select">${downloadable?`<input class="result-check" type="checkbox" data-index="${i}" aria-label="Отметить файл для скачивания">`:'<span style="width:13px"></span>'}<div class="result-body"><div class="result-top"><b>${esc(r.chat_title||r.chat_username||r.chat_id)}</b><small>${r.has_file?'FILE':'MESSAGE'}</small></div><p>${esc(r.text||r.file_name||'')}</p><small>${esc(r.file_name||'')} ${r.file_size?(' · '+fmtBytes(r.file_size)):''} ${r.mime_type?(' · '+esc(r.mime_type)):''}</small>${downloadable?`<div class="result-actions"><button class="tiny result-download" data-index="${i}">⇩ Скачать</button><span class="result-route">→ ${esc(last.role_id||'')} / ${esc(last.target_id||'')}</span></div>`:''}</div></div></div>`;
  }).join('');
  document.querySelectorAll('.result-check').forEach(el=>el.addEventListener('change',()=>{
    const checked=[...document.querySelectorAll('.result-check:checked')];
    if(checked.length>5){el.checked=false;toast('За один запуск можно отметить максимум 5 файлов')}
    updateDownloadSelectedState();
  }));
  document.querySelectorAll('.result-download').forEach(el=>el.addEventListener('click',()=>downloadRow(Number(el.dataset.index))));
  updateDownloadSelectedState();
}

async function action(payload){
  try{
    const r=await api('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    toast('Запущено: '+r.job.kind+' · '+r.job.command_id);
    setTimeout(refresh,500);
    return r;
  }catch(e){toast('Не запущено: '+e.message);throw e}
}

$('#roleSelect').addEventListener('change',()=>{renderTopics();latestSearch=null;latestRows=[];$('#results').innerHTML='';$('#resultCount').textContent='0';$('#searchContextBadge').textContent='новый контекст';$('#searchState').style.display='block';$('#searchState').textContent='Введите запрос для выбранной роли и темы.'});
$('#topicSelect').addEventListener('change',()=>{updateDestination();latestSearch=null;latestRows=[];$('#results').innerHTML='';$('#resultCount').textContent='0';$('#searchContextBadge').textContent='новый контекст'});
$('#searchBtn').onclick=()=>{const q=$('#queryInput').value.trim();const r=currentRoute();if(!q)return toast('Введите поисковый запрос');if(!r.role||!r.target_id)return toast('Выберите роль и тему');action({action:'TELEGRAM_QUERY_PROBE',query:q,...r})};
$('#queryInput').addEventListener('keydown',e=>{if(e.key==='Enter')$('#searchBtn').click()});
$('#downloadSelectedBtn').onclick=async()=>{const checked=[...document.querySelectorAll('.result-check:checked')].slice(0,5);if(!checked.length)return;for(const box of checked){await downloadRow(Number(box.dataset.index))}};
$('#libraryStartBtn').onclick=()=>{
  const role=$('#libraryRoleSelect').value;
  const maturity=$('#libraryMaturitySelect').value;
  const mode=$('#libraryModeSelect').value;
  if(!role)return toast('Выберите роль');
  action({action:'LIBRARY_ORDER_START',role,maturity,mode});
};
$('#refreshBtn').onclick=refresh;
$('#probeBtn').onclick=()=>action({action:'PROGRAMMER_BIBLIOGRAPHY_PROBE'});
$('#planBtn').onclick=()=>action({action:'PROGRAMMER_BIBLIOGRAPHY_PLAN'});
$('#remainingBtn').onclick=()=>action({action:'REMAINING_P0_WINDOWS'});

document.querySelectorAll('.nav[data-view]').forEach(btn=>btn.addEventListener('click',()=>{
  const map={overview:'metricCards',library:'libraryPanel',search:'searchPanel',downloads:'downloadsPanel',jobs:'jobs',trace:'tracePanel'};
  const id=map[btn.dataset.view];if(id){document.getElementById(id)?.scrollIntoView({behavior:'smooth',block:'start'})}
}));

setInterval(refresh,2000);
refresh();
