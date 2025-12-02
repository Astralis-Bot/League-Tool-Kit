"""
Refactored champion select automation - cleaner separation of concerns.
"""

import threading
import time
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Set
from difflib import get_close_matches
import logging

logger = logging.getLogger(__name__)


@dataclass
class ChampionSelection:
    """Configuration for champion selection (pick or ban)."""
    primary: str = "None"
    backup_2: str = "None"
    backup_3: str = "None"
    enabled: bool = False
    
    def get_champions(self) -> List[str]:
        """Get list of configured champions in priority order."""
        champs = []
        if self.primary != "None":
            champs.append(self.primary)
        if self.backup_2 != "None":
            champs.append(self.backup_2)
        if self.backup_3 != "None":
            champs.append(self.backup_3)
        return champs


@dataclass
class SelectionOptions:
    """Additional options for champion selection."""
    pre_hover_enabled: bool = True
    avoid_ally_hovers: bool = True


class ChampionRegistry:
    """Manages champion data and name/ID conversion."""
    
    def __init__(self, rengar):
        self.rengar = rengar
        self._champ_dict: Dict[str, int] = {}
        self._lock = threading.Lock()
    
    def load(self) -> bool:
        """Load champion list from client."""
        try:
            # Try primary endpoint
            response = self.rengar.lcu_request("GET", "/lol-champ-select/v1/all-grid-champions", "")
            
            if response.status_code == 200:
                self._parse_data(response.json())
                logger.info(f"✅ Loaded {len(self._champ_dict)} champions")
                return True
            
            # Fallback endpoint
            response = self.rengar.lcu_request("GET", "/lol-champions/v1/inventories/local-player/champions", "")
            
            if response.status_code == 200:
                self._parse_data(response.json(), filter_invalid=True)
                logger.info(f"✅ Loaded {len(self._champ_dict)} champions")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error loading champions: {e}")
            return False
    
    def _parse_data(self, data: List[dict], filter_invalid: bool = False) -> None:
        """Parse champion data from API response."""
        with self._lock:
            self._champ_dict.clear()
            for champ in data:
                champ_id = champ.get("id")
                champ_name = champ.get("name")
                
                if champ_id and champ_name:
                    if filter_invalid and champ_id == -1:
                        continue
                    self._champ_dict[champ_name.lower()] = champ_id
    
    def get_id(self, name: str) -> int:
        """Convert champion name to ID. Returns -1 if not found."""
        if not self._champ_dict:
            self.load()
        
        name = name.lower().strip()
        
        # Exact match
        if name in self._champ_dict:
            return self._champ_dict[name]
        
        # Partial match
        for champ_name, champ_id in self._champ_dict.items():
            if name in champ_name or champ_name in name:
                return champ_id
        
        return -1
    
    def get_suggestions(self, partial: str, limit: int = 5) -> List[str]:
        """Get champion name suggestions for partial input."""
        if not self._champ_dict:
            return []
        
        partial = partial.lower().strip()
        all_names = list(self._champ_dict.keys())
        
        # Fuzzy matching
        matches = get_close_matches(partial, all_names, n=limit, cutoff=0.6)
        
        # Partial matches
        partial_matches = [n for n in all_names if partial in n and n not in matches]
        
        suggestions = matches + partial_matches
        return [name.title() for name in suggestions[:limit]]
    
    def get_all_ids(self) -> List[int]:
        """Get all champion IDs."""
        return list(self._champ_dict.values())
    
    def get_name(self, champ_id: int) -> str:
        """Get champion name from ID."""
        for name, cid in self._champ_dict.items():
            if cid == champ_id:
                return name.title()
        return "Unknown"
    
    def is_loaded(self) -> bool:
        """Check if champion data is loaded."""
        return bool(self._champ_dict)


