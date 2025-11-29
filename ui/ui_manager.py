import customtkinter as ctk
from ui.ui_config import COLORS, THEME
from ui.components import Sidebar, StatusBar


class UIManager:
    """Premium UI Manager with modern layout"""
    
    def __init__(self, app, colors=None, theme=None):
        self.app = app
        self.colors = colors or COLORS
        self.theme = theme or THEME
        self.components = {}
        self.feature_cards = []
        self.action_cards = []
        self.main_frame = None
        self.content_frame = None
        self.scroll_area = None
        self.header_frame = None
        self.status_bar = None
        self.sidebar = None
        
        self.instalock_card = None
        self.autoban_card = None
    
    def create_main_layout(self):
        """Create premium layout with modern design"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(
            self.app,
            fg_color=self.colors.get('bg_dark')
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(
            self.main_frame,
            self.app.switch_category,
            self.colors,
            self.theme
        )
        self.sidebar.pack(side="left", fill="y")
        self.components['sidebar'] = self.sidebar
        
        # Right section (header + content + statusbar)
        right_section = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors.get('bg_medium')
        )
        right_section.pack(side="left", fill="both", expand=True)
        
        # Premium header
        self.create_premium_header(right_section)
        
        # Scrollable content with custom styling
        self.scroll_area = ctk.CTkScrollableFrame(
            right_section,
            fg_color=self.colors.get('bg_medium'),
            corner_radius=0,
            scrollbar_button_color=self.colors.get('bg_elevated'),
            scrollbar_button_hover_color=self.colors.get('primary')
        )
        self.scroll_area.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=20
        )
        self.components['scroll_area'] = self.scroll_area
        
        # Modern status bar
        self.status_bar = StatusBar(
            right_section,
            self.app.get_status_data,
            self.colors,
            self.theme
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.components['status_bar'] = self.status_bar
    
    def create_premium_header(self, parent):
        """Create premium header with glassmorphism"""
        
        self.header_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors.get('bg_elevated'),
            height=100,
            corner_radius=0,
            border_width=2,
            border_color=self.colors.get('border_color')
        )
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        
        content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32, pady=20)
        
        # Left: Page info with icon
        left_section = ctk.CTkFrame(content, fg_color="transparent")
        left_section.pack(side="left", fill="y")
        
        # Icon circle
        icon_container = ctk.CTkFrame(
            left_section,
            fg_color=self.colors.get('primary'),
            width=60,
            height=60,
            corner_radius=16
        )
        icon_container.pack(side="left", padx=(0, 20))
        icon_container.pack_propagate(False)
        
        self.header_icon = ctk.CTkLabel(
            icon_container,
            text="⚡",
            font=("Segoe UI Emoji", 28),
            text_color="white"
        )
        self.header_icon.pack(expand=True)
        self.components['header_icon'] = self.header_icon
        
        # Text info
        text_section = ctk.CTkFrame(left_section, fg_color="transparent")
        text_section.pack(side="left", fill="y")
        
        self.header_title = ctk.CTkLabel(
            text_section,
            text="DASHBOARD",
            font=("Segoe UI", 22, "bold"),
            text_color=self.colors.get('text_primary'),
            anchor="w"
        )
        self.header_title.pack(anchor="w")
        self.components['header_title'] = self.header_title
        
        self.header_subtitle = ctk.CTkLabel(
            text_section,
            text="Manage your automation features",
            font=("Segoe UI", 11),
            text_color=self.colors.get('text_secondary'),
            anchor="w"
        )
        self.header_subtitle.pack(anchor="w", pady=(4, 0))
        self.components['header_subtitle'] = self.header_subtitle
        
        # Right: Quick actions
        right_section = ctk.CTkFrame(content, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Active features counter
        self.active_badge = ctk.CTkFrame(
            right_section,
            fg_color=self.colors.get('bg_card'),
            corner_radius=12,
            border_width=2,
            border_color=self.colors.get('success')
        )
        self.active_badge.pack(side="left", padx=(0, 12))
        
        active_content = ctk.CTkFrame(self.active_badge, fg_color="transparent")
        active_content.pack(padx=16, pady=10)
        
        ctk.CTkLabel(
            active_content,
            text="⚡",
            font=("Segoe UI Emoji", 16),
            text_color=self.colors.get('success')
        ).pack(side="left", padx=(0, 8))
        
        self.active_count = ctk.CTkLabel(
            active_content,
            text="0 Active",
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors.get('success')
        )
        self.active_count.pack(side="left")
        self.components['active_count'] = self.active_count
        

    
    def clear_scroll_area(self):
        """Clear scroll area"""
        for widget in self.scroll_area.winfo_children():
            widget.destroy()
        self.feature_cards = []
        self.action_cards = []
    
    def add_title(self, text, icon="⚡"):
        """Add modern section title"""
        title_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        title_container.pack(fill="x", pady=(0, 24))
        
        # Icon background
        icon_bg = ctk.CTkFrame(
            title_container,
            fg_color=self.colors.get('bg_card'),
            width=48,
            height=48,
            corner_radius=12,
            border_width=2,
            border_color=self.colors.get('primary')
        )
        icon_bg.pack(side="left", padx=(0, 16))
        icon_bg.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=("Segoe UI Emoji", 20),
            text_color=self.colors.get('primary')
        ).pack(expand=True)
        
        # Text section
        text_section = ctk.CTkFrame(title_container, fg_color="transparent")
        text_section.pack(side="left", fill="both", expand=True)
        
        title = ctk.CTkLabel(
            text_section,
            text=text,
            font=("Segoe UI", 26, "bold"),
            text_color=self.colors.get('text_primary'),
            anchor="w"
        )
        title.pack(anchor="w")
        
        # Decorative line
        line = ctk.CTkFrame(
            text_section,
            fg_color=self.colors.get('primary'),
            height=3,
            corner_radius=2
        )
        line.pack(fill="x", anchor="w", pady=(8, 0))
        
        return title
    
    def add_section_title(self, text):
        """Add subsection title"""
        section = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        section.pack(fill="x", pady=(20, 16))
        
        # Dot indicator
        ctk.CTkLabel(
            section,
            text="●",
            font=("Segoe UI", 16),
            text_color=self.colors.get('primary')
        ).pack(side="left", padx=(0, 12))
        
        # Title
        title = ctk.CTkLabel(
            section,
            text=text,
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors.get('text_primary'),
            anchor="w"
        )
        title.pack(side="left")
        
        return title
    
    def add_spacing(self, height=20):
        """Add spacing"""
        ctk.CTkFrame(
            self.scroll_area,
            fg_color="transparent",
            height=height
        ).pack()
    
    def add_feature_card(self, card):
        """Add feature card with spacing"""
        card.pack(fill="x", pady=12)
        self.feature_cards.append(card)
        
        if "Instalock" in card.title_text or "instalock" in card.title_text.lower():
            self.instalock_card = card
        elif "Auto Ban" in card.title_text or "autoban" in card.title_text.lower():
            self.autoban_card = card
        
        return card
    
    def add_action_card(self, card):
        """Add action card with spacing"""
        card.pack(fill="x", pady=12)
        self.action_cards.append(card)
        return card
    
    def create_info_panel(self, title, items, icon="💡"):
        """Create premium info panel"""
        panel = ctk.CTkFrame(
            self.scroll_area,
            fg_color=self.colors.get('bg_card'),
            corner_radius=16,
            border_width=2,
            border_color=self.colors.get('info')
        )
        panel.pack(fill="x", pady=(20, 0))
        
        content = ctk.CTkFrame(panel, fg_color="transparent")
        content.pack(fill="x", padx=24, pady=20)
        
        # Header with icon
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))
        
        # Icon circle
        icon_circle = ctk.CTkFrame(
            header,
            fg_color=self.colors.get('info'),
            width=36,
            height=36,
            corner_radius=18
        )
        icon_circle.pack(side="left", padx=(0, 12))
        icon_circle.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_circle,
            text=icon,
            font=("Segoe UI Emoji", 18),
            text_color="white"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 15, "bold"),
            text_color=self.colors.get('info')
        ).pack(side="left")
        
        # Items
        for item in items:
            item_frame = ctk.CTkFrame(content, fg_color="transparent")
            item_frame.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                item_frame,
                text="›",
                font=("Segoe UI", 14, "bold"),
                text_color=self.colors.get('primary')
            ).pack(side="left", padx=(0, 8))
            
            ctk.CTkLabel(
                item_frame,
                text=item,
                font=("Segoe UI", 11),
                text_color=self.colors.get('text_secondary'),
                anchor="w",
                justify="left"
            ).pack(side="left", fill="x", expand=True)
        
        return panel
    
    def update_active_count(self):
        """Update active features counter"""
        try:
            count = sum(1 for card in self.feature_cards if card.is_enabled)
            if hasattr(self, 'components') and 'active_count' in self.components:
                self.components['active_count'].configure(
                    text=f"{count} Active" if count > 0 else "None Active"
                )
        except:
            pass
    
    def update_colors(self, colors):
        """Update all colors"""
        self.colors = colors
        
        self.app.configure(fg_color=colors.get('bg_dark'))
        self.main_frame.configure(fg_color=colors.get('bg_dark'))
        self.scroll_area.configure(fg_color=colors.get('bg_medium'))
        self.header_frame.configure(
            fg_color=colors.get('bg_elevated'),
            border_color=colors.get('border_color')
        )
        
        if self.sidebar:
            self.sidebar.update_colors(colors)
        
        if self.status_bar:
            self.status_bar.update_colors(colors)
        
        for card in self.feature_cards:
            if hasattr(card, 'update_colors'):
                card.update_colors(colors)
        
        for card in self.action_cards:
            if hasattr(card, 'update_colors'):
                card.update_colors(colors)