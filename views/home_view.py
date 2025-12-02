"""
HOME VIEW - Dashboard Principal
Interface moderna com quick access e configurações avançadas
"""

import customtkinter as ctk
from ui.components import ActionCard, FeatureCard


class HomeView:
    """View principal com dashboard e acesso rápido às features"""

    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme
        self.toggle_switches = {}  # Armazena referências aos switches

    def create(self, parent, app):
        """Cria a view principal do dashboard"""
        
        # Título principal
        app.ui_manager.add_title("⚡ DASHBOARD")

        # Descrição
        desc = ctk.CTkLabel(
            app.ui_manager.scroll_area,
            text="Quick access to all features with intelligent backup system",
            font=self.theme['fonts']['small'],
            text_color=self.colors['text_secondary']
        )
        desc.pack(anchor="w", pady=(0, 20))

        # Container principal em grid
        main_container = self._create_main_grid(app.ui_manager.scroll_area)
        
        # Colunas principais
        self._create_champion_column(main_container, app)
        self._create_actions_column(main_container, app)

        # Configurações avançadas
        self._create_advanced_settings_section(app.ui_manager.scroll_area, app)

        # Restaura ícones após renderização
        app.after(50, lambda: self._restore_champion_icons(app))

    def _create_main_grid(self, parent):
        """Cria grid principal responsivo"""
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        return grid

    def _create_champion_column(self, parent, app):
        """Coluna de automação de campeões"""
        
        column = ctk.CTkFrame(parent, fg_color="transparent")
        column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Header da seção
        self._create_section_header(
            column,
            "🎮 CHAMPION AUTOMATION",
            "Automatic selection and banning"
        )

        # Instalock Card
        instalock_desc = self._build_instalock_description(app)
        instalock_card = FeatureCard(
            column,
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

        # Auto Ban Card
        autoban_desc = self._build_autoban_description(app)
        autoban_card = FeatureCard(
            column,
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
        """Coluna de ações rápidas"""
        
        column = ctk.CTkFrame(parent, fg_color="transparent")
        column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Auto Accept Section
        self._create_section_header(
            column,
            "⚡ GAME AUTOMATION",
            "Queue and match automation"
        )

        auto_accept_card = FeatureCard(
            column,
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

        # Quick Actions Section
        ctk.CTkFrame(column, fg_color="transparent", height=20).pack()
        
        self._create_section_header(
            column,
            "🚀 QUICK ACTIONS",
            "One-click utilities"
        )

        # Chat Toggle
        chat_card = ActionCard(
            column,
            "💬 CHAT TOGGLE",
            "Enable/disable in-game chat",
            self.colors['accent'],
            app.toggle_chat,
            self.colors,
            self.theme
        )
        app.ui_manager.add_action_card(chat_card)

        # Lobby Reveal
        lobby_card = ActionCard(
            column,
            "📊 LOBBY REVEAL",
            "Open Porofessor analysis",
            self.colors['info'],
            app.lobby_reveal,
            self.colors,
            self.theme
        )
        app.ui_manager.add_action_card(lobby_card)

    def _create_section_header(self, parent, title, subtitle):
        """Cria header de seção consistente"""
        
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(
            header,
            text=title,
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w")

        if subtitle:
            ctk.CTkLabel(
                header,
                text=subtitle,
                font=("Segoe UI", 9),
                text_color=self.colors['text_secondary']
            ).pack(anchor="w", pady=(2, 0))

    def _create_advanced_settings_section(self, parent, app):
        """Seção de configurações avançadas com toggles organizados"""
        
        # Espaçamento
        ctk.CTkFrame(parent, fg_color="transparent", height=30).pack()

        # Card principal
        settings_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['accent']
        )
        settings_card.pack(fill="x", pady=(10, 0))

        # Header elegante
        self._create_advanced_header(settings_card)

        # Container de settings
        settings_container = ctk.CTkFrame(settings_card, fg_color="transparent")
        settings_container.pack(fill="x", padx=20, pady=(0, 20))

        # Toggle: Pre-Hover Champion
        self._create_setting_toggle(
            settings_container,
            icon="👆",
            title="Pre-Hover Champion",
            description="Show your pick intention before ban phase",
            color=self.colors['primary'],
            setting_key="pre_hover",
            initial_state=getattr(app.instalock_autoban, 'pre_hover_enabled', True),
            callback=lambda state: self._handle_pre_hover_toggle(app, state)
        )

        # Toggle: Protect Ally Picks
        self._create_setting_toggle(
            settings_container,
            icon="🛡️",
            title="Protect Ally Picks",
            description="Avoid banning champions your allies want to play",
            color=self.colors['success'],
            setting_key="protect_allies",
            initial_state=getattr(app.instalock_autoban, 'avoid_ally_hovers', True),
            callback=lambda state: self._handle_ally_protection_toggle(app, state)
        )

    def _create_advanced_header(self, parent):
        """Header moderno para configurações avançadas"""
        
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 15))

        # Container horizontal
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x")

        # Ícone com fundo
        icon_bg = ctk.CTkFrame(
            header_content,
            fg_color=self.colors['accent'],
            width=40,
            height=40,
            corner_radius=12
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        ctk.CTkLabel(
            icon_bg,
            text="🎛️",
            font=("Segoe UI Emoji", 20),
            text_color="white"
        ).pack(expand=True)

        # Textos
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text="Advanced Settings",
            font=("Segoe UI", 15, "bold"),
            text_color=self.colors['accent'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Fine-tune champion select behavior",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Linha decorativa
        ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20)

    def _create_setting_toggle(self, parent, icon, title, description, color, 
                               setting_key, initial_state, callback):
        """Cria toggle de configuração moderno e interativo"""
        
        # Card do setting
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=12,
            border_width=2,
            border_color=color
        )
        card.pack(fill="x", pady=(0, 10))

        # Efeito hover
        def on_enter(e):
            card.configure(border_color=self.colors['primary'])
        
        def on_leave(e):
            card.configure(border_color=color)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)

        # Layout horizontal
        left_section = ctk.CTkFrame(content, fg_color="transparent")
        left_section.pack(side="left", fill="x", expand=True)

        # Linha do ícone e título
        title_row = ctk.CTkFrame(left_section, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkLabel(
            title_row,
            text=icon,
            font=("Segoe UI Emoji", 22),
            text_color=color
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            title_row,
            text=title,
            font=("Segoe UI", 12, "bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        ).pack(side="left")

        # Descrição
        ctk.CTkLabel(
            left_section,
            text=description,
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w",
            wraplength=400
        ).pack(anchor="w", padx=(34, 0), pady=(4, 0))

        # Switch moderno
        switch = ctk.CTkSwitch(
            content,
            text="",
            width=50,
            height=26,
            switch_width=50,
            switch_height=26,
            fg_color=self.colors['bg_medium'],
            progress_color=color,
            button_color="white",
            button_hover_color=self.colors['bg_card'],
            command=lambda: callback(switch.get())
        )
        switch.pack(side="right", padx=(15, 0))

        # Define estado inicial
        if initial_state:
            switch.select()
        else:
            switch.deselect()

        # Armazena referência
        self.toggle_switches[setting_key] = switch

    def _handle_pre_hover_toggle(self, app, state):
        """Handler para toggle de pre-hover"""
        try:
            app.instalock_autoban.pre_hover_enabled = bool(state)
            
            status = "✅ ENABLED" if state else "❌ DISABLED"
            message = "Your pick will be shown early" if state else "Pre-hover disabled"
            
            print(f"👆 Pre-Hover: {status}")
            print(f"   {message}")
            
            self._show_feedback_toast(
                app,
                f"Pre-Hover {status}",
                "info" if state else "warning"
            )
            
        except Exception as e:
            print(f"❌ Error toggling pre-hover: {e}")
            import traceback
            traceback.print_exc()

    def _handle_ally_protection_toggle(self, app, state):
        """Handler para toggle de proteção de aliados"""
        try:
            app.instalock_autoban.avoid_ally_hovers = bool(state)
            
            status = "✅ ENABLED" if state else "❌ DISABLED"
            message = "Won't ban ally champions" if state else "Protection disabled"
            
            print(f"🛡️ Ally Protection: {status}")
            print(f"   {message}")
            
            self._show_feedback_toast(
                app,
                f"Ally Protection {status}",
                "success" if state else "warning"
            )
            
        except Exception as e:
            print(f"❌ Error toggling protection: {e}")
            import traceback
            traceback.print_exc()

    def _show_feedback_toast(self, app, message, toast_type="info"):
        """Toast de feedback visual elegante"""
        try:
            color_map = {
                "info": self.colors['info'],
                "success": self.colors['success'],
                "warning": self.colors['warning'],
                "error": self.colors['danger']
            }
            
            bg_color = color_map.get(toast_type, self.colors['info'])
            
            # Toast no topo direito
            toast = ctk.CTkFrame(
                app,
                fg_color=bg_color,
                corner_radius=10,
                border_width=2,
                border_color="white"
            )
            toast.place(relx=0.98, rely=0.02, anchor="ne")

            # Conteúdo
            content = ctk.CTkFrame(toast, fg_color="transparent")
            content.pack(padx=18, pady=12)

            ctk.CTkLabel(
                content,
                text=message,
                font=("Segoe UI", 11, "bold"),
                text_color="white"
            ).pack()

            # Animação de saída
            def fade_out():
                try:
                    toast.destroy()
                except:
                    pass

            toast.after(2500, fade_out)
            
        except Exception as e:
            print(f"Erro no toast: {e}")

    def _build_instalock_description(self, app):
        """Constrói descrição do instalock com backups"""
        if not app.instalock_champion:
            return "No champion selected"

        picks = [f"1st: {app.instalock_champion}"]

        if app.instalock_backup_2:
            picks.append(f"2nd: {app.instalock_backup_2}")

        if app.instalock_backup_3:
            picks.append(f"3rd: {app.instalock_backup_3}")

        return " | ".join(picks)

    def _build_autoban_description(self, app):
        """Constrói descrição do autoban com backups"""
        if not app.autoban_champion:
            return "No champion selected"

        bans = [f"1st: {app.autoban_champion}"]

        if hasattr(app, 'autoban_backup_2') and app.autoban_backup_2:
            bans.append(f"2nd: {app.autoban_backup_2}")

        if hasattr(app, 'autoban_backup_3') and app.autoban_backup_3:
            bans.append(f"3rd: {app.autoban_backup_3}")

        return " | ".join(bans)

    def _restore_champion_icons(self, app):
        """Restaura ícones de campeões após recriar view"""
        try:
            print("\n" + "=" * 60)
            print("🔄 RESTORING CHAMPION ICONS")
            print("=" * 60)

            if app.instalock_champion:
                print(f"♻️ Restoring Instalock: {app.instalock_champion}")
                app.champion_manager.update_instalock_display(app, app.instalock_champion)
            else:
                print("ℹ️ No Instalock champion to restore")

            if app.autoban_champion:
                print(f"♻️ Restoring AutoBan: {app.autoban_champion}")
                app.champion_manager.update_autoban_display(app, app.autoban_champion)
            else:
                print("ℹ️ No AutoBan champion to restore")

            print("=" * 60)
            print("✅ RESTORATION COMPLETED")
            print("=" * 60 + "\n")
            
        except Exception as e:
            print(f"❌ Error restoring icons: {e}")
            import traceback
            traceback.print_exc()

    def update_colors(self, colors):
        """Atualiza cores do tema"""
        self.colors = colors