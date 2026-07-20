# Etapa 3 — Modelagem Lógica (Mapeamento Conceitual → Lógico)

Convenção: PK = chave primária, FK = chave estrangeira, NN = NOT NULL.

```
VETERINARIO (
    id_veterinario  INTEGER   PK
    nome            TEXT      NN
    crmv            TEXT      NN, UNIQUE
    telefone        TEXT
)

ANIMAL (
    id_animal       INTEGER   PK
    nome            TEXT      NN
    especie         TEXT      NN
    raca            TEXT
    porte           TEXT      NN   -- 'pequeno' | 'medio' | 'grande'
    sexo            TEXT      NN   -- 'M' | 'F'
    data_resgate    DATE      NN
    local_resgate   TEXT      NN
    status          TEXT      NN   -- 'resgatado' | 'em_tratamento' |
                                   -- 'disponivel' | 'em_lar_temporario' |
                                   -- 'adotado'
    obs_saude       TEXT
)

PRONTUARIO_MEDICO (
    id_prontuario     INTEGER   PK
    id_animal         INTEGER   FK -> ANIMAL.id_animal        NN
    id_veterinario    INTEGER   FK -> VETERINARIO.id_veterinario  NN
    data_atendimento  DATE      NN
    tipo              TEXT      NN  -- 'vacina'|'cirurgia'|'consulta'|'exame'
    descricao         TEXT      NN
    proxima_dose      DATE
)

LAR_TEMPORARIO (
    id_lar           INTEGER   PK
    nome_voluntario  TEXT      NN
    endereco         TEXT      NN
    telefone         TEXT      NN
    capacidade       INTEGER   NN
    ativo            INTEGER   NN  -- 0/1 (boolean)
)

ABRIGAMENTO (                       -- resolve N:M ANIMAL x LAR_TEMPORARIO
    id_abrigamento   INTEGER   PK
    id_animal        INTEGER   FK -> ANIMAL.id_animal          NN
    id_lar           INTEGER   FK -> LAR_TEMPORARIO.id_lar     NN
    data_entrada     DATE      NN
    data_saida       DATE
)

ADOTANTE (
    id_adotante   INTEGER   PK
    nome          TEXT      NN
    cpf           TEXT      NN, UNIQUE
    endereco      TEXT      NN
    telefone      TEXT      NN
    email         TEXT
)

VISITA (                            -- resolve N:M ANIMAL x ADOTANTE
    id_visita      INTEGER   PK
    id_adotante    INTEGER   FK -> ADOTANTE.id_adotante        NN
    id_animal      INTEGER   FK -> ANIMAL.id_animal            NN
    data_visita    DATE      NN
    observacoes    TEXT
    resultado      TEXT      NN  -- 'interessado'|'nao_interessado'|'pendente'
)

ADOCAO (                            -- resolve N:M ANIMAL x ADOTANTE
    id_adocao        INTEGER   PK
    id_animal        INTEGER   FK -> ANIMAL.id_animal          NN
    id_adotante      INTEGER   FK -> ADOTANTE.id_adotante      NN
    data_adocao      DATE      NN
    termo_assinado   INTEGER   NN  -- 0/1 (boolean)
    status           TEXT      NN  -- 'ativa' | 'devolvida'
)
```

## Regras de integridade adicionais
- `VETERINARIO.crmv` e `ADOTANTE.cpf`: únicos (UNIQUE).
- Todas as FKs com `ON DELETE RESTRICT` (não se apaga animal/adotante/lar/
  veterinário que possua registros associados), garantindo a integridade do
  histórico.
- Regra de negócio RN05 (um animal com no máximo uma adoção `ativa` por vez)
  é garantida por índice único parcial em `ADOCAO (id_animal)` para
  `status = 'ativa'`, implementado no script SQL da Etapa 4.

Esta modelagem lógica corresponde diretamente às tabelas criadas nos
*scripts* SQL da Etapa 4 (`sql/01_schema.sql`).
