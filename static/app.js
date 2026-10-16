// ==============================================================================
// Controle de Férias - CBMRN
// JavaScript do Front-End (Interações, APIs, Calendário e Validações)
// ==============================================================================

let usuarioLogado = null;
let mesCalendarioAtual = new Date().getMonth() + 1;
let anoCalendarioAtual = new Date().getFullYear();
let listaTodosAgendamentos = [];

const MESES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

// Inicialização ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  verificarSessao();
  carregarInfoRede();
});

// ================= Autenticação =================

async function verificarSessao() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    if (data.logado) {
      usuarioLogado = data.usuario;
      exibirApp();
    } else {
      exibirLogin();
    }
  } catch (err) {
    console.error("Erro ao verificar sessão:", err);
    exibirLogin();
  }
}

function exibirLogin() {
  document.getElementById("loginScreen").style.display = "flex";
  document.getElementById("appScreen").style.display = "none";
}

function exibirApp() {
  document.getElementById("loginScreen").style.display = "none";
  document.getElementById("appScreen").style.display = "block";

  // Preencher dados do topo
  document.getElementById("userName").textContent = `${usuarioLogado.posto_graduacao} ${usuarioLogado.nome_guerra}`;
  document.getElementById("userRole").textContent = `${usuarioLogado.setor_subunidade} • ${usuarioLogado.papel === 'gestor' ? 'Gestão / RH' : 'Militar'}`;
  document.getElementById("userAvatar").textContent = usuarioLogado.nome_guerra.substring(0, 2).toUpperCase();

  // Se não for gestor, esconde aba de controles gerais se quiser, ou deixa visível como consulta
  if (usuarioLogado.papel !== 'gestor') {
    document.getElementById("tabBtnGestao").title = "Visão geral da tropa (Modo Consulta)";
  }

  // Carregar dados da aba inicial
  carregarPeriodosUsuario();
  carregarCalendario();
}

async function realizarLogin(e) {
  e.preventDefault();
  const mat = document.getElementById("loginMatricula").value.trim();
  const pin = document.getElementById("loginPin").value.trim();
  const erroEl = document.getElementById("loginError");
  erroEl.style.display = "none";

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ matricula: mat, pin })
    });
    const data = await res.json();

    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha no login.';
      erroEl.style.display = 'block';
      return;
    }

    usuarioLogado = data.usuario;
    exibirApp();
  } catch (err) {
    erroEl.textContent = 'Erro de comunicação com o servidor.';
    erroEl.style.display = 'block';
  }
}

async function realizarLogout() {
  if (confirm("Deseja realmente sair do sistema?")) {
    await fetch('/api/auth/logout', { method: 'POST' });
    usuarioLogado = null;
    window.location.reload();
  }
}

function preencherLogin(mat, pin) {
  document.getElementById("loginMatricula").value = mat;
  document.getElementById("loginPin").value = pin;
  document.getElementById("loginMatricula").focus();
}

// ================= Informações de Rede e Compartilhamento =================

async function carregarInfoRede() {
  try {
    const res = await fetch('/api/info/rede');
    const data = await res.json();
    const btnIp = document.getElementById("labelIpRede");
    const inputUrl = document.getElementById("inputUrlRede");

    if (btnIp && data.ip_local) {
      btnIp.textContent = `Rede: ${data.ip_local}:5000`;
    }
    if (inputUrl && data.url_local) {
      inputUrl.value = data.url_local;
    }
  } catch (err) {
    console.warn("Não foi possível obter IP de rede:", err);
  }
}

function copiarLinkRede() {
  const input = document.getElementById("inputUrlRede");
  input.select();
  input.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(input.value);
  alert("✅ Link de acesso copiado! Envie para seus colegas na rede:\n" + input.value);
}

// ================= Navegação entre Abas =================

