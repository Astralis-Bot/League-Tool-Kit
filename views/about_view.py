"""
ABOUT VIEW - Informações e Sistema de Atualização
Interface moderna com informações do app, updates e contatos
"""

import customtkinter as ctk
import webbrowser
import threading


class AboutView:
    """View sobre o aplicativo com sistema de atualização integrado"""

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme
        self.status_label = None
        self.version_badge = None
        self.update_button = None
        self.latest_version_row = None
        self.latest_version_label = None
        self.latest_version_value = None

    def create(self, parent, app=None):
        """Cria a view About"""
        
        self.app = app
        
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Header moderno
        self._create_about_header(container)

        # Main info card
        info_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['primary']
        )
        info_card.pack(fill="x", pady=(0, 15))

        # Seções do card
        self._create_app_info(info_card)
        self._create_divider(info_card)
        self._create_credits(info_card)
        self._create_divider(info_card)
        self._create_features(info_card)

        # Update section
        if app and hasattr(app, 'updater'):
            self._create_divider(info_card)
            self._create_update_section(info_card, app)

        # Contact section
        self._create_divider(info_card)
        self._create_contact_section(info_card)

    def _create_about_header(self, parent):
        """Header moderno para About"""
        
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 20))

        # Container horizontal
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x")

        # Ícone grande
        icon_bg = ctk.CTkFrame(
            header_content,
            fg_color=self.colors['info'],
            width=48,
            height=48,
            corner_radius=14
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        ctk.CTkLabel(
            icon_bg,
            text="ℹ️",
            font=("Segoe UI Emoji", 24),
            text_color="white"
        ).pack(expand=True)

        # Textos
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text="ABOUT",
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Application information, updates and support",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _create_app_info(self, parent):
        """Seção de informações do app"""
        
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)

        # Container horizontal
        app_row = ctk.CTkFrame(section, fg_color="transparent")
        app_row.pack(fill="x")

        # Ícone do app (grande)
        ctk.CTkLabel(
            app_row,
            text=self.colors.get('app_icon', '⚡'),
            font=("Segoe UI Emoji", 56),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 20))

        # Informações do app
        info_section = ctk.CTkFrame(app_row, fg_color="transparent")
        info_section.pack(side="left", fill="both", expand=True)

        # Nome do app
        ctk.CTkLabel(
            info_section,
            text=self.colors.get('app_name', "LEAGUE TOOLKIT"),
            font=("Segoe UI", 20, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        ).pack(anchor="w")

        # Subtítulo
        ctk.CTkLabel(
            info_section,
            text="League of Legends Automation Toolkit",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Versão badge
        if self.app and hasattr(self.app, 'updater'):
            version_row = ctk.CTkFrame(info_section, fg_color="transparent")
            version_row.pack(anchor="w", pady=(8, 0))

            self.version_badge = ctk.CTkLabel(
                version_row,
                text=f"v{self.app.updater.CURRENT_VERSION}",
                font=("Segoe UI", 10, "bold"),
                text_color="white",
                fg_color=self.colors['primary'],
                corner_radius=8
            )
            self.version_badge.pack(side="left", ipadx=12, ipady=6)

        # Descrição
        ctk.CTkLabel(
            section,
            text="Advanced automation toolkit for League of Legends with intelligent backup systems, "
                 "champion selection, auto-banning, and quick actions.",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w",
            wraplength=550,
            justify="left"
        ).pack(anchor="w", pady=(15, 0))

    def _create_credits(self, parent):
        """Seção de créditos"""
        
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="👨‍💻",
            font=("Segoe UI Emoji", 20),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Credits & Developers",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(side="left")

        # Desenvolvedores
        developers = [
            ("⚡ Younk", "Lead Developer & Designer", self.colors['primary']),
            ("🔧 Gyaf", "Core Developer & Architect", self.colors['secondary'])
        ]

        for name, role, color in developers:
            self._create_developer_card(section, name, role, color)

    def _create_developer_card(self, parent, name, role, color):
        """Card individual de desenvolvedor"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=10
        )
        card.pack(fill="x", pady=(0, 8))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)

        ctk.CTkLabel(
            content,
            text=name,
            font=("Segoe UI", 12, "bold"),
            text_color=color,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=role,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _create_features(self, parent):
        """Seção de features (corrigida)"""
        
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="⚡",
            font=("Segoe UI Emoji", 20),
            text_color=self.colors['success']
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Key Features",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['success']
        ).pack(side="left")

        # Grid
        features_grid = ctk.CTkFrame(section, fg_color="transparent")
        features_grid.pack(fill="x")

        features_grid.columnconfigure(0, weight=1)
        features_grid.columnconfigure(1, weight=1)

        features = [
            ("🔒", "Instalock", "Instant champion selection with 3 backups"),
            ("⛔", "Auto Ban", "Automatic champion banning with 3 backups"),
            ("✓", "Auto Accept", "Auto-accept queue matches"),
            ("💬", "Chat Toggle", "Enable/disable in-game chat"),
            ("📊", "Lobby Reveal", "Open Porofessor team analysis"),
            ("🎨", "Themes", "Customizable interface themes")
        ]

        for idx, (icon, title, desc) in enumerate(features):
            row = idx // 2
            col = idx % 2

            self._create_feature_item(
                features_grid, icon, title, desc, row, col
            )

    def _create_feature_item(self, parent, icon, title, description, row, column):
        """Item individual de feature"""

        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.grid(
            row=row,
            column=column,
            sticky="w",
            padx=(0, 20) if column == 0 else (20, 0),
            pady=6
        )

        row_frame = ctk.CTkFrame(item, fg_color="transparent")
        row_frame.pack(anchor="w")

        ctk.CTkLabel(
            row_frame,
            text=icon,
            font=("Segoe UI Emoji", 18),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 10))

        text_container = ctk.CTkFrame(row_frame, fg_color="transparent")
        text_container.pack(side="left")

        ctk.CTkLabel(
            text_container,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_container,
            text=description,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w",
            wraplength=220,
            justify="left"
        ).pack(anchor="w")


    def _create_update_section(self, parent, app):
        """Seção de atualizações"""
        
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="🔄",
            font=("Segoe UI Emoji", 20),
            text_color=self.colors['info']
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Updates",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['info']
        ).pack(side="left")

        # Info card
        info_card = ctk.CTkFrame(
            section,
            fg_color=self.colors['bg_light'],
            corner_radius=10
        )
        info_card.pack(fill="x", pady=(0, 15))

        info_content = ctk.CTkFrame(info_card, fg_color="transparent")
        info_content.pack(fill="x", padx=15, pady=12)

        # Versão atual
        self._create_info_row(
            info_content,
            "Current Version:",
            f"v{app.updater.CURRENT_VERSION}",
            self.colors['primary']
        )

        # Latest version (preparar container)
        self.latest_version_row = ctk.CTkFrame(info_content, fg_color="transparent")
        self.latest_version_row.pack(fill="x", pady=3)

        self.latest_version_label = ctk.CTkLabel(
            self.latest_version_row,
            text="Latest Version:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        )

        self.latest_version_value = ctk.CTkLabel(
            self.latest_version_row,
            text="Checking...",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        )

        # Status
        status_row = ctk.CTkFrame(info_content, fg_color="transparent")
        status_row.pack(fill="x", pady=3)

        ctk.CTkLabel(
            status_row,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            status_row,
            text="⏳ Checking for updates...",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(side="left", padx=(8, 0))

        # Botões
        buttons = ctk.CTkFrame(section, fg_color="transparent")
        buttons.pack(fill="x")

        self.update_button = ctk.CTkButton(
            buttons,
            text="🔍 Check for Updates",
            height=40,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary'],
            text_color="white",
            corner_radius=10,
            command=lambda: self._check_updates(app)
        )
        self.update_button.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            buttons,
            text="📥 GitHub Releases",
            height=40,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['bg_light'],
            hover_color=self.colors['bg_medium'],
            text_color=self.colors['text_primary'],
            border_width=2,
            border_color=self.colors['primary'],
            corner_radius=10,
            command=self._open_github_releases
        ).pack(side="left", fill="x", expand=True)

        # Inicia verificação inicial
        parent.after(500, lambda: self._initial_update_check(app))

    def _create_contact_section(self, parent):
        """Seção de contato"""
        
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(
            header,
            text="📨",
            font=("Segoe UI Emoji", 20),
            text_color=self.colors['accent']
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Support & Contact",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['accent']
        ).pack(side="left")

        # Descrição
        ctk.CTkLabel(
            section,
            text="Have suggestions, found bugs, or need help? Feel free to reach out:",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))

        # Botões de contato
        buttons = ctk.CTkFrame(section, fg_color="transparent")
        buttons.pack(anchor="w")

        # Discord
        ctk.CTkButton(
            buttons,
            text="💬 Discord",
            fg_color="#5865F2",
            hover_color="#4752C4",
            text_color="white",
            height=38,
            font=("Segoe UI", 11, "bold"),
            corner_radius=10,
            width=160,
            command=lambda: webbrowser.open("https://discord.com/users/424379062845177876")
        ).pack(side="left", padx=(0, 10))

        # Twitter/X
        ctk.CTkButton(
            buttons,
            text="🦅 Twitter (X)",
            fg_color="#000000",
            hover_color="#222222",
            text_color="white",
            height=38,
            font=("Segoe UI", 11, "bold"),
            corner_radius=10,
            width=160,
            command=lambda: webbrowser.open("https://x.com/novaktheprince")
        ).pack(side="left")

    def _create_divider(self, parent):
        """Linha divisória"""
        ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20)

    def _create_info_row(self, parent, label, value, value_color=None):
        """Linha de informação"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=3)

        ctk.CTkLabel(
            row,
            text=label,
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=value,
            font=("Segoe UI", 10),
            text_color=value_color or self.colors['text_secondary']
        ).pack(side="left", padx=(8, 0))

    def _initial_update_check(self, app):
        """Verificação inicial silenciosa"""
        if not hasattr(app, 'updater'):
            return

        def check():
            try:
                app.updater.check_for_updates(silent=True)
                if hasattr(self, 'status_label') and self.status_label:
                    parent = self.status_label.master.master.master.master
                    parent.after(0, lambda: self._update_ui_status(app))
            except Exception as e:
                print(f"Error in initial check: {e}")

        threading.Thread(target=check, daemon=True).start()

    def _check_updates(self, app):
        """Verificação manual de updates"""
        if not hasattr(app, 'updater'):
            return

        if self.update_button:
            self.update_button.configure(state="disabled", text="⏳ Checking...")

        if self.status_label:
            self.status_label.configure(
                text="⏳ Checking for updates...",
                text_color=self.colors['text_secondary']
            )

        def check():
            try:
                app.updater.check_for_updates(silent=False)
                if hasattr(self, 'status_label') and self.status_label:
                    parent = self.status_label.master.master.master.master
                    parent.after(0, lambda: self._update_ui_status(app))
            except Exception as e:
                print(f"Error checking updates: {e}")
            finally:
                if self.update_button:
                    parent = self.update_button.master.master.master
                    parent.after(0, lambda: self.update_button.configure(
                        state="normal",
                        text="🔍 Check for Updates"
                    ))

        threading.Thread(target=check, daemon=True).start()

    def _update_ui_status(self, app):
        """Atualiza UI com status"""
        if not hasattr(app, 'updater') or not self.status_label:
            return

        updater = app.updater

        # Atualiza versão disponível
        if self.latest_version_value and updater.latest_version:
            self.latest_version_label.pack(side="left")
            self.latest_version_value.pack(side="left", padx=(8, 0))
            self.latest_version_value.configure(
                text=f"v{updater.latest_version}",
                text_color=self.colors['primary']
            )
        elif self.latest_version_value:
            self.latest_version_label.pack_forget()
            self.latest_version_value.pack_forget()

        # Atualiza status
        if updater.update_available:
            self.status_label.configure(
                text=f"🔔 Update available: v{updater.latest_version}",
                text_color=self.colors['warning']
            )
            if self.update_button:
                self.update_button.configure(
                    text="📥 Download Update",
                    fg_color=self.colors['success'],
                    command=lambda: app.updater.download_and_install()
                )
            if self.version_badge:
                self.version_badge.configure(fg_color=self.colors['warning'])
        elif updater.is_up_to_date:
            self.status_label.configure(
                text="✅ Up to date",
                text_color=self.colors['success']
            )
            if self.version_badge:
                self.version_badge.configure(fg_color=self.colors['success'])
        else:
            self.status_label.configure(
                text="⚠️ Unable to check",
                text_color=self.colors['error']
            )

    def _open_github_releases(self):
        """Abre releases no GitHub"""
        if self.app and hasattr(self.app, 'updater'):
            url = f"https://github.com/{self.app.updater.GITHUB_USER}/{self.app.updater.GITHUB_REPO}/releases"
            webbrowser.open(url)

    def update_colors(self, colors):
        """Atualiza cores"""
        self.colors = colors