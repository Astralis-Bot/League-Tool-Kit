"""
SETTINGS VIEW - Configurações Gerais
Interface de configuração de temas e preferências
"""

import customtkinter as ctk
from ui.theme.theme_switcher_ui import ThemeSettingsView


class SettingsView:
    """View de configurações do aplicativo"""

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme

    def create(self, parent, on_theme_change):
        """Cria a view de configurações"""
        
        # Container principal
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Header moderno
        self._create_settings_header(container)

        # Theme Settings Card
        self._create_theme_settings_card(container, on_theme_change)

    def _create_settings_header(self, parent):
        """Cria header moderno para settings"""
        
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 25))

        # Container horizontal
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x")

        # Ícone grande com fundo
        icon_bg = ctk.CTkFrame(
            header_content,
            fg_color=self.colors['primary'],
            width=48,
            height=48,
            corner_radius=14
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        ctk.CTkLabel(
            icon_bg,
            text="⚙️",
            font=("Segoe UI Emoji", 24),
            text_color="white"
        ).pack(expand=True)

        # Textos
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text="SETTINGS",
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Customize your League Toolkit experience",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _create_theme_settings_card(self, parent, on_theme_change):
        """Card de configurações de tema"""
        
        # Card principal
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['primary']
        )
        card.pack(fill="both", expand=True)

        # Header do card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(20, 15))

        # Ícone e título
        header_left = ctk.CTkFrame(card_header, fg_color="transparent")
        header_left.pack(side="left", fill="x", expand=True)

        title_row = ctk.CTkFrame(header_left, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkLabel(
            title_row,
            text="🎨",
            font=("Segoe UI Emoji", 20),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            title_row,
            text="Theme Configuration",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(side="left")

        ctk.CTkLabel(
            header_left,
            text="Manage themes, import custom themes, and customize appearance",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", padx=(30, 0), pady=(2, 0))

        # Linha divisória
        ctk.CTkFrame(
            card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20)

        # Theme Settings View
        theme_container = ctk.CTkFrame(card, fg_color="transparent")
        theme_container.pack(fill="both", expand=True, padx=20, pady=20)

        theme_view = ThemeSettingsView(
            theme_container,
            on_theme_change=on_theme_change,
            fg_color=self.colors['bg_medium']
        )
        theme_view.pack(fill="both", expand=True)

        # Footer informativo
        self._create_settings_footer(card)

    def _create_settings_footer(self, parent):
        """Footer com informações adicionais"""
        
        # Linha divisória
        ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20)

        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=15)

    def update_colors(self, colors):
        """Atualiza cores do tema"""
        self.colors = colors