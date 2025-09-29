import flet as ft

class AppToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.configurar_pagina()
        from database import DataBase  # Certifique-se de que existe um arquivo database.py com a classe DataBase
        self.banco_dados = DataBase()
        self.usuario = None
        self.verificar_usuario()

    def configurar_pagina(self):
        #configurar as propriedaded iniciais da pagina
        self.page.title = 'Aplicativo ToDo'
        self.page.window_width = 400
        self.page.window_height = 750
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.theme_mode = ft.ThemeMode.DARK # define o tema escuro
        self.page.padding = 20
        self.definir_cores()

    def definir_cores(self):
        # Define o esquema de cores para o modo escuro
        self.cor = {
            'primaria': '#3498db',
            'secundaria': '#2ecc71',
            'fundo': '#121212',
            'texto': '#ffffff',
            'texto_secundario': '#b3b3b3',
            'destaque': '#e74c3c',
            'item_fundo': '#1e1e1e',
            'borda': '#333333',
            'checkbox': '#3498db',
            'botao': '#3498db'
        }

    def verificar_usuario(self):
        # verifica se o usuario ja foi definido, caso contrario pede o nome
        if self.usuario is None:
            self.pedir_nome_usuario()
        else:
            self.main()

    def pedir_nome_usuario(self):
        # Cria e exibe o formulário para o usuário inserir seu nome
        def salvar_usuario(e):
            self.usuario = campo_usuario.value if campo_usuario.value else "Usuário"
            self.page.controls.clear()
            self.main()

        campo_usuario = ft.TextField(
            label="Digite seu nome",
            border_color=self.cor['primaria'],
            focused_border_color=self.cor['secundaria'],
            text_style=ft.TextStyle(color=self.cor['texto']),
            bgcolor=self.cor['item_fundo'],
            border_radius=8,
        )

        botao_confirmar = ft.ElevatedButton(
            text="Confirmar",
            on_click=salvar_usuario,
            style=ft.ButtonStyle(
                color=self.cor['texto'],
                bgcolor=self.cor['botao'],
                shape=ft.RoundedRectangleBorder(radius=8),
            )
        )

        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Digite seu nome", color=self.cor['texto'], size=18),
                    campo_usuario,
                    botao_confirmar
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=20,
                bgcolor=self.cor['fundo'],
            )
        )
        
        
    def main(self):
        #configura e exibe a interface principal do plicativo
        self.page.bgcolor = self.cor['fundo']
        self.page.add(
            self.criar_cabeçalho(),
            self.criar_secao_entrada(),
            self.criar_abas(),
            self.criar_lista_tarefas(),

        ) 

    def criar_cabeçalho(self):
        #cria o cabeçalho com saudaçao ao usuario
        return ft.Container(
            content=ft.Column([
                ft.Text(f'Olá {self.usuario} 😊', size=24, color=self.cor['texto'], weight=ft.FontWeight.BOLD),
                ft.Text('Gerencie suas tarefas diarias', size=16, color=self.cor['texto_secundario'])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            padding=ft.padding.symmetric(vertical=20)
        )
    def criar_secao_entrada(self):
        #cria a secao de entrada para adicionar novas tarefas
        self.entrada_tarefa = ft.TextField(
            hint_text='adcione uma nova tarefa...',
            expand=True,
            border_color=self.cor['borda'],
            focused_border_color=self.cor['primaria'],
            text_style=ft.TextStyle(color=self.cor['texto']),
            hint_style=ft.TextStyle(color=self.cor['texto_secundario']),
            bgcolor=self.cor['item_fundo'],
            border_radius=8,
        )

        botao_adicionar = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE,
            icon_color=self.cor['botao'],
            icon_size=30,
            on_click=self.adicionar_tarefa,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                bgcolor=self.cor['item_fundo'],
            )
        )

        return ft.Container(
            content=ft.Row([self.entrada_tarefa, botao_adicionar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
            bgcolor=self.cor['item_fundo'],
            border_radius=8,

        )
    
    def criar_abas(self):
        #cria abas para filtrar as tartefas (todas, pendentes, conluidas)
        self.abas = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Todas", icon=ft.icons.LIST),
                ft.Tab(text="Pendentes", icon=ft.icons.PENDING_ACTIONS),
                ft.Tab(text="Concluídas", icon=ft.icons.TASK_ALT)
            ],
            on_change=self.atualizar_lista_tarefas
        )
        return self.abas
    
    def criar_lista_tarefas(self):
        # Cria o container para a lista de tarefas
        self.lista_tarefas = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
        self.atualizar_lista_tarefas()
        return ft.Container(
            content=self.lista_tarefas,
            height=400,
            padding=10,
            bgcolor=self.cor['fundo'],
        )
    
    def atualizar_lista_tarefas(self, e=None):
        #atualiza a lista de tarefas com base na aba selecionada
        self.lista_tarefas.controls.clear()
        query = 'SELECT * FROM "tasks"'
        if self.abas.selected_index == 1:
            query += 'WHERE "status = "incomplete"'
        elif self.abas.selected_index == 2:
            query += 'WHERE "status" = "complete"'

        tarefas = self.banco_dados.searchItens(query)
        for tarefa in tarefas:
            self.lista_tarefas.controls.append(self.criar_item_tarefa(tarefa))
        self.page.update()

    def criar_item_tarefa(self, tarefa):
        return ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=tarefa[1] == 'complete',
                    on_change=lambda e, t=tarefa[0]: self.alternar_status_tarefa(e, t),
                    fill_color=self.cor['checkbox'],
                ),
                ft.Text(tarefa[0], color=self.cor['texto'], size=16, expand=True),
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color=self.cor['destaque'],
                    on_click=lambda _, t=tarefa[0]: self.excluir_tarefa(t)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.border.all(1, self.cor['borda']),
            border_radius=8,
            padding=10,
            bgcolor=self.cor['item_fundo']
        )
    def adicionar_tarefa(self, e):
            #adiciona uma nova tarefa ao banco de dados e atualiza a lista
            if self.entrada_tarefa.value:
                self.banco_dados.addTasks(self.entrada_tarefa.value, 'incomplete')
                self.entrada_tarefa.value = ''
                self.atualizar_lista_tarefas()

    def alternar_status_tarefa(self, e, tarefa):
            #alterna o status da uma  tarefa entre completa e imcompleta
            novo_status = 'complete' if e.control.value else 'incomplete'
            self.banco_dados.updateTasks(novo_status, tarefa)
            self.atualizar_lista_tarefas()

    def excluir_tarefa(self, tarefa):
        #exclui uma tarefa do banco de dados e atualiza a lista
        self.banco_dados.deleteTasks(tarefa)
        self.atualizar_lista_tarefas()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Tarefa '{tarefa}' excluida com sucesso", color=self.cor['texto']),
            bgcolor=self.cor['item_fundo']
        )
        self.page.snack_bar.open = True
        self.page.update()

if __name__ == "__main__":
    ft.app(target=AppToDo) #inicia o aplicativo flet com essa classe
                