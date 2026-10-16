import os
import sqlite3
import socket
import datetime
from datetime import datetime as dt, timedelta
from functools import wraps
from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'), static_url_path='/static')
app.secret_key = os.urandom(24)

DB_PATH = os.path.join(BASE_DIR, 'ferias_cbmrn.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT UNIQUE NOT NULL,
        nome_completo TEXT NOT NULL,
        nome_guerra TEXT NOT NULL,
        posto_graduacao TEXT NOT NULL,
        setor_subunidade TEXT NOT NULL,
        pin_hash TEXT NOT NULL,
        papel TEXT DEFAULT 'militar',
        ativo INTEGER DEFAULT 1,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS periodos_aquisitivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        exercicio TEXT NOT NULL,
        total_dias INTEGER DEFAULT 30,
        dias_utilizados INTEGER DEFAULT 0,
        status TEXT DEFAULT 'aberto',
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(usuario_id, exercicio)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ferias_agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        periodo_aquisitivo_id INTEGER NOT NULL REFERENCES periodos_aquisitivos(id) ON DELETE CASCADE,
        parcela INTEGER NOT NULL,
        total_parcelas INTEGER NOT NULL,
        data_inicio TEXT NOT NULL,
        dias INTEGER NOT NULL,
        data_fim TEXT NOT NULL,
        data_retorno TEXT NOT NULL,
        status TEXT DEFAULT 'homologado',
        observacoes TEXT,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reaprazamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ferias_id INTEGER NOT NULL REFERENCES ferias_agendamentos(id) ON DELETE CASCADE,
        usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        data_inicio_anterior TEXT NOT NULL,
        dias_anterior INTEGER NOT NULL,
        data_inicio_nova TEXT NOT NULL,
        dias_novo INTEGER NOT NULL,
        data_fim_nova TEXT NOT NULL,
        data_retorno_nova TEXT NOT NULL,
        motivo TEXT NOT NULL,
        solicitado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        homologado_por TEXT DEFAULT 'Chefia Imediata'
    );
    """)

    # Verificar se já existe admin
    cursor.execute("SELECT id FROM usuarios WHERE matricula = 'admin'")
    if not cursor.fetchone():
        admin_pin = generate_password_hash("193")
        cursor.execute("""
        INSERT INTO usuarios (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel)
        VALUES ('admin', 'Administrador Geral CBMRN', 'ADMIN RH', 'Capitão BM', 'Diretoria de Recursos Humanos (DRH)', ?, 'gestor')
        """, (admin_pin,))
        admin_id = cursor.lastrowid

        # Exemplos de militares do CBMRN para demonstração inicial realista
        militares_iniciais = [
            ('193001', 'Eduardo Santos Bezerra', 'Cap. Eduardo', 'Capitão BM', '1º Grupamento de Bombeiros (1º GB)', 'gestor'),
            ('193002', 'Marcela Fernandes de Lima', 'Ten. Marcela', '1º Tenente BM', 'Centro de Operações (CIOSP/CBMRN)', 'militar'),
            ('193003', 'Francisco de Assis Silva', 'Sgt. Silva', '1º Sargento BM', '1º Grupamento de Bombeiros (1º GB)', 'militar'),
            ('193004', 'Rodrigo Oliveira Costa', 'Cb. Oliveira', 'Cabo BM', 'Serviço de Salvamento Aquático (GBSA)', 'militar'),
            ('193005', 'Lucas Alencar Nascimento', 'Sd. Alencar', 'Soldado BM', '1º Grupamento de Bombeiros (1º GB)', 'militar'),
        ]

        default_pin = generate_password_hash("193")
        for mat, nome, guerra, posto, setor, papel in militares_iniciais:
            cursor.execute("""
            INSERT INTO usuarios (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (mat, nome, guerra, posto, setor, default_pin, papel))
            uid = cursor.lastrowid

            # Adicionar períodos aquisitivos padrão (2024/2025 e 2025/2026)
            for ex in ['2024/2025', '2025/2026']:
                cursor.execute("""
                INSERT INTO periodos_aquisitivos (usuario_id, exercicio, total_dias, dias_utilizados)
                VALUES (?, ?, 30, 0)
                """, (uid, ex))

        # Adicionar agendamento prévio com 2 parcelas (15 e 15 dias) para o Sgt. Silva como demonstração
        cursor.execute("SELECT id FROM usuarios WHERE matricula = '193003'")
        sgt_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM periodos_aquisitivos WHERE usuario_id = ? AND exercicio = '2024/2025'", (sgt_id,))
        p_id = cursor.fetchone()[0]

        d_ini1 = "2026-11-03"
        d_fim1 = "2026-11-17"
        d_ret1 = "2026-11-18"
        cursor.execute("""
        INSERT INTO ferias_agendamentos (usuario_id, periodo_aquisitivo_id, parcela, total_parcelas, data_inicio, dias, data_fim, data_retorno, status, observacoes)
        VALUES (?, ?, 1, 2, ?, 15, ?, ?, 'homologado', '1ª Parcela planejada')
        """, (sgt_id, p_id, d_ini1, d_fim1, d_ret1))

        d_ini2 = "2027-02-01"
        d_fim2 = "2027-02-15"
        d_ret2 = "2027-02-16"
        cursor.execute("""
        INSERT INTO ferias_agendamentos (usuario_id, periodo_aquisitivo_id, parcela, total_parcelas, data_inicio, dias, data_fim, data_retorno, status, observacoes)
        VALUES (?, ?, 2, 2, ?, 15, ?, ?, 'homologado', '2ª Parcela planejada')
        """, (sgt_id, p_id, d_ini2, d_fim2, d_ret2))

        cursor.execute("UPDATE periodos_aquisitivos SET dias_utilizados = 30 WHERE id = ?", (p_id,))

    conn.commit()
    conn.close()

    # Garantir que o efetivo do CFIS 2026 esteja carregado
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE matricula = '193010'")
        if not cursor.fetchone():
            conn.close()
            from cadastrar_efetivo_cfis import seed_cfis
            seed_cfis()
        else:
            conn.close()
    except Exception as e:
        print("Aviso:", e)

