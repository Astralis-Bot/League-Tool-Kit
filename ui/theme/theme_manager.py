"""
LEAGUE TOOLKIT - Protected Theme Manager
Sistema de temas com proteção criptográfica
Apenas temas assinados pelo desenvolvedor podem ser importados
"""

import json
import os
import hashlib
import base64
from typing import Dict, Tuple
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Cryptography não disponível - instale: pip install cryptography")


class ThemeManager:
    """
    Gerenciador de temas com proteção criptográfica
    Apenas temas assinados pelo desenvolvedor são aceitos
    """
    # FIX: Definir como atributo de classe (não de instância)
    _DEVELOPER_SECRET = b'7f3a9c2e5b8d1f4a6c9e3b7d2f5a8c1e4b7d9f3a6c2e5b8d1f4a7c9e2b5d8f1a3'
    _SALT = b'e4b7d1f9a3c6e2b8d5f1a7c4e9b2d6f3a8c1e5b9d2f7a4c8e3b6d1f5a9c2e7b4d'

    
    # Temas padrão integrados
    DEFAULT_THEMES = {
        "dark_classic": {
            "name": "Dark Classic",
            "app_name": "LTK",
            "app_icon": "⚡",
            "icon_file": "tiamat.ico",

            "primary": "#6366F1",
            "secondary": "#8B5CF6",
            "accent": "#F59E0B",

            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "info": "#3B82F6",

            "bg_dark": "#0D0D0F",
            "bg_medium": "#16161A",
            "bg_light": "#1F1F25",
            "bg_card": "#1A1A20",
            "bg_elevated": "#24242C",
            "bg_hover": "#2E2E38",

            "text_primary": "#F3F4F6",
            "text_secondary": "#D1D5DB",
            "text_tertiary": "#9CA3AF",
            "text_dark": "#111827",

            "border_color": "#2E2E38",
            "border_accent": "#6366F1"
        },
        "blue_steel": {
            "name": "Blue Steel",
            "app_name": "LTK",
            "app_icon": "⚡",
            "icon_file": "tiamat.ico",

            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "accent": "#93C5FD",

            "success": "#22C55E",
            "warning": "#EAB308",
            "danger": "#EF4444",
            "info": "#38BDF8",

            "bg_dark": "#0A0F18",
            "bg_medium": "#101722",
            "bg_light": "#16202D",
            "bg_card": "#131B26",
            "bg_elevated": "#1A2433",
            "bg_hover": "#213044",

            "text_primary": "#F1F5F9",
            "text_secondary": "#CBD5E1",
            "text_tertiary": "#94A3B8",
            "text_dark": "#0F172A",

            "border_color": "#213044",
            "border_accent": "#3B82F6"
        },
        "light": {
            "name": "Light",
            "app_name": "LTK",
            "app_icon": "⚡",
            "icon_file": "tiamat.ico",

            "primary": "#10B981",
            "secondary": "#34D399",
            "accent": "#6EE7B7",

            "success": "#10B981",
            "warning": "#FBBF24",
            "danger": "#EF4444",
            "info": "#3B82F6",

            "bg_dark": "#F0FDF4",
            "bg_medium": "#DCFCE7",
            "bg_light": "#D1FAE5",
            "bg_card": "#E3FCEF",
            "bg_elevated": "#C7F9DD",
            "bg_hover": "#BAF7D3",

            "text_primary": "#064E3B",
            "text_secondary": "#0F766E",
            "text_tertiary": "#6EE7B7",
            "text_dark": "#0F172A",

            "border_color": "#BAF7D3",
            "border_accent": "#10B981"
        },


    }

    REQUIRED_FIELDS = [
        'name', 'app_name', 'app_icon', 'primary', 'secondary', 'accent',
        'bg_dark', 'bg_medium', 'bg_light', 'bg_card', 'text_primary', 
        'text_secondary', 'text_dark', 'success', 'danger'
    ]
    
    # Campos opcionais com valores padrão
    OPTIONAL_FIELDS = {
        'icon_file': 'tiamat.ico',
        'bg_elevated': None,  # Será derivado de bg_light
        'bg_hover': None,     # Será derivado de bg_light
        'text_tertiary': None,  # Será derivado de text_secondary
        'warning': '#F59E0B',
        'info': '#3B82F6',
        'border_color': None,  # Será derivado de bg_light
        'border_accent': None,  # Será derivado de primary
    }

    def __init__(self, config_file: str = "theme_config.json", 
                 custom_themes_dir: str = "custom_themes"):
        self.config_file = config_file
        self.custom_themes_dir = custom_themes_dir
        self.themes = self.DEFAULT_THEMES.copy()
        self.cipher = None  # Inicializar antes
        
        os.makedirs(self.custom_themes_dir, exist_ok=True)
        
        self._init_encryption()
        self._load_custom_themes()
        self.current_theme = self._load_current_theme()

    def _init_encryption(self):
        """Inicializa sistema de criptografia"""
        if not CRYPTO_AVAILABLE:
            print("⚠️ Criptografia desabilitada")
            self.cipher = None
            return
            
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self._SALT,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(self._DEVELOPER_SECRET))
            self.cipher = Fernet(key)
            print("✅ Sistema de segurança inicializado")
        except Exception as e:
            print(f"❌ Erro ao inicializar segurança: {e}")
            self.cipher = None

    def _generate_signature(self, theme_data: Dict) -> str:
        """Gera assinatura digital do tema"""
        clean_data = {k: v for k, v in theme_data.items() 
                     if not k.startswith('_')}
        
        data_str = json.dumps(clean_data, sort_keys=True, ensure_ascii=False)
        signature = hashlib.sha256(
            (data_str + self._DEVELOPER_SECRET.decode()).encode()
        ).hexdigest()
        
        return signature

    def _verify_signature(self, theme_data: Dict) -> bool:
        """Verifica assinatura do tema"""
        if '_signature' not in theme_data:
            return False
        
        stored_sig = theme_data['_signature']
        theme_copy = {k: v for k, v in theme_data.items() 
                     if k not in ['_signature', '_version']}
        
        calculated_sig = self._generate_signature(theme_copy)
        return stored_sig == calculated_sig

    def _encrypt_theme(self, theme_data: Dict) -> str:
        """Criptografa tema com assinatura"""
        if not self.cipher:
            raise Exception("Criptografia não disponível")
        
        theme_data['_signature'] = self._generate_signature(theme_data)
        theme_data['_version'] = '2.0'
        
        json_data = json.dumps(theme_data, ensure_ascii=False)
        encrypted = self.cipher.encrypt(json_data.encode('utf-8'))
        
        return base64.b64encode(encrypted).decode('utf-8')

    def _decrypt_theme(self, encrypted_data: str) -> Dict:
        """Descriptografa e valida tema"""
        if not self.cipher:
            raise Exception("Criptografia não disponível")
        
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.cipher.decrypt(encrypted_bytes)
            theme_data = json.loads(decrypted.decode('utf-8'))
            
            if not self._verify_signature(theme_data):
                raise ValueError("Assinatura inválida - tema não oficial")
            
            theme_data.pop('_signature', None)
            theme_data.pop('_version', None)
            
            return theme_data
        except Exception as e:
            raise ValueError(f"Tema inválido ou corrompido: {str(e)}")

    def _validate_theme(self, theme_data: Dict) -> bool:
        """Valida estrutura do tema"""
        if not isinstance(theme_data, dict):
            return False
        
        for field in self.REQUIRED_FIELDS:
            if field not in theme_data:
                print(f"⚠️ Campo ausente: {field}")
                return False
        
        color_fields = ['primary', 'secondary', 'accent', 'bg_dark', 
                       'bg_medium', 'bg_light', 'text_primary', 
                       'text_secondary', 'success', 'danger']
        
        for field in color_fields:
            if not self._is_valid_hex_color(theme_data.get(field, '')):
                print(f"⚠️ Cor inválida: {field}")
                return False
        
        return True
    
    def _fill_optional_fields(self, theme_data: Dict) -> Dict:
        """Preenche campos opcionais com valores padrão ou derivados"""
        theme = theme_data.copy()
        
        # Preenche campos opcionais fixos
        for field, default_value in self.OPTIONAL_FIELDS.items():
            if field not in theme or theme[field] is None:
                if default_value is not None:
                    theme[field] = default_value
        
        # Deriva cores se não existirem
        if 'bg_elevated' not in theme or not theme.get('bg_elevated'):
            theme['bg_elevated'] = theme.get('bg_light', theme['bg_medium'])
        
        if 'bg_hover' not in theme or not theme.get('bg_hover'):
            # Tenta iluminar bg_light (aproximação simples)
            theme['bg_hover'] = theme.get('bg_light', theme['bg_medium'])
        
        if 'text_tertiary' not in theme or not theme.get('text_tertiary'):
            theme['text_tertiary'] = theme.get('text_secondary', theme['text_primary'])
        
        if 'border_color' not in theme or not theme.get('border_color'):
            theme['border_color'] = theme.get('bg_light', theme['bg_medium'])
        
        if 'border_accent' not in theme or not theme.get('border_accent'):
            theme['border_accent'] = theme.get('primary', '#8B5CF6')
        
        return theme

    def _is_valid_hex_color(self, color: str) -> bool:
        """Valida formato de cor hexadecimal"""
        if not isinstance(color, str) or not color.startswith('#'):
            return False
        
        hex_part = color[1:]
        if len(hex_part) not in [3, 6]:
            return False
        
        try:
            int(hex_part, 16)
            return True
        except ValueError:
            return False

    def _load_custom_themes(self):
        """Carrega apenas temas oficiais criptografados (.ltt)"""
        if not os.path.exists(self.custom_themes_dir):
            return
        
        for filename in os.listdir(self.custom_themes_dir):
            if not filename.endswith('.ltt'):
                continue
            
            theme_path = os.path.join(self.custom_themes_dir, filename)
            try:
                with open(theme_path, 'r', encoding='utf-8') as f:
                    encrypted_data = f.read()
                
                theme_data = self._decrypt_theme(encrypted_data)
                
                if self._validate_theme(theme_data):
                    # Preenche campos opcionais
                    theme_data = self._fill_optional_fields(theme_data)
                    
                    theme_id = filename.replace('.ltt', '')
                    self.themes[theme_id] = theme_data
                    print(f"✅ Tema oficial carregado: {theme_data['name']}")
                else:
                    print(f"⚠️ Tema inválido: {filename}")
            
            except Exception as e:
                print(f"❌ Erro ao carregar {filename}: {e}")

    def _load_current_theme(self) -> str:
        """Carrega tema atual"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    theme = config.get('theme', 'dark_classic')
                    if theme in self.themes:
                        return theme
            except:
                pass
        return 'dark_classic'

    def _save_current_theme(self, theme_name: str):
        """Salva tema atual"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'theme': theme_name}, f, indent=4)
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")

    def import_theme(self, file_path: str) -> Tuple[bool, str]:
        """
        Importa apenas temas oficiais (.ltt)
        Usuários não podem criar temas próprios
        """
        if not CRYPTO_AVAILABLE:
            return False, "Sistema de segurança não disponível"
        
        try:
            if not os.path.exists(file_path):
                return False, "Arquivo não encontrado"
            
            if not file_path.endswith('.ltt'):
                return False, ("Formato inválido. Apenas temas oficiais (.ltt) "
                             "são aceitos. Contate o desenvolvedor para criar "
                             "um tema personalizado.")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            
            # Tenta descriptografar e validar
            theme_data = self._decrypt_theme(encrypted_data)
            
            if not self._validate_theme(theme_data):
                return False, "Tema inválido ou corrompido"
            
            # Preenche campos opcionais
            theme_data = self._fill_optional_fields(theme_data)
            
            # Gera ID único
            theme_name = theme_data['name']
            theme_id = self._generate_theme_id(theme_name)
            
            counter = 1
            original_id = theme_id
            while theme_id in self.themes:
                theme_id = f"{original_id}_{counter}"
                counter += 1
            
            # Salva tema
            custom_theme_path = os.path.join(
                self.custom_themes_dir, 
                f"{theme_id}.ltt"
            )
            
            with open(custom_theme_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            
            self.themes[theme_id] = theme_data
            
            return True, f"✅ Tema oficial '{theme_name}' importado com sucesso!"
        
        except ValueError as e:
            return False, f"❌ Tema não oficial ou inválido: {str(e)}"
        except Exception as e:
            return False, f"❌ Erro ao importar tema: {str(e)}"

    def _generate_theme_id(self, theme_name: str) -> str:
        """Gera ID do tema"""
        theme_id = theme_name.lower()
        theme_id = ''.join(c if c.isalnum() else '_' for c in theme_id)
        return theme_id.strip('_') or 'custom_theme'

    def delete_custom_theme(self, theme_id: str) -> Tuple[bool, str]:
        """Deleta tema customizado"""
        if theme_id in self.DEFAULT_THEMES:
            return False, "Não é possível deletar temas padrão"
        
        if theme_id not in self.themes:
            return False, "Tema não encontrado"
        
        try:
            theme_file = os.path.join(self.custom_themes_dir, f"{theme_id}.ltt")
            
            if os.path.exists(theme_file):
                os.remove(theme_file)
            
            del self.themes[theme_id]
            
            if self.current_theme == theme_id:
                self.apply_theme('dark_classic')
            
            return True, "Tema deletado com sucesso!"
        
        except Exception as e:
            return False, f"Erro ao deletar tema: {str(e)}"

    def get_theme(self, theme_name: str = None) -> Dict[str, str]:
        """Retorna dados do tema com todos os campos preenchidos"""
        if theme_name is None:
            theme_name = self.current_theme
        
        theme = self.themes.get(theme_name, self.themes['dark_classic']).copy()
        
        # Garante que todos os campos opcionais existem
        return self._fill_optional_fields(theme)

    def get_current_theme(self) -> Dict[str, str]:
        """Retorna tema atual"""
        return self.get_theme(self.current_theme)

    def get_theme_names(self) -> Dict[str, str]:
        """Retorna dicionário com IDs e nomes"""
        return {key: self.themes[key]['name'] for key in self.themes}

    def is_custom_theme(self, theme_id: str) -> bool:
        """Verifica se é tema customizado"""
        return theme_id not in self.DEFAULT_THEMES and theme_id in self.themes

    def apply_theme(self, theme_name: str) -> bool:
        """Aplica tema"""
        if theme_name not in self.themes:
            return False
        
        self.current_theme = theme_name
        self._save_current_theme(theme_name)
        return True


# ============================================================
# FERRAMENTA PARA DESENVOLVEDORES - CRIAR TEMAS OFICIAIS
# ============================================================

def create_official_theme(theme_data: Dict, output_file: str):
    """
    USO EXCLUSIVO DO DESENVOLVEDOR
    Cria tema oficial assinado e criptografado (.ltt)
    
    Exemplo:
        theme = {
            "name": "Meu Tema",
            "app_name": "LEAGUE TOOLKIT",
            ...
        }
        create_official_theme(theme, "meu_tema.ltt")
    """
    if not CRYPTO_AVAILABLE:
        print("❌ Cryptography não disponível")
        return False
    
    manager = ThemeManager()
    
    if not manager._validate_theme(theme_data):
        print("❌ Tema inválido")
        return False
    
    try:
        encrypted = manager._encrypt_theme(theme_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        
        print(f"✅ Tema oficial criado: {output_file}")
        print(f"   Nome: {theme_data['name']}")
        print(f"   Assinatura: ✓")
        print(f"   Formato: .ltt (criptografado)")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao criar tema: {e}")
        return False


# Exemplo de uso para desenvolvedores:
if __name__ == "__main__":
    # APENAS PARA O DESENVOLVEDOR
    exemplo_tema = {
        "name": "Crimson Night",
        "app_name": "LEAGUE TOOLKIT",
        "app_icon": "🔥",
        "icon_file": "tiamat.ico",
        
        "primary": '#DC2626',
        "secondary": '#7C2D12',
        "accent": '#EA580C',
        
        "success": '#10B981',
        "warning": '#F59E0B',
        "danger": '#EF4444',
        "info": '#3B82F6',
        
        "bg_dark": '#0C0A09',
        "bg_medium": '#1C1917',
        "bg_light": '#292524',
        "bg_card": '#1C1917',
        "bg_elevated": '#292524',
        "bg_hover": '#44403C',
        
        "text_primary": '#FAFAF9',
        "text_secondary": '#E7E5E4',
        "text_tertiary": '#D6D3D1',
        "text_dark": '#0C0A09',
        
        "border_color": '#292524',
        "border_accent": '#DC2626',
    }
    
    # Descomente para criar um tema oficial:
    # create_official_theme(exemplo_tema, "crimson_night.ltt")