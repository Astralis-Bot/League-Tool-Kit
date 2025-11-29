"""
LEAGUE TOOLKIT - Theme Switcher UI (Simplified)
Interface simplificada para seleção de temas oficiais
"""

import customtkinter as ctk
from ui.theme.theme_manager import ThemeManager
from tkinter import filedialog, messagebox
import os


class ThemeSwitcher(ctk.CTkFrame):
    """Seletor de temas oficial - apenas temas assinados"""
    
    def __init__(self, parent, on_theme_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme_manager = ThemeManager()
        self.on_theme_change = on_theme_change
        self.current_colors = self.theme_manager.get_current_theme()
        self.theme_buttons = {}
        
        self._create_widgets()

    def _create_widgets(self):
        """Cria interface"""
        # Header com botão de importar
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=5, pady=(5, 10))
        
        import_btn = ctk.CTkButton(
            header,
            text="📥 IMPORTAR TEMA OFICIAL",
            font=("Segoe UI", 11, "bold"),
            fg_color=self.current_colors['primary'],
            hover_color=self.current_colors['secondary'],
            text_color=self.current_colors['bg_dark'],
            height=35,
            command=self._import_theme
        )
        import_btn.pack(side="left", padx=5)
        
        info_label = ctk.CTkLabel(
            header,
            text="💡 Apenas temas oficiais (.ltt) são aceitos",
            font=("Segoe UI", 9),
            text_color=self.current_colors['text_secondary']
        )
        info_label.pack(side="left", padx=15)
        
        # Separador
        ctk.CTkFrame(
            self,
            fg_color=self.current_colors['bg_light'],
            height=2
        ).pack(fill="x", pady=10)
        
        # Lista de temas
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=400
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._refresh_theme_list()

    def _refresh_theme_list(self):
        """Atualiza lista de temas"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.theme_buttons.clear()
        
        themes = self.theme_manager.get_theme_names()
        current = self.theme_manager.current_theme
        
        # Separa temas padrão e customizados
        default_themes = {}
        custom_themes = {}
        
        for theme_id, theme_name in themes.items():
            if self.theme_manager.is_custom_theme(theme_id):
                custom_themes[theme_id] = theme_name
            else:
                default_themes[theme_id] = theme_name
        
        # Temas padrão
        if default_themes:
            ctk.CTkLabel(
                self.scroll_frame,
                text="🎨 TEMAS PADRÃO",
                font=("Segoe UI", 12, "bold"),
                text_color=self.current_colors['primary']
            ).pack(anchor="w", pady=(5, 10), padx=10)
            
            for theme_id, theme_name in default_themes.items():
                self._create_theme_card(theme_id, theme_name, current, False)
        
        # Temas importados
        if custom_themes:
            ctk.CTkLabel(
                self.scroll_frame,
                text="✨ TEMAS IMPORTADOS",
                font=("Segoe UI", 12, "bold"),
                text_color=self.current_colors['accent']
            ).pack(anchor="w", pady=(20, 10), padx=10)
            
            for theme_id, theme_name in custom_themes.items():
                self._create_theme_card(theme_id, theme_name, current, True)

    def _create_theme_card(self, theme_id, theme_name, current_theme, is_custom):
        """Cria card de tema"""
        theme_colors = self.theme_manager.get_theme(theme_id)
        is_selected = theme_id == current_theme
        
        # Card principal
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme_colors['bg_medium'],
            border_width=3 if is_selected else 2,
            border_color=theme_colors['primary'],
            corner_radius=10
        )
        card.pack(fill="x", pady=8, padx=5)
        
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        # Preview de cores
        preview = ctk.CTkFrame(container, fg_color="transparent")
        preview.pack(side="left", padx=12, pady=10)
        
        dots = ctk.CTkFrame(preview, fg_color="transparent")
        dots.pack()
        
        for color in [theme_colors['primary'], theme_colors['secondary'], 
                      theme_colors['accent']]:
            dot = ctk.CTkFrame(
                dots,
                width=20,
                height=20,
                fg_color=color,
                corner_radius=4
            )
            dot.pack(side="left", padx=4)
            dot.pack_propagate(False)
        
        # Informações
        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=10, pady=8)
        
        name_container = ctk.CTkFrame(info, fg_color="transparent")
        name_container.pack(anchor="w", fill="x")
        
        ctk.CTkLabel(
            name_container,
            text=theme_name,
            font=("Segoe UI", 11, "bold"),
            text_color=theme_colors['text_primary']
        ).pack(side="left")
        
        if is_custom:
            ctk.CTkLabel(
                name_container,
                text="OFICIAL",
                font=("Segoe UI", 8, "bold"),
                text_color=theme_colors['bg_dark'],
                fg_color=theme_colors['accent'],
                corner_radius=4
            ).pack(side="left", padx=(8, 0), ipadx=6, ipady=2)
        
        ctk.CTkLabel(
            info,
            text=f"ID: {theme_id}",
            font=("Segoe UI", 8),
            text_color=theme_colors['text_secondary']
        ).pack(anchor="w", pady=(2, 0))
        
        # Botões
        btn_container = ctk.CTkFrame(container, fg_color="transparent")
        btn_container.pack(side="right", padx=12, pady=8)
        
        select_btn = ctk.CTkButton(
            btn_container,
            text="✓ ATIVO" if is_selected else "SELECIONAR",
            font=("Segoe UI", 10, "bold"),
            fg_color=theme_colors['primary'],
            text_color=theme_colors['bg_dark'],
            hover_color=theme_colors['secondary'],
            width=120,
            height=35,
            command=lambda: self._select_theme(theme_id),
            state="disabled" if is_selected else "normal"
        )
        select_btn.pack(side="left", padx=(0, 5))
        
        if is_custom:
            delete_btn = ctk.CTkButton(
                btn_container,
                text="🗑️",
                font=("Segoe UI", 14),
                fg_color=theme_colors['danger'],
                text_color=theme_colors['bg_dark'],
                hover_color="#CC0000",
                width=40,
                height=35,
                command=lambda: self._delete_theme(theme_id, theme_name)
            )
            delete_btn.pack(side="left")
        
        self.theme_buttons[theme_id] = (card, select_btn)

    def _select_theme(self, theme_id):
        """Seleciona tema"""
        if self.theme_manager.apply_theme(theme_id):
            if self.on_theme_change:
                self.on_theme_change(self.theme_manager.get_current_theme())
            
            self._refresh_theme_list()

    def _import_theme(self):
        """Importa tema oficial (.ltt)"""
        file_path = filedialog.askopenfilename(
            title="Selecione o tema oficial",
            filetypes=[("League Toolkit Theme", "*.ltt"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            success, message = self.theme_manager.import_theme(file_path)
            
            if success:
                messagebox.showinfo("✅ Sucesso", message)
                self._refresh_theme_list()
                self.current_colors = self.theme_manager.get_current_theme()
            else:
                messagebox.showerror("❌ Erro", message)

    def _delete_theme(self, theme_id, theme_name):
        """Deleta tema importado"""
        confirm = messagebox.askyesno(
            "⚠️ Confirmar Exclusão",
            f"Deseja realmente deletar o tema '{theme_name}'?\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if confirm:
            success, message = self.theme_manager.delete_custom_theme(theme_id)
            
            if success:
                messagebox.showinfo("✅ Sucesso", message)
                self._refresh_theme_list()
                
                if self.theme_manager.current_theme != theme_id:
                    self.current_colors = self.theme_manager.get_current_theme()
                    if self.on_theme_change:
                        self.on_theme_change(self.current_colors)
            else:
                messagebox.showerror("❌ Erro", message)


class ThemeSettingsView(ctk.CTkFrame):
    """View de configurações de tema"""
    
    def __init__(self, parent, on_theme_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_current_theme()
        self.on_theme_change = on_theme_change
        
        self._create_layout()

    def _create_layout(self):
        """Cria layout"""
        # Título
        ctk.CTkLabel(
            self,
            text="⚡ GERENCIADOR DE TEMAS",
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=(20, 5), padx=20)
        
        # Descrição
        ctk.CTkLabel(
            self,
            text="Escolha um tema padrão ou importe temas oficiais",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 15), padx=20)
        
        # Frame do switcher
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
            on_theme_change=self._on_theme_selected,
            fg_color=self.colors['bg_medium']
        )
        switcher.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info footer
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
        
        ctk.CTkLabel(
            info_container,
            text="📋 TEMA ATUAL",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 20))
        
        self.info_text = ctk.CTkLabel(
            info_container,
            text=self._get_theme_info(),
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            justify="left"
        )
        self.info_text.pack(side="left")

    def _get_theme_info(self):
        """Retorna info do tema atual"""
        theme = self.theme_manager.get_current_theme()
        theme_names = self.theme_manager.get_theme_names()
        current_name = theme_names.get(
            self.theme_manager.current_theme, 
            "Desconhecido"
        )
        
        is_custom = self.theme_manager.is_custom_theme(
            self.theme_manager.current_theme
        )
        badge = " [OFICIAL]" if is_custom else ""
        
        return (f"{current_name}{badge} • "
                f"Primary: {theme['primary']} • "
                f"BG: {theme['bg_dark']}")

    def _on_theme_selected(self, new_colors):
        """Callback de mudança de tema"""
        self.colors = new_colors
        self.info_text.configure(text=self._get_theme_info())
        
        self.configure(fg_color=new_colors['bg_medium'])
        
        if self.on_theme_change:
            self.on_theme_change(new_colors)