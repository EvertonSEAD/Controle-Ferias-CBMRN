import sqlite3

conn = sqlite3.connect('ferias_cbmrn.db')
c = conn.cursor()

c.execute("SELECT count(*) FROM usuarios WHERE setor_subunidade LIKE '%Fiscaliza%'")
print('Militares CFIS cadastrados:', c.fetchone()[0])

c.execute("SELECT count(*) FROM ferias_agendamentos")
print('Total parcelas de ferias cadastradas:', c.fetchone()[0])

c.execute("SELECT count(*) FROM reaprazamentos")
print('Total reaprazamentos cadastrados:', c.fetchone()[0])

print('\n--- Lista de Militares do Centro de Fiscalizacao 2026 ---')
c.execute("SELECT matricula, posto_graduacao, nome_guerra, setor_subunidade FROM usuarios WHERE setor_subunidade LIKE '%Fiscaliza%' ORDER BY matricula")
for r in c.fetchall():
    print(f"Matricula: {r[0]} | {r[1]} {r[2]} | {r[3]}")

print('\n--- Amostra de Reaprazamentos Auditados do Documento ---')
c.execute("SELECT u.nome_guerra, r.data_inicio_anterior, r.data_inicio_nova, r.motivo FROM reaprazamentos r JOIN usuarios u ON r.usuario_id = u.id")
for r in c.fetchall():
    print(f"Militar: {r[0]:15} | De {r[1]} para {r[2]} | Motivo: {r[3][:70]}...")

conn.close()
