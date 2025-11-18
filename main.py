from PIL import Image
import customtkinter as ctk 
from tkinter import messagebox 
import sys 
import os 

from ui.ui_manager import UIManager 
from ui.theme.theme_manager import ThemeManager 
from views import HomeView, ChampionsView, AutomationView, StatusView, AboutView, SettingsView 
from ui.champion_manager import ChampionManager 
from ui.modern_instalock_config import open_modern_instalock_config 
from ui.modern_autoban_config import open_modern_autoban_config 

from core.api_manager import api_manager 

try:
    from automation.AutoAccept import AutoAccept 
except ImportError:
    AutoAccept = None 
    print("AutoAccept nao disponivel")

try:
    from automation.InstalockAutoban import InstalockAutoban 
except ImportError:
    InstalockAutoban = None 
    print("InstalockAutoban nao disponivel")

try:
    from automation.disconnect_reconnect_chat import Chat 
except ImportError:
    Chat = None 
    print("Chat nao disponivel")

try:
    from automation.Reveal import reveal 
except ImportError:
    reveal = None 
    print("Reveal nao disponivel")


class LeagueToolkitApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        print("=" * 60)
        print("LEAGUE TOOLKIT v2.0 - INICIANDO")
        print("=" * 60)

        self.title("League Toolkit v2.0")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        print("\nInicializando Managers...")

        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_current_theme()
        print(f"Tema carregado: {self.colors.get('name', 'Unknown')}")

        self.api_manager = api_manager 
        print("API Manager inicializado")

        self.champion_manager = ChampionManager()
        print("Champion Manager inicializado")

        print("\nConfigurando estados...")

        self.instalock_enabled = False 
        self.instalock_champion = None 
        self.instalock_backup_2 = None 
        self.instalock_backup_3 = None 

        self.autoban_enabled = False 
        self.autoban_champion = None 
        self.autoban_backup_2 = None 
        self.autoban_backup_3 = None 

        print("\nInicializando modulos de automacao...")

        if AutoAccept:
            try:
                self.auto_accept = AutoAccept()
                print("Auto Accept inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Auto Accept: {e}")
                self.auto_accept = None 
        else:
            self.auto_accept = None 

        if InstalockAutoban:
            try:
                self.instalock_autoban = InstalockAutoban()
                print("InstalockAutoban inicializado (aguardando ativação)")
            except Exception as e:
                print(f"Erro ao inicializar InstalockAutoban: {e}")
                self.instalock_autoban = None 
        else:
            self.instalock_autoban = None 

        if Chat:
            try:
                self.chat_toggle = Chat()
                print("Chat Toggle inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Chat Toggle: {e}")
                self.chat_toggle = None 
        else:
            self.chat_toggle = None 

        if reveal:
            try:
                self.lobby_reveal_module = reveal 
                print("Lobby Reveal inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Lobby Reveal: {e}")
                self.lobby_reveal_module = None 
        else:
            self.lobby_reveal_module = None 

        print("\nConfigurando interface...")
        self.configure(fg_color=self.colors['bg_dark'])

        self.ui_manager = UIManager(self, self.colors)
        self.ui_manager.create_main_layout()
        print("Layout principal criado")

        print("\nCriando views...")
        self.views = {
            'home': HomeView(self.colors, self.ui_manager.theme),
            'champions': ChampionsView(self.colors, self.ui_manager.theme),
            'automation': AutomationView(self.colors, self.ui_manager.theme),
            'status': StatusView(self.colors, self.ui_manager.theme),
            'about': AboutView(self.colors, self.ui_manager.theme),
            'settings': SettingsView(self.colors, self.ui_manager.theme)
        }
        print("Views criadas")

        print("\nCarregando view inicial...")
        self.switch_category('home')

        try:
            icon_path = self.colors.get('icon_file', 'tiamat.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print(f"Icone carregado: {icon_path}")
        except Exception as e:
            print(f"Nao foi possivel carregar icone: {e}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        print("\n" + "=" * 60)
        print("LEAGUE TOOLKIT INICIADO COM SUCESSO!")
        print("=" * 60 + "\n")
        self._setup_icon()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        print("\n" + "=" * 60)
        print("LEAGUE TOOLKIT INICIADO COM SUCESSO!")
        print("=" * 60 + "\n")

    def _setup_icon(self):
        """Configura o ícone da aplicação para janela e barra de tarefas"""
        try:
            icon_path = self.colors.get('icon_file', 'tiamat.ico')
            

            if not os.path.exists(icon_path):
                print(f"⚠️ Arquivo de ícone não encontrado: {icon_path}")

                alternative_paths = [
                    'assets/tiamat.ico',
                    'ui/assets/tiamat.ico',
                    'resources/tiamat.ico',
                    os.path.join(os.path.dirname(__file__), 'tiamat.ico')
                ]
                
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        icon_path = alt_path
                        print(f"✅ Ícone encontrado em: {icon_path}")
                        break
                else:
                    print("❌ Ícone não encontrado em nenhum caminho")
                    return
            
            if sys.platform == 'win32' and icon_path.endswith('.ico'):
                self.iconbitmap(icon_path)
                print(f"✅ Ícone .ico carregado: {icon_path}")
            
            elif icon_path.endswith(('.png', '.jpg', '.jpeg')):
                icon_image = Image.open(icon_path)
                icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(32, 32))
                self.iconphoto(True, photo)
                print(f"✅ Ícone de imagem carregado: {icon_path}")
            
            elif icon_path.endswith('.ico'):
                try:
                    icon_image = Image.open(icon_path)
                    icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
                    photo = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(32, 32))
                    self.iconphoto(True, photo)
                    print(f"✅ Ícone .ico carregado como imagem: {icon_path}")
                except Exception as e:
                    print(f"⚠️ Não foi possível carregar .ico como imagem: {e}")
                    
        except Exception as e:
            print(f"❌ Erro ao carregar ícone: {e}")
            import traceback
            traceback.print_exc()

    def switch_category(self, category_id):
        print(f"\nMudando para: {category_id}")
        self.ui_manager.clear_scroll_area()

        try:
            if category_id == 'home':
                self.views['home'].create(self.ui_manager.scroll_area, self)
            elif category_id == 'champions':
                self.views['champions'].create(self.ui_manager.scroll_area, self)
            elif category_id == 'automation':
                self.views['automation'].create(self.ui_manager.scroll_area, self)
            elif category_id == 'status':
                self.views['status'].create(self.ui_manager.scroll_area, self.get_status_data)
            elif category_id == 'about':
                self.views['about'].create(self.ui_manager.scroll_area)
            elif category_id == 'settings':
                self.views['settings'].create(self.ui_manager.scroll_area, self.on_theme_change)

            print(f"View '{category_id}' carregada")

            self.after(150, lambda: self.champion_manager.sync_icons_after_view_change(self))

        except Exception as e:
            print(f"Erro ao carregar view '{category_id}': {e}")
            import traceback 
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao carregar {category_id}")

    def open_instalock_hub(self):
        print("\nAbrindo Modern Instalock Configuration...")
        open_modern_instalock_config(self, self)

    def update_instalock_card(self):
        if hasattr(self.ui_manager, 'instalock_card') and self.ui_manager.instalock_card:
            status_parts = [self.instalock_champion]

            if self.instalock_backup_2:
                status_parts.append(f"2nd: {self.instalock_backup_2}")
            if self.instalock_backup_3:
                status_parts.append(f"3rd: {self.instalock_backup_3}")

            description = f"Selected: {' | '.join(status_parts)}"
            self.ui_manager.instalock_card.update_description(description)

            if self.instalock_champion and self.instalock_champion != "Random":
                self.champion_manager.update_instalock_display(self, self.instalock_champion)

    def toggle_instalock(self, enabled):
        if not self.instalock_autoban:
            messagebox.showerror("Erro", "InstalockAutoban nao disponivel")
            return 

        if enabled and not self.instalock_champion:
            print("❌ Nenhum campeao selecionado para Instalock")
            messagebox.showwarning("Aviso", "Selecione um campeao primeiro!")
            self.after(100, self.update_feature_cards)
            return 

        self.instalock_enabled = enabled 
        self.instalock_autoban.instalock_enabled = enabled 

        if enabled:
            if not hasattr(self.instalock_autoban, 'monitor_thread') or \
            self.instalock_autoban.monitor_thread is None or \
            not self.instalock_autoban.monitor_thread.is_alive():
                self.instalock_autoban.start_monitor()
                print("✅ Instalock ATIVADO - Monitor iniciado")
            else:
                print("✅ Instalock ATIVADO - Monitor já estava rodando")
        else:
            print("⚠️ Instalock DESATIVADO")

        self.update_feature_cards()

    def open_autoban_hub(self):
        print("\nAbrindo Modern Auto Ban Configuration...")
        open_modern_autoban_config(self, self)

    def toggle_autoban(self, enabled):
        if not self.instalock_autoban:
            messagebox.showerror("Erro", "InstalockAutoban nao disponivel")
            return 

        if enabled and not self.autoban_champion:
            print("❌ Nenhum campeao selecionado para Auto Ban")
            messagebox.showwarning("Aviso", "Selecione um campeao primeiro!")
            self.after(100, self.update_feature_cards)
            return 

        self.autoban_enabled = enabled 
        self.instalock_autoban.auto_ban_enabled = enabled 

        if enabled:
            if not hasattr(self.instalock_autoban, 'monitor_thread') or \
               not self.instalock_autoban.monitor_thread.is_alive():
                self.instalock_autoban.start_monitor()
                print("✅ Auto Ban ATIVADO - Monitor iniciado")
            else:
                print("✅ Auto Ban ATIVADO - Monitor já estava rodando")
        else:
            print("⚠️ Auto Ban DESATIVADO")

        self.update_feature_cards()

    def toggle_auto_accept(self, enabled):
        if not self.auto_accept:
            messagebox.showerror("Erro", "Auto Accept nao disponivel")
            return 

        self.auto_accept.auto_accept_enabled = enabled 

        if enabled:
            import threading 
            if not hasattr(self.auto_accept, 'monitor_thread') or \
               not self.auto_accept.monitor_thread.is_alive():
                self.auto_accept.monitor_thread = threading.Thread(
                    target=self.auto_accept.monitor_queue,
                    daemon=True 
                )
                self.auto_accept.monitor_thread.start()
                print("✅ Auto Accept ATIVADO - Monitor iniciado")
            else:
                print("✅ Auto Accept ATIVADO - Monitor já estava rodando")
        else:
            print("⚠️ Auto Accept DESATIVADO")

    def toggle_chat(self):
        if not self.chat_toggle:
            messagebox.showerror("Erro", "Chat Toggle nao disponivel")
            return 

        try:
            self.chat_toggle.toggle_chat()
            
            current_state = self.chat_toggle.return_state()
            
            messagebox.showinfo(
                "Chat Toggle", 
                f"Chat alternado com sucesso!"
            )
            print(f"✅ Chat alternado - Estado: {current_state}")
            
        except Exception as e:
            print(f"❌ Erro ao alternar chat: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao alternar chat: {e}")

    def lobby_reveal(self):
        if not self.lobby_reveal_module:
            messagebox.showerror("Erro", "Lobby Reveal nao disponivel")
            return 

        try:
            if callable(self.lobby_reveal_module):
                self.lobby_reveal_module()
            elif hasattr(self.lobby_reveal_module, 'open_porofessor'):
                self.lobby_reveal_module.open_porofessor()

            messagebox.showinfo("Lobby Reveal", "Porofessor aberto!")
            print("Lobby Reveal executado")
        except Exception as e:
            print(f"Erro no Lobby Reveal: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir Porofessor: {e}")

    def update_feature_cards(self):
        for card in self.ui_manager.feature_cards:
            try:
                if 'INSTALOCK' in card.title_text.upper():
                    card.set_enabled(self.instalock_enabled)
                    self.update_instalock_card()

                elif 'AUTO BAN' in card.title_text.upper():
                    card.set_enabled(self.autoban_enabled)
                    if self.autoban_champion:
                        card.update_description(f"Selected: {self.autoban_champion}")
                    else:
                        card.update_description("No champion selected")

                elif 'AUTO ACCEPT' in card.title_text.upper():
                    if self.auto_accept:
                        card.set_enabled(self.auto_accept.auto_accept_enabled)

            except Exception as e:
                print(f"Erro ao atualizar card: {e}")

    def get_status_data(self):
        instalock_status = None 
        if self.instalock_enabled and self.instalock_champion:
            instalock_status = self.instalock_champion 
            if self.instalock_backup_2 or self.instalock_backup_3:
                backups = []
                if self.instalock_backup_2:
                    backups.append(f"2nd:{self.instalock_backup_2}")
                if self.instalock_backup_3:
                    backups.append(f"3rd:{self.instalock_backup_3}")
                instalock_status += f" ({', '.join(backups)})"

        chat_status = 'connected'
        if self.chat_toggle:
            try:
                chat_status = self.chat_toggle.return_state()
            except:
                chat_status = 'unknown'

        return {
            'auto_accept': self.auto_accept.auto_accept_enabled if self.auto_accept else False,
            'instalock': instalock_status,
            'auto_ban': self.autoban_champion if self.autoban_enabled else None,
            'chat': chat_status,
        }

    def on_theme_change(self, new_colors):
        print(f"\nMudando tema para: {new_colors.get('name', 'Unknown')}")

        self.colors = new_colors 
        self.configure(fg_color=new_colors['bg_dark'])
        self.ui_manager.update_colors(new_colors)

        for view in self.views.values():
            if hasattr(view, 'update_colors'):
                view.update_colors(new_colors)

        print("Tema atualizado")

    def on_closing(self):
        print("\nFechando aplicacao...")

        try:
            if self.instalock_autoban:
                self.instalock_autoban.stop()

            if self.auto_accept and hasattr(self.auto_accept, 'auto_accept_enabled'):
                self.auto_accept.auto_accept_enabled = False

            print("Modulos parados")
        except Exception as e:
            print(f"Erro ao parar modulos: {e}")

        print("Ate logo!")
        self.destroy()


if __name__ == "__main__":
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        app = LeagueToolkitApp()
        app.mainloop()

    except KeyboardInterrupt:
        print("\n\nAplicacao interrompida pelo usuario")
        sys.exit(0)

    except Exception as e:
        print(f"\n\nERRO FATAL: {e}")
        import traceback 
        traceback.print_exc()

        messagebox.showerror(
            "Erro Fatal",
            f"Ocorreu um erro critico:\n\n{e}\n\nVerifique o console para mais detalhes."
        )
        sys.exit(1)