# ui/theme/theme_switcher_ui.py - Interface de troca de temas
import customtkinter as ctk
from ui.theme.theme_manager import ThemeManager
from tkinter import filedialog, messagebox
import os


class ThemeSwitcher(ctk.CTkFrame):
    """Widget para trocar de tema - Com importação"""
    
    def __init__(self, parent, on_theme_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme_manager = ThemeManager()
        self.on_theme_change = on_theme_change
        self.current_colors = self.theme_manager.get_current_theme()
        self.theme_buttons = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets do seletor de tema"""
        
        # Cabeçalho com botões de ação
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=(5, 10))
        
        # Botão de importar tema
        import_btn = ctk.CTkButton(
            header_frame,
            text="📥 IMPORTAR TEMA",
            font=("Consolas", 11, "bold"),
            fg_color=self.current_colors['primary'],
            hover_color=self.current_colors['secondary'],
            text_color=self.current_colors['bg_dark'],
            height=35,
            command=self.import_theme
        )
        import_btn.pack(side="left", padx=5)
        
        # Separador
        separator = ctk.CTkFrame(self, fg_color=self.current_colors['bg_light'], height=2)
        separator.pack(fill="x", pady=10)
        
        # Container scrollável para os botões de tema
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=400
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh_theme_list()
    
    def refresh_theme_list(self):
        """Atualiza a lista de temas"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.theme_buttons.clear()
        
        themes = self.theme_manager.get_theme_names()
        current = self.theme_manager.current_theme
        
        # Separar temas padrão e customizados
        default_themes = {}
        custom_themes = {}
        
        for theme_id, theme_name in themes.items():
            if self.theme_manager.is_custom_theme(theme_id):
                custom_themes[theme_id] = theme_name
            else:
                default_themes[theme_id] = theme_name
        
        # Mostrar temas padrão
        if default_themes:
            default_label = ctk.CTkLabel(
                self.scroll_frame,
                text="🎨 TEMAS PADRÃO",
                font=("Consolas", 12, "bold"),
                text_color=self.current_colors['primary']
            )
            default_label.pack(anchor="w", pady=(5, 10), padx=10)
            
            for theme_id, theme_name in default_themes.items():
                self.create_theme_button(theme_id, theme_name, current, is_custom=False)
        
        # Mostrar temas customizados
        if custom_themes:
            custom_label = ctk.CTkLabel(
                self.scroll_frame,
                text="✨ TEMAS PERSONALIZADOS",
                font=("Consolas", 12, "bold"),
                text_color=self.current_colors['accent']
            )
            custom_label.pack(anchor="w", pady=(20, 10), padx=10)
            
            for theme_id, theme_name in custom_themes.items():
                self.create_theme_button(theme_id, theme_name, current, is_custom=True)
    
    def create_theme_button(self, theme_id, theme_name, current_theme, is_custom=False):
        """Cria um botão de tema individual"""
        
        theme_colors = self.theme_manager.get_theme(theme_id)
        is_selected = theme_id == current_theme
        
        btn_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme_colors['bg_medium'],
            border_width=3 if is_selected else 2,
            border_color=theme_colors['primary'],
            corner_radius=10
        )
        btn_frame.pack(fill="x", pady=8, padx=5)
        
        # Container principal
        main_container = ctk.CTkFrame(btn_frame, fg_color="transparent")
        main_container.pack(fill="x", expand=True)
        
        # Preview com cores do tema (esquerda)
        preview_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        preview_frame.pack(side="left", padx=12, pady=10)
        
        color_dots = ctk.CTkFrame(preview_frame, fg_color="transparent")
        color_dots.pack()
        
        for color in [theme_colors['primary'], theme_colors['secondary'], theme_colors['accent']]:
            dot = ctk.CTkFrame(
                color_dots,
                width=20,
                height=20,
                fg_color=color,
                corner_radius=4
            )
            dot.pack(side="left", padx=4)
            dot.pack_propagate(False)
        
        # Informação do tema (centro)
        info_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
        
        # Nome do tema
        name_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_container.pack(anchor="w", fill="x")
        
        label = ctk.CTkLabel(
            name_container,
            text=theme_name,
            font=("Consolas", 11, "bold"),
            text_color=theme_colors['text_primary']
        )
        label.pack(side="left")
        
        # Badge de customizado
        if is_custom:
            custom_badge = ctk.CTkLabel(
                name_container,
                text="CUSTOM",
                font=("Consolas", 8, "bold"),
                text_color=theme_colors['bg_dark'],
                fg_color=theme_colors['accent'],
                corner_radius=4
            )
            custom_badge.pack(side="left", padx=(8, 0), ipadx=6, ipady=2)
        
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"ID: {theme_id}",
            font=("Consolas", 8),
            text_color=theme_colors['text_secondary']
        )
        status_label.pack(anchor="w", pady=(2, 0))
        
        # Botões (direita)
        btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_container.pack(side="right", padx=12, pady=8)
        
        # Botão de seleção
        select_btn = ctk.CTkButton(
            btn_container,
            text="✓ ATIVO" if is_selected else "SELECIONAR",
            font=("Consolas", 10, "bold"),
            fg_color=theme_colors['primary'],
            text_color=theme_colors['bg_dark'],
            hover_color=theme_colors['secondary'],
            width=120,
            height=35,
            command=lambda: self.select_theme(theme_id),
            state="disabled" if is_selected else "normal"
        )
        select_btn.pack(side="left", padx=(0, 5))
        
        # Botão de deletar (apenas para temas customizados)
        if is_custom:
            delete_btn = ctk.CTkButton(
                btn_container,
                text="🗑️",
                font=("Consolas", 14),
                fg_color=theme_colors['danger'],
                text_color=theme_colors['bg_dark'],
                hover_color="#CC0000",
                width=40,
                height=35,
                command=lambda: self.delete_theme(theme_id, theme_name)
            )
            delete_btn.pack(side="left")
        
        self.theme_buttons[theme_id] = (btn_frame, select_btn)
    
    def select_theme(self, theme_id):
        """Seleciona um novo tema"""
        if self.theme_manager.apply_theme(theme_id):
            if self.on_theme_change:
                self.on_theme_change(self.theme_manager.get_current_theme())
            
            self.refresh_theme_list()
    
    def import_theme(self):
        """Abre diálogo para importar tema"""
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo de tema",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            success, message = self.theme_manager.import_theme(file_path)
            
            if success:
                messagebox.showinfo("✅ Sucesso", message)
                self.refresh_theme_list()
                self.current_colors = self.theme_manager.get_current_theme()
            else:
                messagebox.showerror("❌ Erro", message)
    
    def delete_theme(self, theme_id, theme_name):
        """Deleta um tema customizado"""
        confirm = messagebox.askyesno(
            "⚠️ Confirmar Exclusão",
            f"Deseja realmente deletar o tema '{theme_name}'?\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if confirm:
            success, message = self.theme_manager.delete_custom_theme(theme_id)
            
            if success:
                messagebox.showinfo("✅ Sucesso", message)
                self.refresh_theme_list()
                
                if self.theme_manager.current_theme != theme_id:
                    self.current_colors = self.theme_manager.get_current_theme()
                    if self.on_theme_change:
                        self.on_theme_change(self.current_colors)
            else:
                messagebox.showerror("❌ Erro", message)


class ThemeSettingsView(ctk.CTkFrame):
    """View completa de configurações de tema"""
    
    def __init__(self, parent, on_theme_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_current_theme()
        self.on_theme_change = on_theme_change
        
        self.create_layout()
    
    def create_layout(self):
        """Cria o layout da view"""
        
        # Título principal
        main_title = ctk.CTkLabel(
            self,
            text="⚡ GERENCIADOR DE TEMAS",
            font=("Consolas", 18, "bold"),
            text_color=self.colors['primary']
        )
        main_title.pack(pady=(20, 5), padx=20)
        
        # Descrição
        desc = ctk.CTkLabel(
            self,
            text="Escolha um tema existente ou importe seu próprio tema personalizado",
            font=("Consolas", 10),
            text_color=self.colors['text_secondary']
        )
        desc.pack(pady=(0, 15), padx=20)
        
        # Seletor de tema
        theme_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['bg_medium'],
            border_width=1,
            border_color=self.colors['primary'],
            corner_radius=10
        )
        theme_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        switcher = ThemeSwitcher(
            theme_frame,
            on_theme_change=self.on_theme_selected,
            fg_color=self.colors['bg_medium']
        )
        switcher.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Informações do tema atual
        info_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['bg_light'],
            border_width=1,
            border_color=self.colors['primary'],
            corner_radius=10
        )
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=15, pady=12)
        
        info_title = ctk.CTkLabel(
            info_container,
            text="📋 TEMA ATUAL",
            font=("Consolas", 10, "bold"),
            text_color=self.colors['primary']
        )
        info_title.pack(side="left", padx=(0, 20))
        
        self.info_text = ctk.CTkLabel(
            info_container,
            text=self.get_theme_info_short(),
            font=("Consolas", 9),
            text_color=self.colors['text_secondary'],
            justify="left"
        )
        self.info_text.pack(side="left")
    
    def get_theme_info_short(self):
        """Retorna informações resumidas do tema atual"""
        theme = self.theme_manager.get_current_theme()
        theme_names = self.theme_manager.get_theme_names()
        current_name = theme_names.get(self.theme_manager.current_theme, "Desconhecido")
        
        is_custom = self.theme_manager.is_custom_theme(self.theme_manager.current_theme)
        custom_badge = " [PERSONALIZADO]" if is_custom else ""
        
        return f"{current_name}{custom_badge} · Primary: {theme['primary']} · BG: {theme['bg_dark']}"
    
    def on_theme_selected(self, new_colors):
        """Callback quando um novo tema é selecionado"""
        self.colors = new_colors
        self.info_text.configure(text=self.get_theme_info_short())
        
        self.configure(fg_color=new_colors['bg_medium'])
        
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                if "GERENCIADOR" in widget.cget("text"):
                    widget.configure(text_color=new_colors['primary'])
                elif "Escolha" in widget.cget("text"):
                    widget.configure(text_color=new_colors['text_secondary'])
            elif isinstance(widget, ctk.CTkFrame):
                if widget.cget('border_width') > 0:
                    widget.configure(
                        fg_color=new_colors['bg_light'],
                        border_color=new_colors['primary']
                    )
        
        if self.on_theme_change:
            self.on_theme_change(new_colors)