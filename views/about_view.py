# views/about_view.py
"""About View - Informações sobre o aplicativo"""
import customtkinter as ctk


class AboutView:
    """View de informações sobre o app"""
    
    def __init__(self, colors, theme):
        self.colors = colors
        self.theme = theme
    
    def create(self, parent):
        """Cria a view de about"""
        # Container principal
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        # Título
        title = ctk.CTkLabel(
            container,
            text="ℹ️ ABOUT",
            font=("Consolas", 24, "bold"),
            text_color=self.colors['primary']
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Main Info Card
        info_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_card'],
            corner_radius=self.theme['radius']['lg'],
            border_width=2,
            border_color=self.colors['primary']
        )
        info_card.pack(fill="x", pady=10, padx=20)
        
        # App Info
        self._create_app_info(info_card)
        
        # Divider
        ctk.CTkFrame(
            info_card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=10)
        
        # Credits
        self._create_credits(info_card)
        
        # Divider
        ctk.CTkFrame(
            info_card,
            fg_color=self.colors['bg_light'],
            height=2
        ).pack(fill="x", padx=20, pady=10)
        
        # Features
        self._create_features(info_card)
    
    def _create_app_info(self, parent):
        """Cria seção de informações do app"""
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
            font=("Consolas", 18, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            name_frame,
            text="League Automation Toolkit v2.0",
            font=("Consolas", 11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
        
        ctk.CTkLabel(
            app_frame,
            text="Advanced automation toolkit for League of Legends",
            font=("Consolas", 10),
            text_color=self.colors['text_secondary'],
            justify="left"
        ).pack(anchor="w", pady=(10, 0))
    
    def _create_credits(self, parent):
        """Cria seção de créditos"""
        credits_frame = ctk.CTkFrame(parent, fg_color="transparent")
        credits_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            credits_frame,
            text="👨‍💻 Credits & Developers",
            font=("Consolas", 14, "bold"),
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
                font=("Consolas", 12, "bold"),
                text_color=self.colors['primary']
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                dev_content,
                text=dev_role,
                font=("Consolas", 9),
                text_color=self.colors['text_secondary']
            ).pack(anchor="w", pady=(2, 0))
    
    def _create_features(self, parent):
        """Cria seção de features"""
        features_frame = ctk.CTkFrame(parent, fg_color="transparent")
        features_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            features_frame,
            text="⚡ Features",
            font=("Consolas", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(anchor="w", pady=(0, 10))
        
        features_list = [
            ("🔒 Instalock", "Instant champion selection"),
            ("⛔ Auto Ban", "Automatic champion banning"),
            ("✓ Auto Accept", "Auto-accept queue matches"),
            ("💬 Chat Toggle", "Enable/disable in-game chat"),
            ("📊 Lobby Reveal", "Open Porofessor analysis"),
            ("🚀 Dodge Queue", "Quick queue dodging"),
            ("🎨 Theme Selector", "Manage and import themes")
        ]
        
        for icon_title, description in features_list:
            feature_item = ctk.CTkFrame(features_frame, fg_color="transparent")
            feature_item.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                feature_item,
                text=icon_title,
                font=("Consolas", 11, "bold"),
                text_color=self.colors['primary'],
                anchor="w",
                width=120
            ).pack(side="left")
            
            ctk.CTkLabel(
                feature_item,
                text=f"- {description}",
                font=("Consolas", 10),
                text_color=self.colors['text_secondary'],
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
    
    def update_colors(self, colors):
        """Atualiza as cores da view"""
        self.colors = colors