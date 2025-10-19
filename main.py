# main.py - League Toolkit v2.0
"""
League Toolkit - Automacao para League of Legends
Versao: 2.0
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Imports dos modulos do projeto
from ui.ui_manager import UIManager
from ui.theme.theme_manager import ThemeManager
from views import HomeView, ChampionsView, AutomationView, StatusView, AboutView, SettingsView
from ui.champion_manager import ChampionManager
from ui.champion_selector_optimized import OptimizedChampionSelector, preload_champion_data

# Imports dos modulos de automacao
from core.api_manager import api_manager

# ========================================
# IMPORTS CORRIGIDOS
# ========================================

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

try:
    from automation.Dodge import dodge
except ImportError:
    dodge = None
    print("Dodge nao disponivel")


class LeagueToolkitApp(ctk.CTk):
    """Aplicacao Principal - League Toolkit v2.0"""
    
    def __init__(self):
        super().__init__()
        
        print("=" * 60)
        print("LEAGUE TOOLKIT v2.0 - INICIANDO")
        print("=" * 60)
        
        # ========================
        # CONFIGURACOES BASICAS
        # ========================
        self.title("League Toolkit v2.0")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # ========================
        # INICIALIZAR MANAGERS
        # ========================
        print("\nInicializando Managers...")
        
        # Theme Manager
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_current_theme()
        print(f"Tema carregado: {self.colors.get('name', 'Unknown')}")
        
        # API Manager
        self.api_manager = api_manager
        print("API Manager inicializado")
        
        # Champion Manager
        self.champion_manager = ChampionManager()
        print("Champion Manager inicializado")
        
        # ========================
        # ESTADOS DA APLICACAO
        # ========================
        print("\nConfigurando estados...")
        
        # Estados de features
        self.instalock_enabled = False
        self.instalock_champion = None
        
        self.autoban_enabled = False
        self.autoban_champion = None
        
        # ========================
        # MODULOS DE AUTOMACAO
        # ========================
        print("\nInicializando modulos de automacao...")
        
        # Auto Accept
        if AutoAccept:
            try:
                self.auto_accept = AutoAccept()
                print("Auto Accept inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Auto Accept: {e}")
                self.auto_accept = None
        else:
            self.auto_accept = None
        
        # InstalockAutoban
        if InstalockAutoban:
            try:
                self.instalock_autoban = InstalockAutoban()
                self.instalock_autoban.start_monitor()
                print("InstalockAutoban inicializado")
            except Exception as e:
                print(f"Erro ao inicializar InstalockAutoban: {e}")
                self.instalock_autoban = None
        else:
            self.instalock_autoban = None
        
        # Chat Toggle
        if Chat:
            try:
                self.chat_toggle = Chat()
                print("Chat Toggle inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Chat Toggle: {e}")
                self.chat_toggle = None
        else:
            self.chat_toggle = None
        
        # Lobby Reveal
        if reveal:
            try:
                self.lobby_reveal_module = reveal
                print("Lobby Reveal inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Lobby Reveal: {e}")
                self.lobby_reveal_module = None
        else:
            self.lobby_reveal_module = None
        
        # Dodge Queue
        if dodge:
            try:
                self.dodge_queue_module = dodge
                print("Dodge Queue inicializado")
            except Exception as e:
                print(f"Erro ao inicializar Dodge Queue: {e}")
                self.dodge_queue_module = None
        else:
            self.dodge_queue_module = None
        
        # ========================
        # PRE-CARREGAMENTO
        # ========================
        print("\nPre-carregando dados dos campeoes...")
        preload_champion_data(self.api_manager)
        
        # ========================
        # CONFIGURAR UI
        # ========================
        print("\nConfigurando interface...")
        self.configure(fg_color=self.colors['bg_dark'])
        
        # Criar UI Manager
        self.ui_manager = UIManager(self, self.colors)
        self.ui_manager.create_main_layout()
        print("Layout principal criado")
        
        # ========================
        # CRIAR VIEWS
        # ========================
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
        
        # ========================
        # CARREGAR VIEW INICIAL
        # ========================
        print("\nCarregando view inicial...")
        self.switch_category('home')
        
        # ========================
        # CONFIGURAR ICONE
        # ========================
        try:
            icon_path = self.colors.get('icon_file', 'tiamat.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print(f"Icone carregado: {icon_path}")
        except Exception as e:
            print(f"Nao foi possivel carregar icone: {e}")
        
        # ========================
        # PROTOCOLO DE FECHAMENTO
        # ========================
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("\n" + "=" * 60)
        print("LEAGUE TOOLKIT INICIADO COM SUCESSO!")
        print("=" * 60 + "\n")
    
    # ========================================
    # NAVEGACAO E VIEWS
    # ========================================
    def switch_category(self, category_id):
        """Troca de categoria/view"""
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
            
            # SINCRONIZAR ICONES APOS CRIAR A VIEW
            self.after(150, lambda: self.champion_manager.sync_icons_after_view_change(self))
            
        except Exception as e:
            print(f"Erro ao carregar view '{category_id}': {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao carregar {category_id}")
    
    # ========================================
    # INSTALOCK
    # ========================================
    
    def open_instalock_hub(self):
        """Abre seletor de campeoes para instalock"""
        print("\nAbrindo Instalock Hub...")
        
        try:
            OptimizedChampionSelector(
                parent=self,
                title="INSTALOCK CHAMPION",
                icon="LOCK",
                color=self.colors['primary'],
                callback=self.handle_instalock_selection,
                api_manager=self.api_manager
            )
        except Exception as e:
            print(f"Erro ao abrir Instalock Hub: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir seletor: {e}")
    
    def handle_instalock_selection(self, champion_name):
        """Callback quando campeao eh selecionado no instalock"""
        if not self.instalock_autoban:
            messagebox.showerror("Erro", "InstalockAutoban nao disponivel")
            return False
        
        if champion_name == "disable":
            self.instalock_enabled = False
            self.instalock_champion = None
            self.instalock_autoban.instalock_enabled = False
            
            print("Instalock desabilitado")
            self.champion_manager.update_instalock_display(self, None)
            return True
        
        if champion_name:
            success = self.instalock_autoban.set_instalock_champion(champion_name)
            
            if success:
                self.instalock_champion = champion_name
                self.instalock_enabled = True
                
                print(f"Instalock configurado: {champion_name}")
                
                # Atualizar display
                self.champion_manager.update_instalock_display(self, champion_name)
                
                messagebox.showinfo("Sucesso", f"Instalock configurado para {champion_name}!")
                return True
            else:
                messagebox.showerror("Erro", f"Nao foi possivel configurar {champion_name}")
                return False
        
        return False
    
    def toggle_instalock(self, enabled):
        """Toggle do instalock"""
        if not self.instalock_autoban:
            return
        
        if enabled and not self.instalock_champion:
            print("Nenhum campeao selecionado para Instalock")
            messagebox.showwarning("Aviso", "Selecione um campeao primeiro!")
            self.update_feature_cards()
            return
        
        self.instalock_enabled = enabled
        self.instalock_autoban.instalock_enabled = enabled
        
        status = "ATIVADO" if enabled else "DESATIVADO"
        print(f"Instalock {status}")
    
    # ========================================
    # AUTO BAN
    # ========================================
    
    def open_autoban_hub(self):
        """Abre seletor de campeoes para autoban"""
        print("\nAbrindo Auto Ban Hub...")
        
        try:
            OptimizedChampionSelector(
                parent=self,
                title="AUTO BAN CHAMPION",
                icon="BAN",
                color=self.colors['secondary'],
                callback=self.handle_autoban_selection,
                api_manager=self.api_manager
            )
        except Exception as e:
            print(f"Erro ao abrir Auto Ban Hub: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir seletor: {e}")
    
    def handle_autoban_selection(self, champion_name):
        """Callback quando campeao eh selecionado no autoban"""
        if not self.instalock_autoban:
            messagebox.showerror("Erro", "InstalockAutoban nao disponivel")
            return False
        
        if champion_name == "disable":
            self.autoban_enabled = False
            self.autoban_champion = None
            self.instalock_autoban.auto_ban_enabled = False
            
            print("Auto Ban desabilitado")
            self.champion_manager.update_autoban_display(self, None)
            return True
        
        if champion_name:
            success = self.instalock_autoban.set_auto_ban_champion(champion_name)
            
            if success:
                self.autoban_champion = champion_name
                self.autoban_enabled = True
                
                print(f"Auto Ban configurado: {champion_name}")
                
                # Atualizar display
                self.champion_manager.update_autoban_display(self, champion_name)
                
                messagebox.showinfo("Sucesso", f"Auto Ban configurado para {champion_name}!")
                return True
            else:
                messagebox.showerror("Erro", f"Nao foi possivel configurar {champion_name}")
                return False
        
        return False

    def toggle_autoban(self, enabled):
        """Toggle do autoban"""
        if not self.instalock_autoban:
            return
        
        if enabled and not self.autoban_champion:
            print("Nenhum campeao selecionado para Auto Ban")
            messagebox.showwarning("Aviso", "Selecione um campeao primeiro!")
            self.update_feature_cards()
            return
        
        self.autoban_enabled = enabled
        self.instalock_autoban.auto_ban_enabled = enabled
        
        status = "ATIVADO" if enabled else "DESATIVADO"
        print(f"Auto Ban {status}")
    
    # ========================================
    # AUTO ACCEPT
    # ========================================
    
    def toggle_auto_accept(self, enabled):
        """Toggle do auto accept"""
        if not self.auto_accept:
            print("Auto Accept nao disponivel")
            return
        
        self.auto_accept.auto_accept_enabled = enabled
        
        if enabled:
            import threading
            if not hasattr(self.auto_accept, 'monitor_thread') or not self.auto_accept.monitor_thread.is_alive():
                self.auto_accept.monitor_thread = threading.Thread(
                    target=self.auto_accept.monitor_queue, 
                    daemon=True
                )
                self.auto_accept.monitor_thread.start()
            print("Auto Accept ATIVADO")
        else:
            print("Auto Accept DESATIVADO")
    
    # ========================================
    # ACOES RAPIDAS
    # ========================================
    
    def toggle_chat(self):
        """Ativa/desativa o chat"""
        if not self.chat_toggle:
            messagebox.showerror("Erro", "Chat Toggle nao disponivel")
            return
        
        try:
            if hasattr(self.chat_toggle, 'toggle'):
                self.chat_toggle.toggle()
            elif hasattr(self.chat_toggle, 'disconnect') and hasattr(self.chat_toggle, 'reconnect'):
                pass
            
            messagebox.showinfo("Chat Toggle", "Chat alternado com sucesso!")
            print("Chat alternado")
        except Exception as e:
            print(f"Erro ao alternar chat: {e}")
            messagebox.showerror("Erro", f"Erro ao alternar chat: {e}")
    
    def lobby_reveal(self):
        """Abre analise do Porofessor"""
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
    
    def dodge_queue(self):
        """Abandona a fila"""
        if not self.dodge_queue_module:
            messagebox.showerror("Erro", "Dodge Queue nao disponivel")
            return
        
        try:
            confirm = messagebox.askyesno(
                "Confirmar",
                "Deseja realmente sair da fila?\n\nIsso pode resultar em penalidade!"
            )
            
            if confirm:
                if callable(self.dodge_queue_module):
                    self.dodge_queue_module()
                elif hasattr(self.dodge_queue_module, 'dodge'):
                    self.dodge_queue_module.dodge()
                
                messagebox.showinfo("Dodge Queue", "Fila abandonada!")
                print("Dodge Queue executado")
        except Exception as e:
            print(f"Erro ao abandonar fila: {e}")
            messagebox.showerror("Erro", f"Erro ao abandonar fila: {e}")
    
    # ========================================
    # UTILITARIOS
    # ========================================
    
    def update_feature_cards(self):
        """Atualiza estado de todas as feature cards"""
        for card in self.ui_manager.feature_cards:
            try:
                if 'INSTALOCK' in card.title_text.upper():
                    card.set_enabled(self.instalock_enabled)
                    if self.instalock_champion:
                        card.update_description(f"CHAMPION: {self.instalock_champion}")
                    else:
                        card.update_description("Nenhum campeao selecionado")
                
                elif 'AUTO BAN' in card.title_text.upper():
                    card.set_enabled(self.autoban_enabled)
                    if self.autoban_champion:
                        card.update_description(f"CHAMPION: {self.autoban_champion}")
                    else:
                        card.update_description("Nenhum campeao selecionado")
                
                elif 'AUTO ACCEPT' in card.title_text.upper():
                    if self.auto_accept:
                        card.set_enabled(self.auto_accept.auto_accept_enabled)
            except Exception as e:
                print(f"Erro ao atualizar card: {e}")
    
    def get_status_data(self):
        """Retorna dados de status para a view de status"""
        return {
            'auto_accept': self.auto_accept.auto_accept_enabled if self.auto_accept else False,
            'instalock': self.instalock_champion if self.instalock_enabled else None,
            'auto_ban': self.autoban_champion if self.autoban_enabled else None,
            'chat': 'connected'
        }
    
    def on_theme_change(self, new_colors):
        """Callback quando tema eh alterado"""
        print(f"\nMudando tema para: {new_colors.get('name', 'Unknown')}")
        
        self.colors = new_colors
        self.configure(fg_color=new_colors['bg_dark'])
        self.ui_manager.update_colors(new_colors)
        
        for view in self.views.values():
            if hasattr(view, 'update_colors'):
                view.update_colors(new_colors)
        
        print("Tema atualizado")
    
    def on_closing(self):
        """Callback quando a janela eh fechada"""
        print("\nFechando aplicacao...")
        
        try:
            if self.instalock_autoban:
                self.instalock_autoban.stop()
            
            print("Modulos parados")
        except Exception as e:
            print(f"Erro ao parar modulos: {e}")
        
        print("Ate logo!")
        self.destroy()


# ========================================
# PONTO DE ENTRADA
# ========================================

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