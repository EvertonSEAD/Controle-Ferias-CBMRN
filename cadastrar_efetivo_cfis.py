import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'ferias_cbmrn.db')

def seed_cfis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Garantir que o admin existe
    cursor.execute("SELECT id FROM usuarios WHERE matricula = 'admin'")
    if not cursor.fetchone():
        admin_pin = generate_password_hash("193")
        cursor.execute("""
        INSERT INTO usuarios (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel)
        VALUES ('admin', 'Administrador Geral CBMRN', 'ADMIN RH', 'Capitão BM', 'Diretoria de Recursos Humanos (DRH)', ?, 'gestor')
        """, (admin_pin,))

    pin_padrao = generate_password_hash("193")

    efetivo = [
        {
            'matricula': '193010',
            'nome_completo': 'Daniel Santos de Farias',
            'nome_guerra': 'TC Daniel',
            'posto_graduacao': 'Tenente-Coronel BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'gestor',
            'turma': '7ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 1, 'data_inicio': '2026-07-01', 'dias': 30, 'data_fim': '2026-07-30', 'data_retorno': '2026-07-31', 'status': 'homologado', 'obs': '7ª Turma de Férias 2026'}
            ],
            'reaprazamentos': []
        },
        {
            'matricula': '193011',
            'nome_completo': 'Kaio Sueldo de Oliveira',
            'nome_guerra': 'Ten. Sueldo',
            'posto_graduacao': '1º Tenente BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '6ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 2, 'data_inicio': '2026-05-01', 'dias': 15, 'data_fim': '2026-05-15', 'data_retorno': '2026-05-16', 'status': 'homologado', 'obs': '1ª Parcela (Maio/2026)'},
                {'parcela': 2, 'total_parcelas': 2, 'data_inicio': '2026-11-16', 'dias': 15, 'data_fim': '2026-11-30', 'data_retorno': '2026-12-01', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada - Proc. SEI 088100860.01256/2025-10'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-05-16',
                    'dias_ant': 15,
                    'data_inicio_nova': '2026-11-16',
                    'dias_novo': 15,
                    'data_fim_nova': '2026-11-30',
                    'data_retorno_nova': '2026-12-01',
                    'motivo': 'Reaprazamento de 15 dias de férias para 16/11 a 30/11/2026 (SEI 088100860.01256/2025-10) e Licença Recompensa de 5 dias (09/11 a 13/11/2026 - SEI 08810142.001786/2026-19).'
                }
            ]
        },
        {
            'matricula': '193012',
            'nome_completo': 'Hudson Mendes Soares',
            'nome_guerra': '1º Sgt. Hudson',
            'posto_graduacao': '1º Sargento BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '2ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 1, 'data_inicio': '2026-01-05', 'dias': 30, 'data_fim': '2026-02-03', 'data_retorno': '2026-02-04', 'status': 'homologado', 'obs': '2ª Turma de Férias 2026'}
            ],
            'reaprazamentos': []
        },
        {
            'matricula': '193013',
            'nome_completo': 'Tiago Paulo da Silva Pimentel Gomes',
            'nome_guerra': 'Sgt. Pimentel',
            'posto_graduacao': '3º Sargento BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '6ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 3, 'data_inicio': '2026-02-18', 'dias': 10, 'data_fim': '2026-02-27', 'data_retorno': '2026-02-28', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (Fevereiro)'},
                {'parcela': 2, 'total_parcelas': 3, 'data_inicio': '2026-04-22', 'dias': 10, 'data_fim': '2026-05-01', 'data_retorno': '2026-05-02', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (Abril/Maio)'},
                {'parcela': 3, 'total_parcelas': 3, 'data_inicio': '2026-05-13', 'dias': 10, 'data_fim': '2026-05-22', 'data_retorno': '2026-05-23', 'status': 'reaprazado', 'obs': '3ª Parcela reaprazada (Maio)'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-06-01',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-02-18',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-02-27',
                    'data_retorno_nova': '2026-02-28',
                    'motivo': 'Reaprazamento da 1ª parcela de 10 dias para 18/02 a 27/02/2026 conforme necessidade do serviço e adequação de escala.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-06-11',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-04-22',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-05-01',
                    'data_retorno_nova': '2026-05-02',
                    'motivo': 'Reaprazamento da 2ª parcela de 10 dias para 22/04 a 01/05/2026 para atendimento à escala de fiscalização.'
                },
                {
                    'parcela_idx': 2,
                    'data_inicio_ant': '2026-06-21',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-05-13',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-05-22',
                    'data_retorno_nova': '2026-05-23',
                    'motivo': 'Reaprazamento da 3ª parcela de 10 dias para 13/05 a 22/05/2026 conforme planejamento setorial.'
                }
            ]
        },
        {
            'matricula': '193014',
            'nome_completo': 'Reinaldo Protazio Siqueira',
            'nome_guerra': 'Sgt. Protazio',
            'posto_graduacao': '3º Sargento BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '2ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 1, 'data_inicio': '2026-01-05', 'dias': 30, 'data_fim': '2026-02-03', 'data_retorno': '2026-02-04', 'status': 'homologado', 'obs': '2ª Turma de Férias 2026'}
            ],
            'reaprazamentos': []
        },
        {
            'matricula': '193015',
            'nome_completo': 'Rodrigo Francis Revorêdo',
            'nome_guerra': 'Cb. Revorêdo',
            'posto_graduacao': 'Cabo BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '3ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 2, 'data_inicio': '2026-07-08', 'dias': 20, 'data_fim': '2026-07-27', 'data_retorno': '2026-07-28', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (20 dias) - Proc. SEI 08810142.000181/2026-19'},
                {'parcela': 2, 'total_parcelas': 2, 'data_inicio': '2026-08-19', 'dias': 10, 'data_fim': '2026-08-28', 'data_retorno': '2026-08-29', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (10 dias) - Proc. SEI 08810142.000181/2026-19'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-02-23',
                    'dias_ant': 20,
                    'data_inicio_nova': '2026-07-08',
                    'dias_novo': 20,
                    'data_fim_nova': '2026-07-27',
                    'data_retorno_nova': '2026-07-28',
                    'motivo': 'Reaprazamento de 20 dias para 08/07 a 27/07/2026 conforme Processo SEI 08810142.000181/2026-19.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-03-15',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-08-19',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-08-28',
                    'data_retorno_nova': '2026-08-29',
                    'motivo': 'Reaprazamento de 10 dias para 19/08 a 28/08/2026 conforme Processo SEI 08810142.000181/2026-19.'
                }
            ]
        },
        {
            'matricula': '193016',
            'nome_completo': 'Hugo Felipe Pinheiro',
            'nome_guerra': 'Cb. F. Pinheiro',
            'posto_graduacao': 'Cabo BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '1ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 3, 'data_inicio': '2026-03-09', 'dias': 10, 'data_fim': '2026-03-18', 'data_retorno': '2026-03-19', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (Março/2026)'},
                {'parcela': 2, 'total_parcelas': 3, 'data_inicio': '2026-06-15', 'dias': 10, 'data_fim': '2026-06-24', 'data_retorno': '2026-06-25', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (Junho/2026)'},
                {'parcela': 3, 'total_parcelas': 3, 'data_inicio': '2026-09-21', 'dias': 10, 'data_fim': '2026-09-30', 'data_retorno': '2026-10-01', 'status': 'reaprazado', 'obs': '3ª Parcela reaprazada (Setembro/2026)'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2025-12-01',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-03-09',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-03-18',
                    'data_retorno_nova': '2026-03-19',
                    'motivo': 'Reaprazamento e fracionamento de férias do exercício anterior para 09/03 a 18/03/2026.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2025-12-11',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-06-15',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-06-24',
                    'data_retorno_nova': '2026-06-25',
                    'motivo': 'Reaprazamento da 2ª parcela para 15/06 a 24/06/2026.'
                },
                {
                    'parcela_idx': 2,
                    'data_inicio_ant': '2025-12-21',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-09-21',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-09-30',
                    'data_retorno_nova': '2026-10-01',
                    'motivo': 'Reaprazamento da 3ª parcela para 21/09 a 30/09/2026.'
                }
            ]
        },
        {
            'matricula': '193017',
            'nome_completo': 'Reinaldo Fernandes de Macedo',
            'nome_guerra': 'Cb. Macedo',
            'posto_graduacao': 'Cabo BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '2ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 2, 'data_inicio': '2026-07-01', 'dias': 20, 'data_fim': '2026-07-20', 'data_retorno': '2026-07-21', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (20 dias - Julho)'},
                {'parcela': 2, 'total_parcelas': 2, 'data_inicio': '2026-12-09', 'dias': 10, 'data_fim': '2026-12-18', 'data_retorno': '2026-12-19', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (10 dias - Dezembro)'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-01-05',
                    'dias_ant': 20,
                    'data_inicio_nova': '2026-07-01',
                    'dias_novo': 20,
                    'data_fim_nova': '2026-07-20',
                    'data_retorno_nova': '2026-07-21',
                    'motivo': 'Reaprazamento da 1ª parcela (20 dias) de janeiro para julho/2026.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-01-25',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-12-09',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-12-18',
                    'data_retorno_nova': '2026-12-19',
                    'motivo': 'Reaprazamento da 2ª parcela (10 dias) de janeiro para dezembro/2026.'
                }
            ]
        },
        {
            'matricula': '193018',
            'nome_completo': 'Saulo Erick Linhares de Queiroga',
            'nome_guerra': 'Sd. Queiroga',
            'posto_graduacao': 'Soldado BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '7ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 1, 'data_inicio': '2026-07-01', 'dias': 30, 'data_fim': '2026-07-30', 'data_retorno': '2026-07-31', 'status': 'homologado', 'obs': '7ª Turma de Férias 2026'}
            ],
            'reaprazamentos': []
        },
        {
            'matricula': '193019',
            'nome_completo': 'André Câmara de Brito',
            'nome_guerra': 'Sd. André Câmara',
            'posto_graduacao': 'Soldado BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '10ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 3, 'data_inicio': '2026-05-11', 'dias': 10, 'data_fim': '2026-05-20', 'data_retorno': '2026-05-21', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada - Proc. SEI 08810142.000536/2025-81'},
                {'parcela': 2, 'total_parcelas': 3, 'data_inicio': '2026-09-14', 'dias': 10, 'data_fim': '2026-09-23', 'data_retorno': '2026-09-24', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada - Proc. SEI 08810142.000536/2025-81'},
                {'parcela': 3, 'total_parcelas': 3, 'data_inicio': '2026-10-12', 'dias': 10, 'data_fim': '2026-10-21', 'data_retorno': '2026-10-22', 'status': 'homologado', 'obs': '3ª Parcela regulamentar (Outubro)'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-10-22',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-05-11',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-05-20',
                    'data_retorno_nova': '2026-05-21',
                    'motivo': 'Reaprazamento de 10 dias para 11/05 a 20/05/2026 conforme Processo SEI 08810142.000536/2025-81.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-11-01',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-09-14',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-09-23',
                    'data_retorno_nova': '2026-09-24',
                    'motivo': 'Reaprazamento de 10 dias para 14/09 a 23/09/2026 conforme Processo SEI 08810142.000536/2025-81.'
                }
            ]
        },
        {
            'matricula': '193020',
            'nome_completo': 'Ayran Magno de Andrade Lima',
            'nome_guerra': 'Sd. Ayran',
            'posto_graduacao': 'Soldado BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '9ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 1, 'data_inicio': '2026-09-09', 'dias': 30, 'data_fim': '2026-10-08', 'data_retorno': '2026-10-09', 'status': 'homologado', 'obs': '9ª Turma de Férias 2026'}
            ],
            'reaprazamentos': []
        },
        {
            'matricula': '193021',
            'nome_completo': 'Everton Pereira de Souza e Silva',
            'nome_guerra': 'Sd. Everton',
            'posto_graduacao': 'Soldado BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '8ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 3, 'data_inicio': '2026-08-24', 'dias': 10, 'data_fim': '2026-09-02', 'data_retorno': '2026-09-03', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (Agosto/2026)'},
                {'parcela': 2, 'total_parcelas': 3, 'data_inicio': '2027-01-11', 'dias': 10, 'data_fim': '2027-01-20', 'data_retorno': '2027-01-21', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (Janeiro/2027)'},
                {'parcela': 3, 'total_parcelas': 3, 'data_inicio': '2027-06-07', 'dias': 10, 'data_fim': '2027-06-16', 'data_retorno': '2027-06-17', 'status': 'reaprazado', 'obs': '3ª Parcela reaprazada (Junho/2027)'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-08-03',
                    'dias_ant': 10,
                    'data_inicio_nova': '2026-08-24',
                    'dias_novo': 10,
                    'data_fim_nova': '2026-09-02',
                    'data_retorno_nova': '2026-09-03',
                    'motivo': 'Reaprazamento da 1ª parcela de 10 dias para 24/08 a 02/09/2026.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-08-13',
                    'dias_ant': 10,
                    'data_inicio_nova': '2027-01-11',
                    'dias_novo': 10,
                    'data_fim_nova': '2027-01-20',
                    'data_retorno_nova': '2027-01-21',
                    'motivo': 'Reaprazamento da 2ª parcela de 10 dias para 11/01 a 20/01/2027.'
                },
                {
                    'parcela_idx': 2,
                    'data_inicio_ant': '2026-08-23',
                    'dias_ant': 10,
                    'data_inicio_nova': '2027-06-07',
                    'dias_novo': 10,
                    'data_fim_nova': '2027-06-16',
                    'data_retorno_nova': '2027-06-17',
                    'motivo': 'Reaprazamento da 3ª parcela de 10 dias para 07/06 a 16/06/2027.'
                }
            ]
        },
        {
            'matricula': '193022',
            'nome_completo': 'Jaedson Corcino da Silva',
            'nome_guerra': 'Sd. Corcino',
            'posto_graduacao': 'Soldado BM',
            'setor_subunidade': 'Centro de Fiscalização (CFIS)',
            'papel': 'militar',
            'turma': '6ª',
            'exercicio': '2025/2026',
            'parcelas': [
                {'parcela': 1, 'total_parcelas': 2, 'data_inicio': '2026-11-23', 'dias': 20, 'data_fim': '2026-12-12', 'data_retorno': '2026-12-13', 'status': 'reaprazado', 'obs': '1ª Parcela reaprazada (20 dias) - Proc. SEI 08810142.000765/2026-86'},
                {'parcela': 2, 'total_parcelas': 2, 'data_inicio': '2027-04-06', 'dias': 10, 'data_fim': '2027-04-15', 'data_retorno': '2027-04-17', 'status': 'reaprazado', 'obs': '2ª Parcela reaprazada (10 dias) + 1 dia compensação Desfile Cívico em 16/04/2027'}
            ],
            'reaprazamentos': [
                {
                    'parcela_idx': 0,
                    'data_inicio_ant': '2026-06-01',
                    'dias_ant': 20,
                    'data_inicio_nova': '2026-11-23',
                    'dias_novo': 20,
                    'data_fim_nova': '2026-12-12',
                    'data_retorno_nova': '2026-12-13',
                    'motivo': 'Reaprazamento de 20 dias para 23/11 a 12/12/2026 conforme Processo SEI 08810142.000765/2026-86.'
                },
                {
                    'parcela_idx': 1,
                    'data_inicio_ant': '2026-06-21',
                    'dias_ant': 10,
                    'data_inicio_nova': '2027-04-06',
                    'dias_novo': 10,
                    'data_fim_nova': '2027-04-15',
                    'data_retorno_nova': '2027-04-17',
                    'motivo': 'Reaprazamento de 10 dias para 06/04 a 15/04/2027 com compensação do Desfile Cívico em 16/04/2027 (Proc. SEI 08810142.000765/2026-86).'
                }
            ]
        }
    ]

    for m in efetivo:
        # Cadastrar ou atualizar usuario
        cursor.execute("SELECT id FROM usuarios WHERE matricula = ?", (m['matricula'],))
        row = cursor.fetchone()
        if row:
            usuario_id = row[0]
            cursor.execute("""
            UPDATE usuarios SET 
                nome_completo = ?, nome_guerra = ?, posto_graduacao = ?, setor_subunidade = ?, papel = ?
            WHERE id = ?
            """, (m['nome_completo'], m['nome_guerra'], m['posto_graduacao'], m['setor_subunidade'], m['papel'], usuario_id))
        else:
            cursor.execute("""
            INSERT INTO usuarios (matricula, nome_completo, nome_guerra, posto_graduacao, setor_subunidade, pin_hash, papel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (m['matricula'], m['nome_completo'], m['nome_guerra'], m['posto_graduacao'], m['setor_subunidade'], pin_padrao, m['papel']))
            usuario_id = cursor.lastrowid

        # Cadastrar período aquisitivo
        cursor.execute("SELECT id FROM periodos_aquisitivos WHERE usuario_id = ? AND exercicio = ?", (usuario_id, m['exercicio']))
        p_row = cursor.fetchone()
        if p_row:
            periodo_id = p_row[0]
        else:
            cursor.execute("""
            INSERT INTO periodos_aquisitivos (usuario_id, exercicio, total_dias, dias_utilizados)
            VALUES (?, ?, 30, 0)
            """, (usuario_id, m['exercicio']))
            periodo_id = cursor.lastrowid

        # Limpar agendamentos anteriores do período para recriar conforme o documento
        cursor.execute("DELETE FROM ferias_agendamentos WHERE periodo_aquisitivo_id = ?", (periodo_id,))

        # Inserir parcelas
        inserted_ids = []
        total_dias = 0
        for p in m['parcelas']:
            cursor.execute("""
            INSERT INTO ferias_agendamentos (
                usuario_id, periodo_aquisitivo_id, parcela, total_parcelas,
                data_inicio, dias, data_fim, data_retorno, status, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_id, periodo_id, p['parcela'], p['total_parcelas'],
                p['data_inicio'], p['dias'], p['data_fim'], p['data_retorno'],
                p['status'], p['obs']
            ))
            inserted_ids.append(cursor.lastrowid)
            total_dias += p['dias']

        # Atualizar saldo
        cursor.execute("UPDATE periodos_aquisitivos SET dias_utilizados = ? WHERE id = ?", (total_dias, periodo_id))

        # Inserir reaprazamentos históricos correspondentes
        for r in m['reaprazamentos']:
            ferias_id = inserted_ids[r['parcela_idx']]
            cursor.execute("""
            INSERT INTO reaprazamentos (
                ferias_id, usuario_id,
                data_inicio_anterior, dias_anterior,
                data_inicio_nova, dias_novo, data_fim_nova, data_retorno_nova,
                motivo, homologado_por
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ferias_id, usuario_id,
                r['data_inicio_ant'], r['dias_ant'],
                r['data_inicio_nova'], r['dias_novo'], r['data_fim_nova'], r['data_retorno_nova'],
                r['motivo'], 'Diretoria / Comando CFIS'
            ))

    conn.commit()
    conn.close()
    print("Sucesso: Todo o efetivo do Centro de Fiscalização (CFIS) 2026 cadastrado!")

if __name__ == '__main__':
    seed_cfis()
