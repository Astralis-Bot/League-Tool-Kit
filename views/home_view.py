import customtkinter as ctk 
from ui.components import ActionCard, FeatureCard 


class HomeView:

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme

    def create(self, parent, app):
        app.ui_manager.add_title("⚡ DASHBOARD")

        desc = ctk.CTkLabel(
            app.ui_manager.scroll_area,
            text="Quick access to all features with backup system",
            font=self.theme['fonts']['small'],
            text_color=self.colors['text_secondary']
        )
        desc.pack(anchor="w", pady=(0, 20))

        # Grid principal
        grid_container = ctk.CTkFrame(app.ui_manager.scroll_area, fg_color="transparent")
        grid_container.pack(fill="both", expand=True)
        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=1)

        self._create_champion_column(grid_container, app)
        self._create_actions_column(grid_container, app)

        # Seção de configurações avançadas
        self._create_advanced_settings(app.ui_manager.scroll_area, app)

        app.after(50, lambda: self._restore_champion_icons(app))

    def _create_champion_column(self, parent, app):
        champ_frame = ctk.CTkFrame(parent, fg_color="transparent")
        champ_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            champ_frame,
            text="🎮 CHAMPION AUTOMATION",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 10))

        instalock_desc = self._get_instalock_description(app)

        instalock_card = FeatureCard(
            champ_frame,
            "🔒 INSTALOCK",
            instalock_desc,
            self.colors['primary'],
            app.toggle_instalock,
            app.open_instalock_hub,
            self.colors,
            self.theme,
            is_enabled=app.instalock_enabled,
            show_icon=True
        )
        app.ui_manager.add_feature_card(instalock_card)

        autoban_desc = f"Selected: {app.autoban_champion}" if app.autoban_champion else "No champion selected"
        autoban_card = FeatureCard(
            champ_frame,
            "⛔ AUTO BAN",
            autoban_desc,
            self.colors['secondary'],
            app.toggle_autoban,
            app.open_autoban_hub,
            self.colors,
            self.theme,
            is_enabled=app.autoban_enabled,
            show_icon=True
        )
        app.ui_manager.add_feature_card(autoban_card)

    def _create_actions_column(self, parent, app):
        quick_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quick_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            quick_frame,
            text="⚡ QUICK ACTIONS",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 10))

        auto_accept_card = FeatureCard(
            quick_frame,
            "✓ AUTO ACCEPT",
            "Accept matches automatically",
            self.colors['success'],
            app.toggle_auto_accept,
            None,
            self.colors,
            self.theme,
            is_enabled=app.auto_accept.auto_accept_enabled if app.auto_accept else False,
            show_icon=False
        )
        app.ui_manager.add_feature_card(auto_accept_card)

        chat_card = ActionCard(
            quick_frame,
            "💬 CHAT TOGGLE",
            "Enable/disable in-game chat",
            self.colors['accent'],
            app.toggle_chat,
            self.colors,
            self.theme
        )
        app.ui_manager.add_action_card(chat_card)

        lobby_card = ActionCard(
            quick_frame,
            "📊 LOBBY REVEAL",
            "Open Porofessor analysis",
            self.colors['info'],
            app.lobby_reveal,
            self.colors,
            self.theme
        )
        app.ui_manager.add_action_card(lobby_card)

    def _create_advanced_settings(self, parent, app):
        """Seção de configurações avançadas organizada"""
        
        # Espaçamento
        ctk.CTkFrame(parent, fg_color="transparent", height=30).pack()

        # Card principal
        advanced_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['accent']
        )
        advanced_card.pack(fill="x", pady=(10, 0))

        # Header
        header = ctk.CTkFrame(advanced_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 12))

        header_left = ctk.CTkFrame(header, fg_color="transparent")
        header_left.pack(side="left")

        # Ícone
        icon_frame = ctk.CTkFrame(
            header_left,
            fg_color=self.colors['accent'],
            width=36,
            height=36,
            corner_radius=10
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(
            icon_frame,
            text="🎛️",
            font=("Segoe UI Emoji", 18),
            text_color="white"
        ).pack(expand=True)

        # Texto
        text_frame = ctk.CTkFrame(header_left, fg_color="transparent")
        text_frame.pack(side="left")

        ctk.CTkLabel(
            text_frame,
            text="Advanced Settings",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['accent'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Configure champion select behavior",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w")

        # Container de settings
        settings_container = ctk.CTkFrame(advanced_card, fg_color="transparent")
        settings_container.pack(fill="x", padx=20, pady=(0, 15))

        # Protect Ally Picks
        self._create_compact_toggle(
            settings_container,
            icon="🛡️",
            title="Protect Ally Picks",
            description="Avoid banning ally champions",
            color=self.colors['success'],
            initial_state=getattr(app.instalock_autoban, 'avoid_ally_hovers', True),
            command=lambda: self._toggle_ally_protection(app)
        )

    def _create_compact_toggle(self, parent, icon, title, description, color, initial_state, command):
        """Toggle compacto e organizado"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=10,
            border_width=2,
            border_color=color
        )
        card.pack(fill="x", pady=(0, 8))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=10)

        # Linha superior: ícone e textos
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")

        # Ícone
        ctk.CTkLabel(
            top_row,
            text=icon,
            font=("Segoe UI Emoji", 20),
            text_color=color
        ).pack(side="left", padx=(0, 10))

        # Textos
        text_container = ctk.CTkFrame(top_row, fg_color="transparent")
        text_container.pack(side="left", fill="x", expand=True)

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
            font=("Segoe UI", 8),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w")

        # Linha inferior: switch centralizado
        switch_container = ctk.CTkFrame(content, fg_color="transparent")
        switch_container.pack(fill="x", pady=(8, 0))

        # Cria switch sem passar command diretamente
        switch = ctk.CTkSwitch(
            switch_container,
            text="",
            width=44,
            height=22,
            switch_width=44,
            switch_height=22,
            fg_color=self.colors['bg_medium'],
            progress_color=color,
            button_color=self.colors['text_primary'],
            button_hover_color=self.colors['bg_dark']
        )
        switch.pack()

        # Configura command que chama o callback
        switch.configure(command=command)

        # Define estado inicial
        if initial_state:
            switch.select()
        else:
            switch.deselect()

    def _toggle_ally_protection(self, app):
        """Toggle proteção de aliados"""
        try:
            # Inverte o estado atual
            current_state = getattr(app.instalock_autoban, 'avoid_ally_hovers', True)
            new_state = not current_state
            
            app.instalock_autoban.avoid_ally_hovers = new_state
            status = "✅ ON" if new_state else "❌ OFF"
            print(f"Protect Ally Picks: {status}")
            
            # Feedback visual

        except Exception as e:
            print(f"❌ Erro ao alternar proteção: {e}")

    def _show_mini_toast(self, app, message, toast_type="info"):
        """Notificação toast compacta"""
        try:
            color_map = {
                "info": self.colors['info'],
                "success": self.colors['success'],
                "warning": self.colors['warning'],
                "error": self.colors['danger']
            }
            
            toast_color = color_map.get(toast_type, self.colors['info'])
            
            # Toast no canto superior direito
            toast = ctk.CTkFrame(
                app,
                fg_color=toast_color,
                corner_radius=8,
                border_width=2,
                border_color=self.colors['bg_dark']
            )
            
            toast.place(relx=0.98, rely=0.02, anchor="ne")
            
            toast_content = ctk.CTkFrame(toast, fg_color="transparent")
            toast_content.pack(padx=16, pady=10)
            
            ctk.CTkLabel(
                toast_content,
                text=message,
                font=("Segoe UI", 10, "bold"),
                text_color="white"
            ).pack()
            
            # Remove após 2 segundos
            toast.after(2000, toast.destroy)
            
        except Exception as e:
            print(f"Erro ao mostrar toast: {e}")

    def _get_instalock_description(self, app):
        """Descrição com sistema de backup"""
        if not app.instalock_champion:
            return "No champion selected"

        parts = [f"1st: {app.instalock_champion}"]

        if app.instalock_backup_2:
            parts.append(f"2nd: {app.instalock_backup_2}")

        if app.instalock_backup_3:
            parts.append(f"3rd: {app.instalock_backup_3}")

        return " | ".join(parts)

    def _restore_champion_icons(self, app):
        """Restaura ícones após recriar view"""
        try:
            print("\n" + "=" * 60)
            print("🔄 RESTAURANDO ÍCONES APÓS RECRIAR VIEW")
            print("=" * 60)

            if app.instalock_champion:
                print(f"♻️ Restaurando Instalock: {app.instalock_champion}")
                app.champion_manager.update_instalock_display(app, app.instalock_champion)
            else:
                print("ℹ️ Nenhum campeão Instalock para restaurar")

            if app.autoban_champion:
                print(f"♻️ Restaurando AutoBan: {app.autoban_champion}")
                app.champion_manager.update_autoban_display(app, app.autoban_champion)
            else:
                print("ℹ️ Nenhum campeão AutoBan para restaurar")

            print("=" * 60)
            print("✅ RESTAURAÇÃO CONCLUÍDA")
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"❌ Erro ao restaurar ícones: {e}")
            import traceback
            traceback.print_exc()

    def update_colors(self, colors):
        """Atualiza cores do tema"""
        self.colors = colors