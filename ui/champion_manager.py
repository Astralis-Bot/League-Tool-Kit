import customtkinter as ctk
from PIL import Image
from io import BytesIO
import urllib.request
from threading import Thread


class ChampionManager:
    """Gerencia ícones e displays de campeões - VERDADEIRA PERSISTÊNCIA"""
    
    def __init__(self):
        self._champion_image_cache = {}
        self._persistent_references = []
        
        # NOVO: Dados persistentes que NUNCA são perdidos
        self._instalock_data = {
            'champion_name': None,
            'icon': None,
            'card_ref': None
        }
        
        self._autoban_data = {
            'champion_name': None,
            'icon': None,
            'card_ref': None
        }
    
    def get_champion_icon_url(self, champion_name, api_manager):
        """Retorna URL do ícone do campeão"""
        try:
            champions = api_manager.get_champions()
            for champ in champions:
                if champ['name'].lower() == champion_name.lower():
                    return champ.get('icon', '')
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar URL: {e}")
            return None
    
    def load_champion_icon(self, champion_name, api_manager, size=(50, 50)):
        """Carrega ícone do campeão com cache PERSISTENTE"""
        cache_key = f"{champion_name}_{size[0]}x{size[1]}"
        
        if cache_key in self._champion_image_cache:
            print(f"✅ Ícone em cache: {champion_name}")
            return self._champion_image_cache[cache_key]
        
        try:
            url = self.get_champion_icon_url(champion_name, api_manager)
            if not url:
                print(f"⚠️ URL não encontrada para {champion_name}")
                return None
            
            print(f"🔥 Carregando ícone: {champion_name}")
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                image_data = response.read()
            
            image = Image.open(BytesIO(image_data))
            image = image.resize(size, Image.Resampling.LANCZOS)
            
            photo = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            
            self._champion_image_cache[cache_key] = photo
            self._persistent_references.append(photo)
            
            print(f"✅ Ícone carregado e cacheado: {champion_name}")
            return photo
            
        except Exception as e:
            print(f"❌ Erro ao carregar ícone de {champion_name}: {e}")
            return None
    
    def update_instalock_display(self, app, champion_name):
        """Atualiza display do instalock - GUARDA DADOS PERSISTENTES"""
        try:
            if champion_name:
                print(f"🔄 Configurando Instalock: {champion_name}")
                
                # Carregar ícone
                cache_key = f"{champion_name}_50x50"
                if cache_key not in self._champion_image_cache:
                    icon = self.load_champion_icon(champion_name, app.api_manager, size=(50, 50))
                else:
                    icon = self._champion_image_cache[cache_key]
                
                # GUARDAR DADOS PERMANENTES
                self._instalock_data['champion_name'] = champion_name
                self._instalock_data['icon'] = icon
                
                # Buscar card atual
                if hasattr(app, 'ui_manager') and app.ui_manager:
                    for card in app.ui_manager.feature_cards:
                        if hasattr(card, 'title_text') and 'INSTALOCK' in card.title_text.upper():
                            self._instalock_data['card_ref'] = card
                            self._apply_icon_now(card, icon, champion_name)
                            break
            else:
                # Limpar
                self._instalock_data['champion_name'] = None
                self._instalock_data['icon'] = None
                self._instalock_data['card_ref'] = None
        
        except Exception as e:
            print(f"❌ Erro ao atualizar Instalock: {e}")
            import traceback
            traceback.print_exc()
    
    def update_autoban_display(self, app, champion_name):
        """Atualiza display do autoban - GUARDA DADOS PERSISTENTES"""
        try:
            if champion_name:
                print(f"🔄 Configurando Auto Ban: {champion_name}")
                
                # Carregar ícone
                cache_key = f"{champion_name}_50x50"
                if cache_key not in self._champion_image_cache:
                    icon = self.load_champion_icon(champion_name, app.api_manager, size=(50, 50))
                else:
                    icon = self._champion_image_cache[cache_key]
                
                # GUARDAR DADOS PERMANENTES
                self._autoban_data['champion_name'] = champion_name
                self._autoban_data['icon'] = icon
                
                # Buscar card atual
                if hasattr(app, 'ui_manager') and app.ui_manager:
                    for card in app.ui_manager.feature_cards:
                        if hasattr(card, 'title_text') and 'AUTO BAN' in card.title_text.upper():
                            self._autoban_data['card_ref'] = card
                            self._apply_icon_now(card, icon, champion_name)
                            break
            else:
                # Limpar
                self._autoban_data['champion_name'] = None
                self._autoban_data['icon'] = None
                self._autoban_data['card_ref'] = None
        
        except Exception as e:
            print(f"❌ Erro ao atualizar Auto Ban: {e}")
            import traceback
            traceback.print_exc()
    
    def _apply_icon_now(self, card, icon, champion_name):
        """Aplica ícone imediatamente"""
        try:
            if not card or not hasattr(card, 'winfo_exists') or not card.winfo_exists():
                print(f"⚠️ Card não existe")
                return
            
            if hasattr(card, 'update_description'):
                card.update_description(f"🎯 {champion_name}")
            
            if hasattr(card, 'set_champion_icon'):
                card.set_champion_icon(icon, champion_name)
                print(f"✅ Ícone aplicado: {champion_name}")
        
        except Exception as e:
            print(f"❌ Erro ao aplicar ícone: {e}")
    
    def sync_icons_after_view_change(self, app):
        """SINCRONIZA ícones após mudança de view - CRÍTICO"""
        print("\n" + "="*60)
        print("🔄 SINCRONIZANDO ÍCONES APÓS MUDANÇA DE VIEW")
        print("="*60)
        
        try:
            if not hasattr(app, 'ui_manager') or not app.ui_manager:
                print("⚠️ UI Manager não disponível")
                return
            
            # INSTALOCK
            if self._instalock_data['champion_name'] and self._instalock_data['icon']:
                champ_name = self._instalock_data['champion_name']
                icon = self._instalock_data['icon']
                
                print(f"\n📍 Procurando card Instalock para: {champ_name}")
                
                found = False
                for card in app.ui_manager.feature_cards:
                    if hasattr(card, 'title_text') and 'INSTALOCK' in card.title_text.upper():
                        print(f"   ✅ Card encontrado: {id(card)}")
                        self._instalock_data['card_ref'] = card
                        self._apply_icon_now(card, icon, champ_name)
                        found = True
                        break
                
                if not found:
                    print(f"   ⚠️ Card Instalock não encontrado!")
            
            # AUTO BAN
            if self._autoban_data['champion_name'] and self._autoban_data['icon']:
                champ_name = self._autoban_data['champion_name']
                icon = self._autoban_data['icon']
                
                print(f"\n📍 Procurando card Auto Ban para: {champ_name}")
                
                found = False
                for card in app.ui_manager.feature_cards:
                    if hasattr(card, 'title_text') and 'AUTO BAN' in card.title_text.upper():
                        print(f"   ✅ Card encontrado: {id(card)}")
                        self._autoban_data['card_ref'] = card
                        self._apply_icon_now(card, icon, champ_name)
                        found = True
                        break
                
                if not found:
                    print(f"   ⚠️ Card Auto Ban não encontrada!")
            
            print("\n" + "="*60)
            print("✅ SINCRONIZAÇÃO CONCLUÍDA")
            print("="*60 + "\n")
        
        except Exception as e:
            print(f"❌ Erro na sincronização: {e}")
            import traceback
            traceback.print_exc()
    
    def get_instalock_data(self):
        """Retorna dados salvos do instalock"""
        return self._instalock_data.copy()
    
    def get_autoban_data(self):
        """Retorna dados salvos do autoban"""
        return self._autoban_data.copy()
    
    def clear_cache(self):
        """Limpa cache de imagens"""
        self._champion_image_cache.clear()
        self._persistent_references.clear()
        print("🗑️ Cache de ícones limpo")