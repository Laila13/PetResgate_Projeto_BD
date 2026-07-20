import graphviz

g = graphviz.Digraph('DER', format='png')
g.attr(rankdir='LR', splines='true', fontsize='10')
g.attr('node', fontname='Helvetica', fontsize='10')
g.attr('edge', fontname='Helvetica', fontsize='9')

ENT = dict(shape='box', style='filled', fillcolor='#EAF2FB', color='#2C5F8A', fontname='Helvetica-Bold')
REL = dict(shape='diamond', style='filled', fillcolor='#FCE9D8', color='#B5651D')
ATT = dict(shape='ellipse', style='filled', fillcolor='#F5F5F5', color='#777777')
KEY = dict(shape='ellipse', style='filled', fillcolor='#F5F5F5', color='#777777', fontname='Helvetica-Bold, underline')

def entity(name, label):
    g.node(name, label, **ENT)

def attr(node_id, ent, label, key=False):
    g.node(node_id, label, **(KEY if key else ATT))
    g.edge(ent, node_id, arrowhead='none')

def rel(name, label):
    g.node(name, label, **REL)

def link(a, b, label):
    g.edge(a, b, label=label, arrowhead='none')

# Entidades principais
entity('ANIMAL', 'ANIMAL')
attr('a_id', 'ANIMAL', 'id_animal', key=True)
attr('a_nome', 'ANIMAL', 'nome')
attr('a_especie', 'ANIMAL', 'especie')
attr('a_porte', 'ANIMAL', 'porte')
attr('a_status', 'ANIMAL', 'status')

entity('VETERINARIO', 'VETERINARIO')
attr('v_id', 'VETERINARIO', 'id_veterinario', key=True)
attr('v_crmv', 'VETERINARIO', 'crmv')
attr('v_nome', 'VETERINARIO', 'nome')

entity('LAR_TEMPORARIO', 'LAR_TEMPORARIO')
attr('l_id', 'LAR_TEMPORARIO', 'id_lar', key=True)
attr('l_volunt', 'LAR_TEMPORARIO', 'nome_voluntario')
attr('l_cap', 'LAR_TEMPORARIO', 'capacidade')

entity('ADOTANTE', 'ADOTANTE')
attr('ad_id', 'ADOTANTE', 'id_adotante', key=True)
attr('ad_cpf', 'ADOTANTE', 'cpf')
attr('ad_nome', 'ADOTANTE', 'nome')

# Entidades associativas (registram histórico / N:M com atributos)
entity('PRONTUARIO', 'PRONTUARIO_\nMEDICO')
attr('p_id', 'PRONTUARIO', 'id_prontuario', key=True)
attr('p_tipo', 'PRONTUARIO', 'tipo')
attr('p_data', 'PRONTUARIO', 'data_atendimento')

entity('ABRIGAMENTO', 'ABRIGAMENTO')
attr('ab_id', 'ABRIGAMENTO', 'id_abrigamento', key=True)
attr('ab_ent', 'ABRIGAMENTO', 'data_entrada')
attr('ab_sai', 'ABRIGAMENTO', 'data_saida')

entity('VISITA', 'VISITA')
attr('vi_id', 'VISITA', 'id_visita', key=True)
attr('vi_data', 'VISITA', 'data_visita')
attr('vi_res', 'VISITA', 'resultado')

entity('ADOCAO', 'ADOCAO')
attr('do_id', 'ADOCAO', 'id_adocao', key=True)
attr('do_data', 'ADOCAO', 'data_adocao')
attr('do_status', 'ADOCAO', 'status')

# Relacionamentos
rel('R1', 'possui')
link('ANIMAL', 'R1', '1')
link('R1', 'PRONTUARIO', 'N')

rel('R2', 'responsavel_por')
link('VETERINARIO', 'R2', '1')
link('R2', 'PRONTUARIO', 'N')

rel('R3', 'e_abrigado')
link('ANIMAL', 'R3', '1')
link('R3', 'ABRIGAMENTO', 'N')

rel('R4', 'acolhe')
link('LAR_TEMPORARIO', 'R4', '1')
link('R4', 'ABRIGAMENTO', 'N')

rel('R5', 'e_visitado')
link('ANIMAL', 'R5', '1')
link('R5', 'VISITA', 'N')

rel('R6', 'realiza_visita')
link('ADOTANTE', 'R6', '1')
link('R6', 'VISITA', 'N')

rel('R7', 'e_adotado')
link('ANIMAL', 'R7', '1')
link('R7', 'ADOCAO', 'N')

rel('R8', 'adota')
link('ADOTANTE', 'R8', '1')
link('R8', 'ADOCAO', 'N')

g.render('der_diagram', cleanup=True)
print("ok")
