import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

import db


# ------------------------------------------------------------------
# Utilidades de UI
# ------------------------------------------------------------------
def make_tree(parent, columns):
    tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="w")
    vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)
    return tree


def fill_tree(tree, rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=[row[c] for c in row.keys()])


def combo_from_query(rows, id_field, label_field):
    """Retorna (lista de labels, dict label->id) a partir de linhas do banco."""
    labels, mapping = [], {}
    for r in rows:
        label = f"{r[id_field]} - {r[label_field]}"
        labels.append(label)
        mapping[label] = r[id_field]
    return labels, mapping


# ------------------------------------------------------------------
# Aba: Animais
# ------------------------------------------------------------------
class AbaAnimais(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        form = ttk.LabelFrame(self, text="Cadastrar animal resgatado")
        form.pack(side="left", fill="y", padx=8, pady=8)

        self.vars = {}
        campos = [
            ("nome", "Nome"), ("especie", "Espécie"), ("raca", "Raça"),
            ("data_resgate", "Data resgate (AAAA-MM-DD)"),
            ("local_resgate", "Local do resgate"),
        ]
        for i, (key, label) in enumerate(campos):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=4, pady=3)
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=28).grid(row=i, column=1, padx=4, pady=3)
            self.vars[key] = var

        r = len(campos)
        ttk.Label(form, text="Porte").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        self.porte = ttk.Combobox(form, values=["pequeno", "medio", "grande"], width=25, state="readonly")
        self.porte.grid(row=r, column=1, padx=4, pady=3)
        r += 1

        ttk.Label(form, text="Sexo").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        self.sexo = ttk.Combobox(form, values=["M", "F"], width=25, state="readonly")
        self.sexo.grid(row=r, column=1, padx=4, pady=3)
        r += 1

        ttk.Label(form, text="Status inicial").grid(row=r, column=0, sticky="w", padx=4, pady=3)
        self.status = ttk.Combobox(form, values=["resgatado", "em_tratamento", "disponivel"],
                                    width=25, state="readonly")
        self.status.set("resgatado")
        self.status.grid(row=r, column=1, padx=4, pady=3)
        r += 1

        ttk.Label(form, text="Obs. saúde").grid(row=r, column=0, sticky="nw", padx=4, pady=3)
        self.obs = tk.Text(form, width=22, height=4)
        self.obs.grid(row=r, column=1, padx=4, pady=3)
        r += 1

        ttk.Button(form, text="Salvar", command=self.salvar).grid(row=r, column=0, columnspan=2, pady=10)

        # Consulta
        consulta = ttk.Frame(self)
        consulta.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        filtro_frame = ttk.Frame(consulta)
        filtro_frame.pack(fill="x")
        ttk.Label(filtro_frame, text="Filtrar por status:").pack(side="left")
        self.filtro_status = ttk.Combobox(
            filtro_frame,
            values=["", "resgatado", "em_tratamento", "disponivel", "em_lar_temporario", "adotado"],
            width=18, state="readonly")
        self.filtro_status.pack(side="left", padx=4)
        ttk.Label(filtro_frame, text="Nome:").pack(side="left", padx=(10, 0))
        self.filtro_nome = ttk.Entry(filtro_frame, width=16)
        self.filtro_nome.pack(side="left", padx=4)
        ttk.Button(filtro_frame, text="Consultar", command=self.consultar).pack(side="left", padx=8)

        tree_frame = ttk.Frame(consulta)
        tree_frame.pack(fill="both", expand=True, pady=6)
        cols = ("id_animal", "nome", "especie", "porte", "sexo", "data_resgate", "status")
        self.tree = make_tree(tree_frame, cols)

        self.consultar()

    def salvar(self):
        try:
            db.inserir_animal(
                self.vars["nome"].get(), self.vars["especie"].get(), self.vars["raca"].get(),
                self.porte.get(), self.sexo.get(), self.vars["data_resgate"].get(),
                self.vars["local_resgate"].get(), self.status.get(), self.obs.get("1.0", "end").strip())
            messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso.")
            self.consultar()
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def consultar(self):
        status = self.filtro_status.get() or None
        nome = self.filtro_nome.get() or None
        rows = db.listar_animais(status, nome)
        fill_tree(self.tree, [{k: r[k] for k in ("id_animal", "nome", "especie", "porte",
                                                   "sexo", "data_resgate", "status")} for r in rows])