function trocarAba(abaId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(content => content.classList.remove("active"));

  const botaoAtivo = Array.from(document.querySelectorAll(".tab-btn")).find(btn => 
    btn.getAttribute("onclick")?.includes(`'${abaId}'`)
  );
  if (botaoAtivo) botaoAtivo.classList.add("active");

  const conteudoAtivo = document.getElementById(`aba-${abaId}`);
  if (conteudoAtivo) conteudoAtivo.classList.add("active");

  if (abaId === 'minhas-ferias') carregarMinhasFerias();
  if (abaId === 'reaprazamentos') carregarHistoricoReaprazamentos();
  if (abaId === 'calendario') carregarCalendario();
  if (abaId === 'gestao') carregarQuadroGeral();
}

// ================= Minhas Férias =================

async function carregarPeriodosUsuario() {
  try {
    const res = await fetch(`/api/periodos?usuario_id=${usuarioLogado.id}`);
    const periodos = await res.json();
    const select = document.getElementById("selectPeriodoUsuario");
    const selectAgendamento = document.getElementById("agendamentoPeriodo");

    select.innerHTML = "";
    selectAgendamento.innerHTML = "";

    if (periodos.length === 0) {
      select.innerHTML = "<option value=''>Nenhum período cadastrado</option>";
      selectAgendamento.innerHTML = "<option value=''>Cadastre um período antes</option>";
      return;
    }

    periodos.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = `Exercício ${p.exercicio} (Saldo: ${p.saldo_dias} dias)`;
      opt.dataset.exercicio = p.exercicio;
      opt.dataset.saldo = p.saldo_dias;
      opt.dataset.total = p.total_dias;
      opt.dataset.utilizados = p.dias_utilizados;
      select.appendChild(opt);

      const opt2 = opt.cloneNode(true);
      selectAgendamento.appendChild(opt2);
    });

    carregarMinhasFerias();
  } catch (err) {
    console.error("Erro ao carregar períodos:", err);
  }
}

