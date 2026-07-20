# PetResgate — Sistema para ONG de Resgate e Adoção de Animais

Projeto prático das disciplinas CSI440/CSI602 — Banco de Dados (UFOP).

## Sobre

Sistema desktop, em **Python**, para apoiar o fluxo de uma ONG de resgate
animal: cadastro de animais resgatados, prontuário médico, lares
temporários, adotantes, visitas e adoções.

- **SGBD:** SQLite 3 (relacional)
- **Interface:** Tkinter (desktop)
- **Acesso ao banco:** exclusivamente via comandos **SQL puro**
  (`sqlite3`, biblioteca padrão do Python, usada apenas como *driver* de
  conexão) — **sem ORM, sem APIs, sem ferramentas de administração de
  SGBD.**

## Estrutura do repositório

```
.
├── docs/
│   ├── 01_problema_e_requisitos.md   (Etapa 1)
│   ├── 02_der.md + der_diagram.png   (Etapa 2 — DER, notação de Chen)
│   ├── gen_der.py                    (script que gera o diagrama)
│   └── 03_modelagem_logica.md        (Etapa 3 — mapeamento lógico)
├── sql/
│   ├── 01_schema.sql                 (Etapa 4 — DDL)
│   └── 02_seed.sql                   (Etapa 4 — povoamento inicial)
└── app/
    ├── db.py                         (Etapa 5 — toda a camada SQL)
    └── main.py                       (Etapa 5 — interface Tkinter)
```

## Como executar

Requisitos: Python 3.10+ com o módulo `tkinter` instalado (já vem por
padrão na instalação oficial do Python; em algumas distribuições Linux é
necessário `sudo apt install python3-tk`).

```bash
cd app
python3 main.py
```

Na primeira execução, o banco `petresgate.db` é criado automaticamente na
raiz do projeto a partir de `sql/01_schema.sql`, e já é populado com dados
de exemplo (`sql/02_seed.sql`).

Para recriar o banco do zero, basta apagar o arquivo `petresgate.db` e
executar novamente `python3 app/main.py`.

## Funcionalidades

- **Animais:** cadastro do animal resgatado e consulta filtrando por
  status e/ou nome.
- **Prontuários Médicos:** cadastro de veterinários e registro de
  atendimentos (vacina, cirurgia, consulta, exame) vinculados a um animal
  e a um veterinário; consulta do histórico completo.
- **Lares Temporários:** cadastro de voluntários/lares e registro do
  histórico de abrigamento de cada animal (entrada/saída).
- **Adotantes e Visitas:** cadastro de adotantes e registro das visitas
  realizadas antes da adoção.
- **Adoções:** formalização da adoção entre um adotante e um animal
  disponível, atualizando automaticamente o status do animal.
