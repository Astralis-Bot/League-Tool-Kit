"""Champions View - Gerenciamento de campeões"""
import customtkinter as ctk
from ui.components import FeatureCard


class ChampionsView:
    """View de configuração de campeões"""
    
    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme
    
    def create(self, parent, app):
        """Cria a view de campeões"""
        app.ui_manager.add_title("🎮 CHAMPION SETTINGS")
        
        # Descrição
        desc = ctk.CTkLabel(
            app.ui_manager.scroll_area,
            text="Configure automatic champion selection and banning",
            font=self.theme['fonts']['small'],
            text_color=self.colors['text_secondary']
        )
        desc.pack(anchor="w", pady=(0, 20))
        
        # Instalock Card
        instalock_card = FeatureCard(
            app.ui_manager.scroll_area,
            "🔒 INSTALOCK",
            f"Selected: {app.instalock_champion}" if app.instalock_champion else "No champion selected",
            self.colors['primary'],
            app.toggle_instalock,
            app.open_instalock_hub,
            self.colors,
            self.theme,
            is_enabled=app.instalock_enabled
        )
        app.ui_manager.add_feature_card(instalock_card)
        
        # Auto Ban Card
        autoban_card = FeatureCard(
            app.ui_manager.scroll_area,
            "⛔ AUTO BAN",
            f"Selected: {app.autoban_champion}" if app.autoban_champion else "No champion selected",
            self.colors['secondary'],
            app.toggle_autoban,
            app.open_autoban_hub,
            self.colors,
            self.theme,
            is_enabled=app.autoban_enabled
        )
        app.ui_manager.add_feature_card(autoban_card)
        
        # Info Card
        info_frame = ctk.CTkFrame(
            app.ui_manager.scroll_area,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['info']
        )
        info_frame.pack(fill="x", pady=(20, 0))
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            info_content,
            text="💡 Tips",
            font=self.theme['fonts']['subheading'],
            text_color=self.colors['info']
        ).pack(anchor="w", pady=(0, 10))
        
        tips = [
            "• Click the ⚙️ button to select your champion",
            "• Instalock works in blind pick and draft pick",
            "• Auto Ban only works in ranked and draft pick",
            "• Toggle ON to enable the feature",
            "• The champion icon will appear when selected"
        ]
        
        for tip in tips:
            ctk.CTkLabel(
                info_content,
                text=tip,
                font=self.theme['fonts']['small'],
                text_color=self.colors['text_secondary'],
                anchor="w"
            ).pack(anchor="w", pady=2)
    
    def update_colors(self, colors):
        """Atualiza as cores da view"""
        self.colors = colors