async function carregarMinhasFerias() {
  const select = document.getElementById("selectPeriodoUsuario");
  const selectedOpt = select.selectedOptions[0];

  if (!selectedOpt || !selectedOpt.value) {
    document.getElementById("kpiExercicio").textContent = "-";
    document.getElementById("kpiDiasAgendados").textContent = "0 Dias";
    document.getElementById("kpiSaldoRestante").textContent = "30 Dias";
    document.getElementById("listaMinhasFerias").innerHTML = "<p class='text-muted'>Nenhum período selecionado.</p>";
    return;
  }

  const periodoId = selectedOpt.value;
  const exercicio = selectedOpt.dataset.exercicio;

  try {
    const res = await fetch(`/api/ferias?usuario_id=${usuarioLogado.id}`);
    const todasMinhasFerias = await res.json();
    const parcelasPeriodo = todasMinhasFerias.filter(f => f.periodo_aquisitivo_id == periodoId);

    const totalDiasAgendados = parcelasPeriodo.reduce((acc, curr) => acc + curr.dias, 0);
    const saldo = 30 - totalDiasAgendados;

    document.getElementById("kpiExercicio").textContent = exercicio;
    document.getElementById("kpiDiasAgendados").textContent = `${totalDiasAgendados} Dias`;
    document.getElementById("kpiSaldoRestante").textContent = `${saldo} Dias`;

    const grid = document.getElementById("listaMinhasFerias");
    grid.innerHTML = "";

    if (parcelasPeriodo.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px;">
          <p style="font-size: 1.1rem; font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Nenhuma parcela agendada para o exercício ${exercicio}</p>
          <p style="font-size: 0.875rem; color: #64748b; margin-bottom: 1.25rem;">Você tem 30 dias integrais disponíveis para programar.</p>
          <button class="btn btn-primary" onclick="abrirModalAgendamento()">
            📅 Agendar Minhas Férias Agora
          </button>
        </div>
      `;
      return;
    }

    parcelasPeriodo.forEach(p => {
      const card = document.createElement("div");
      card.className = "parcela-card";

      const dataIniFmt = formatarDataBR(p.data_inicio);
      const dataFimFmt = formatarDataBR(p.data_fim);
      const dataRetFmt = formatarDataBR(p.data_retorno);

      const statusBadge = p.status === 'reaprazado' 
        ? '<span class="badge-status badge-warning">🔄 Reaprazada</span>'
        : '<span class="badge-status badge-success">✓ Homologada</span>';

      card.innerHTML = `
        <div>
          <div class="parcela-card-header">
            <span class="parcela-title">${p.parcela}ª Parcela (${p.dias} dias)</span>
            ${statusBadge}
          </div>

          <div class="parcela-dates">
            <div class="date-row">
              <span class="date-label">Início da Fruição:</span>
              <span class="date-val">${dataIniFmt}</span>
            </div>
            <div class="date-row">
              <span class="date-label">Último Dia de Férias:</span>
              <span class="date-val">${dataFimFmt}</span>
            </div>
            <div class="date-row">
              <span class="date-label">Retorno ao Serviço:</span>
              <span class="date-val highlight">${dataRetFmt}</span>
            </div>
            ${p.observacoes ? `<div class="date-row" style="margin-top:0.4rem; font-size:0.8rem; color:#64748b;"><em>Obs: ${p.observacoes}</em></div>` : ''}
          </div>
        </div>

        <div class="parcela-card-footer">
          <button class="btn btn-primary btn-sm btn-block" onclick='abrirModalReaprazamento(${JSON.stringify(p)})'>
            🔄 Solicitar Reaprazamento
          </button>
        </div>
      `;
      grid.appendChild(card);
    });

  } catch (err) {
    console.error("Erro ao carregar minhas férias:", err);
  }
}

// ================= Agendamento e Fracionamento Flexível =================

function abrirModalAgendamento() {
  document.getElementById("modalAgendamento").classList.add("active");
  atualizarFormParcelas();
}

function atualizarFormParcelas() {
  const modalidade = document.querySelector('input[name="modalidadeFracionamento"]:checked').value;
  const container = document.getElementById("containerParcelas");
  container.innerHTML = "";

  const hoje = new Date().toISOString().split('T')[0];

  if (modalidade === "1") {
    // 1 parcela de 30 dias
    container.innerHTML = `
      <div class="parcela-form-row">
        <div class="form-group" style="margin:0;">
          <label>Data de Início das Férias (30 dias integrais) *</label>
          <input type="date" id="p1_inicio" required value="${hoje}">
        </div>
        <div class="form-group" style="margin:0;">
          <label>Duração</label>
          <input type="number" id="p1_dias" value="30" readonly style="background:#f1f5f9;">
        </div>
      </div>
    `;
  } else if (modalidade === "2") {
    // 2 parcelas (qualquer divisão somando 30: 15/15, 12/18, 20/10, etc.)
    container.innerHTML = `
      <div class="parcela-form-row">
        <div class="form-group" style="margin:0;">
          <label>1ª Parcela - Data de Início *</label>
          <input type="date" id="p1_inicio" required value="${hoje}">
        </div>
        <div class="form-group" style="margin:0;">
          <label>Dias (1ª Parcela) *</label>
          <input type="number" id="p1_dias" value="15" min="1" max="29" required oninput="ajustarSegundaParcela()">
        </div>
      </div>

      <div class="parcela-form-row" style="margin-top:1rem;">
        <div class="form-group" style="margin:0;">
          <label>2ª Parcela - Data de Início *</label>
          <input type="date" id="p2_inicio" required>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Dias (2ª Parcela) *</label>
          <input type="number" id="p2_dias" value="15" min="1" max="29" required oninput="validarSomaDias()">
        </div>
      </div>
    `;
  } else if (modalidade === "3") {
    // 3 parcelas (nenhuma menor que 10 dias -> 10 + 10 + 10 = 30)
    container.innerHTML = `
      <div class="parcela-form-row">
        <div class="form-group" style="margin:0;">
          <label>1ª Parcela - Início *</label>
          <input type="date" id="p1_inicio" required value="${hoje}">
        </div>
        <div class="form-group" style="margin:0;">
          <label>Dias (Mín. 10)</label>
          <input type="number" id="p1_dias" value="10" min="10" max="10" readonly style="background:#f1f5f9;">
        </div>
      </div>

      <div class="parcela-form-row" style="margin-top:1rem;">
        <div class="form-group" style="margin:0;">
          <label>2ª Parcela - Início *</label>
          <input type="date" id="p2_inicio" required>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Dias (Mín. 10)</label>
          <input type="number" id="p2_dias" value="10" min="10" max="10" readonly style="background:#f1f5f9;">
        </div>
      </div>

      <div class="parcela-form-row" style="margin-top:1rem;">
        <div class="form-group" style="margin:0;">
          <label>3ª Parcela - Início *</label>
          <input type="date" id="p3_inicio" required>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Dias (Mín. 10)</label>
          <input type="number" id="p3_dias" value="10" min="10" max="10" readonly style="background:#f1f5f9;">
        </div>
      </div>
    `;
  }

  validarSomaDias();
}

function ajustarSegundaParcela() {
  const p1 = parseInt(document.getElementById("p1_dias").value) || 0;
  const p2El = document.getElementById("p2_dias");
  if (p2El) {
    p2El.value = Math.max(1, 30 - p1);
  }
  validarSomaDias();
}

function validarSomaDias() {
  const modalidade = document.querySelector('input[name="modalidadeFracionamento"]:checked').value;
  let soma = 0;

  if (modalidade === "1") {
    soma = 30;
  } else if (modalidade === "2") {
    const p1 = parseInt(document.getElementById("p1_dias")?.value) || 0;
    const p2 = parseInt(document.getElementById("p2_dias")?.value) || 0;
    soma = p1 + p2;
  } else if (modalidade === "3") {
    const p1 = parseInt(document.getElementById("p1_dias")?.value) || 0;
    const p2 = parseInt(document.getElementById("p2_dias")?.value) || 0;
    const p3 = parseInt(document.getElementById("p3_dias")?.value) || 0;
    soma = p1 + p2 + p3;
  }

  const totalEl = document.getElementById("totalDiasAlocados");
  const statusEl = document.getElementById("statusSomaDias");

  if (totalEl && statusEl) {
    totalEl.textContent = soma;
    if (soma === 30) {
      statusEl.className = "badge-status badge-success";
      statusEl.textContent = "Válido (30 dias)";
    } else {
      statusEl.className = "badge-status badge-danger";
      statusEl.textContent = `Inválido (${soma}/30 dias)`;
    }
  }
}

async function salvarAgendamento(e) {
  e.preventDefault();
  const erroEl = document.getElementById("agendamentoErro");
  erroEl.style.display = "none";

  const periodoId = document.getElementById("agendamentoPeriodo").value;
  const modalidade = parseInt(document.querySelector('input[name="modalidadeFracionamento"]:checked').value);
  const obs = document.getElementById("agendamentoObs").value.trim();

  const parcelas = [];

  if (modalidade === 1) {
    parcelas.push({
      data_inicio: document.getElementById("p1_inicio").value,
      dias: 30
    });
  } else if (modalidade === 2) {
    parcelas.push({
      data_inicio: document.getElementById("p1_inicio").value,
      dias: parseInt(document.getElementById("p1_dias").value)
    });
    parcelas.push({
      data_inicio: document.getElementById("p2_inicio").value,
      dias: parseInt(document.getElementById("p2_dias").value)
    });
  } else if (modalidade === 3) {
    parcelas.push({
      data_inicio: document.getElementById("p1_inicio").value,
      dias: parseInt(document.getElementById("p1_dias").value)
    });
    parcelas.push({
      data_inicio: document.getElementById("p2_inicio").value,
      dias: parseInt(document.getElementById("p2_dias").value)
    });
    parcelas.push({
      data_inicio: document.getElementById("p3_inicio").value,
      dias: parseInt(document.getElementById("p3_dias").value)
    });
  }

  try {
    const res = await fetch('/api/ferias', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        periodo_aquisitivo_id: periodoId,
        parcelas: parcelas,
        observacoes: obs
      })
    });

    const data = await res.json();
    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha ao agendar férias.';
      erroEl.style.display = 'block';
      return;
    }

    fecharModal("modalAgendamento");
    alert("✅ Férias agendadas com sucesso!");
    carregarPeriodosUsuario();
    carregarCalendario();
  } catch (err) {
    erroEl.textContent = 'Erro ao conectar ao servidor.';
    erroEl.style.display = 'block';
  }
}

// ================= Reaprazamento de Férias =================

function abrirModalReaprazamento(ferias) {
  document.getElementById("reaprazarFeriasId").value = ferias.id;
  document.getElementById("reaprazarDiasOriginal").value = ferias.dias;
  document.getElementById("reaprazarQuantidadeDias").value = ferias.dias;
  document.getElementById("reaprazarNovaDataInicio").value = ferias.data_inicio;
  document.getElementById("reaprazarMotivo").value = "";

  document.getElementById("reaprazarDetalhesMilitar").innerHTML = `
    <strong>Militar:</strong> ${ferias.posto_graduacao || usuarioLogado.posto_graduacao} ${ferias.nome_guerra || usuarioLogado.nome_guerra} (${ferias.matricula || usuarioLogado.matricula})
  `;
  document.getElementById("reaprazarDetalhesPeriodo").innerHTML = `
    <strong>Parcela Atual:</strong> ${ferias.parcela}ª Parcela de ${ferias.dias} dias | De ${formatarDataBR(ferias.data_inicio)} a ${formatarDataBR(ferias.data_fim)}
  `;

  calcularPreviaReaprazamento();
  document.getElementById("modalReaprazamento").classList.add("active");
}

function calcularPreviaReaprazamento() {
  const dataIniStr = document.getElementById("reaprazarNovaDataInicio").value;
  const dias = parseInt(document.getElementById("reaprazarQuantidadeDias").value) || 0;

  if (!dataIniStr || dias <= 0) {
    document.getElementById("previaDataFim").textContent = "-";
    document.getElementById("previaDataRetorno").textContent = "-";
    return;
  }

  const [ano, mes, dia] = dataIniStr.split("-").map(Number);
  const dataIni = new Date(ano, mes - 1, dia);

  const dataFim = new Date(dataIni);
  dataFim.setDate(dataFim.getDate() + (dias - 1));

  const dataRetorno = new Date(dataFim);
  dataRetorno.setDate(dataRetorno.getDate() + 1);

  document.getElementById("previaDataFim").textContent = formatarDataBR(dataFim.toISOString().split("T")[0]);
  document.getElementById("previaDataRetorno").textContent = formatarDataBR(dataRetorno.toISOString().split("T")[0]);
}

async function salvarReaprazamento(e) {
  e.preventDefault();
  const erroEl = document.getElementById("reaprazarErro");
  erroEl.style.display = "none";

  const feriasId = document.getElementById("reaprazarFeriasId").value;
  const novaDataInicio = document.getElementById("reaprazarNovaDataInicio").value;
  const novosDias = document.getElementById("reaprazarQuantidadeDias").value;
  const motivo = document.getElementById("reaprazarMotivo").value.trim();

  if (!motivo) {
    erroEl.textContent = "A justificativa/motivo do reaprazamento é obrigatória.";
    erroEl.style.display = "block";
    return;
  }

  try {
    const res = await fetch(`/api/ferias/${feriasId}/reaprazar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nova_data_inicio: novaDataInicio,
        novos_dias: novosDias,
        motivo: motivo
      })
    });

    const data = await res.json();
    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha ao reaprazar férias.';
      erroEl.style.display = 'block';
      return;
    }

    fecharModal("modalReaprazamento");
    alert("✅ Reaprazamento registrado e efetivado com sucesso!");
    carregarMinhasFerias();
    carregarCalendario();
    carregarHistoricoReaprazamentos();
  } catch (err) {
    erroEl.textContent = 'Erro ao conectar ao servidor.';
    erroEl.style.display = 'block';
  }
}

