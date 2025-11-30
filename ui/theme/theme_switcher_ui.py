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
            text="🔥 IMPORTAR TEMA OFICIAL",
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
        
        # Temas importados (PREMIUM)
        if custom_themes:
            premium_header = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=self.current_colors['bg_card'],
                corner_radius=10,
                border_width=2,
                border_color=self.current_colors['accent']
            )
            premium_header.pack(fill="x", pady=(20, 10), padx=10)
            
            header_content = ctk.CTkFrame(premium_header, fg_color="transparent")
            header_content.pack(fill="x", padx=15, pady=12)
            
            title_row = ctk.CTkFrame(header_content, fg_color="transparent")
            title_row.pack(fill="x")
            
            ctk.CTkLabel(
                title_row,
                text="✨",
                font=("Segoe UI Emoji", 16)
            ).pack(side="left", padx=(0, 8))
            
            ctk.CTkLabel(
                title_row,
                text="PREMIUM THEMES",
                font=("Segoe UI", 12, "bold"),
                text_color=self.current_colors['accent']
            ).pack(side="left")
            
            ctk.CTkLabel(
                title_row,
                text=f"{len(custom_themes)} imported",
                font=("Segoe UI", 9),
                text_color=self.current_colors['text_secondary']
            ).pack(side="left", padx=(10, 0))
            
            ctk.CTkLabel(
                header_content,
                text="Exclusive designs with enhanced visual effects",
                font=("Segoe UI", 9),
                text_color=self.current_colors['text_secondary']
            ).pack(anchor="w", pady=(4, 0))
            
            for theme_id, theme_name in custom_themes.items():
                self._create_theme_card(theme_id, theme_name, current, True)

    def _create_theme_card(self, theme_id, theme_name, current_theme, is_custom):
        """Cria card de tema com efeitos especiais para premium"""
        theme_colors = self.theme_manager.get_theme(theme_id)
        is_selected = theme_id == current_theme
        
        # Card com efeitos especiais para temas premium
        border_width = 3 if is_selected else 2
        corner_radius = 12 if is_custom else 10
        
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme_colors['bg_medium'],
            border_width=border_width,
            border_color=theme_colors['primary'],
            corner_radius=corner_radius
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Efeito de brilho sutil para temas premium
        if is_custom:
            self._add_premium_glow(card, theme_colors)
        
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        # Preview de cores com efeito especial para premium
        preview = ctk.CTkFrame(container, fg_color="transparent")
        preview.pack(side="left", padx=12, pady=10)
        
        dots = ctk.CTkFrame(preview, fg_color="transparent")
        dots.pack()
        
        colors_to_show = [theme_colors['primary'], theme_colors['secondary'], theme_colors['accent']]
        
        for i, color in enumerate(colors_to_show):
            # Dots maiores e com sombra para temas premium
            dot_size = 24 if is_custom else 20
            dot_radius = 6 if is_custom else 4
            
            dot = ctk.CTkFrame(
                dots,
                width=dot_size,
                height=dot_size,
                fg_color=color,
                corner_radius=dot_radius
            )
            dot.pack(side="left", padx=4)
            dot.pack_propagate(False)
            
            # Adiciona ícone especial no primeiro dot de temas premium
            if is_custom and i == 0:
                ctk.CTkLabel(
                    dot,
                    text="✨",
                    font=("Segoe UI Emoji", 10),
                    text_color="white"
                ).pack(expand=True)
        
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
            # Badge animado premium
            badge_frame = ctk.CTkFrame(
                name_container,
                fg_color=theme_colors['accent'],
                corner_radius=6
            )
            badge_frame.pack(side="left", padx=(8, 0))
            
            badge_content = ctk.CTkFrame(badge_frame, fg_color="transparent")
            badge_content.pack(padx=8, pady=3)
            
            ctk.CTkLabel(
                badge_content,
                text="✨",
                font=("Segoe UI Emoji", 10)
            ).pack(side="left", padx=(0, 4))
            
            ctk.CTkLabel(
                badge_content,
                text="PREMIUM",
                font=("Segoe UI", 8, "bold"),
                text_color=theme_colors['bg_dark']
            ).pack(side="left")
            
            # Efeito de brilho
            self._animate_premium_badge(badge_frame, theme_colors['accent'])
        
        ctk.CTkLabel(
            info,
            text=f"ID: {theme_id}",
            font=("Segoe UI", 8),
            text_color=theme_colors['text_secondary']
        ).pack(anchor="w", pady=(2, 0))
        
        # Botões com estilo especial para premium
        btn_container = ctk.CTkFrame(container, fg_color="transparent")
        btn_container.pack(side="right", padx=12, pady=8)
        
        # Botão de seleção com gradiente visual para premium
        select_text = "✓ ATIVO" if is_selected else ("⭐ SELECIONAR" if is_custom else "SELECIONAR")
        select_width = 140 if is_custom else 120
        
        select_btn = ctk.CTkButton(
            btn_container,
            text=select_text,
            font=("Segoe UI", 10, "bold"),
            fg_color=theme_colors['primary'],
            text_color=theme_colors['bg_dark'],
            hover_color=theme_colors['secondary'],
            width=select_width,
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
        
        # Info extra para temas premium (fora do container de botões)
        if is_custom:
            premium_info = ctk.CTkFrame(
                container,
                fg_color=self._lighten_color(theme_colors['bg_medium'], 1.1),
                corner_radius=8
            )
            premium_info.pack(fill="x", pady=(8, 0), padx=12)
            
            info_content = ctk.CTkFrame(premium_info, fg_color="transparent")
            info_content.pack(fill="x", padx=12, pady=6)
            
            ctk.CTkLabel(
                info_content,
                text="✨ Premium Theme",
                font=("Segoe UI", 9, "bold"),
                text_color=theme_colors['accent']
            ).pack(side="left")
            
            ctk.CTkLabel(
                info_content,
                text="• Exclusive design • Official source",
                font=("Segoe UI", 8),
                text_color=theme_colors['text_secondary']
            ).pack(side="left", padx=(8, 0))
        
        self.theme_buttons[theme_id] = (card, select_btn)
        
        # Efeito hover especial para temas premium
        if is_custom:
            def on_enter(e):
                card.configure(border_width=4)
            
            def on_leave(e):
                card.configure(border_width=3 if is_selected else 2)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            container.bind("<Enter>", on_enter)
            container.bind("<Leave>", on_leave)

    def _animate_premium_badge(self, badge_frame, color):
        """Anima badge premium com efeito de pulso"""
        def pulse():
            if badge_frame.winfo_exists():
                try:
                    # Alterna entre cor normal e mais clara
                    current_color = badge_frame.cget("fg_color")
                    if current_color == color:
                        # Versão mais clara
                        badge_frame.configure(fg_color=self._lighten_color(color, 1.2))
                    else:
                        badge_frame.configure(fg_color=color)
                    
                    badge_frame.after(800, pulse)
                except:
                    pass
        
        pulse()
    
    def _lighten_color(self, hex_color, factor):
        """Clareia uma cor hexadecimal"""
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color
    
    def _add_premium_glow(self, card, theme_colors):
        """Adiciona efeito de brilho sutil em temas premium"""
        def glow_effect():
            if card.winfo_exists():
                try:
                    # Alterna sutil brilho na borda
                    current_width = card.cget("border_width")
                    if current_width == 2:
                        card.configure(border_width=3)
                    else:
                        card.configure(border_width=2)
                    
                    card.after(1500, glow_effect)
                except:
                    pass
        
        glow_effect()

    def _select_theme(self, theme_id):
        """Seleciona tema"""
        if self.theme_manager.apply_theme(theme_id):
            if self.on_theme_change:
                self.on_theme_change(self.theme_manager.get_current_theme())
            
            self._refresh_theme_list()

    def _import_theme(self):
        """Importa tema oficial (.ltt)"""
        file_path = filedialog.askopenfilename(
            title="Select Premium Theme",
            filetypes=[("League Toolkit Theme", "*.ltt"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            success, message = self.theme_manager.import_theme(file_path)
            
            if success:
                messagebox.showinfo(
                    "✨ Success", 
                    f"{message}\n\nYour premium theme is now available with exclusive features!",
                    icon='info'
                )
                self._refresh_theme_list()
                self.current_colors = self.theme_manager.get_current_theme()
            else:
                messagebox.showerror("❌ Error", message)

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