class ChampSelectSession:
    """Handles champion select session queries."""
    
    def __init__(self, rengar):
        self.rengar = rengar
    
    def get_session(self) -> Optional[dict]:
        """Get current champion select session data."""
        try:
            response = self.rengar.lcu_request("GET", "/lol-champ-select/v1/session", "")
            if response.status_code == 200 and "RPC_ERROR" not in response.text:
                return response.json()
            return None
        except Exception:
            return None
    
    def get_cell_id(self, session: dict) -> Optional[int]:
        """Get local player's cell ID from session."""
        return session.get("localPlayerCellId")
    
    def is_champion_banned(self, champion_id: int, session: dict) -> bool:
        """Check if champion is already banned."""
        # Check completed ban actions
        for actions in session.get("actions", []):
            if not isinstance(actions, list):
                continue
            
            for action in actions:
                if (action.get("type") == "ban" and
                    action.get("completed") and
                    action.get("championId") == champion_id):
                    return True
        
        # Check bans object
        bans = session.get("bans", {})
        if isinstance(bans, dict):
            for team_bans in bans.values():
                if isinstance(team_bans, list) and champion_id in team_bans:
                    return True
        
        return False
    
    def get_ally_hovers(self, session: dict, cell_id: int) -> List[int]:
        """Get list of champions that allies have hovered."""
        ally_hovers = []
        
        for actions in session.get("actions", []):
            if not isinstance(actions, list):
                continue
            
            for action in actions:
                if action.get("actorCellId") == cell_id:
                    continue
                
                if action.get("type") == "pick":
                    champ_id = action.get("championId", 0)
                    if champ_id > 0 and not action.get("completed", False):
                        if champ_id not in ally_hovers:
                            ally_hovers.append(champ_id)
        
        return ally_hovers


class ChampionSelector:
    """Selects champions based on configuration and availability."""
    
    def __init__(self, registry: ChampionRegistry, session_handler: ChampSelectSession):
        self.registry = registry
        self.session = session_handler
    
    def select_pick(self, config: ChampionSelection, session_data: dict) -> int:
        """Select a champion to pick based on configuration."""
        # Random selection
        if config.primary == "Random":
            available = [
                cid for cid in self.registry.get_all_ids()
                if not self.session.is_champion_banned(cid, session_data)
            ]
            return random.choice(available) if available else -1
        
        # Try champions in priority order
        for i, champ_name in enumerate(config.get_champions(), 1):
            champ_id = self.registry.get_id(champ_name)
            
            if champ_id == -1:
                continue
            
            if self.session.is_champion_banned(champ_id, session_data):
                logger.warning(f"⚠️ {i}{'st' if i==1 else 'nd' if i==2 else 'rd'} choice {champ_name.title()} is BANNED")
                continue
            
            logger.info(f"✅ Picking {i}{'st' if i==1 else 'nd' if i==2 else 'rd'} choice: {champ_name.title()}")
            return champ_id
        
        logger.error("🚫 All pick options unavailable!")
        return -1
    
    def select_ban(self, config: ChampionSelection, session_data: dict, 
                   cell_id: int, avoid_ally_hovers: bool) -> int:
        """Select a champion to ban based on configuration."""
        # Get ally hovers if needed
        ally_hovers = []
        if avoid_ally_hovers:
            ally_hovers = self.session.get_ally_hovers(session_data, cell_id)
            if ally_hovers:
                logger.info(f"🛡️ Protecting {len(ally_hovers)} ally champion(s)")
        
        # Try champions in priority order
        for i, champ_name in enumerate(config.get_champions(), 1):
            champ_id = self.registry.get_id(champ_name)
            
            if champ_id == -1:
                continue
            
            if self.session.is_champion_banned(champ_id, session_data):
                logger.warning(f"⚠️ {i}{'st' if i==1 else 'nd' if i==2 else 'rd'} ban {champ_name.title()} already BANNED")
                continue
            
            if champ_id in ally_hovers:
                logger.warning(f"👥 {i}{'st' if i==1 else 'nd' if i==2 else 'rd'} ban {champ_name.title()} wanted by ALLY")
                continue
            
            logger.info(f"✅ Banning {i}{'st' if i==1 else 'nd' if i==2 else 'rd'} choice: {champ_name.title()}")
            return champ_id
        
        logger.error("🚫 All ban options unavailable!")
        return -1


