import requests
import json
from threading import Thread
from datetime import datetime, timedelta

class ChampionAPI:
    """Gerenciador de dados de campeões via API"""
    
    def __init__(self):
        self.api_url = "https://ddragon.leagueoflegends.com/api"
        self.cdn_url = "https://ddragon.leagueoflegends.com/cdn"
        self.version = None
        self.champions = []
        self.cache_expiry = None
        self.CACHE_DURATION = timedelta(hours=24)
        
        # Carregar versão e campeões na inicialização
        self.update_champions()
    
    def get_latest_version(self):
        """Obtém a versão mais recente do jogo"""
        try:
            response = requests.get(f"{self.api_url}/versions.json", timeout=10)
            if response.status_code == 200:
                versions = response.json()
                self.version = versions[0]
                return self.version
        except Exception as e:
            print(f"Erro ao obter versão: {e}")
        return None
    
    def update_champions(self):
        """Atualiza a lista de campeões da API"""
        try:
            # Verificar se cache ainda está válido
            if self.cache_expiry and datetime.now() < self.cache_expiry:
                return self.champions
            
            # Obter versão se não tiver
            if not self.version:
                self.get_latest_version()
            
            if not self.version:
                print("Erro: Não foi possível obter a versão do jogo")
                return []
            
            # Buscar dados dos campeões
            url = f"{self.cdn_url}/{self.version}/data/pt_BR/champion.json"
            print(f"Carregando campeões de: {url}")
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                self.champions = []
                
                for champion_key, champion_data in data['data'].items():
                    champ = {
                        'name': champion_data['name'],
                        'title': champion_data['title'],
                        'key': champion_key,
                        'id': champion_data['id'],
                        'icon': f"{self.cdn_url}/{self.version}/img/champion/{champion_key}.png"
                    }
                    self.champions.append(champ)
                
                # Ordenar alfabeticamente
                self.champions.sort(key=lambda x: x['name'])
                
                # Atualizar cache
                self.cache_expiry = datetime.now() + self.CACHE_DURATION
                
                print(f"✓ {len(self.champions)} campeões carregados com sucesso!")
                return self.champions
            else:
                print(f"Erro ao buscar campeões: Status {response.status_code}")
        except requests.exceptions.Timeout:
            print("Erro: Timeout ao conectar à API")
        except requests.exceptions.ConnectionError:
            print("Erro: Falha na conexão com a API")
        except Exception as e:
            print(f"Erro ao atualizar campeões: {e}")
        
        return []
    
    def get_champions(self):
        """Retorna a lista de campeões"""
        if not self.champions:
            self.update_champions()
        return self.champions
    
    def search_champion(self, query):
        """Busca um campeão pelo nome"""
        query = query.lower()
        return [c for c in self.champions if query in c['name'].lower()]
    
    def get_champion_by_name(self, name):
        """Obtém um campeão pelo nome exato"""
        for champ in self.champions:
            if champ['name'].lower() == name.lower():
                return champ
        return None


class APIManager:
    """Gerenciador de APIs do jogo"""
    
    def __init__(self):
        self.champion_api = ChampionAPI()
        self.loading = False
        # Carregar campeões na inicialização
        self.champion_api.update_champions()
    
    def load_champions_async(self, callback=None):
        """Carrega campeões em uma thread separada"""
        def load():
            self.loading = True
            try:
                self.champion_api.update_champions()
                if callback:
                    callback(True)
            except Exception as e:
                print(f"Erro ao carregar campeões: {e}")
                if callback:
                    callback(False)
            finally:
                self.loading = False
        
        thread = Thread(target=load, daemon=True)
        thread.start()
    
    def get_champions(self):
        """Retorna lista de campeões"""
        champs = self.champion_api.get_champions()
        if not champs:
            print("⚠️ Aviso: Nenhum campeão carregado, tentando novamente...")
            champs = self.champion_api.update_champions()
        return champs
    
    def search_champions(self, query):
        """Busca campeões"""
        return self.champion_api.search_champion(query)
    
    def get_champion_icon(self, champion_name):
        """Obtém a URL do ícone de um campeão"""
        champ = self.champion_api.get_champion_by_name(champion_name)
        if champ:
            return champ['icon']
        return None


# Instância global
api_manager = APIManager()