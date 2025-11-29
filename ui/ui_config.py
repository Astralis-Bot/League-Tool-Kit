"""
LEAGUE TOOLKIT - UI Configuration
Central configuration for UI layout, spacing, fonts, and sidebar
Themes are managed by theme_manager.py
"""

# ============================================================
# UI THEME SETTINGS (Design System)
# ============================================================
THEME = {
    'fonts': {
        'title': ("Segoe UI", 28, "bold"),
        'heading': ("Segoe UI Semibold", 22, "bold"),
        'subheading': ("Segoe UI", 16, "bold"),
        'body': ("Segoe UI", 12),
        'small': ("Segoe UI", 10),
        'mono': ("Consolas", 11),
        'accent': ("Segoe UI Semibold", 13, "bold")
    },
    'spacing': {
        'xs': 6,
        'sm': 12,
        'md': 20,
        'lg': 28,
        'xl': 36
    },
    'radius': {
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 20
    },
    'animations': {
        'duration': 250,
        'hover_scale': 1.02,
        'pulse_speed': 2000
    },
    'layout': {
        'sidebar_width': 260,
        'header_height': 100,
        'statusbar_height': 55,
        'card_min_height': 120
    },
    'shadows': {
        'small': '0 2px 12px rgba(0, 0, 0, 0.15)',
        'medium': '0 6px 20px rgba(0, 0, 0, 0.25)',
        'large': '0 12px 40px rgba(0, 0, 0, 0.35)',
        'glow': '0 0 24px'
    }
}

# ============================================================
# SIDEBAR NAVIGATION ITEMS
# ============================================================
SIDEBAR_ITEMS = [
    {'icon': '🏠', 'text': 'Home', 'id': 'home', 'desc': 'Dashboard'},
    {'icon': '🎯', 'text': 'Champions', 'id': 'champions', 'desc': 'Selection'},
    {'icon': '⚡', 'text': 'Automation', 'id': 'automation', 'desc': 'Systems'},
    {'icon': '📊', 'text': 'Status', 'id': 'status', 'desc': 'Monitor'},
    {'icon': 'ℹ️', 'text': 'About', 'id': 'about', 'desc': 'Info'},
    {'icon': '⚙️', 'text': 'Settings', 'id': 'settings', 'desc': 'Config'}
]

# ============================================================
# COLOR THEMES - NOTE:
# This is just a fallback. The real themes are managed by
# ui/theme/theme_manager.py which handles:
# - Default themes
# - Custom themes
# - Theme encryption
# - Theme import/export
# ============================================================

# Fallback default colors (if theme_manager fails)
COLORS = {
    'name': 'Midnight Purple',
    'app_name': 'LEAGUE TOOLKIT',
    'app_icon': '🛡️',
    'icon_file': 'tiamat.ico',
    
    'primary': '#8B5CF6',
    'secondary': '#EC4899',
    'accent': '#F59E0B',
    
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    
    'bg_dark': '#0F0A1F',
    'bg_medium': '#1A1229',
    'bg_light': '#251B35',
    'bg_card': '#1E1532',
    'bg_elevated': '#2A2040',
    'bg_hover': '#342952',
    
    'text_primary': '#F3F4F6',
    'text_secondary': '#D1D5DB',
    'text_tertiary': '#9CA3AF',
    'text_dark': '#111827',
    
    'border_color': '#2A2040',
    'border_accent': '#8B5CF6',
}

# Legacy support - redirects to theme_manager
THEMES = {
    'midnight_purple': COLORS.copy()
}