# Inicializar banco de dados ao carregar aplicacao
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({'erro': 'Acesso não autorizado. Faça login.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def calcular_datas(data_inicio_str, dias):
    data_ini = dt.strptime(data_inicio_str, "%Y-%m-%d")
    data_fim = data_ini + timedelta(days=dias - 1)
    data_retorno = data_fim + timedelta(days=1)
    return data_fim.strftime("%Y-%m-%d"), data_retorno.strftime("%Y-%m-%d")

def atualizar_saldo_periodo(conn, periodo_id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COALESCE(SUM(dias), 0) FROM ferias_agendamentos 
    WHERE periodo_aquisitivo_id = ? AND status != 'cancelado'
    """, (periodo_id,))
    total_usado = cursor.fetchone()[0]
    cursor.execute("""
    UPDATE periodos_aquisitivos 
    SET dias_utilizados = ? 
    WHERE id = ?
    """, (total_usado, periodo_id))
    conn.commit()

# ================= Rotas de Autenticação =================

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json or {}
    matricula = str(data.get('matricula', '')).strip()
    pin = str(data.get('pin', '')).strip()

    if not matricula or not pin:
        return jsonify({'erro': 'Matrícula e PIN/Senha são obrigatórios.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE matricula = ? AND ativo = 1", (matricula,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user['pin_hash'], pin):
        return jsonify({'erro': 'Matrícula ou PIN incorreto.'}), 401

    session['usuario_id'] = user['id']
    session['matricula'] = user['matricula']
    session['nome_guerra'] = user['nome_guerra']
    session['papel'] = user['papel']

    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {
            'id': user['id'],
            'matricula': user['matricula'],
            'nome_completo': user['nome_completo'],
            'nome_guerra': user['nome_guerra'],
            'posto_graduacao': user['posto_graduacao'],
            'setor_subunidade': user['setor_subunidade'],
            'papel': user['papel']
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'mensagem': 'Sessão encerrada com sucesso'})

@app.route('/api/auth/me', methods=['GET'])
def api_me():
    if 'usuario_id' not in session:
        return jsonify({'logado': False}), 200

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, papel FROM usuarios WHERE id = ? AND ativo = 1", (session['usuario_id'],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        session.clear()
        return jsonify({'logado': False}), 200

    return jsonify({
        'logado': True,
        'usuario': dict(user)
    })

@app.route('/api/auth/alterar-pin', methods=['POST'])
@login_required
def api_alterar_pin():
    data = request.json or {}
    pin_atual = str(data.get('pin_atual', '')).strip()
    novo_pin = str(data.get('novo_pin', '')).strip()

    if not pin_atual or not novo_pin:
        return jsonify({'erro': 'Preencha o PIN atual e o novo PIN.'}), 400

    if len(novo_pin) < 3:
        return jsonify({'erro': 'O novo PIN deve ter pelo menos 3 dígitos.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pin_hash FROM usuarios WHERE id = ?", (session['usuario_id'],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['pin_hash'], pin_atual):
        conn.close()
        return jsonify({'erro': 'PIN atual incorreto.'}), 400

    novo_hash = generate_password_hash(novo_pin)
    cursor.execute("UPDATE usuarios SET pin_hash = ? WHERE id = ?", (novo_hash, session['usuario_id']))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'PIN alterado com sucesso!'})

# ================= Rotas de Informações do Sistema =================

@app.route('/api/info/rede', methods=['GET'])
def api_info_rede():
    ip = get_local_ip()
    port = 5000
    return jsonify({
        'ip_local': ip,
        'porta': port,
        'url_local': f'http://{ip}:{port}',
        'url_localhost': f'http://localhost:{port}'
    })

# ================= Rotas de Usuários =================

@app.route('/api/usuarios', methods=['GET'])
@login_required
def api_listar_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, papel, ativo 
    FROM usuarios WHERE ativo = 1 
    ORDER BY posto_graduacao, nome_guerra
    """)
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(usuarios)

@app.route('/api/usuarios', methods=['POST'])
@login_required
def api_criar_usuario():
    if session.get('papel') != 'gestor':
        return jsonify({'erro': 'Apenas gestores/administradores podem cadastrar novos servidores.'}), 403

    data = request.json or {}
    matricula = str(data.get('matricula', '')).strip()
    nome_completo = str(data.get('nome_completo', '')).strip()
    nome_guerra = str(data.get('nome_guerra', '')).strip()
    posto_graduacao = str(data.get('posto_graduacao', '')).strip()
    setor_subunidade = str(data.get('setor_subunidade', '')).strip()
    pin = str(data.get('pin', '193')).strip()
    papel = data.get('papel', 'militar')

    if not matricula or not nome_completo or not nome_guerra or not posto_graduacao or not setor_subunidade:
        return jsonify({'erro': 'Todos os campos obrigatórios devem ser preenchidos.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE matricula = ?", (matricula,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Já existe um militar cadastrado com esta matrícula.'}), 400

    pin_hash = generate_password_hash(pin)
    cursor.execute("""
    INSERT INTO usuarios (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel))
    novo_id = cursor.lastrowid

    # Criar período aquisitivo atual automaticamente
    ano_atual = dt.now().year
    exercicio_padrao = f"{ano_atual}/{ano_atual + 1}"
    cursor.execute("""
    INSERT INTO periodos_aquisitivos (usuario_id, exercicio, total_dias, dias_utilizados)
    VALUES (?, ?, 30, 0)
    """, (novo_id, exercicio_padrao))

    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Militar cadastrado com sucesso!', 'id': novo_id})

# ================= Rotas de Períodos Aquisitivos =================

@app.route('/api/periodos', methods=['GET'])
@login_required
def api_listar_periodos():
    usuario_id = request.args.get('usuario_id', session['usuario_id'])
    
    # Se não for gestor, só pode ver os próprios períodos
    if session.get('papel') != 'gestor' and int(usuario_id) != session['usuario_id']:
        usuario_id = session['usuario_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.*, (p.total_dias - p.dias_utilizados) as saldo_dias
    FROM periodos_aquisitivos p
    WHERE p.usuario_id = ?
    ORDER BY p.exercicio DESC
    """, (usuario_id,))
    periodos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(periodos)

@app.route('/api/periodos', methods=['POST'])
@login_required
def api_criar_periodo():
    data = request.json or {}
    usuario_id = data.get('usuario_id', session['usuario_id'])
    exercicio = str(data.get('exercicio', '')).strip()

    if session.get('papel') != 'gestor' and int(usuario_id) != session['usuario_id']:
        return jsonify({'erro': 'Permissão negada.'}), 403

    if not exercicio:
        return jsonify({'erro': 'O exercício do período aquisitivo é obrigatório (ex: 2025/2026).'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO periodos_aquisitivos (usuario_id, exercicio, total_dias, dias_utilizados)
        VALUES (?, ?, 30, 0)
        """, (usuario_id, exercicio))
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        return jsonify({'mensagem': 'Período aquisitivo cadastrado!', 'id': novo_id})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'erro': 'Este período aquisitivo já está cadastrado para este militar.'}), 400

# ================= Rotas de Férias e Agendamento =================

@app.route('/api/ferias', methods=['GET'])
@login_required
def api_listar_ferias():
    usuario_id = request.args.get('usuario_id')
    setor = request.args.get('setor')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    query = """
    SELECT f.*, 
           u.nome_guerra, u.nome_completo, u.matricula, u.posto_graduacao, u.setor_subunidade,
           p.exercicio as periodo_exercicio
    FROM ferias_agendamentos f
    JOIN usuarios u ON f.usuario_id = u.id
    JOIN periodos_aquisitivos p ON f.periodo_aquisitivo_id = p.id
    WHERE f.status != 'cancelado'
    """
    params = []

    # Se for militar comum e não especificou ou se especificou outro sem permissão
    if session.get('papel') != 'gestor' and not request.args.get('visao_equipe'):
        query += " AND f.usuario_id = ?"
        params.append(session['usuario_id'])
    elif usuario_id:
        query += " AND f.usuario_id = ?"
        params.append(usuario_id)

    if setor:
        query += " AND u.setor_subunidade = ?"
        params.append(setor)

    if ano:
        query += " AND (strftime('%Y', f.data_inicio) = ? OR strftime('%Y', f.data_fim) = ?)"
        params.extend([ano, ano])

    if mes and ano:
        mes_formatado = f"{int(mes):02d}"
        query += " AND (strftime('%m', f.data_inicio) = ? OR strftime('%m', f.data_fim) = ?)"
        params.extend([mes_formatado, mes_formatado])

    query += " ORDER BY f.data_inicio ASC"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    ferias = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(ferias)

@app.route('/api/ferias', methods=['POST'])
@login_required
def api_agendar_ferias():
    data = request.json or {}
    usuario_id = data.get('usuario_id', session['usuario_id'])
    periodo_id = data.get('periodo_aquisitivo_id')
    parcelas = data.get('parcelas', [])
    observacoes = data.get('observacoes', '')

    if session.get('papel') != 'gestor' and int(usuario_id) != session['usuario_id']:
        return jsonify({'erro': 'Você só pode agendar suas próprias férias.'}), 403

    if not periodo_id or not parcelas:
        return jsonify({'erro': 'Período aquisitivo e parcelas são obrigatórios.'}), 400

    qtd_parcelas = len(parcelas)
    if qtd_parcelas not in [1, 2, 3]:
        return jsonify({'erro': 'O fracionamento deve ser em 1, 2 ou 3 períodos.'}), 400

    total_dias = sum(int(p.get('dias', 0)) for p in parcelas)
    if total_dias != 30:
        return jsonify({'erro': f'A soma dos dias das parcelas deve totalizar 30 dias. Atualmente soma {total_dias} dias.'}), 400

    # Validação da regra estadual de fracionamento:
    # Em 3 parcelas: nenhuma menor que 10 dias (portanto 10, 10, 10).
    # Em 2 parcelas: qualquer combinação (ex: 12 e 18, 15 e 15, 20 e 10, etc.)
    # Em 1 parcela: 30 dias.
    if qtd_parcelas == 3:
        for p in parcelas:
            d = int(p.get('dias', 0))
            if d < 10:
                return jsonify({'erro': 'Ao fracionar em 3 parcelas, nenhum período pode ter menos que 10 dias.'}), 400
    elif qtd_parcelas == 2:
        for p in parcelas:
            d = int(p.get('dias', 0))
            if d <= 0:
                return jsonify({'erro': 'Cada parcela deve conter no mínimo 1 dia.'}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Verificar se o período existe e pertence ao militar
    cursor.execute("SELECT id, total_dias, dias_utilizados FROM periodos_aquisitivos WHERE id = ? AND usuario_id = ?", (periodo_id, usuario_id))
    periodo = cursor.fetchone()
    if not periodo:
        conn.close()
        return jsonify({'erro': 'Período aquisitivo não encontrado para este militar.'}), 404

    # Limpar agendamentos anteriores deste período para recalcular/substituir se for reprogramação completa
    cursor.execute("DELETE FROM ferias_agendamentos WHERE periodo_aquisitivo_id = ?", (periodo_id,))

    # Inserir cada parcela
    novos_ids = []
    for idx, p in enumerate(parcelas, start=1):
        data_ini = p.get('data_inicio')
        dias = int(p.get('dias'))
        data_fim, data_retorno = calcular_datas(data_ini, dias)

        cursor.execute("""
        INSERT INTO ferias_agendamentos (
            usuario_id, periodo_aquisitivo_id, parcela, total_parcelas,
            data_inicio, dias, data_fim, data_retorno, status, observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'homologado', ?)
        """, (usuario_id, periodo_id, idx, qtd_parcelas, data_ini, dias, data_fim, data_retorno, observacoes))
        novos_ids.append(cursor.lastrowid)

    atualizar_saldo_periodo(conn, periodo_id)
    conn.close()

    return jsonify({'mensagem': 'Férias agendadas com sucesso!', 'ids': novos_ids})

# ================= Módulo de Reaprazamento =================

@app.route('/api/ferias/<int:ferias_id>/reaprazar', methods=['POST'])
@login_required
def api_reaprazar_ferias(ferias_id):
    data = request.json or {}
    nova_data_inicio = str(data.get('nova_data_inicio', '')).strip()
    novos_dias = data.get('novos_dias')
    motivo = str(data.get('motivo', '')).strip()

    if not nova_data_inicio:
        return jsonify({'erro': 'A nova data de início é obrigatória.'}), 400

    if not motivo:
        return jsonify({'erro': 'É obrigatório informar a justificativa/motivo do reaprazamento.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT f.*, u.nome_guerra 
    FROM ferias_agendamentos f 
    JOIN usuarios u ON f.usuario_id = u.id 
    WHERE f.id = ?
    """, (ferias_id,))
    ferias = cursor.fetchone()

    if not ferias:
        conn.close()
        return jsonify({'erro': 'Agendamento de férias não encontrado.'}), 404

    if session.get('papel') != 'gestor' and ferias['usuario_id'] != session['usuario_id']:
        conn.close()
        return jsonify({'erro': 'Você não tem permissão para reaprazar as férias de outro militar.'}), 403

    dias_efetivos = int(novos_dias) if novos_dias else ferias['dias']
    nova_data_fim, nova_data_retorno = calcular_datas(nova_data_inicio, dias_efetivos)

    # Inserir no histórico de reaprazamentos
    cursor.execute("""
    INSERT INTO reaprazamentos (
        ferias_id, usuario_id, 
        data_inicio_anterior, dias_anterior,
        data_inicio_nova, dias_novo, data_fim_nova, data_retorno_nova,
        motivo, homologado_por
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ferias_id, ferias['usuario_id'],
        ferias['data_inicio'], ferias['dias'],
        nova_data_inicio, dias_efetivos, nova_data_fim, nova_data_retorno,
        motivo, session.get('nome_guerra', 'Chefia')
    ))

    # Atualizar o agendamento de férias
    cursor.execute("""
    UPDATE ferias_agendamentos
    SET data_inicio = ?, dias = ?, data_fim = ?, data_retorno = ?, status = 'reaprazado', observacoes = ?
    WHERE id = ?
    """, (nova_data_inicio, dias_efetivos, nova_data_fim, nova_data_retorno, f"Reaprazado: {motivo}", ferias_id))

    atualizar_saldo_periodo(conn, ferias['periodo_aquisitivo_id'])
    conn.close()

    return jsonify({'mensagem': 'Reaprazamento registrado e efetivado com sucesso!'})

@app.route('/api/reaprazamentos', methods=['GET'])
@login_required
def api_listar_reaprazamentos():
    usuario_id = request.args.get('usuario_id')
    query = """
    SELECT r.*, 
           u.nome_guerra, u.nome_completo, u.matricula, u.posto_graduacao, u.setor_subunidade,
           f.parcela, f.total_parcelas
    FROM reaprazamentos r
    JOIN usuarios u ON r.usuario_id = u.id
    JOIN ferias_agendamentos f ON r.ferias_id = f.id
    """
    params = []
    if session.get('papel') != 'gestor' and not request.args.get('todos'):
        query += " WHERE r.usuario_id = ?"
        params.append(session['usuario_id'])
    elif usuario_id:
        query += " WHERE r.usuario_id = ?"
        params.append(usuario_id)

    query += " ORDER BY r.solicitado_em DESC"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    reaprazamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(reaprazamentos)

# ================= Calendário e Conflitos da Equipe =================

@app.route('/api/calendario/escala', methods=['GET'])
@login_required
def api_calendario_escala():
    mes = request.args.get('mes', str(dt.now().month))
    ano = request.args.get('ano', str(dt.now().year))
    setor = request.args.get('setor')

    try:
        mes_int = int(mes)
        ano_int = int(ano)
    except ValueError:
        return jsonify({'erro': 'Mês e ano inválidos.'}), 400

    conn = get_db()
    cursor = conn.cursor()

    query = """
    SELECT f.*, u.nome_guerra, u.nome_completo, u.matricula, u.posto_graduacao, u.setor_subunidade
    FROM ferias_agendamentos f
    JOIN usuarios u ON f.usuario_id = u.id
    WHERE f.status != 'cancelado'
    """
    params = []

    if setor:
        query += " AND u.setor_subunidade = ?"
        params.append(setor)

    cursor.execute(query, params)
    todos_agendamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # Mapear dias do mês com quem está de férias e detectar sobreposições no mesmo setor
    primeiro_dia_mes = dt(ano_int, mes_int, 1)
    if mes_int == 12:
        ultimo_dia_mes = dt(ano_int + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia_mes = dt(ano_int, mes_int + 1, 1) - timedelta(days=1)

    dias_calendario = {}
    total_dias_mes = (ultimo_dia_mes - primeiro_dia_mes).days + 1

    for dia_idx in range(1, total_dias_mes + 1):
        data_corrente = dt(ano_int, mes_int, dia_idx).strftime("%Y-%m-%d")
        dias_calendario[data_corrente] = {
            'data': data_corrente,
            'dia': dia_idx,
            'militares': [],
            'conflito_setor': False,
            'setores_conflito': []
        }

    for ag in todos_agendamentos:
        d_ini = dt.strptime(ag['data_inicio'], "%Y-%m-%d")
        d_fim = dt.strptime(ag['data_fim'], "%Y-%m-%d")

        dia_iter = d_ini
        while dia_iter <= d_fim:
            data_str = dia_iter.strftime("%Y-%m-%d")
            if data_str in dias_calendario:
                dias_calendario[data_str]['militares'].append({
                    'id': ag['id'],
                    'usuario_id': ag['usuario_id'],
                    'nome_guerra': ag['nome_guerra'],
                    'posto_graduacao': ag['posto_graduacao'],
                    'setor_subunidade': ag['setor_subunidade'],
                    'parcela': ag['parcela'],
                    'total_parcelas': ag['total_parcelas'],
                    'status': ag['status']
                })
            dia_iter += timedelta(days=1)

    # Identificar conflitos por setor (> 1 militar do mesmo setor de férias no mesmo dia)
    for data_str, info in dias_calendario.items():
        setor_contagem = {}
        for m in info['militares']:
            s = m['setor_subunidade']
            setor_contagem[s] = setor_contagem.get(s, 0) + 1
        conflitos = [s for s, count in setor_contagem.items() if count > 1]
        if conflitos:
            info['conflito_setor'] = True
            info['setores_conflito'] = conflitos

    return jsonify({
        'ano': ano_int,
        'mes': mes_int,
        'dias': list(dias_calendario.values()),
        'total_agendamentos': len(todos_agendamentos)
    })

# ================= Estatísticas e Indicadores =================

@app.route('/api/estatisticas', methods=['GET'])
@login_required
def api_estatisticas():
    conn = get_db()
    cursor = conn.cursor()

    hoje = dt.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ativo = 1")
    total_efetivo = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT usuario_id) FROM ferias_agendamentos 
    WHERE ? BETWEEN data_inicio AND data_fim AND status != 'cancelado'
    """, (hoje,))
    em_fruicao_hoje = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) FROM ferias_agendamentos 
    WHERE data_inicio > ? AND status != 'cancelado'
    """, (hoje,))
    previstas_futuras = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reaprazamentos")
    total_reaprazamentos = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'total_efetivo': total_efetivo,
        'em_fruicao_hoje': em_fruicao_hoje,
        'previstas_futuras': previstas_futuras,
        'total_reaprazamentos': total_reaprazamentos
    })

# ================= Rota Principal Front-end =================

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

if __name__ == '__main__':
    init_db()
    ip = get_local_ip()
    print("=" * 65)
    print(">>> CONTROLE DE FERIAS - CBMRN INICIADO COM SUCESSO! <<<")
    print(f"[*] Acesso Local:     http://localhost:5000")
    print(f"[*] Acesso na Rede:   http://{ip}:5000")
    print("[*] Login Padrao:     Matricula: admin  |  PIN: 193")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