# ------------------------------------------------------------------
# Aba: Veterinários e Prontuários
# ------------------------------------------------------------------
class AbaProntuarios(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.LabelFrame(self, text="Registrar prontuário médico")
        form.pack(side="left", fill="y", padx=8, pady=8)

        ttk.Label(form, text="Animal").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.animal_cb = ttk.Combobox(form, width=28, state="readonly")
        self.animal_cb.grid(row=0, column=1, padx=4, pady=3)

        ttk.Label(form, text="Veterinário").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.vet_cb = ttk.Combobox(form, width=28, state="readonly")
        self.vet_cb.grid(row=1, column=1, padx=4, pady=3)

        ttk.Label(form, text="Data (AAAA-MM-DD)").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.data_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.data_var, width=30).grid(row=2, column=1, padx=4, pady=3)

        ttk.Label(form, text="Tipo").grid(row=3, column=0, sticky="w", padx=4, pady=3)
        self.tipo_cb = ttk.Combobox(form, values=["vacina", "cirurgia", "consulta", "exame"],
                                     width=28, state="readonly")
        self.tipo_cb.grid(row=3, column=1, padx=4, pady=3)

        ttk.Label(form, text="Descrição").grid(row=4, column=0, sticky="nw", padx=4, pady=3)
        self.desc_txt = tk.Text(form, width=24, height=4)
        self.desc_txt.grid(row=4, column=1, padx=4, pady=3)

        ttk.Label(form, text="Próxima dose (opcional)").grid(row=5, column=0, sticky="w", padx=4, pady=3)
        self.prox_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.prox_var, width=30).grid(row=5, column=1, padx=4, pady=3)

        ttk.Button(form, text="Salvar", command=self.salvar).grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Separator(form, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(form, text="Cadastrar veterinário", font=("", 9, "bold")).grid(row=8, column=0, columnspan=2)
        self.vet_nome = tk.StringVar()
        self.vet_crmv = tk.StringVar()
        self.vet_tel = tk.StringVar()
        ttk.Label(form, text="Nome").grid(row=9, column=0, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.vet_nome, width=28).grid(row=9, column=1, padx=4)
        ttk.Label(form, text="CRMV").grid(row=10, column=0, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.vet_crmv, width=28).grid(row=10, column=1, padx=4)
        ttk.Label(form, text="Telefone").grid(row=11, column=0, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.vet_tel, width=28).grid(row=11, column=1, padx=4)
        ttk.Button(form, text="Salvar veterinário", command=self.salvar_vet).grid(
            row=12, column=0, columnspan=2, pady=6)

        consulta = ttk.Frame(self)
        consulta.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        ttk.Button(consulta, text="Atualizar lista", command=self.consultar).pack(anchor="w")
        tree_frame = ttk.Frame(consulta)
        tree_frame.pack(fill="both", expand=True, pady=6)
        cols = ("id_prontuario", "animal", "veterinario", "data_atendimento", "tipo", "descricao", "proxima_dose")
        self.tree = make_tree(tree_frame, cols)

        self.atualizar_combos()
        self.consultar()

    def atualizar_combos(self):
        animais = db.listar_animais_simples()
        self.animal_labels, self.animal_map = combo_from_query(animais, "id_animal", "nome")
        self.animal_cb["values"] = self.animal_labels

        vets = db.listar_veterinarios()
        self.vet_labels, self.vet_map = combo_from_query(vets, "id_veterinario", "nome")
        self.vet_cb["values"] = self.vet_labels

    def salvar(self):
        try:
            id_animal = self.animal_map[self.animal_cb.get()]
            id_vet = self.vet_map[self.vet_cb.get()]
            db.inserir_prontuario(
                id_animal, id_vet, self.data_var.get(), self.tipo_cb.get(),
                self.desc_txt.get("1.0", "end").strip(), self.prox_var.get() or None)
            messagebox.showinfo("Sucesso", "Prontuário registrado.")
            self.consultar()
        except KeyError:
            messagebox.showerror("Erro", "Selecione um animal e um veterinário válidos.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def salvar_vet(self):
        try:
            db.inserir_veterinario(self.vet_nome.get(), self.vet_crmv.get(), self.vet_tel.get())
            messagebox.showinfo("Sucesso", "Veterinário cadastrado.")
            self.atualizar_combos()
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def consultar(self):
        rows = db.listar_prontuarios()
        fill_tree(self.tree, rows)


# ------------------------------------------------------------------
# Aba: Lares temporários e Abrigamento
# ------------------------------------------------------------------
class AbaLares(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.LabelFrame(self, text="Cadastrar lar temporário")
        form.pack(side="left", fill="y", padx=8, pady=8)
        self.nome_v = tk.StringVar()
        self.end_v = tk.StringVar()
        self.tel_v = tk.StringVar()
        self.cap_v = tk.StringVar()
        for i, (label, var) in enumerate([("Nome do voluntário", self.nome_v), ("Endereço", self.end_v),
                                           ("Telefone", self.tel_v), ("Capacidade", self.cap_v)]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=4, pady=3)
            ttk.Entry(form, textvariable=var, width=26).grid(row=i, column=1, padx=4, pady=3)
        ttk.Button(form, text="Salvar lar", command=self.salvar_lar).grid(row=4, column=0, columnspan=2, pady=8)

        ttk.Separator(form, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(form, text="Registrar abrigamento", font=("", 9, "bold")).grid(row=6, column=0, columnspan=2)

        ttk.Label(form, text="Animal").grid(row=7, column=0, sticky="w", padx=4)
        self.animal_cb = ttk.Combobox(form, width=24, state="readonly")
        self.animal_cb.grid(row=7, column=1, padx=4)

        ttk.Label(form, text="Lar temporário").grid(row=8, column=0, sticky="w", padx=4)
        self.lar_cb = ttk.Combobox(form, width=24, state="readonly")
        self.lar_cb.grid(row=8, column=1, padx=4)

        ttk.Label(form, text="Data entrada (AAAA-MM-DD)").grid(row=9, column=0, sticky="w", padx=4)
        self.ent_v = tk.StringVar()
        ttk.Entry(form, textvariable=self.ent_v, width=26).grid(row=9, column=1, padx=4)

        ttk.Label(form, text="Data saída (opcional)").grid(row=10, column=0, sticky="w", padx=4)
        self.sai_v = tk.StringVar()
        ttk.Entry(form, textvariable=self.sai_v, width=26).grid(row=10, column=1, padx=4)

        ttk.Button(form, text="Salvar abrigamento", command=self.salvar_abrigamento).grid(
            row=11, column=0, columnspan=2, pady=8)

        consulta = ttk.Frame(self)
        consulta.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        ttk.Button(consulta, text="Atualizar lista de abrigamentos", command=self.consultar).pack(anchor="w")
        tree_frame = ttk.Frame(consulta)
        tree_frame.pack(fill="both", expand=True, pady=6)
        cols = ("id_abrigamento", "animal", "lar", "data_entrada", "data_saida")
        self.tree = make_tree(tree_frame, cols)

        self.atualizar_combos()
        self.consultar()

    def atualizar_combos(self):
        animais = db.listar_animais_simples()
        self.animal_labels, self.animal_map = combo_from_query(animais, "id_animal", "nome")
        self.animal_cb["values"] = self.animal_labels

        lares = db.listar_lares()
        self.lar_labels, self.lar_map = combo_from_query(lares, "id_lar", "nome_voluntario")
        self.lar_cb["values"] = self.lar_labels

    def salvar_lar(self):
        try:
            db.inserir_lar(self.nome_v.get(), self.end_v.get(), self.tel_v.get(),
                            int(self.cap_v.get()), 1)
            messagebox.showinfo("Sucesso", "Lar temporário cadastrado.")
            self.atualizar_combos()
        except (sqlite3.Error, ValueError) as e:
            messagebox.showerror("Erro", str(e))

    def salvar_abrigamento(self):
        try:
            id_animal = self.animal_map[self.animal_cb.get()]
            id_lar = self.lar_map[self.lar_cb.get()]
            db.inserir_abrigamento(id_animal, id_lar, self.ent_v.get(), self.sai_v.get())
            messagebox.showinfo("Sucesso", "Abrigamento registrado.")
            self.consultar()
        except KeyError:
            messagebox.showerror("Erro", "Selecione um animal e um lar válidos.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def consultar(self):
        rows = db.listar_abrigamentos()
        fill_tree(self.tree, rows)


# ------------------------------------------------------------------
# Aba: Adotantes e Visitas
# ------------------------------------------------------------------
class AbaAdotantesVisitas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.LabelFrame(self, text="Cadastrar adotante")
        form.pack(side="left", fill="y", padx=8, pady=8)
        self.nome_v = tk.StringVar()
        self.cpf_v = tk.StringVar()
        self.end_v = tk.StringVar()
        self.tel_v = tk.StringVar()
        self.email_v = tk.StringVar()
        for i, (label, var) in enumerate([("Nome", self.nome_v), ("CPF", self.cpf_v),
                                           ("Endereço", self.end_v), ("Telefone", self.tel_v),
                                           ("E-mail", self.email_v)]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=4, pady=3)
            ttk.Entry(form, textvariable=var, width=26).grid(row=i, column=1, padx=4, pady=3)
        ttk.Button(form, text="Salvar adotante", command=self.salvar_adotante).grid(
            row=5, column=0, columnspan=2, pady=8)

        ttk.Separator(form, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(form, text="Registrar visita", font=("", 9, "bold")).grid(row=7, column=0, columnspan=2)

        ttk.Label(form, text="Adotante").grid(row=8, column=0, sticky="w", padx=4)
        self.adotante_cb = ttk.Combobox(form, width=24, state="readonly")
        self.adotante_cb.grid(row=8, column=1, padx=4)

        ttk.Label(form, text="Animal").grid(row=9, column=0, sticky="w", padx=4)
        self.animal_cb = ttk.Combobox(form, width=24, state="readonly")
        self.animal_cb.grid(row=9, column=1, padx=4)

        ttk.Label(form, text="Data visita (AAAA-MM-DD)").grid(row=10, column=0, sticky="w", padx=4)
        self.data_v = tk.StringVar()
        ttk.Entry(form, textvariable=self.data_v, width=26).grid(row=10, column=1, padx=4)

        ttk.Label(form, text="Resultado").grid(row=11, column=0, sticky="w", padx=4)
        self.resultado_cb = ttk.Combobox(form, values=["interessado", "nao_interessado", "pendente"],
                                          width=24, state="readonly")
        self.resultado_cb.set("pendente")
        self.resultado_cb.grid(row=11, column=1, padx=4)

        ttk.Label(form, text="Observações").grid(row=12, column=0, sticky="nw", padx=4)
        self.obs_txt = tk.Text(form, width=22, height=3)
        self.obs_txt.grid(row=12, column=1, padx=4, pady=3)

        ttk.Button(form, text="Salvar visita", command=self.salvar_visita).grid(
            row=13, column=0, columnspan=2, pady=8)

        consulta = ttk.Frame(self)
        consulta.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        ttk.Button(consulta, text="Atualizar lista de visitas", command=self.consultar).pack(anchor="w")
        tree_frame = ttk.Frame(consulta)
        tree_frame.pack(fill="both", expand=True, pady=6)
        cols = ("id_visita", "adotante", "animal", "data_visita", "observacoes", "resultado")
        self.tree = make_tree(tree_frame, cols)

        self.atualizar_combos()
        self.consultar()

    def atualizar_combos(self):
        adotantes = db.listar_adotantes()
        self.adotante_labels, self.adotante_map = combo_from_query(adotantes, "id_adotante", "nome")
        self.adotante_cb["values"] = self.adotante_labels

        animais = db.listar_animais_simples()
        self.animal_labels, self.animal_map = combo_from_query(animais, "id_animal", "nome")
        self.animal_cb["values"] = self.animal_labels

    def salvar_adotante(self):
        try:
            db.inserir_adotante(self.nome_v.get(), self.cpf_v.get(), self.end_v.get(),
                                 self.tel_v.get(), self.email_v.get())
            messagebox.showinfo("Sucesso", "Adotante cadastrado.")
            self.atualizar_combos()
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def salvar_visita(self):
        try:
            id_adotante = self.adotante_map[self.adotante_cb.get()]
            id_animal = self.animal_map[self.animal_cb.get()]
            db.inserir_visita(id_adotante, id_animal, self.data_v.get(),
                               self.obs_txt.get("1.0", "end").strip(), self.resultado_cb.get())
            messagebox.showinfo("Sucesso", "Visita registrada.")
            self.consultar()
        except KeyError:
            messagebox.showerror("Erro", "Selecione um adotante e um animal válidos.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def consultar(self):
        rows = db.listar_visitas()
        fill_tree(self.tree, rows)


# ------------------------------------------------------------------
# Aba: Adoções
# ------------------------------------------------------------------
class AbaAdocoes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.LabelFrame(self, text="Registrar adoção")
        form.pack(side="left", fill="y", padx=8, pady=8)

        ttk.Label(form, text="Animal (disponível)").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.animal_cb = ttk.Combobox(form, width=26, state="readonly")
        self.animal_cb.grid(row=0, column=1, padx=4, pady=3)

        ttk.Label(form, text="Adotante").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.adotante_cb = ttk.Combobox(form, width=26, state="readonly")
        self.adotante_cb.grid(row=1, column=1, padx=4, pady=3)

        ttk.Label(form, text="Data adoção (AAAA-MM-DD)").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.data_v = tk.StringVar()
        ttk.Entry(form, textvariable=self.data_v, width=28).grid(row=2, column=1, padx=4, pady=3)

        self.termo_v = tk.BooleanVar()
        ttk.Checkbutton(form, text="Termo de responsabilidade assinado",
                         variable=self.termo_v).grid(row=3, column=0, columnspan=2, pady=4)

        ttk.Button(form, text="Confirmar adoção", command=self.salvar).grid(
            row=4, column=0, columnspan=2, pady=10)

        consulta = ttk.Frame(self)
        consulta.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        ttk.Button(consulta, text="Atualizar lista de adoções", command=self.consultar).pack(anchor="w")
        tree_frame = ttk.Frame(consulta)
        tree_frame.pack(fill="both", expand=True, pady=6)
        cols = ("id_adocao", "animal", "adotante", "data_adocao", "termo_assinado", "status")
        self.tree = make_tree(tree_frame, cols)

        self.atualizar_combos()
        self.consultar()

    def atualizar_combos(self):
        # Apenas animais disponíveis podem ser adotados
        animais = db.listar_animais(filtro_status="disponivel")
        self.animal_labels, self.animal_map = combo_from_query(animais, "id_animal", "nome")
        self.animal_cb["values"] = self.animal_labels

        adotantes = db.listar_adotantes()
        self.adotante_labels, self.adotante_map = combo_from_query(adotantes, "id_adotante", "nome")
        self.adotante_cb["values"] = self.adotante_labels

    def salvar(self):
        try:
            id_animal = self.animal_map[self.animal_cb.get()]
            id_adotante = self.adotante_map[self.adotante_cb.get()]
            db.inserir_adocao(id_animal, id_adotante, self.data_v.get(), int(self.termo_v.get()))
            messagebox.showinfo("Sucesso", "Adoção registrada com sucesso!")
            self.atualizar_combos()
            self.consultar()
        except KeyError:
            messagebox.showerror("Erro", "Selecione um animal e um adotante válidos.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def consultar(self):
        rows = db.listar_adocoes()
        fill_tree(self.tree, rows)


# ------------------------------------------------------------------
# Janela principal
# ------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PetResgate — Sistema para ONG de Resgate e Adoção de Animais")
        self.geometry("980x560")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        notebook.add(AbaAnimais(notebook), text="Animais")
        notebook.add(AbaProntuarios(notebook), text="Prontuários Médicos")
        notebook.add(AbaLares(notebook), text="Lares Temporários")
        notebook.add(AbaAdotantesVisitas(notebook), text="Adotantes e Visitas")
        notebook.add(AbaAdocoes(notebook), text="Adoções")


if __name__ == "__main__":
    db.init_db(seed=True)
    App().mainloop()