async function carregarHistoricoReaprazamentos() {
  try {
    const res = await fetch('/api/reaprazamentos?todos=1');
    const lista = await res.json();
    const tbody = document.getElementById("tabelaReaprazamentos");
    tbody.innerHTML = "";

    if (lista.length === 0) {
      tbody.innerHTML = `<tr><td colspan="9" class="text-center" style="padding:2rem;">Nenhum reaprazamento registrado até o momento.</td></tr>`;
      return;
    }

    lista.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><small class="text-muted">${formatarDataHoraBR(r.solicitado_em)}</small></td>
        <td><strong>${r.posto_graduacao} ${r.nome_guerra}</strong><br><small class="text-muted">Mat: ${r.matricula}</small></td>
        <td>${r.setor_subunidade}</td>
        <td>${r.parcela}ª Parcela</td>
        <td><span style="text-decoration: line-through; color: #94a3b8;">${formatarDataBR(r.data_inicio_anterior)}</span> (${r.dias_anterior}d)</td>
        <td><strong style="color: #d97706;">${formatarDataBR(r.data_inicio_nova)}</strong> a ${formatarDataBR(r.data_fim_nova)} (${r.dias_novo}d)</td>
        <td><strong style="color: #16a34a;">${formatarDataBR(r.data_retorno_nova)}</strong></td>
        <td style="max-width: 250px;">${r.motivo}</td>
        <td><span class="badge-status badge-success">${r.homologado_por}</span></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Erro ao carregar reaprazamentos:", err);
  }
}

