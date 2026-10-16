# 🚒 Controle de Férias — CBMRN (Corpo de Bombeiros Militar do RN)

Sistema web para gestão, agendamento, fracionamento e reaprazamento de férias regulamentares do efetivo do **Corpo de Bombeiros Militar do Estado do Rio Grande do Norte (CBMRN)**.

---

## 🚀 Como Iniciar o Sistema (1 Clique)

1. Dê um duplo clique no arquivo **`iniciar_ferias.bat`**.
2. O servidor iniciará automaticamente em Python e abrirá o painel no seu navegador padrão em:
   * **Acesso Local (seu PC):** `http://localhost:5000`
   * **Acesso na Rede Interna / Wi-Fi da Unidade:** `http://10.103.0.113:5000` *(ou o IP informado na barra superior do sistema)*

---

## 📋 Efetivo Cadastrado — Centro de Fiscalização 2026 (SEI 08810142.000019/2025-10)

Todos os militares do requerimento oficial de férias de 2026 foram cadastrados com suas turmas, agendamentos e reaprazamentos:

| Matrícula | Posto/Graduação | Nome Completo | Turma | Situação / Reaprazamento | PIN Padrão |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`admin`** | Capitão BM | Administrador Geral CBMRN | - | Gestor Geral / RH | `193` |
| **`193010`** | TC BM | Daniel Santos de Farias | 7ª | 30 dias em Julho (01/07 a 30/07/26) | `193` |
| **`193011`** | 1º Ten. BM | Kaio Sueldo de Oliveira | 6ª | Reaprazado (15d Maio / 15d Nov + Licença) | `193` |
| **`193012`** | 1º Sgt. BM | Hudson Mendes Soares | 2ª | 30 dias em Janeiro (05/01 a 03/02/26) | `193` |
| **`193013`** | 3º Sgt. BM | Tiago Paulo da Silva Pimentel Gomes | 6ª | Fracionado 3x 10d (Fev, Abr e Mai/26) | `193` |
| **`193014`** | 3º Sgt. BM | Reinaldo Protazio Siqueira | 2ª | 30 dias em Janeiro (05/01 a 03/02/26) | `193` |
| **`193015`** | Cb. BM | Rodrigo Francis Revorêdo | 3ª | Reaprazado 20d (Jul) e 10d (Ago) - Proc. SEI | `193` |
| **`193016`** | Cb. BM | Hugo Felipe Pinheiro | 1ª | Fracionado 3x 10d (Mar, Jun e Set/26) | `193` |
| **`193017`** | Cb. BM | Reinaldo Fernandes de Macedo | 2ª | Reaprazado 20d (Jul) e 10d (Dez) | `193` |
| **`193018`** | Sd. BM | Saulo Erick Linhares de Queiroga | 7ª | 30 dias em Julho (01/07 a 30/07/26) | `193` |
| **`193019`** | Sd. BM | André Câmara de Brito | 10ª | Fracionado 3x 10d (Mai, Set e Out) - Proc. SEI | `193` |
| **`193020`** | Sd. BM | Ayran Magno de Andrade Lima | 9ª | 30 dias em Setembro (09/09 a 08/10/26) | `193` |
| **`193021`** | Sd. BM | Everton Pereira de Souza e Silva | 8ª | Fracionado 3x 10d (Ago/26, Jan/27 e Jun/27) | `193` |
| **`193022`** | Sd. BM | Jaedson Corcino da Silva | 6ª | Reaprazado 20d (Nov/26) e 10d (Abr/27) + Desfile | `193` |

> Qualquer militar pode alterar seu PIN individual no ícone de cadeado no topo da página.

---

## ⚖️ Regras de Fracionamento de Férias (Militares Estaduais do RN)

* **Direito Anual:** 30 dias corridos por exercício/período aquisitivo.
* **1 Período:** 30 dias integrais.
* **2 Períodos:** Fracionamento flexível somando 30 dias (ex: 20 e 10, 15 e 15, 12 e 18, 11 e 19 dias).
* **3 Períodos:** Nenhum período pode ser inferior a 10 dias (10 + 10 + 10 dias).
* **Cálculo Automático:** Ao selecionar a data de início e os dias, o sistema calcula automaticamente a **data de término** e o **dia de retorno ao serviço**.
