-- ============================================================
-- PetResgate - Script de povoamento inicial (DML)
-- ============================================================

INSERT INTO VETERINARIO (nome, crmv, telefone) VALUES
    ('Dra. Marina Souza', 'CRMV-MG 12345', '(31) 99111-2233'),
    ('Dr. Rafael Lima',   'CRMV-MG 54321', '(31) 99222-3344');

INSERT INTO ANIMAL (nome, especie, raca, porte, sexo, data_resgate, local_resgate, status, obs_saude) VALUES
    ('Bidu',    'Cachorro', 'SRD',        'medio',   'M', '2026-05-10', 'Rua das Flores, 120', 'disponivel',       'Desnutrido, em recuperação'),
    ('Mimi',    'Gato',     'Siamês',     'pequeno', 'F', '2026-05-15', 'Praça Central',        'em_tratamento',    'Fratura na pata traseira'),
    ('Thor',    'Cachorro', 'Pastor SRD', 'grande',  'M', '2026-06-01', 'BR-262, km 45',        'em_lar_temporario','Saudável após vacinação'),
    ('Luna',    'Gato',     'SRD',        'pequeno', 'F', '2026-06-10', 'Beco da Esperança',    'disponivel',       'Saudável'),
    ('Toby',    'Cachorro', 'Vira-lata',  'pequeno', 'M', '2026-04-20', 'Av. Brasil, 900',      'adotado',          'Recuperado, castrado');

INSERT INTO PRONTUARIO_MEDICO (id_animal, id_veterinario, data_atendimento, tipo, descricao, proxima_dose) VALUES
    (1, 1, '2026-05-11', 'consulta', 'Avaliação inicial pós-resgate', NULL),
    (1, 1, '2026-05-20', 'vacina',   'V10 - primeira dose', '2026-06-20'),
    (2, 2, '2026-05-16', 'cirurgia', 'Cirurgia ortopédica na pata traseira', NULL),
    (3, 1, '2026-06-02', 'vacina',   'Antirrábica', '2027-06-02'),
    (5, 2, '2026-04-25', 'cirurgia', 'Castração', NULL);

INSERT INTO LAR_TEMPORARIO (nome_voluntario, endereco, telefone, capacidade, ativo) VALUES
    ('Ana Paula Ferreira', 'Rua dos Lírios, 45',   '(31) 99333-4455', 2, 1),
    ('Carlos Eduardo',     'Rua das Palmeiras, 78', '(31) 99444-5566', 3, 1);

INSERT INTO ABRIGAMENTO (id_animal, id_lar, data_entrada, data_saida) VALUES
    (3, 1, '2026-06-05', NULL),
    (5, 2, '2026-04-27', '2026-05-30');

INSERT INTO ADOTANTE (nome, cpf, endereco, telefone, email) VALUES
    ('Juliana Alves',   '111.111.111-11', 'Rua A, 10',  '(31) 98888-1111', 'juliana@example.com'),
    ('Pedro Henrique',  '222.222.222-22', 'Rua B, 20',  '(31) 98888-2222', 'pedro@example.com');

INSERT INTO VISITA (id_adotante, id_animal, data_visita, observacoes, resultado) VALUES
    (1, 1, '2026-06-20', 'Gostou muito do Bidu, quer voltar com a família', 'interessado'),
    (2, 4, '2026-06-22', 'Ainda em dúvida sobre ter um gato em apartamento', 'pendente'),
    (1, 5, '2026-04-28', 'Visita antes da adoção do Toby', 'interessado');

INSERT INTO ADOCAO (id_animal, id_adotante, data_adocao, termo_assinado, status) VALUES
    (5, 1, '2026-05-02', 1, 'ativa');
