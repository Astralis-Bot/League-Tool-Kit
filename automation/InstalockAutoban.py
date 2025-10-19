import threading
import time
import random
from core import Rengar


class InstalockAutoban:
    def __init__(self):
        self.champ_dict = {}
        self.instalock_enabled = False
        self.instalock_champion = "None"
        self.auto_ban_enabled = False
        self.auto_ban_champion = "None"
        self.rengar = Rengar()
        self.monitor_thread = None
        self.is_running = True
        
        # Tenta carregar campeões na inicialização
        print("🔄 Loading champion data...")
        success = self.update_champion_list()
        if not success:
            print("⚠️  Champion list will be loaded when League Client is available")

    def update_champion_list(self):
        """
        Atualiza a lista de campeões obtendo seus IDs e nomes da API LCU.
        """
        try:
            # Tenta o endpoint principal
            response = self.rengar.lcu_request("GET", "/lol-champ-select/v1/all-grid-champions", "")
            
            if response.status_code == 200:
                champion_data = response.json()
                for champ in champion_data:
                    champ_id = champ.get("id")
                    champ_name = champ.get("name")
                    if champ_id and champ_name:
                        self.champ_dict[champ_name.lower()] = champ_id
                print(f"✓ Champion list loaded: {len(self.champ_dict)} champions available")
                return True
            else:
                # Tenta endpoint alternativo
                response = self.rengar.lcu_request("GET", "/lol-champions/v1/inventories/local-player/champions", "")
                if response.status_code == 200:
                    champion_data = response.json()
                    for champ in champion_data:
                        champ_id = champ.get("id")
                        champ_name = champ.get("name")
                        if champ_id and champ_name and champ_id != -1:
                            self.champ_dict[champ_name.lower()] = champ_id
                    print(f"✓ Champion list loaded: {len(self.champ_dict)} champions available")
                    return True
                else:
                    return False
        except Exception as e:
            return False

    def champ_name_to_id(self, champ_name):
        """
        Converte o nome de um campeão para o ID correspondente.
        """
        if not self.champ_dict:
            self.update_champion_list()
        
        champ_name = champ_name.lower().strip()
        champ_id = self.champ_dict.get(champ_name, -1)
        
        # Se não encontrou, tenta buscar por correspondência parcial
        if champ_id == -1:
            for name, id in self.champ_dict.items():
                if champ_name in name or name in champ_name:
                    return id
        
        return champ_id
    
    def get_champion_suggestions(self, partial_name):
        """Retorna sugestões de campeões baseado em nome parcial"""
        if not self.champ_dict:
            return []
        partial = partial_name.lower().strip()
        suggestions = [name.title() for name in self.champ_dict.keys() if partial in name]
        return suggestions[:5]

    def set_instalock_champion(self, champion_name):
        """Define o campeão para instalock"""
        champion_name = champion_name.strip()
        
        if champion_name == "99" or champion_name.lower() == "disable":
            self.instalock_enabled = False
            self.instalock_champion = "None"
            return True
        else:
            if champion_name.lower() == "random":
                if not self.champ_dict:
                    print("⚠️  Champion list not loaded yet. Please wait...")
                    self.update_champion_list()
                    if not self.champ_dict:
                        return False
                self.instalock_champion = "Random"
                self.instalock_enabled = True
                return True
            else:
                champ_id = self.champ_name_to_id(champion_name)
                if champ_id == -1:
                    suggestions = self.get_champion_suggestions(champion_name)
                    if suggestions:
                        print(f"💡 Did you mean: {', '.join(suggestions)}?")
                    if self.champ_dict:
                        print(f"📊 Total champions loaded: {len(self.champ_dict)}")
                    else:
                        print(f"⚠️  Champion list not loaded. Make sure League Client is running!")
                    return False
                else:
                    # Encontra o nome correto do campeão (com capitalização)
                    correct_name = next((name for name in self.champ_dict.keys() if name == champion_name.lower()), champion_name.lower())
                    self.instalock_champion = correct_name
                    self.instalock_enabled = True
                    return True

    def set_auto_ban_champion(self, champion_name):
        """Define o campeão para auto ban"""
        champion_name = champion_name.strip()
        
        if champion_name == "99" or champion_name.lower() == "disable":
            self.auto_ban_enabled = False
            self.auto_ban_champion = "None"
            return True
        else:
            champ_id = self.champ_name_to_id(champion_name)
            if champ_id == -1:
                suggestions = self.get_champion_suggestions(champion_name)
                if suggestions:
                    print(f"💡 Did you mean: {', '.join(suggestions)}?")
                if self.champ_dict:
                    print(f"📊 Total champions loaded: {len(self.champ_dict)}")
                else:
                    print(f"⚠️  Champion list not loaded. Make sure League Client is running!")
                return False
            else:
                # Encontra o nome correto do campeão (com capitalização)
                correct_name = next((name for name in self.champ_dict.keys() if name == champion_name.lower()), champion_name.lower())
                self.auto_ban_champion = correct_name
                self.auto_ban_enabled = True
                return True

    def monitor_champ_select(self):
        """
        Monitora continuamente o estado da seleção de campeões e executa
        Instalock ou AutoBan quando apropriado.
        """
        last_action_id = None
        champion_list_updated = False
        
        while self.is_running:
            try:
                # Atualiza lista de campeões se ainda não foi feito
                if not champion_list_updated and not self.champ_dict:
                    if self.update_champion_list():
                        champion_list_updated = True
                
                champ_select_resp = self.rengar.lcu_request("GET", "/lol-champ-select/v1/session", "")
                
                # Verifica se está em seleção de campeões
                if champ_select_resp.status_code != 200 or "RPC_ERROR" in champ_select_resp.text:
                    time.sleep(0.5)
                    last_action_id = None
                    continue

                root_champ_select = champ_select_resp.json()
                cell_id = root_champ_select.get("localPlayerCellId")

                if cell_id is None:
                    time.sleep(0.3)
                    continue

                # Processa as ações disponíveis
                for actions in root_champ_select.get("actions", []):
                    if not isinstance(actions, list):
                        continue
                    
                    for action in actions:
                        # Verifica se é a vez do jogador local
                        if action.get("actorCellId") != cell_id:
                            continue
                        
                        # Evita processar a mesma ação múltiplas vezes
                        action_id = action.get("id")
                        if action.get("completed", False) or action_id == last_action_id:
                            continue
                        
                        # INSTALOCK - Pick de campeão
                        if self.instalock_enabled and action.get("type") == "pick" and action.get("isInProgress", False):
                            
                            if self.instalock_champion == "Random":
                                if self.champ_dict:
                                    instalock_champs = list(self.champ_dict.items())
                                    champion_id = random.choice(instalock_champs)[1]
                                else:
                                    continue
                            else:
                                champion_id = self.champ_name_to_id(self.instalock_champion)

                            if champion_id != -1:
                                try:
                                    patch_resp = self.rengar.lcu_request(
                                        "PATCH",
                                        f"/lol-champ-select/v1/session/actions/{action_id}",
                                        {"completed": True, "championId": champion_id}
                                    )
                                    
                                    if patch_resp.status_code in [204, 200]:
                                        last_action_id = action_id
                                except:
                                    pass
                        
                        # AUTO BAN - Ban de campeão
                        elif self.auto_ban_enabled and action.get("type") == "ban" and action.get("isInProgress", False):
                            champion_id = self.champ_name_to_id(self.auto_ban_champion)

                            if champion_id != -1:
                                try:
                                    patch_resp = self.rengar.lcu_request(
                                        "PATCH",
                                        f"/lol-champ-select/v1/session/actions/{action_id}",
                                        {"completed": True, "championId": champion_id}
                                    )
                                    
                                    if patch_resp.status_code in [204, 200]:
                                        last_action_id = action_id
                                except:
                                    pass

                time.sleep(0.2)
                
            except:
                time.sleep(0.5)

    def toggle_instalock(self):
        """Alterna o estado do Instalock"""
        self.instalock_enabled = not self.instalock_enabled
        return self.instalock_enabled

    def toggle_auto_ban(self):
        """Alterna o estado do AutoBan"""
        self.auto_ban_enabled = not self.auto_ban_enabled
        return self.auto_ban_enabled

    def start_monitor(self):
        """Inicia o monitoramento em uma única thread"""
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.monitor_thread = threading.Thread(target=self.monitor_champ_select, daemon=True)
            self.monitor_thread.start()

    def start_threads(self):
        """Método mantido para compatibilidade - inicia o monitor"""
        self.start_monitor()
    
    def stop(self):
        """Para o monitoramento"""
        self.is_running = False