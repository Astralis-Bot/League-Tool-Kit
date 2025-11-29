"""
ABOUT VIEW COM SISTEMA DE ATUALIZAÇÃO + CONTATOS
Arquivo completo para substituir views/about_view.py
"""

import customtkinter as ctk
import webbrowser


class AboutView:

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme

    def create(self, parent, app=None):
        """Cria a view About com botões de atualização e contato"""

        self.app = app  # Guarda referência do app
        
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            container,
            text="ℹ️ ABOUT",
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['primary']
        )
        title.pack(anchor="w", pady=(0, 20))

        # Info card
        info_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['primary']
        )
        info_card.pack(fill="x", pady=10, padx=20)

        self._create_app_info(info_card)

        ctk.CTkFrame(info_card, fg_color=self.colors['bg_light'], height=2)\
            .pack(fill="x", padx=20, pady=10)

        self._create_credits(info_card)

        ctk.CTkFrame(info_card, fg_color=self.colors['bg_light'], height=2)\
            .pack(fill="x", padx=20, pady=10)

        self._create_features(info_card)

        # Seção de atualização
        if app and hasattr(app, 'updater'):
            ctk.CTkFrame(info_card, fg_color=self.colors['bg_light'], height=2)\
                .pack(fill="x", padx=20, pady=10)

            self._create_update_section(info_card, app)

        # =============================================
        # SEÇÃO DE CONTATO (Twitter + Discord)
        # =============================================
        ctk.CTkFrame(info_card, fg_color=self.colors['bg_light'], height=2)\
            .pack(fill="x", padx=20, pady=10)

        self._create_contact_section(info_card)

    # ======================================================================
    # ✓ INFO (mantido 100% igual)
    # ======================================================================

    def _create_app_info(self, parent):
        app_frame = ctk.CTkFrame(parent, fg_color="transparent")
        app_frame.pack(fill="x", padx=20, pady=15)

        header_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text=self.colors.get('app_icon', '⚡'),
            font=("Segoe UI Emoji", 48),
            text_color=self.colors['primary']
        ).pack(side="left", padx=(0, 15))

        name_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            name_frame,
            text=self.colors.get('app_name', "LEAGUE TOOLKIT"),
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        ).pack(anchor="w")

        version_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        version_frame.pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            version_frame,
            text="League Automation Toolkit",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(side="left")

        if self.app and hasattr(self.app, 'updater'):
            version_badge = ctk.CTkLabel(
                version_frame,
                text=f"v{self.app.updater.CURRENT_VERSION}",
                font=("Segoe UI", 9, "bold"),
                text_color=self.colors['bg_dark'],
                fg_color=self.colors['primary'],
                corner_radius=6
            )
            version_badge.pack(side="left", padx=(10, 0), ipadx=8, ipady=2)

        ctk.CTkLabel(
            app_frame,
            text="Advanced automation toolkit for League of Legends",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", pady=(10, 0))

    # ======================================================================
    # Créditos
    # ======================================================================

    def _create_credits(self, parent):
        credits_frame = ctk.CTkFrame(parent, fg_color="transparent")
        credits_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            credits_frame,
            text="👨‍💻 Credits & Developers",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 10))

        devs = [
            ("⚡ Younk", "Lead Developer & Designer"),
            ("🔧 Gyaf", "Core Developer & Architect")
        ]

        for dev_name, dev_role in devs:
            dev_card = ctk.CTkFrame(
                credits_frame,
                fg_color=self.colors['bg_light'],
                corner_radius=8
            )
            dev_card.pack(fill="x", pady=5)

            dev_content = ctk.CTkFrame(dev_card, fg_color="transparent")
            dev_content.pack(fill="x", padx=15, pady=12)

            ctk.CTkLabel(
                dev_content,
                text=dev_name,
                font=("Segoe UI", 12, "bold"),
                text_color=self.colors['primary']
            ).pack(anchor="w")

            ctk.CTkLabel(
                dev_content,
                text=dev_role,
                font=("Segoe UI", 9),
                text_color=self.colors['text_secondary']
            ).pack(anchor="w", pady=(2, 0))

    # ======================================================================
    # Features
    # ======================================================================

    def _create_features(self, parent):
        features_frame = ctk.CTkFrame(parent, fg_color="transparent")
        features_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            features_frame,
            text="⚡ Features",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 10))

        features_list = [
            ("🔒 Instalock", "Instant champion selection with 3 backups"),
            ("⛔ Auto Ban", "Automatic champion banning with 3 backups"),
            ("✓ Auto Accept", "Auto-accept queue matches"),
            ("💬 Chat Toggle", "Enable/disable in-game chat"),
            ("📊 Lobby Reveal", "Open Porofessor analysis"),
            ("🎨 Theme Selector", "Manage and import themes")
        ]

        for icon_title, description in features_list:
            feature_item = ctk.CTkFrame(features_frame, fg_color="transparent")
            feature_item.pack(fill="x", pady=3)

            ctk.CTkLabel(
                feature_item,
                text=icon_title,
                font=("Segoe UI", 11, "bold"),
                text_color=self.colors['primary'],
                width=140,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                feature_item,
                text=f"- {description}",
                font=("Segoe UI", 10),
                text_color=self.colors['text_secondary'],
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

    # ======================================================================
    # Updates
    # ======================================================================

    def _create_update_section(self, parent, app):
        update_frame = ctk.CTkFrame(parent, fg_color="transparent")
        update_frame.pack(fill="x", padx=20, pady=15)

        # Header
        header = ctk.CTkFrame(update_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header,
            text="🔄 Updates",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(side="left")

        # Card
        info_card = ctk.CTkFrame(
            update_frame,
            fg_color=self.colors['bg_light'],
            corner_radius=8
        )
        info_card.pack(fill="x", pady=(0, 10))

        info_content = ctk.CTkFrame(info_card, fg_color="transparent")
        info_content.pack(fill="x", padx=15, pady=12)

        # Versão atual
        version_row = ctk.CTkFrame(info_content, fg_color="transparent")
        version_row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            version_row,
            text="Current Version:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        ctk.CTkLabel(
            version_row,
            text=f"v{app.updater.CURRENT_VERSION}",
            font=("Segoe UI", 10),
            text_color=self.colors['success']
        ).pack(side="left", padx=(8, 0))

        # Status
        status_row = ctk.CTkFrame(info_content, fg_color="transparent")
        status_row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            status_row,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            status_row,
            text="Checking for updates...",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(side="left", padx=(8, 0))

        parent.after(1000, lambda: self._update_status(app))

        # Botões
        btn_frame = ctk.CTkFrame(update_frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        ctk.CTkButton(
            btn_frame,
            text="🔍 Verificar Atualizações",
            height=38,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary'],
            text_color="white",
            corner_radius=10,
            command=lambda: self._check_updates(app)
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="📥 GitHub Releases",
            height=38,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['bg_light'],
            hover_color=self.colors['bg_medium'],
            text_color=self.colors['text_primary'],
            corner_radius=10,
            command=self._open_github_releases
        ).pack(side="left", fill="x", expand=True)

    # ======================================================================
    # CONTATO (NOVO)
    # ======================================================================

    def _create_contact_section(self, parent):
        contact_frame = ctk.CTkFrame(parent, fg_color="transparent")
        contact_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            contact_frame,
            text="📨 Suggestions, Bugs & Support",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(anchor="w")

        ctk.CTkLabel(
            contact_frame,
            text="If you have suggestions, found bugs or have doubts,\nfeel free to contact me using the buttons below:",
            justify="left",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", pady=(5, 10))

        btns = ctk.CTkFrame(contact_frame, fg_color="transparent")
        btns.pack(anchor="w", pady=5)

        # Discord Button
        ctk.CTkButton(
            btns,
            text="Discord",
            fg_color="#5865F2",
            hover_color="#4752C4",
            text_color="white",
            height=36,
            font=("Segoe UI", 11, "bold"),
            corner_radius=10,
            width=130,
            command=lambda: webbrowser.open("https://discord.com/users/424379062845177876")
        ).pack(side="left", padx=(0, 10))

        # Twitter / X Button
        ctk.CTkButton(
            btns,
            text="Twitter (X)",
            fg_color="#000000",
            hover_color="#222222",
            text_color="white",
            height=36,
            font=("Segoe UI", 11, "bold"),
            corner_radius=10,
            width=130,
            command=lambda: webbrowser.open("https://x.com/novaktheprince")
        ).pack(side="left")

    # ======================================================================
    # Update Helpers
    # ======================================================================

    def _update_status(self, app):
        if hasattr(self, 'status_label'):
            if app.updater.update_available:
                self.status_label.configure(
                    text=f"Update available: v{app.updater.latest_version}",
                    text_color=self.colors['warning']
                )
            else:
                self.status_label.configure(
                    text="Up to date",
                    text_color=self.colors['success']
                )

    def _check_updates(self, app):
        import threading

        def check():
            has_update, version = app.updater.check_for_updates(silent=False)
            if has_update and hasattr(self, 'status_label'):
                parent = self.status_label.master.master.master.master
                parent.after(100, lambda: self._update_status(app))

        if hasattr(self, 'status_label'):
            self.status_label.configure(
                text="Checking...",
                text_color=self.colors['text_secondary']
            )

        thread = threading.Thread(target=check, daemon=True)
        thread.start()

    def _open_github_releases(self):
        if self.app and hasattr(self.app, 'updater'):
            url = f"https://github.com/{self.app.updater.GITHUB_USER}/{self.app.updater.GITHUB_REPO}/releases"
            webbrowser.open(url)

    def update_colors(self, colors):
        self.colors = colors
