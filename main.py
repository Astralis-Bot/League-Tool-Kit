"""
LEAGUE TOOLKIT v2.2.1 - Main Application
Refactored for better performance and maintainability
"""

from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from typing import Optional, Dict, Any

from ui.ui_manager import UIManager
from ui.theme.theme_manager import ThemeManager
from views import (HomeView, ChampionsView, AutomationView, 
                   StatusView, AboutView, SettingsView)
from ui.champion_manager import ChampionManager
from ui.modern_instalock_config import open_modern_instalock_config
from ui.modern_autoban_config import open_modern_autoban_config
from core.api_manager import api_manager
from core.updater import Updater

# Optional imports with graceful degradation
try:
    from automation.AutoAccept import AutoAccept
except ImportError:
    AutoAccept = None

try:
    from automation.InstalockAutoban import InstalockAutoban
except ImportError:
    InstalockAutoban = None

try:
    from automation.disconnect_reconnect_chat import Chat
except ImportError:
    Chat = None

try:
    from automation.Reveal import reveal
except ImportError:
    reveal = None


class LeagueToolkitApp(ctk.CTk):
    """Main Application Class"""
    
    VERSION = "2.2.1"
    MIN_SIZE = (1000, 600)
    DEFAULT_SIZE = (1200, 1150)
    UPDATE_CHECK_DELAY = 3000  # ms

    def __init__(self):
        super().__init__()
        
        self._log_startup()
        self._init_window()
        self._init_managers()
        self._init_state()
        self._init_automation_modules()
        self._init_ui()
        self._setup_icon()
        self._finalize_setup()

    # ==================== INITIALIZATION ====================

    def _log_startup(self):
        """Log application startup"""
        print("=" * 60)
        print(f"LEAGUE TOOLKIT v{self.VERSION} - STARTING")
        print("=" * 60)

    def _init_window(self):
        """Initialize window properties"""
        self.title(f"League Toolkit v{self.VERSION}")
        self.geometry(f"{self.DEFAULT_SIZE[0]}x{self.DEFAULT_SIZE[1]}")
        self.minsize(*self.MIN_SIZE)

    def _init_managers(self):
        """Initialize core managers"""
        print("\nInitializing Managers...")
        
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_current_theme()
        print(f"Theme loaded: {self.colors.get('name', 'Unknown')}")
        
        self.api_manager = api_manager
        print("API Manager initialized")
        
        self.champion_manager = ChampionManager()
        print("Champion Manager initialized")
        
        print("\nInitializing update system...")
        self.updater = Updater(app=self)
        print("Updater initialized")

    def _init_state(self):
        """Initialize application state"""
        print("\nConfiguring states...")
        
        # Instalock
        self.instalock_enabled = False
        self.instalock_champion = None
        self.instalock_backup_2 = None
        self.instalock_backup_3 = None
        
        # Auto-ban
        self.autoban_enabled = False
        self.autoban_champion = None
        self.autoban_backup_2 = None
        self.autoban_backup_3 = None

    def _init_automation_modules(self):
        """Initialize automation modules"""
        print("\nInitializing automation modules...")
        
        self.auto_accept = self._safe_init(AutoAccept, "Auto Accept")
        self.instalock_autoban = self._safe_init(InstalockAutoban, "InstalockAutoban")
        self.chat_toggle = self._safe_init(Chat, "Chat Toggle")
        
        self.lobby_reveal_module = reveal
        if reveal:
            print("Lobby Reveal initialized")

    def _safe_init(self, module_class, name: str) -> Optional[Any]:
        """Safely initialize a module with error handling"""
        if not module_class:
            return None
        
        try:
            instance = module_class()
            print(f"{name} initialized")
            return instance
        except Exception as e:
            print(f"Error initializing {name}: {e}")
            return None

    def _init_ui(self):
        """Initialize UI components"""
        print("\nConfiguring interface...")
        
        self.configure(fg_color=self.colors['bg_dark'])
        
        self.ui_manager = UIManager(self, self.colors)
        self.ui_manager.create_main_layout()
        print("Main layout created")
        
        print("\nCreating views...")
        self.views = {
            'home': HomeView(self.colors, self.ui_manager.theme),
            'champions': ChampionsView(self.colors, self.ui_manager.theme),
            'automation': AutomationView(self.colors, self.ui_manager.theme),
            'status': StatusView(self.colors, self.ui_manager.theme),
            'about': AboutView(self.colors, self.ui_manager.theme),
            'settings': SettingsView(self.colors, self.ui_manager.theme)
        }
        print("Views created")
        
        print("\nLoading initial view...")
        self.switch_category('home')

    def _setup_icon(self):
        """Setup application icon with multiple search paths"""
        icon_path = self._find_icon()
        if not icon_path:
            print("❌ Icon not found")
            return
        
        try:
            if sys.platform == 'win32' and icon_path.endswith('.ico'):
                self.iconbitmap(icon_path)
                print(f"✅ Icon loaded: {icon_path}")
            else:
                self._set_image_icon(icon_path)
        except Exception as e:
            print(f"⚠️ Error loading icon: {e}")

    def _find_icon(self) -> Optional[str]:
        """Find icon file in search paths"""
        search_paths = [
            self.colors.get('icon_file', 'tiamat.ico'),
            'assets/tiamat.ico',
            'ui/assets/tiamat.ico',
            'resources/tiamat.ico',
            os.path.join(os.path.dirname(__file__), 'tiamat.ico')
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        return None

    def _set_image_icon(self, path: str):
        """Set icon from image file"""
        try:
            icon_image = Image.open(path).resize((32, 32), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(32, 32))
            self.iconphoto(True, photo)
            print(f"✅ Image icon loaded: {path}")
        except Exception as e:
            print(f"⚠️ Could not load image icon: {e}")

    def _finalize_setup(self):
        """Finalize application setup"""
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("\nScheduling update check...")
        self.after(self.UPDATE_CHECK_DELAY, self._check_updates_on_startup)
        
        print("\n" + "=" * 60)
        print("LEAGUE TOOLKIT STARTED SUCCESSFULLY!")
        print("=" * 60 + "\n")

    def _check_updates_on_startup(self):
        """Check for updates on startup (silent)"""
        try:
            print("\n🔍 Checking for updates in background...")
            self.updater.check_on_startup()
        except Exception as e:
            print(f"⚠️ Error checking updates: {e}")

    # ==================== VIEW MANAGEMENT ====================

    def switch_category(self, category_id: str):
        """Switch to a different view"""
        print(f"\nSwitching to: {category_id}")
        self.ui_manager.clear_scroll_area()

        view_handlers = {
            'status': lambda v: v.create(self.ui_manager.scroll_area, self.get_status_data),
            'settings': lambda v: v.create(self.ui_manager.scroll_area, self.on_theme_change),
        }

        try:
            view = self.views[category_id]
            handler = view_handlers.get(category_id, 
                                       lambda v: v.create(self.ui_manager.scroll_area, self))
            handler(view)
            
            print(f"View '{category_id}' loaded")
            self.after(150, lambda: self.champion_manager.sync_icons_after_view_change(self))

        except Exception as e:
            print(f"Error loading view '{category_id}': {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error loading {category_id}")

    # ==================== INSTALOCK MANAGEMENT ====================

    def open_instalock_hub(self):
        """Open instalock configuration"""
        print("\nOpening Modern Instalock Configuration...")
        open_modern_instalock_config(self, self)

    def update_instalock_card(self):
        """Update instalock card description and icon"""
        if not (hasattr(self.ui_manager, 'instalock_card') and self.ui_manager.instalock_card):
            return

        status_parts = [self.instalock_champion]
        
        if self.instalock_backup_2:
            status_parts.append(f"2nd: {self.instalock_backup_2}")
        if self.instalock_backup_3:
            status_parts.append(f"3rd: {self.instalock_backup_3}")

        description = f"Selected: {' | '.join(status_parts)}"
        self.ui_manager.instalock_card.update_description(description)

        if self.instalock_champion and self.instalock_champion != "Random":
            self.champion_manager.update_instalock_display(self, self.instalock_champion)

    def toggle_instalock(self, enabled: bool):
        """Toggle instalock on/off"""
        if not self._validate_module(self.instalock_autoban, "InstalockAutoban"):
            return

        if enabled and not self.instalock_champion:
            print("❌ No champion selected for Instalock")
            messagebox.showwarning("Warning", "Select a champion first!")
            self.after(100, self.update_feature_cards)
            return

        self._log_toggle("INSTALOCK", enabled)
        
        self.instalock_enabled = enabled
        self.instalock_autoban.instalock.enabled = enabled
        self._manage_monitor()
        
        if enabled:
            print(f"✅ Instalock ENABLED: {self.instalock_champion}")
        else:
            print("⚠️ Instalock DISABLED")
        
        print(f"{'='*60}\n")
        self.update_feature_cards()

    # ==================== AUTO-BAN MANAGEMENT ====================

    def open_autoban_hub(self):
        """Open auto-ban configuration"""
        print("\nOpening Modern Auto Ban Configuration...")
        open_modern_autoban_config(self, self)

    def toggle_autoban(self, enabled: bool):
        """Toggle auto-ban on/off"""
        if not self._validate_module(self.instalock_autoban, "InstalockAutoban"):
            return

        if enabled and not self.autoban_champion:
            print("❌ No champion selected for Auto Ban")
            messagebox.showwarning("Warning", "Select a champion first!")
            self.after(100, self.update_feature_cards)
            return

        self._log_toggle("AUTO-BAN", enabled)
        
        self.autoban_enabled = enabled
        self.instalock_autoban.auto_ban.enabled = enabled
        self._manage_monitor()
        
        if enabled:
            print(f"✅ Auto-ban ENABLED: {self.autoban_champion}")
        else:
            print("⚠️ Auto-ban DISABLED")
        
        print(f"{'='*60}\n")
        self.update_feature_cards()

    def _manage_monitor(self):
        """Manage monitor thread for instalock/autoban"""
        should_run = self.instalock_enabled or self.autoban_enabled
        
        if not should_run:
            print("ℹ️ No active features - Monitor idle")
            return
        
        monitor_alive = (
            hasattr(self.instalock_autoban, 'monitor_thread') and 
            self.instalock_autoban.monitor_thread is not None and 
            self.instalock_autoban.monitor_thread.is_alive()
        )
        
        if not monitor_alive:
            self.instalock_autoban.start_monitor()
            print("✅ Monitor STARTED")
        else:
            print("ℹ️ Monitor already running")

    # ==================== OTHER FEATURES ====================

    def toggle_auto_accept(self, enabled: bool):
        """Toggle auto-accept on/off"""
        if not self._validate_module(self.auto_accept, "Auto Accept"):
            return

        self.auto_accept.auto_accept_enabled = enabled

        if enabled:
            self._start_auto_accept_monitor()
        else:
            print("⚠️ Auto Accept DISABLED")

    def _start_auto_accept_monitor(self):
        """Start auto-accept monitor thread"""
        import threading
        
        if not (hasattr(self.auto_accept, 'monitor_thread') and 
                self.auto_accept.monitor_thread.is_alive()):
            self.auto_accept.monitor_thread = threading.Thread(
                target=self.auto_accept.monitor_queue,
                daemon=True
            )
            self.auto_accept.monitor_thread.start()
            print("✅ Auto Accept ENABLED - Monitor started")
        else:
            print("✅ Auto Accept ENABLED - Monitor already running")

    def toggle_chat(self):
        """Toggle chat on/off"""
        if not self._validate_module(self.chat_toggle, "Chat Toggle"):
            return

        try:
            self.chat_toggle.toggle_chat()
            current_state = self.chat_toggle.return_state()
            
            messagebox.showinfo("Chat Toggle", "Chat toggled successfully!")
            print(f"✅ Chat toggled - State: {current_state}")
            
        except Exception as e:
            print(f"❌ Error toggling chat: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error toggling chat: {e}")

    def lobby_reveal(self):
        """Execute lobby reveal"""
        if not self.lobby_reveal_module:
            messagebox.showerror("Error", "Lobby Reveal not available")
            return

        try:
            if callable(self.lobby_reveal_module):
                self.lobby_reveal_module()
            elif hasattr(self.lobby_reveal_module, 'open_porofessor'):
                self.lobby_reveal_module.open_porofessor()

            messagebox.showinfo("Lobby Reveal", "Porofessor opened!")
            print("Lobby Reveal executed")
        except Exception as e:
            print(f"Error in Lobby Reveal: {e}")
            messagebox.showerror("Error", f"Error opening Porofessor: {e}")

    # ==================== UTILITY METHODS ====================

    def _validate_module(self, module, name: str) -> bool:
        """Validate if module is available"""
        if not module:
            messagebox.showerror("Error", f"{name} not available")
            return False
        return True

    def _log_toggle(self, feature: str, enabled: bool):
        """Log feature toggle"""
        print(f"\n{'='*60}")
        print(f"TOGGLE {feature}: {enabled}")
        print(f"{'='*60}")

    def update_feature_cards(self):
        """Update all feature cards with correct state"""
        card_handlers = {
            'INSTALOCK': self._update_instalock_card_state,
            'AUTO BAN': self._update_autoban_card_state,
            'AUTO ACCEPT': self._update_auto_accept_card_state
        }

        for card in self.ui_manager.feature_cards:
            try:
                title = card.title_text.upper()
                for key, handler in card_handlers.items():
                    if key in title:
                        handler(card)
                        break
            except Exception as e:
                print(f"Error updating card: {e}")
        
        if hasattr(self.ui_manager, 'update_active_count'):
            self.ui_manager.update_active_count()

    def _update_instalock_card_state(self, card):
        """Update instalock card state"""
        card.set_enabled(self.instalock_enabled)
        self.update_instalock_card()

    def _update_autoban_card_state(self, card):
        """Update autoban card state"""
        card.set_enabled(self.autoban_enabled)
        if self.autoban_champion:
            parts = [f"1st: {self.autoban_champion}"]
            if self.autoban_backup_2:
                parts.append(f"2nd: {self.autoban_backup_2}")
            if self.autoban_backup_3:
                parts.append(f"3rd: {self.autoban_backup_3}")
            card.update_description(" | ".join(parts))
        else:
            card.update_description("No champion selected")

    def _update_auto_accept_card_state(self, card):
        """Update auto-accept card state"""
        if self.auto_accept:
            card.set_enabled(self.auto_accept.auto_accept_enabled)

    def get_status_data(self) -> Dict[str, Any]:
        """Get current status data"""
        return {
            'auto_accept': self.auto_accept.auto_accept_enabled if self.auto_accept else False,
            'instalock': self._get_instalock_status(),
            'auto_ban': self.autoban_champion if self.autoban_enabled else None,
            'chat': self._get_chat_status(),
        }

    def _get_instalock_status(self) -> Optional[str]:
        """Get instalock status string"""
        if not (self.instalock_enabled and self.instalock_champion):
            return None
        
        status = self.instalock_champion
        backups = []
        
        if self.instalock_backup_2:
            backups.append(f"2nd:{self.instalock_backup_2}")
        if self.instalock_backup_3:
            backups.append(f"3rd:{self.instalock_backup_3}")
        
        if backups:
            status += f" ({', '.join(backups)})"
        
        return status

    def _get_chat_status(self) -> str:
        """Get chat status"""
        if not self.chat_toggle:
            return 'connected'
        
        try:
            return self.chat_toggle.return_state()
        except:
            return 'unknown'

    def on_theme_change(self, new_colors: Dict[str, str]):
        """Handle theme change"""
        print(f"\nChanging theme to: {new_colors.get('name', 'Unknown')}")

        self.colors = new_colors
        self.configure(fg_color=new_colors['bg_dark'])
        self.ui_manager.update_colors(new_colors)

        for view in self.views.values():
            if hasattr(view, 'update_colors'):
                view.update_colors(new_colors)

        print("Theme updated")

    def on_closing(self):
        """Handle application closing"""
        print("\nClosing application...")

        try:
            if self.instalock_autoban:
                self.instalock_autoban.stop()

            if self.auto_accept and hasattr(self.auto_accept, 'auto_accept_enabled'):
                self.auto_accept.auto_accept_enabled = False

            print("Modules stopped")
        except Exception as e:
            print(f"Error stopping modules: {e}")

        print("Goodbye!")
        self.destroy()


def main():
    """Main entry point"""
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        app = LeagueToolkitApp()
        app.mainloop()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)

    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

        messagebox.showerror(
            "Fatal Error",
            f"A critical error occurred:\n\n{e}\n\nCheck console for details."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()