// ================= Calendário da Tropa e Conflitos =================

function mudarMes(delta) {
  mesCalendarioAtual += delta;
  if (mesCalendarioAtual > 12) {
    mesCalendarioAtual = 1;
    anoCalendarioAtual++;
  } else if (mesCalendarioAtual < 1) {
    mesCalendarioAtual = 12;
    anoCalendarioAtual--;
  }
  carregarCalendario();
}

async function carregarCalendario() {
  const setor = document.getElementById("filtroSetorCalendario")?.value || "";
  document.getElementById("labelMesAnoAtual").textContent = `${MESES[mesCalendarioAtual - 1]} ${anoCalendarioAtual}`;

  try {
    const res = await fetch(`/api/calendario/escala?mes=${mesCalendarioAtual}&ano=${anoCalendarioAtual}&setor=${encodeURIComponent(setor)}`);
    const data = await res.json();
    const grid = document.getElementById("calendarGrid");
    grid.innerHTML = "";

    // Primeiro dia da semana no mês
    const primeiroDiaSemana = new Date(anoCalendarioAtual, mesCalendarioAtual - 1, 1).getDay();
    for (let i = 0; i < primeiroDiaSemana; i++) {
      const blank = document.createElement("div");
      blank.className = "calendar-day-cell other-month";
      grid.appendChild(blank);
    }

    data.dias.forEach(d => {
      const cell = document.createElement("div");
      cell.className = `calendar-day-cell ${d.conflito_setor ? 'has-conflict' : ''}`;

      let conflictHtml = '';
      if (d.conflito_setor) {
        conflictHtml = `<span class="conflict-indicator" title="Alerta: Mais de 1 militar do mesmo setor afastado!">⚠️ Conflito</span>`;
      }

      let eventsHtml = '';
      d.militares.forEach(m => {
        const cls = m.status === 'reaprazado' ? 'reaprazado' : '';
        eventsHtml += `
          <div class="event-pill ${cls}" title="${m.posto_graduacao} ${m.nome_guerra} (${m.setor_subunidade}) - ${m.parcela}ª Parcela">
            👨‍🚒 ${m.nome_guerra} (${m.parcela}ª)
          </div>
        `;
      });

      cell.innerHTML = `
        <div class="day-header">
          <span class="day-num">${d.dia}</span>
          ${conflictHtml}
        </div>
        <div class="day-events">
          ${eventsHtml}
        </div>
      `;
      grid.appendChild(cell);
    });

  } catch (err) {
    console.error("Erro ao carregar calendário:", err);
  }
}