class InstalockAutoban:
    """Main class for champion select automation."""
    
    def __init__(self):
        from core import Rengar
        self.rengar = Rengar()
        
        # Components
        self.registry = ChampionRegistry(self.rengar)
        self.session_handler = ChampSelectSession(self.rengar)
        self.selector = ChampionSelector(self.registry, self.session_handler)
        
        # Configuration
        self.instalock = ChampionSelection()
        self.auto_ban = ChampionSelection()
        self.options = SelectionOptions()
        
        # Thread management
        self.monitor_thread: Optional[threading.Thread] = None
        self.is_running = False
        self._lock = threading.Lock()
        
        # State tracking
        self._last_session_id = None
        self._processed_actions: Set[int] = set()
        self._pre_hover_done = False
        
        logger.info("📄 Loading champion data...")
        if not self.registry.load():
            logger.warning("⚠️ Champion list will be loaded when client is available")
    
    # Compatibility properties for main.py
    @property
    def instalock_enabled(self) -> bool:
        """Compatibility: Get instalock enabled state."""
        return self.instalock.enabled
    
    @instalock_enabled.setter
    def instalock_enabled(self, value: bool):
        """Compatibility: Set instalock enabled state."""
        self.instalock.enabled = value
    
    @property
    def auto_ban_enabled(self) -> bool:
        """Compatibility: Get auto-ban enabled state."""
        return self.auto_ban.enabled
    
    @auto_ban_enabled.setter
    def auto_ban_enabled(self, value: bool):
        """Compatibility: Set auto-ban enabled state."""
        self.auto_ban.enabled = value
    
    # Configuration methods
    def set_instalock_champion(self, name: str) -> bool:
        """Set primary instalock champion."""
        return self._set_champion(name, self.instalock, "primary", is_pick=True)
    
    def set_instalock_backup_2(self, name: str) -> bool:
        """Set second instalock backup."""
        return self._set_champion(name, self.instalock, "backup_2")
    
    def set_instalock_backup_3(self, name: str) -> bool:
        """Set third instalock backup."""
        return self._set_champion(name, self.instalock, "backup_3")
    
    def set_auto_ban_champion(self, name: str) -> bool:
        """Set primary auto-ban champion."""
        result = self._set_champion(name, self.auto_ban, "primary", is_ban=True)
        
        # Log the state after setting
        if result:
            logger.debug(f"Auto-ban configuration after set: enabled={self.auto_ban.enabled}, primary={self.auto_ban.primary}")
        
        return result
    
    def set_auto_ban_backup_2(self, name: str) -> bool:
        """Set second auto-ban backup."""
        return self._set_champion(name, self.auto_ban, "backup_2")
    
    def set_auto_ban_backup_3(self, name: str) -> bool:
        """Set third auto-ban backup."""
        return self._set_champion(name, self.auto_ban, "backup_3")
    
    def _set_champion(self, name: str, config: ChampionSelection, 
                     slot: str, is_pick: bool = False, is_ban: bool = False) -> bool:
        """Internal method to set champion in configuration."""
        name = name.strip()
        
        # Handle disable
        if name.lower() in ["99", "disable", "off", "none"]:
            with self._lock:
                setattr(config, slot, "None")
                if slot == "primary":
                    config.enabled = False
            
            action = "Instalock" if is_pick else "Auto-ban" if is_ban else "Backup"
            logger.info(f"❌ {action} {'disabled' if slot == 'primary' else 'cleared'}")
            return True
        
        # Handle random (only for primary pick)
        if name.lower() == "random" and is_pick and slot == "primary":
            if not self.registry.is_loaded():
                if not self.registry.load():
                    return False
            
            with self._lock:
                config.primary = "Random"
                config.enabled = True
            logger.info("✅ Instalock set to: Random")
            return True
        
        # Validate champion
        champ_id = self.registry.get_id(name)
        if champ_id == -1:
            suggestions = self.registry.get_suggestions(name)
            if suggestions:
                logger.info(f"💡 Did you mean: {', '.join(suggestions)}?")
            logger.error(f"❌ Champion '{name}' not found")
            return False
        
        # Set champion
        correct_name = name.lower()
        with self._lock:
            setattr(config, slot, correct_name)
            if slot == "primary":
                config.enabled = True
        
        slot_desc = "primary" if slot == "primary" else "2nd backup" if slot == "backup_2" else "3rd backup"
        action = "Instalock" if is_pick else "Auto-ban" if is_ban else "Backup"
        logger.info(f"✅ {action} {slot_desc} set: {correct_name.title()}")
        
        # Extra debug for ban
        if is_ban and slot == "primary":
            logger.debug(f"🔍 After setting ban: config.enabled={config.enabled}, config.primary={config.primary}")
        
        return True
    
    # Toggle methods
    def toggle_instalock(self) -> bool:
        """Toggle instalock on/off."""
        with self._lock:
            self.instalock.enabled = not self.instalock.enabled
        logger.info(f"Instalock: {'✅ ON' if self.instalock.enabled else '❌ OFF'}")
        return self.instalock.enabled
    
    def toggle_auto_ban(self) -> bool:
        """Toggle auto-ban on/off."""
        with self._lock:
            self.auto_ban.enabled = not self.auto_ban.enabled
        
        status_msg = f"Auto-ban: {'✅ ON' if self.auto_ban.enabled else '❌ OFF'}"
        if self.auto_ban.enabled and self.auto_ban.primary != "None":
            status_msg += f" - Champion: {self.auto_ban.primary.title()}"
        
        logger.info(status_msg)
        
        # Log current state for debugging
        logger.debug(f"Auto-ban state - enabled={self.auto_ban.enabled}, primary={self.auto_ban.primary}, backup_2={self.auto_ban.backup_2}, backup_3={self.auto_ban.backup_3}")
        
        return self.auto_ban.enabled
    
    def toggle_pre_hover(self) -> bool:
        """Toggle pre-ban hover."""
        with self._lock:
            self.options.pre_hover_enabled = not self.options.pre_hover_enabled
        logger.info(f"Pre-hover: {'✅ ON' if self.options.pre_hover_enabled else '❌ OFF'}")
        return self.options.pre_hover_enabled
    
    def toggle_avoid_ally_hovers(self) -> bool:
        """Toggle avoiding ally hovers."""
        with self._lock:
            self.options.avoid_ally_hovers = not self.options.avoid_ally_hovers
        logger.info(f"Avoid ally bans: {'✅ ON' if self.options.avoid_ally_hovers else '❌ OFF'}")
        return self.options.avoid_ally_hovers
    
    # Monitoring
    def start_monitor(self) -> None:
        """Start champion select monitoring."""
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.is_running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                daemon=True,
                name="ChampSelectMonitor"
            )
            self.monitor_thread.start()
            logger.info("▶️ Monitor started")
    
    def start_threads(self) -> None:
        """Start all monitoring threads (alias for compatibility)."""
        self.start_monitor()
    
    def stop(self) -> None:
        """Stop monitoring."""
        self.is_running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        logger.info("🛑 Monitor stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        logger.info("👀 Champion select monitor active")
        logger.info(f"📋 Instalock: {'✅ ENABLED' if self.instalock.enabled else '❌ DISABLED'} - {self.get_instalock_status()}")
        logger.info(f"📋 Auto-ban: {'✅ ENABLED' if self.auto_ban.enabled else '❌ DISABLED'} - {self.get_auto_ban_status()}")
        consecutive_errors = 0
        max_errors = 10
        
        while self.is_running:
            try:
                # Load champions if not loaded
                if not self.registry.is_loaded():
                    self.registry.load()
                
                session_data = self.session_handler.get_session()
                
                if not session_data:
                    self._reset_state()
                    consecutive_errors = 0
                    time.sleep(0.5)
                    continue
                
                cell_id = self.session_handler.get_cell_id(session_data)
                if cell_id is None:
                    time.sleep(0.3)
                    continue
                
                # Reset on new session
                current_session_id = id(session_data)
                if current_session_id != self._last_session_id:
                    self._reset_state()
                    self._last_session_id = current_session_id
                    logger.info("🔄 New champion select session detected")
                    logger.info(f"📋 Instalock: {'✅ ENABLED' if self.instalock.enabled else '❌ DISABLED'}")
                    logger.info(f"📋 Auto-ban: {'✅ ENABLED' if self.auto_ban.enabled else '❌ DISABLED'}")
                
                # Handle pre-hover
                self._handle_pre_hover(session_data)
                
                # Process actions
                self._process_actions(session_data, cell_id)
                
                consecutive_errors = 0
                time.sleep(0.2)
                
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"⚠️ Monitor error: {e}")
                
                if consecutive_errors >= max_errors:
                    logger.error("❌ Too many consecutive errors, stopping monitor")
                    self.is_running = False
                    break
                
                time.sleep(1)
        
        logger.info("🛑 Champion select monitor stopped")
    
    def _reset_state(self) -> None:
        """Reset session state."""
        self._last_session_id = None
        self._processed_actions.clear()
        self._pre_hover_done = False
    
    def _handle_pre_hover(self, session_data: dict) -> None:
        """Handle pre-ban hovering if enabled."""
        if not (self.options.pre_hover_enabled and 
                self.instalock.enabled and 
                not self._pre_hover_done and
                self.instalock.primary != "None"):
            return
        
        # Get timer and phase info
        timer = session_data.get("timer", {})
        phase = timer.get("phase", "")
        
        # Check if we should hover based on phase
        # We want to hover as soon as champion select starts, before bans
        cell_id = self.session_handler.get_cell_id(session_data)
        if cell_id is None:
            return
        
        # Check if there's a pick action available for us (even if not in progress yet)
        has_pick_action = False
        for actions in session_data.get("actions", []):
            if not isinstance(actions, list):
                continue
            
            for action in actions:
                if (action.get("actorCellId") == cell_id and
                    action.get("type") == "pick" and
                    not action.get("completed", False)):
                    has_pick_action = True
                    break
            
            if has_pick_action:
                break
        
        # Only hover if we have a pick action available
        if not has_pick_action:
            return
        
        # Get champion to hover
        champ_id = self.selector.select_pick(self.instalock, session_data)
        if champ_id != -1:
            if self._hover_champion(champ_id):
                champ_name = self.instalock.primary
                if champ_name == "Random":
                    champ_name = self.registry.get_name(champ_id)
                logger.info(f"✨ Pre-hover successful: {champ_name.title()}")
                self._pre_hover_done = True
            else:
                logger.warning(f"⚠️ Failed to pre-hover champion")
    
    def _hover_champion(self, champion_id: int) -> bool:
        """
        Hover over a champion (show intent without locking).
        
        Args:
            champion_id: Champion ID to hover
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session_handler.get_session()
            
            if not response:
                return False
            
            cell_id = self.session_handler.get_cell_id(response)
            
            if cell_id is None:
                return False
            
            # Find player's pick action
            for actions in response.get("actions", []):
                if not isinstance(actions, list):
                    continue
                
                for action in actions:
                    if (action.get("actorCellId") == cell_id and
                        action.get("type") == "pick" and
                        not action.get("completed", False)):
                        
                        action_id = action.get("id")
                        
                        # Hover (completed=False shows intent without locking)
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
    
    def _process_actions(self, session_data: dict, cell_id: int) -> None:
        """Process champion select actions."""
        for actions in session_data.get("actions", []):
            if not isinstance(actions, list):
                continue
            
            for action in actions:
                # Only process our own actions
                if action.get("actorCellId") != cell_id:
                    continue
                
                action_id = action.get("id")
                action_type = action.get("type")
                is_in_progress = action.get("isInProgress", False)
                is_completed = action.get("completed", False)
                
                # Debug logging
                logger.debug(f"🔍 Action {action_id}: type={action_type}, inProgress={is_in_progress}, completed={is_completed}")
                
                # Skip if already processed or completed
                if action_id in self._processed_actions:
                    continue
                
                if is_completed:
                    self._processed_actions.add(action_id)
                    continue
                
                # Check if action is available (isInProgress=True means it's our turn)
                if not is_in_progress:
                    continue
                
                # Process based on action type and enabled features
                if action_type == "pick":
                    if self.instalock.enabled:
                        logger.info("🎯 Processing PICK action")
                        self._execute_pick(action_id, session_data)
                    else:
                        logger.debug("⏭️ Skipping pick - instalock disabled")
                        
                elif action_type == "ban":
                    if self.auto_ban.enabled:
                        logger.info("🎯 Processing BAN action")
                        self._execute_ban(action_id, session_data, cell_id)
                    else:
                        logger.debug("⏭️ Skipping ban - auto-ban disabled")
    
    def _execute_pick(self, action_id: int, session_data: dict) -> None:
        """Execute pick action."""
        champ_id = self.selector.select_pick(self.instalock, session_data)
        if champ_id != -1:
            self._complete_action(action_id, champ_id, "pick")
    
    def _execute_ban(self, action_id: int, session_data: dict, cell_id: int) -> None:
        """Execute ban action."""
        logger.info(f"🎯 Attempting to ban champion (action_id: {action_id})")
        champ_id = self.selector.select_ban(
            self.auto_ban, 
            session_data, 
            cell_id, 
            self.options.avoid_ally_hovers
        )
        if champ_id != -1:
            self._complete_action(action_id, champ_id, "ban")
        else:
            logger.warning("⚠️ No valid champion to ban found")
    
    def _complete_action(self, action_id: int, champion_id: int, action_type: str) -> None:
        """Complete a champion select action."""
        try:
            response = self.rengar.lcu_request(
                "PATCH",
                f"/lol-champ-select/v1/session/actions/{action_id}",
                {"completed": True, "championId": champion_id}
            )
            
            if response.status_code in [204, 200]:
                self._processed_actions.add(action_id)
                champ_name = self.registry.get_name(champion_id)
                logger.info(f"✅ {action_type.title()} completed: {champ_name}")
            else:
                logger.warning(f"⚠️ Failed to {action_type}: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error completing {action_type}: {e}")
    
    # Status methods
    def get_instalock_status(self) -> str:
        """Get formatted instalock status string."""
        if self.instalock.primary == "None":
            return "None"
        
        status = self.instalock.primary.title()
        backups = []
        
        if self.instalock.backup_2 != "None":
            backups.append(f"2nd: {self.instalock.backup_2.title()}")
        if self.instalock.backup_3 != "None":
            backups.append(f"3rd: {self.instalock.backup_3.title()}")
        
        if backups:
            status += f" ({', '.join(backups)})"
        
        return status
    
    def get_auto_ban_status(self) -> str:
        """Get formatted auto-ban status string."""
        if self.auto_ban.primary == "None":
            return "None"
        
        status = self.auto_ban.primary.title()
        backups = []
        
        if self.auto_ban.backup_2 != "None":
            backups.append(f"2nd: {self.auto_ban.backup_2.title()}")
        if self.auto_ban.backup_3 != "None":
            backups.append(f"3rd: {self.auto_ban.backup_3.title()}")
        
        if backups:
            status += f" ({', '.join(backups)})"
        
        return status
    
    def get_status(self) -> dict:
        """Get complete status information."""
        return {
            "instalock": {
                "enabled": self.instalock.enabled,
                "champion": self.instalock.primary,
                "backup_2": self.instalock.backup_2,
                "backup_3": self.instalock.backup_3,
                "display": self.get_instalock_status(),
                "pre_hover_enabled": self.options.pre_hover_enabled
            },
            "auto_ban": {
                "enabled": self.auto_ban.enabled,
                "champion": self.auto_ban.primary,
                "backup_2": self.auto_ban.backup_2,
                "backup_3": self.auto_ban.backup_3,
                "display": self.get_auto_ban_status(),
                "avoid_ally_hovers": self.options.avoid_ally_hovers
            },
            "monitor": {
                "running": self.is_running,
                "thread_alive": self.monitor_thread.is_alive() if self.monitor_thread else False
            },
            "champions_loaded": len(self.registry._champ_dict)
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()