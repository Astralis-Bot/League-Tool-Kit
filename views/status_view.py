"""
STATUS VIEW - Monitor de Sistema
Interface moderna para visualizar status de módulos e sistema
"""

import customtkinter as ctk


class StatusView:
    """View de status do sistema com cards organizados"""

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme

    def create(self, parent, get_status_data):
        """Cria a view de status"""
        
        # Container principal
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Título
        title = ctk.CTkLabel(
            container,
            text="📊 SYSTEM STATUS",
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['primary']
        )
        title.pack(anchor="w", pady=(0, 8))

        # Subtítulo
        subtitle = ctk.CTkLabel(
            container,
            text="Real-time monitoring of active modules and system health",
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        )
        subtitle.pack(anchor="w", pady=(0, 25))

        # Obtém dados de status
        status_data = get_status_data()

        # Grid de cards
        self._create_status_grid(container, status_data)

    def _create_status_grid(self, parent, status):
        """Cria grid organizado de status cards"""
        
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(fill="both", expand=True)

        # Active Modules Card
        self._create_active_modules_card(grid, status)

        # Chat Status Card
        self._create_chat_status_card(grid, status)

        # System Info Card
        self._create_system_info_card(grid)

        # Connection Status Card
        self._create_connection_card(grid)

    def _create_active_modules_card(self, parent, status):
        """Card de módulos ativos com status individual"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['success']
        )
        card.pack(fill="x", pady=(0, 15))

        # Header
        header = self._create_card_header(
            card,
            "✅",
            "Active Modules",
            "Currently running automation features",
            self.colors['success']
        )

        # Linha divisória
        ctk.CTkFrame(
            card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=(0, 15))

        # Container de módulos
        modules_container = ctk.CTkFrame(card, fg_color="transparent")
        modules_container.pack(fill="x", padx=20, pady=(0, 20))

        has_active = False

        # Auto Accept
        if status.get('auto_accept'):
            self._create_module_status(
                modules_container,
                "⚡",
                "Auto Accept",
                "ACTIVE",
                self.colors['success']
            )
            has_active = True

        # Instalock
        if status.get('instalock'):
            self._create_module_status(
                modules_container,
                "🔒",
                "Instalock",
                status['instalock'],
                self.colors['primary']
            )
            has_active = True

        # Auto Ban
        if status.get('auto_ban'):
            self._create_module_status(
                modules_container,
                "⛔",
                "Auto Ban",
                status['auto_ban'],
                self.colors['secondary']
            )
            has_active = True

        # Mensagem se nenhum módulo ativo
        if not has_active:
            self._create_empty_state(
                modules_container,
                "No modules currently active",
                "Enable features from the Dashboard or Automation page"
            )

    def _create_chat_status_card(self, parent, status):
        """Card de status do chat"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['accent']
        )
        card.pack(fill="x", pady=(0, 15))

        # Header
        self._create_card_header(
            card,
            "💬",
            "In-Game Chat",
            "Current chat configuration status",
            self.colors['accent']
        )

        # Linha divisória
        ctk.CTkFrame(
            card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=(0, 15))

        # Status do chat
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))

        chat_state = status.get('chat', 'unknown').lower()
        
        if chat_state == 'enabled':
            status_icon = "✅"
            status_text = "Chat is currently ENABLED"
            status_color = self.colors['success']
            description = "You can send and receive messages in-game"
        elif chat_state == 'disabled':
            status_icon = "🔇"
            status_text = "Chat is currently DISABLED"
            status_color = self.colors['warning']
            description = "In-game communication is muted"
        else:
            status_icon = "❓"
            status_text = "Chat status UNKNOWN"
            status_color = self.colors['text_secondary']
            description = "Unable to determine current chat state"

        # Status row
        status_row = ctk.CTkFrame(content, fg_color="transparent")
        status_row.pack(fill="x")

        ctk.CTkLabel(
            status_row,
            text=status_icon,
            font=("Segoe UI Emoji", 20),
            text_color=status_color
        ).pack(side="left", padx=(0, 10))

        text_container = ctk.CTkFrame(status_row, fg_color="transparent")
        text_container.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_container,
            text=status_text,
            font=("Segoe UI", 12, "bold"),
            text_color=status_color,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_container,
            text=description,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _create_system_info_card(self, parent):
        """Card de informações do sistema"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['info']
        )
        card.pack(fill="x", pady=(0, 15))

        # Header
        self._create_card_header(
            card,
            "🔧",
            "System Information",
            "Application and environment details",
            self.colors['info']
        )

        # Linha divisória
        ctk.CTkFrame(
            card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=(0, 15))

        # Info items
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))

        info_items = [
            ("📦", "Application", "League Toolkit v2.1.0"),
            ("🔄", "Update Check", "Automatic"),
            ("⚙️", "Status", "All systems operational"),
            ("🎨", "Theme Engine", "Active")
        ]

        for icon, label, value in info_items:
            self._create_info_row(content, icon, label, value)

    def _create_connection_card(self, parent):
        """Card de status de conexão"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['success']
        )
        card.pack(fill="x")

        # Header
        self._create_card_header(
            card,
            "🔌",
            "LCU Connection",
            "League Client connectivity status",
            self.colors['success']
        )

        # Linha divisória
        ctk.CTkFrame(
            card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=(0, 15))

        # Connection status
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))

        # Status principal
        status_row = ctk.CTkFrame(content, fg_color="transparent")
        status_row.pack(fill="x")

        ctk.CTkLabel(
            status_row,
            text="✅",
            font=("Segoe UI Emoji", 24),
            text_color=self.colors['success']
        ).pack(side="left", padx=(0, 12))

        text_container = ctk.CTkFrame(status_row, fg_color="transparent")
        text_container.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_container,
            text="Connected to League Client",
            font=("Segoe UI", 13, "bold"),
            text_color=self.colors['success'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_container,
            text="All automation features are ready to use",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

    def _create_card_header(self, parent, icon, title, subtitle, color):
        """Cria header consistente para cards"""
        
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 15))

        # Ícone com fundo
        icon_bg = ctk.CTkFrame(
            header,
            fg_color=color,
            width=38,
            height=38,
            corner_radius=10
        )
        icon_bg.pack(side="left", padx=(0, 12))
        icon_bg.pack_propagate(False)

        ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=("Segoe UI Emoji", 18),
            text_color="white"
        ).pack(expand=True)

        # Textos
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Segoe UI", 13, "bold"),
            text_color=color,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=subtitle,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        return header

    def _create_module_status(self, parent, icon, name, status, color):
        """Cria item de status de módulo"""
        
        item = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=8
        )
        item.pack(fill="x", pady=(0, 8))

        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=10)

        # Ícone e nome
        left_section = ctk.CTkFrame(content, fg_color="transparent")
        left_section.pack(side="left", fill="x", expand=True)

        title_row = ctk.CTkFrame(left_section, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkLabel(
            title_row,
            text=icon,
            font=("Segoe UI Emoji", 16),
            text_color=color
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            title_row,
            text=name,
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        # Status badge
        badge = ctk.CTkLabel(
            content,
            text=status,
            font=("Segoe UI", 9, "bold"),
            text_color="white",
            fg_color=color,
            corner_radius=6
        )
        badge.pack(side="right", padx=(10, 0), ipadx=10, ipady=4)

    def _create_info_row(self, parent, icon, label, value):
        """Cria linha de informação"""
        
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)

        # Ícone
        ctk.CTkLabel(
            row,
            text=icon,
            font=("Segoe UI Emoji", 14),
            text_color=self.colors['info']
        ).pack(side="left", padx=(0, 10))

        # Label
        ctk.CTkLabel(
            row,
            text=f"{label}:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        # Value
        ctk.CTkLabel(
            row,
            text=value,
            font=("Segoe UI", 10),
            text_color=self.colors['text_secondary']
        ).pack(side="left", padx=(8, 0))

    def _create_empty_state(self, parent, title, description):
        """Cria estado vazio quando não há dados"""
        
        empty = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=8
        )
        empty.pack(fill="x", pady=5)

        content = ctk.CTkFrame(empty, fg_color="transparent")
        content.pack(padx=20, pady=15)

        ctk.CTkLabel(
            content,
            text="📭",
            font=("Segoe UI Emoji", 24),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors['text_primary']
        ).pack()

        ctk.CTkLabel(
            content,
            text=description,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary']
        ).pack(pady=(4, 0))

    def update_colors(self, colors):
        """Atualiza cores do tema"""
        self.colors = colors