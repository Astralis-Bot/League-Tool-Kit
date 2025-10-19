"""Automation View - Funcionalidades de automação - CORRIGIDO"""
import customtkinter as ctk
from ui.components import ActionCard, FeatureCard


class AutomationView:
    """View de módulos de automação"""
    
    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme
    
    def create(self, parent, app):
        """Cria a view de automação"""
        app.ui_manager.add_title("⚡ AUTOMATION")
        
        # Descrição
        desc = ctk.CTkLabel(
            app.ui_manager.scroll_area,
            text="Automate your League of Legends experience",
            font=self.theme['fonts']['small'],
            text_color=self.colors['text_secondary']
        )
        desc.pack(anchor="w", pady=(0, 20))
        
        # Container com 2 colunas
        container = ctk.CTkFrame(app.ui_manager.scroll_area, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        # COLUNA 1: Champion Automation
        self._create_champion_automation(container, app)
        
        # COLUNA 2: Game Automation
        self._create_game_automation(container, app)
        
        # ⭐ RESTAURAR ÍCONES APÓS CRIAR AS CARDS ⭐
        app.after(50, lambda: self._restore_champion_icons(app))
    
    def _create_champion_automation(self, parent, app):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            frame,
            text="🎮 CHAMPION AUTOMATION",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 15))
        
        # Instalock - COM ÍCONE
        instalock_card = FeatureCard(
            frame,
            "🔒 Instalock",
            "Automatically select your champion",
            self.colors['primary'],
            app.toggle_instalock,
            app.open_instalock_hub,
            self.colors,
            self.theme,
            is_enabled=app.instalock_enabled,
            show_icon=True
        )
        instalock_card.pack(fill="x", pady=5)
        app.ui_manager.feature_cards.append(instalock_card)
        app.ui_manager.instalock_card = instalock_card
        
        # Espaço
        app.ui_manager.add_spacing(10)
        
        # Auto Ban - COM ÍCONE
        autoban_card = FeatureCard(
            frame,
            "⛔ Auto Ban",
            "Automatically ban champion",
            self.colors['secondary'],
            app.toggle_autoban,
            app.open_autoban_hub,
            self.colors,
            self.theme,
            is_enabled=app.autoban_enabled,
            show_icon=True
        )
        autoban_card.pack(fill="x", pady=5)
        app.ui_manager.feature_cards.append(autoban_card)
        app.ui_manager.autoban_card = autoban_card

    def _create_game_automation(self, parent, app):
        """Cria seção de automação do jogo"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            frame,
            text="⚡ GAME AUTOMATION",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 15))
        
        # Auto Accept - SEM ÍCONE
        auto_accept_card = FeatureCard(
            frame,
            "✓ Auto Accept",
            "Accept matches automatically",
            self.colors['success'],
            app.toggle_auto_accept,
            None,
            self.colors,
            self.theme,
            is_enabled=app.auto_accept.auto_accept_enabled if app.auto_accept else False,
            show_icon=False
        )
        auto_accept_card.pack(fill="x", pady=5)
        app.ui_manager.feature_cards.append(auto_accept_card)
        
        # Espaço
        app.ui_manager.add_spacing(20)
        
        ctk.CTkLabel(
            frame,
            text="🚀 QUICK ACTIONS",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(15, 15))
        
        # Chat Toggle
        chat_card = ActionCard(
            frame,
            "💬 Chat Toggle",
            "Enable/disable in-game chat",
            self.colors['accent'],
            app.toggle_chat,
            self.colors,
            self.theme
        )
        chat_card.pack(fill="x", pady=5)
        app.ui_manager.action_cards.append(chat_card)
        
        # Lobby Reveal
        lobby_card = ActionCard(
            frame,
            "📊 Lobby Reveal",
            "Open Porofessor analysis",
            self.colors['info'],
            app.lobby_reveal,
            self.colors,
            self.theme
        )
        lobby_card.pack(fill="x", pady=5)
        app.ui_manager.action_cards.append(lobby_card)
        
        # Dodge Queue
        dodge_card = ActionCard(
            frame,
            "🚀 Dodge Queue",
            "Leave queue instantly",
            self.colors['warning'],
            app.dodge_queue,
            self.colors,
            self.theme
        )
        dodge_card.pack(fill="x", pady=5)
        app.ui_manager.action_cards.append(dodge_card)
    
    def _restore_champion_icons(self, app):
        """Restaura ícones dos campeões após recriar as views"""
        try:
            print("\n" + "="*60)
            print("🔄 RESTAURANDO ÍCONES APÓS RECRIAR VIEW")
            print("="*60)
            
            # Restaurar Instalock
            if app.instalock_champion:
                print(f"♻️ Restaurando Instalock: {app.instalock_champion}")
                app.champion_manager.update_instalock_display(app, app.instalock_champion)
            else:
                print("ℹ️ Nenhum campeão Instalock para restaurar")
            
            # Restaurar AutoBan
            if app.autoban_champion:
                print(f"♻️ Restaurando AutoBan: {app.autoban_champion}")
                app.champion_manager.update_autoban_display(app, app.autoban_champion)
            else:
                print("ℹ️ Nenhum campeão AutoBan para restaurar")
            
            print("="*60)
            print("✅ RESTAURAÇÃO CONCLUÍDA")
            print("="*60 + "\n")
        except Exception as e:
            print(f"❌ Erro ao restaurar ícones: {e}")
            import traceback
            traceback.print_exc()
    
    def update_colors(self, colors):
        """Atualiza as cores da view"""
        self.colors = colors