// ================= Controles Gerais e Gestão RH =================

async function carregarQuadroGeral() {
  carregarEstatisticas();
  const setor = document.getElementById("filtroSetorGeral")?.value || "";

  try {
    const res = await fetch(`/api/ferias?visao_equipe=1&setor=${encodeURIComponent(setor)}`);
    listaTodosAgendamentos = await res.json();
    renderizarTabelaGeral(listaTodosAgendamentos);
  } catch (err) {
    console.error("Erro ao carregar quadro geral:", err);
  }
}

function renderizarTabelaGeral(dados) {
  const tbody = document.getElementById("corpoTabelaGeral");
  tbody.innerHTML = "";

  if (dados.length === 0) {
    tbody.innerHTML = `<tr><td colspan="12" class="text-center" style="padding:2rem;">Nenhum registro encontrado.</td></tr>`;
    return;
  }

  dados.forEach(f => {
    const tr = document.createElement("tr");
    const statusBadge = f.status === 'reaprazado' 
      ? '<span class="badge-status badge-warning">Reaprazada</span>'
      : '<span class="badge-status badge-success">Homologada</span>';

    tr.innerHTML = `
      <td><strong>${f.nome_guerra}</strong><br><small class="text-muted">${f.nome_completo}</small></td>
      <td><code>${f.matricula}</code></td>
      <td>${f.posto_graduacao}</td>
      <td><small>${f.setor_subunidade}</small></td>
      <td>${f.periodo_exercicio}</td>
      <td>${f.parcela}ª de ${f.total_parcelas}</td>
      <td>${formatarDataBR(f.data_inicio)}</td>
      <td><strong>${f.dias}d</strong></td>
      <td>${formatarDataBR(f.data_fim)}</td>
      <td><strong style="color: #16a34a;">${formatarDataBR(f.data_retorno)}</strong></td>
      <td>${statusBadge}</td>
      <td>
        <button class="btn btn-outline btn-sm" onclick='abrirModalReaprazamento(${JSON.stringify(f)})' title="Reaprazar">
          🔄
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filtrarTabelaGeral() {
  const termo = document.getElementById("filtroBuscaGeral").value.toLowerCase();
  const filtrados = listaTodosAgendamentos.filter(item => 
    item.nome_guerra.toLowerCase().includes(termo) ||
    item.nome_completo.toLowerCase().includes(termo) ||
    item.matricula.toLowerCase().includes(termo) ||
    item.posto_graduacao.toLowerCase().includes(termo) ||
    item.setor_subunidade.toLowerCase().includes(termo)
  );
  renderizarTabelaGeral(filtrados);
}

async function carregarEstatisticas() {
  try {
    const res = await fetch('/api/estatisticas');
    const dados = await res.json();
    document.getElementById("kpiTotalEfetivo").textContent = dados.total_efetivo;
    document.getElementById("kpiEmFruicaoHoje").textContent = dados.em_fruicao_hoje;
    document.getElementById("kpiPrevistasFuturas").textContent = dados.previstas_futuras;
    document.getElementById("kpiTotalReaprazamentos").textContent = dados.total_reaprazamentos;
  } catch (err) {
    console.error("Erro ao carregar estatísticas:", err);
  }
}

// ================= Cadastros (Militar e Período) =================

function abrirModalNovoMilitar() {
  document.getElementById("modalNovoMilitar").classList.add("active");
}

async function salvarNovoMilitar(e) {
  e.preventDefault();
  const erroEl = document.getElementById("cadMilitarErro");
  erroEl.style.display = "none";

  const matricula = document.getElementById("cadMatricula").value.trim();
  const posto = document.getElementById("cadPosto").value;
  const nomeCompleto = document.getElementById("cadNomeCompleto").value.trim();
  const nomeGuerra = document.getElementById("cadNomeGuerra").value.trim();
  const pin = document.getElementById("cadPin").value.trim();
  const setor = document.getElementById("cadSetor").value;
  const papel = document.getElementById("cadPapel").value;

  try {
    const res = await fetch('/api/usuarios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        matricula, posto_graduacao: posto, nome_completo: nomeCompleto,
        nome_guerra: nomeGuerra, pin, setor_subunidade: setor, papel
      })
    });

    const data = await res.json();
    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha ao cadastrar militar.';
      erroEl.style.display = "block";
      return;
    }

    fecharModal("modalNovoMilitar");
    alert("✅ Militar cadastrado com sucesso!");
    carregarQuadroGeral();
  } catch (err) {
    erroEl.textContent = "Erro ao conectar ao servidor.";
    erroEl.style.display = "block";
  }
}

function abrirModalNovoPeriodo() {
  document.getElementById("modalNovoPeriodo").classList.add("active");
}

async function salvarNovoPeriodo(e) {
  e.preventDefault();
  const erroEl = document.getElementById("novoPeriodoErro");
  erroEl.style.display = "none";

  const exercicio = document.getElementById("novoPeriodoExercicio").value.trim();

  try {
    const res = await fetch('/api/periodos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exercicio })
    });

    const data = await res.json();
    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha ao incluir período.';
      erroEl.style.display = "block";
      return;
    }

    fecharModal("modalNovoPeriodo");
    alert("✅ Período aquisitivo cadastrado com sucesso!");
    carregarPeriodosUsuario();
  } catch (err) {
    erroEl.textContent = "Erro ao conectar ao servidor.";
    erroEl.style.display = "block";
  }
}

// ================= Alteração de PIN =================

function abrirModalPin() {
  document.getElementById("modalPin").classList.add("active");
  document.getElementById("pinAtual").value = "";
  document.getElementById("novoPin").value = "";
}

async function salvarAlteracaoPin(e) {
  e.preventDefault();
  const erroEl = document.getElementById("pinErro");
  erroEl.style.display = "none";

  const pinAtual = document.getElementById("pinAtual").value.trim();
  const novoPin = document.getElementById("novoPin").value.trim();

  try {
    const res = await fetch('/api/auth/alterar-pin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin_atual: pinAtual, novo_pin: novoPin })
    });

    const data = await res.json();
    if (!res.ok) {
      erroEl.textContent = data.erro || 'Falha ao alterar PIN.';
      erroEl.style.display = "block";
      return;
    }

    fecharModal("modalPin");
    alert("✅ PIN alterado com sucesso!");
  } catch (err) {
    erroEl.textContent = "Erro de conexão ao alterar PIN.";
    erroEl.style.display = "block";
  }
}

// ================= Exportação e Impressão =================

function exportarCSV() {
  if (listaTodosAgendamentos.length === 0) {
    alert("Nenhum dado para exportar.");
    return;
  }

  let csv = "Militar;Matrícula;Posto/Graduação;Setor/Unidade;Exercício;Parcela;Início;Dias;Término;Retorno ao Serviço;Status\n";
  listaTodosAgendamentos.forEach(f => {
    csv += `"${f.nome_guerra}";"${f.matricula}";"${f.posto_graduacao}";"${f.setor_subunidade}";"${f.periodo_exercicio}";"${f.parcela}ª";"${formatarDataBR(f.data_inicio)}";"${f.dias}";"${formatarDataBR(f.data_fim)}";"${formatarDataBR(f.data_retorno)}";"${f.status}"\n`;
  });

  const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Escala_Ferias_CBMRN_${new Date().toISOString().split("T")[0]}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

function imprimirEscala() {
  window.print();
}

// ================= Modais e Utilitários =================

function abrirModalRede() {
  document.getElementById("modalRede").classList.add("active");
}

function fecharModal(id) {
  document.getElementById(id).classList.remove("active");
}

function formatarDataBR(dataStr) {
  if (!dataStr) return "-";
  const [ano, mes, dia] = dataStr.split("-");
  return `${dia}/${mes}/${ano}`;
}

function formatarDataHoraBR(dataHoraStr) {
  if (!dataHoraStr) return "-";
  const partes = dataHoraStr.split(" ");
  const data = formatarDataBR(partes[0]);
  return `${data} às ${partes[1] || ''}`;
}
