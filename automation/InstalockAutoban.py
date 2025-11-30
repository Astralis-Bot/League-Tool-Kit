"""
Instalock and Auto-ban module for champion select automation.
Automatically picks and bans champions based on user preferences.
"""

import threading
import time
import random
from core import Rengar
import logging
from typing import Optional, List, Dict
from difflib import get_close_matches

logger = logging.getLogger(__name__)


class InstalockAutoban:
    """
    Manages automatic champion picking (instalock) and banning in champion select.
    Supports primary champion with multiple backups and random selection.
    """
    
    def __init__(self):
        """Initialize instalock and auto-ban system."""
        self.champ_dict: Dict[str, int] = {}
        
        # Instalock settings
        self.instalock_enabled = False
        self.instalock_champion = "None"
        self.instalock_backup_2 = "None"
        self.instalock_backup_3 = "None"
        
        # Auto-ban settings
        self.auto_ban_enabled = False
        self.auto_ban_champion = "None"
        self.auto_ban_backup_2 = "None"
        self.auto_ban_backup_3 = "None"
        
        # Pre-hover settings
        self.pre_hover_enabled = True  # Novo: habilitar hover antes dos bans
        self.avoid_ally_hovers = True  # Novo: evitar banir campeões que aliados querem
        
        # Core components
        self.rengar = Rengar()
        self.monitor_thread: Optional[threading.Thread] = None
        self.is_running = False
        self._lock = threading.Lock()
        
        # State tracking
        self._last_session_id = None
        self._processed_actions = set()
        self._pre_hover_done = False  # Novo: rastrear se já fez hover
        
        logger.info("📄 Loading champion data...")
        success = self.update_champion_list()
        
        if not success:
            logger.warning("⚠️ Champion list will be loaded when League Client is available")
    
    def update_champion_list(self) -> bool:
        """
        Update the champion list from the client.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Try primary endpoint
            response = self.rengar.lcu_request(
                "GET",
                "/lol-champ-select/v1/all-grid-champions",
                ""
            )
            
            if response.status_code == 200:
                champion_data = response.json()
                self._parse_champions(champion_data)
                logger.info(f"✅ Champion list loaded: {len(self.champ_dict)} champions")
                return True
            
            # Try fallback endpoint
            response = self.rengar.lcu_request(
                "GET",
                "/lol-champions/v1/inventories/local-player/champions",
                ""
            )
            
            if response.status_code == 200:
                champion_data = response.json()
                self._parse_champions(champion_data, filter_invalid=True)
                logger.info(f"✅ Champion list loaded: {len(self.champ_dict)} champions")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error loading champions: {e}")
            return False
    
    def _parse_champions(self, champion_data: List[dict], filter_invalid: bool = False) -> None:
        """
        Parse champion data and populate champion dictionary.
        
        Args:
            champion_data: List of champion data from API
            filter_invalid: Whether to filter out invalid champions
        """
        with self._lock:
            self.champ_dict.clear()
            
            for champ in champion_data:
                champ_id = champ.get("id")
                champ_name = champ.get("name")
                
                if champ_id and champ_name:
                    if filter_invalid and champ_id == -1:
                        continue
                    self.champ_dict[champ_name.lower()] = champ_id
    
    def champ_name_to_id(self, champ_name: str) -> int:
        """
        Convert champion name to champion ID.
        
        Args:
            champ_name: Champion name (case-insensitive)
            
        Returns:
            Champion ID or -1 if not found
        """
        if not self.champ_dict:
            self.update_champion_list()
        
        champ_name = champ_name.lower().strip()
        
        # Exact match
        champ_id = self.champ_dict.get(champ_name, -1)
        if champ_id != -1:
            return champ_id
        
        # Partial match
        for name, id_val in self.champ_dict.items():
            if champ_name in name or name in champ_name:
                return id_val
        
        return -1
    
    def get_champion_suggestions(self, partial_name: str, limit: int = 5) -> List[str]:
        """
        Get champion name suggestions based on partial input.
        
        Args:
            partial_name: Partial champion name
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested champion names
        """
        if not self.champ_dict:
            return []
        
        partial = partial_name.lower().strip()
        
        # Use fuzzy matching for better suggestions
        all_names = list(self.champ_dict.keys())
        matches = get_close_matches(partial, all_names, n=limit, cutoff=0.6)
        
        # Also include partial matches
        partial_matches = [
            name for name in all_names
            if partial in name and name not in matches
        ]
        
        # Combine and limit
        suggestions = matches + partial_matches
        return [name.title() for name in suggestions[:limit]]
    
    def get_ally_hovers(self) -> List[int]:
        """
        Get list of champion IDs that allies have hovered/selected.
        
        Returns:
            List of champion IDs that allies want to play
        """
        try:
            response = self.rengar.lcu_request(
                "GET",
                "/lol-champ-select/v1/session",
                ""
            )
            
            if response.status_code != 200:
                return []
            
            session_data = response.json()
            cell_id = session_data.get("localPlayerCellId")
            
            if cell_id is None:
                return []
            
            ally_hovers = []
            
            # Check all pick actions
            for actions in session_data.get("actions", []):
                if not isinstance(actions, list):
                    continue
                
                for action in actions:
                    # Skip if it's our own action
                    if action.get("actorCellId") == cell_id:
                        continue
                    
                    # Check if it's a pick action with a champion selected
                    if action.get("type") == "pick":
                        champ_id = action.get("championId", 0)
                        # If ally has hovered a champion (championId != 0 and not completed)
                        if champ_id > 0 and not action.get("completed", False):
                            if champ_id not in ally_hovers:
                                ally_hovers.append(champ_id)
                                logger.info(f"👥 Ally wants to play: Champion ID {champ_id}")
            
            return ally_hovers
            
        except Exception as e:
            logger.error(f"❌ Error getting ally hovers: {e}")
            return []
    
    def is_champion_banned(self, champion_id: int) -> bool:
        """
        Check if a champion is already banned in current session.
        
        Args:
            champion_id: Champion ID to check
            
        Returns:
            True if champion is banned, False otherwise
        """
        try:
            response = self.rengar.lcu_request(
                "GET",
                "/lol-champ-select/v1/session",
                ""
            )
            
            if response.status_code != 200:
                return False
            
            session_data = response.json()
            
            # Check ban actions
            for actions in session_data.get("actions", []):
                if not isinstance(actions, list):
                    continue
                
                for action in actions:
                    if (action.get("type") == "ban" and
                        action.get("completed") and
                        action.get("championId") == champion_id):
                        return True
            
            # Check bans object
            bans = session_data.get("bans", {})
            if isinstance(bans, dict):
                for team_bans in bans.values():
                    if isinstance(team_bans, list) and champion_id in team_bans:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def get_available_champion(self) -> int:
        """
        Get available champion ID for picking, checking backups if needed.
        
        Returns:
            Champion ID to pick or -1 if none available
        """
        # Random selection
        if self.instalock_champion == "Random":
            if self.champ_dict:
                available_champs = [
                    champ_id for champ_id in self.champ_dict.values()
                    if not self.is_champion_banned(champ_id)
                ]
                if available_champs:
                    return random.choice(available_champs)
            return -1
        
        # Try primary champion
        champion_id = self.champ_name_to_id(self.instalock_champion)
        if champion_id != -1:
            if not self.is_champion_banned(champion_id):
                logger.info(f"✅ Picking 1st choice: {self.instalock_champion}")
                return champion_id
            logger.warning(f"⚠️ 1st choice {self.instalock_champion} is BANNED")
        
        # Try second backup
        if self.instalock_backup_2 != "None":
            backup2_id = self.champ_name_to_id(self.instalock_backup_2)
            if backup2_id != -1:
                if not self.is_champion_banned(backup2_id):
                    logger.info(f"✅ Picking 2nd choice: {self.instalock_backup_2}")
                    return backup2_id
                logger.warning(f"⚠️ 2nd choice {self.instalock_backup_2} is BANNED")
        
        # Try third backup
        if self.instalock_backup_3 != "None":
            backup3_id = self.champ_name_to_id(self.instalock_backup_3)
            if backup3_id != -1:
                if not self.is_champion_banned(backup3_id):
                    logger.info(f"✅ Picking 3rd choice: {self.instalock_backup_3}")
                    return backup3_id
                logger.warning(f"⚠️ 3rd choice {self.instalock_backup_3} is BANNED")
        
        logger.error("🚫 All your champions are banned! Please pick manually.")
        return -1
    
    def _hover_champion(self, champion_id: int) -> bool:
        """
        Hover over a champion (show intent without locking).
        
        Args:
            champion_id: Champion ID to hover
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Primeiro, precisamos encontrar a action de pick disponível
            response = self.rengar.lcu_request(
                "GET",
                "/lol-champ-select/v1/session",
                ""
            )
            
            if response.status_code != 200:
                return False
            
            session_data = response.json()
            cell_id = session_data.get("localPlayerCellId")
            
            if cell_id is None:
                return False
            
            # Procurar pela action de pick do jogador
            for actions in session_data.get("actions", []):
                if not isinstance(actions, list):
                    continue
                
                for action in actions:
                    if (action.get("actorCellId") == cell_id and
                        action.get("type") == "pick" and
                        not action.get("completed", False)):
                        
                        action_id = action.get("id")
                        
                        # Hover (completed=False mostra intenção)
                        hover_response = self.rengar.lcu_request(
                            "PATCH",
                            f"/lol-champ-select/v1/session/actions/{action_id}",
                            {"championId": champion_id, "completed": False}
                        )
                        
                        if hover_response.status_code in [204, 200]:
                            return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error hovering champion: {e}")
            return False
    
    def get_available_ban_champion(self) -> int:
        """
        Get available champion ID for banning, checking backups if needed.
        Also avoids banning champions that allies have hovered.
        
        Returns:
            Champion ID to ban or -1 if none available
        """
        # Get ally hovers if feature is enabled
        ally_hovers = []
        if self.avoid_ally_hovers:
            ally_hovers = self.get_ally_hovers()
            if ally_hovers:
                logger.info(f"🛡️ Protecting {len(ally_hovers)} ally champion(s) from ban")
        
        # Try primary ban champion
        champion_id = self.champ_name_to_id(self.auto_ban_champion)
        if champion_id != -1:
            # Check if already banned
            if self.is_champion_banned(champion_id):
                logger.warning(f"⚠️ 1st ban {self.auto_ban_champion} already BANNED")
            # Check if ally wants this champion
            elif champion_id in ally_hovers:
                logger.warning(f"👥 1st ban {self.auto_ban_champion} is wanted by ALLY - skipping")
            else:
                logger.info(f"✅ Banning 1st choice: {self.auto_ban_champion}")
                return champion_id
        
        # Try second backup
        if self.auto_ban_backup_2 != "None":
            backup2_id = self.champ_name_to_id(self.auto_ban_backup_2)
            if backup2_id != -1:
                if self.is_champion_banned(backup2_id):
                    logger.warning(f"⚠️ 2nd ban {self.auto_ban_backup_2} already BANNED")
                elif backup2_id in ally_hovers:
                    logger.warning(f"👥 2nd ban {self.auto_ban_backup_2} is wanted by ALLY - skipping")
                else:
                    logger.info(f"✅ Banning 2nd choice: {self.auto_ban_backup_2}")
                    return backup2_id
        
        # Try third backup
        if self.auto_ban_backup_3 != "None":
            backup3_id = self.champ_name_to_id(self.auto_ban_backup_3)
            if backup3_id != -1:
                if self.is_champion_banned(backup3_id):
                    logger.warning(f"⚠️ 3rd ban {self.auto_ban_backup_3} already BANNED")
                elif backup3_id in ally_hovers:
                    logger.warning(f"👥 3rd ban {self.auto_ban_backup_3} is wanted by ALLY - skipping")
                else:
                    logger.info(f"✅ Banning 3rd choice: {self.auto_ban_backup_3}")
                    return backup3_id
        
        logger.error("🚫 All ban options unavailable! Skipping ban.")
        return -1
    
    def set_instalock_champion(self, champion_name: str) -> bool:
        """
        Set the primary instalock champion.
        
        Args:
            champion_name: Champion name, "Random", or "99"/"disable" to disable
            
        Returns:
            True if successful, False otherwise
        """
        champion_name = champion_name.strip()
        
        # Disable instalock
        if champion_name in ["99", "disable", "off"]:
            with self._lock:
                self.instalock_enabled = False
                self.instalock_champion = "None"
            logger.info("❌ Instalock disabled")
            return True
        
        # Random selection
        if champion_name.lower() == "random":
            if not self.champ_dict:
                logger.warning("⚠️ Champion list not loaded, attempting to load...")
                if not self.update_champion_list():
                    return False
            
            with self._lock:
                self.instalock_champion = "Random"
                self.instalock_enabled = True
            logger.info("✅ Instalock set to: Random")
            return True
        
        # Specific champion
        champ_id = self.champ_name_to_id(champion_name)
        if champ_id == -1:
            suggestions = self.get_champion_suggestions(champion_name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{champion_name}' not found")
            return False
        
        # Get correct capitalization
        correct_name = next(
            (name for name in self.champ_dict.keys() if name == champion_name.lower()),
            champion_name.lower()
        )
        
        with self._lock:
            self.instalock_champion = correct_name
            self.instalock_enabled = True
        
        logger.info(f"✅ Instalock set to: {correct_name.title()}")
        return True
    
    def set_instalock_backup_2(self, champion_name: str) -> bool:
        """Set second backup champion for instalock."""
        return self._set_backup(champion_name, 2)
    
    def set_instalock_backup_3(self, champion_name: str) -> bool:
        """Set third backup champion for instalock."""
        return self._set_backup(champion_name, 3)
    
    def _set_backup(self, champion_name: str, backup_number: int) -> bool:
        """
        Internal method to set backup champions.
        
        Args:
            champion_name: Champion name or "none" to clear
            backup_number: Backup slot (2 or 3)
            
        Returns:
            True if successful, False otherwise
        """
        champion_name = champion_name.strip()
        backup_attr = f"instalock_backup_{backup_number}"
        
        # Clear backup
        if champion_name.lower() in ["99", "disable", "none", "off"]:
            with self._lock:
                setattr(self, backup_attr, "None")
            logger.info(f"✅ {backup_number}{'nd' if backup_number == 2 else 'rd'} backup cleared")
            return True
        
        # Set specific champion
        champ_id = self.champ_name_to_id(champion_name)
        if champ_id == -1:
            suggestions = self.get_champion_suggestions(champion_name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{champion_name}' not found")
            return False
        
        correct_name = next(
            (name for name in self.champ_dict.keys() if name == champion_name.lower()),
            champion_name.lower()
        )
        
        with self._lock:
            setattr(self, backup_attr, correct_name)
        
        logger.info(f"✅ {backup_number}{'nd' if backup_number == 2 else 'rd'} backup set: {correct_name.title()}")
        return True
    
    def set_auto_ban_champion(self, champion_name: str) -> bool:
        """
        Set champion for automatic banning.
        
        Args:
            champion_name: Champion name or "99"/"disable" to disable
            
        Returns:
            True if successful, False otherwise
        """
        champion_name = champion_name.strip()
        
        # Disable auto-ban
        if champion_name in ["99", "disable", "off"]:
            with self._lock:
                self.auto_ban_enabled = False
                self.auto_ban_champion = "None"
            logger.info("❌ Auto-ban disabled")
            return True
        
        # Set specific champion
        champ_id = self.champ_name_to_id(champion_name)
        if champ_id == -1:
            suggestions = self.get_champion_suggestions(champion_name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{champion_name}' not found")
            return False
        
        correct_name = next(
            (name for name in self.champ_dict.keys() if name == champion_name.lower()),
            champion_name.lower()
        )
        
        with self._lock:
            self.auto_ban_champion = correct_name
            self.auto_ban_enabled = True
        
        logger.info(f"✅ Auto-ban set to: {correct_name.title()}")
        return True
    
    def set_auto_ban_champion(self, champion_name: str) -> bool:
        """
        Set champion for automatic banning.
        
        Args:
            champion_name: Champion name or "99"/"disable" to disable
            
        Returns:
            True if successful, False otherwise
        """
        champion_name = champion_name.strip()
        
        # Disable auto-ban
        if champion_name in ["99", "disable", "off"]:
            with self._lock:
                self.auto_ban_enabled = False
                self.auto_ban_champion = "None"
            logger.info("❌ Auto-ban disabled")
            return True
        
        # Set specific champion
        champ_id = self.champ_name_to_id(champion_name)
        if champ_id == -1:
            suggestions = self.get_champion_suggestions(champion_name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{champion_name}' not found")
            return False
        
        correct_name = next(
            (name for name in self.champ_dict.keys() if name == champion_name.lower()),
            champion_name.lower()
        )
        
        with self._lock:
            self.auto_ban_champion = correct_name
            self.auto_ban_enabled = True
        
        logger.info(f"✅ Auto-ban set to: {correct_name.title()}")
        return True
    
    def set_auto_ban_backup_2(self, champion_name: str) -> bool:
        """Set second backup champion for auto-ban."""
        return self._set_ban_backup(champion_name, 2)
    
    def set_auto_ban_backup_3(self, champion_name: str) -> bool:
        """Set third backup champion for auto-ban."""
        return self._set_ban_backup(champion_name, 3)
    
    def _set_ban_backup(self, champion_name: str, backup_number: int) -> bool:
        """
        Internal method to set ban backup champions.
        
        Args:
            champion_name: Champion name or "none" to clear
            backup_number: Backup slot (2 or 3)
            
        Returns:
            True if successful, False otherwise
        """
        champion_name = champion_name.strip()
        backup_attr = f"auto_ban_backup_{backup_number}"
        
        # Clear backup
        if champion_name.lower() in ["99", "disable", "none", "off"]:
            with self._lock:
                setattr(self, backup_attr, "None")
            logger.info(f"✅ Ban {backup_number}{'nd' if backup_number == 2 else 'rd'} backup cleared")
            return True
        
        # Set specific champion
        champ_id = self.champ_name_to_id(champion_name)
        if champ_id == -1:
            suggestions = self.get_champion_suggestions(champion_name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{champion_name}' not found")
            return False
        
        correct_name = next(
            (name for name in self.champ_dict.keys() if name == champion_name.lower()),
            champion_name.lower()
        )
        
        with self._lock:
            setattr(self, backup_attr, correct_name)
        
        logger.info(f"✅ Ban {backup_number}{'nd' if backup_number == 2 else 'rd'} backup set: {correct_name.title()}")
        return True
    
    def toggle_pre_hover(self) -> bool:
        """
        Toggle pre-ban hover on/off.
        
        Returns:
            New state of pre_hover_enabled
        """
        with self._lock:
            self.pre_hover_enabled = not self.pre_hover_enabled
        
        state = "✅ ON" if self.pre_hover_enabled else "❌ OFF"
        logger.info(f"Pre-ban hover is now {state}")
        return self.pre_hover_enabled
    
    def toggle_avoid_ally_hovers(self) -> bool:
        """
        Toggle avoiding banning ally hovered champions.
        
        Returns:
            New state of avoid_ally_hovers
        """
        with self._lock:
            self.avoid_ally_hovers = not self.avoid_ally_hovers
        
        state = "✅ ON" if self.avoid_ally_hovers else "❌ OFF"
        logger.info(f"Avoid ally bans is now {state}")
        return self.avoid_ally_hovers
    
    def monitor_champ_select(self) -> None:
        """Monitor champion select and perform automatic actions."""
        logger.info("👀 Champion select monitor started")
        champion_list_updated = bool(self.champ_dict)
        consecutive_errors = 0
        max_errors = 10
        
        while self.is_running:
            try:
                # Update champion list if needed
                if not champion_list_updated and not self.champ_dict:
                    if self.update_champion_list():
                        champion_list_updated = True
                
                # Get champion select session
                response = self.rengar.lcu_request(
                    "GET",
                    "/lol-champ-select/v1/session",
                    ""
                )
                
                # Not in champ select
                if response.status_code != 200 or "RPC_ERROR" in response.text:
                    self._last_session_id = None
                    self._processed_actions.clear()
                    self._pre_hover_done = False  # Reset hover status
                    time.sleep(0.5)
                    consecutive_errors = 0
                    continue
                
                session_data = response.json()
                cell_id = session_data.get("localPlayerCellId")
                
                if cell_id is None:
                    time.sleep(0.3)
                    continue
                
                # Reset processed actions on new session
                current_session_id = id(session_data)
                if current_session_id != self._last_session_id:
                    self._processed_actions.clear()
                    self._pre_hover_done = False  # Reset hover on new session
                    self._last_session_id = current_session_id
                
                # NOVO: Fazer hover antes da fase de ban se habilitado
                if (self.pre_hover_enabled and 
                    self.instalock_enabled and 
                    not self._pre_hover_done and
                    self.instalock_champion != "None"):
                    
                    # Verificar se estamos na fase de ban (antes do pick)
                    timer = session_data.get("timer", {})
                    phase = timer.get("phase", "")
                    
                    # Se ainda não começou a fase de pick
                    if phase in ["BAN_PICK", "PLANNING", ""]:
                        champion_id = self.get_available_champion()
                        if champion_id != -1:
                            if self._hover_champion(champion_id):
                                champ_name = self.instalock_champion
                                if champ_name == "Random":
                                    champ_name = "Random Champion"
                                logger.info(f"👆 Pre-hovering champion: {champ_name.title()}")
                                self._pre_hover_done = True
                
                # Process actions
                for actions in session_data.get("actions", []):
                    if not isinstance(actions, list):
                        continue
                    
                    for action in actions:
                        # Skip if not our action
                        if action.get("actorCellId") != cell_id:
                            continue
                        
                        action_id = action.get("id")
                        
                        # Skip if already processed
                        if action_id in self._processed_actions:
                            continue
                        
                        # Skip if completed
                        if action.get("completed", False):
                            self._processed_actions.add(action_id)
                            continue
                        
                        # Handle pick action
                        if (self.instalock_enabled and
                            action.get("type") == "pick" and
                            action.get("isInProgress", False)):
                            self._handle_pick_action(action_id)
                        
                        # Handle ban action
                        elif (self.auto_ban_enabled and
                              action.get("type") == "ban" and
                              action.get("isInProgress", False)):
                            self._handle_ban_action(action_id)
                
                consecutive_errors = 0
                time.sleep(0.2)
                
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"⚠️ Error in champion select monitor: {e}")
                
                if consecutive_errors >= max_errors:
                    logger.error("❌ Too many consecutive errors, stopping monitor")
                    self.is_running = False
                    break
                
                time.sleep(1)
        
        logger.info("🛑 Champion select monitor stopped")
    
    def _handle_pick_action(self, action_id: int) -> None:
        """Handle pick action."""
        champion_id = self.get_available_champion()
        
        if champion_id == -1:
            return
        
        try:
            response = self.rengar.lcu_request(
                "PATCH",
                f"/lol-champ-select/v1/session/actions/{action_id}",
                {"completed": True, "championId": champion_id}
            )
            
            if response.status_code in [204, 200]:
                self._processed_actions.add(action_id)
                logger.info(f"✅ Champion picked successfully! (ID: {champion_id})")
            else:
                logger.warning(f"⚠️ Failed to pick champion: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error picking champion: {e}")
    
    def _handle_ban_action(self, action_id: int) -> None:
        """Handle ban action."""
        champion_id = self.get_available_ban_champion()
        
        if champion_id == -1:
            return
        
        try:
            response = self.rengar.lcu_request(
                "PATCH",
                f"/lol-champ-select/v1/session/actions/{action_id}",
                {"completed": True, "championId": champion_id}
            )
            
            if response.status_code in [204, 200]:
                self._processed_actions.add(action_id)
                
                # Get champion name for logging
                champ_name = "Unknown"
                for name, cid in self.champ_dict.items():
                    if cid == champion_id:
                        champ_name = name.title()
                        break
                
                logger.info(f"✅ Champion banned successfully! ({champ_name})")
            else:
                logger.warning(f"⚠️ Failed to ban champion: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error banning champion: {e}")
    
    def toggle_instalock(self) -> bool:
        """Toggle instalock on/off."""
        with self._lock:
            self.instalock_enabled = not self.instalock_enabled
        
        state = "✅ ON" if self.instalock_enabled else "❌ OFF"
        logger.info(f"Instalock is now {state}")
        return self.instalock_enabled
    
    def toggle_auto_ban(self) -> bool:
        """Toggle auto-ban on/off."""
        with self._lock:
            self.auto_ban_enabled = not self.auto_ban_enabled
        
        state = "✅ ON" if self.auto_ban_enabled else "❌ OFF"
        logger.info(f"Auto-ban is now {state}")
        return self.auto_ban_enabled
    
    def start_monitor(self) -> None:
        """Start champion select monitoring thread."""
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.is_running = True
            self.monitor_thread = threading.Thread(
                target=self.monitor_champ_select,
                daemon=True,
                name="ChampSelectMonitor"
            )
            self.monitor_thread.start()
            logger.info("▶️ Monitor thread started")
    
    def start_threads(self) -> None:
        """Start all monitoring threads."""
        self.start_monitor()
    
    def stop(self) -> None:
        """Stop all monitoring threads."""
        self.is_running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        logger.info("ℹ️ All threads stopped")
    
    def get_instalock_status(self) -> str:
        """
        Get formatted instalock status string.
        
        Returns:
            Status string with primary and backup champions
        """
        status = f"{self.instalock_champion.title() if self.instalock_champion != 'None' else 'None'}"
        
        backups = []
        if self.instalock_backup_2 != "None":
            backups.append(f"2nd: {self.instalock_backup_2.title()}")
        if self.instalock_backup_3 != "None":
            backups.append(f"3rd: {self.instalock_backup_3.title()}")
        
        if backups:
            status += f" ({', '.join(backups)})"
        
        return status
    
    def get_auto_ban_status(self) -> str:
        """
        Get formatted auto-ban status string.
        
        Returns:
            Status string with primary and backup ban champions
        """
        status = f"{self.auto_ban_champion.title() if self.auto_ban_champion != 'None' else 'None'}"
        
        backups = []
        if self.auto_ban_backup_2 != "None":
            backups.append(f"2nd: {self.auto_ban_backup_2.title()}")
        if self.auto_ban_backup_3 != "None":
            backups.append(f"3rd: {self.auto_ban_backup_3.title()}")
        
        if backups:
            status += f" ({', '.join(backups)})"
        
        return status
    
    def get_status(self) -> dict:
        """
        Get complete status information.
        
        Returns:
            Dictionary with all status information
        """
        return {
            "instalock": {
                "enabled": self.instalock_enabled,
                "champion": self.instalock_champion,
                "backup_2": self.instalock_backup_2,
                "backup_3": self.instalock_backup_3,
                "display": self.get_instalock_status(),
                "pre_hover_enabled": self.pre_hover_enabled
            },
            "auto_ban": {
                "enabled": self.auto_ban_enabled,
                "champion": self.auto_ban_champion,
                "backup_2": self.auto_ban_backup_2,
                "backup_3": self.auto_ban_backup_3,
                "display": self.get_auto_ban_status(),
                "avoid_ally_hovers": self.avoid_ally_hovers
            },
            "monitor": {
                "running": self.is_running,
                "thread_alive": self.monitor_thread.is_alive() if self.monitor_thread else False
            },
            "champions_loaded": len(self.champ_dict)
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()