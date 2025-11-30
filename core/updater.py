"""
LEAGUE TOOLKIT - Auto Update System
Sistema completo de atualização automática via GitHub Releases
"""

import requests
import json
import os
import sys
import subprocess
import threading
import zipfile
import shutil
from pathlib import Path
from tkinter import messagebox
from packaging import version
import tempfile


class Updater:
    """
    Sistema de atualização automática
    Verifica e baixa atualizações do GitHub Releases
    """

    # Configurações do repositório
    GITHUB_USER = "Astralis-Bot"
    GITHUB_REPO = "League-Tool-Kit"
    CURRENT_VERSION = "2.1.0"  # Versão atual do aplicativo

    # URLs
    API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"

    def __init__(self, app=None):
        self.app = app
        self.latest_version = None
        self.download_url = None
        self.release_notes = None
        self.update_available = False
        self.checking = False
        self.downloading = False
        self.download_progress = 0

    def check_on_startup(self):
        """
        Verifica atualizações ao iniciar (modo silencioso)
        Apenas mostra notificação se houver atualização
        """
        def check_thread():
            try:
                has_update, version = self.check_for_updates(silent=True)
                
                if has_update:
                    print(f"✅ Nova versão disponível: {version}")
                    # Mostra notificação apenas se houver atualização
                    if self.app:
                        self.app.after(0, self._show_update_notification)
                else:
                    print("✅ Aplicativo está atualizado")
                    
            except Exception as e:
                print(f"⚠️ Erro na verificação de atualização: {e}")
        
        # Executa em thread separada para não bloquear a UI
        threading.Thread(target=check_thread, daemon=True).start()

    def check_for_updates(self, silent=True):
        """
        Verifica se há atualizações disponíveis
        """
        if self.checking:
            return False, None

        self.checking = True

        try:
            print(f"\n🔍 Verificando atualizações...")
            print(f"   Versão atual: {self.CURRENT_VERSION}")
            print(f"   Repositório: {self.GITHUB_USER}/{self.GITHUB_REPO}")

            headers = {'Accept': 'application/vnd.github.v3+json'}
            response = requests.get(self.API_URL, headers=headers, timeout=10)

            if response.status_code == 404:
                print(f"⚠️ Nenhuma release encontrada no repositório")
                if not silent:
                    messagebox.showinfo(
                        "ℹ️ Sem Releases",
                        "Nenhuma release encontrada no GitHub.\n"
                    )
                return False, None

            if response.status_code != 200:
                print(f"⚠️ Erro ao verificar atualizações: {response.status_code}")
                if not silent:
                    messagebox.showwarning(
                        "⚠️ Erro",
                        f"Não foi possível verificar atualizações."
                    )
                return False, None

            data = response.json()

            self.latest_version = data.get('tag_name', '').replace('v', '')
            self.release_notes = data.get('body', 'Sem notas de atualização')

            assets = data.get('assets', [])
            for asset in assets:
                name = asset.get('name', '').lower()
                if name.endswith('.exe') or name.endswith('.zip'):
                    self.download_url = asset.get('browser_download_url')
                    break

            if self.latest_version:
                try:
                    current = version.parse(self.CURRENT_VERSION)
                    latest = version.parse(self.latest_version)

                    self.update_available = latest > current

                    if self.update_available:
                        print(f"✅ Nova versão disponível: {self.latest_version}")
                        print(f"📥 URL: {self.download_url}")

                        if not silent:
                            self._show_update_notification()

                    else:
                        print("✅ Aplicativo atualizado!")

                    return self.update_available, self.latest_version

                except Exception as e:
                    print(f"⚠️ Erro ao comparar versões: {e}")
                    return False, None

            return False, None

        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False, None

        finally:
            self.checking = False

    def _show_update_notification(self):
        """Mostra notificação de atualização disponível"""
        response = messagebox.askyesno(
            "🔔 Atualização Disponível!",
            f"Uma nova versão está disponível!\n\n"
            f"Versão Atual: {self.CURRENT_VERSION}\n"
            f"Nova Versão: {self.latest_version}\n\n"
            f"Deseja instalar?"
        )

        if response:
            self.download_and_install()

    def download_and_install(self, callback=None):
        """Baixa e instala a atualização"""
        if self.downloading:
            messagebox.showwarning("⚠️", "Já existe um download em progresso.")
            return

        if not self.download_url:
            messagebox.showerror("❌", "URL de download não encontrada.")
            return

        def download_thread():
            try:
                self.downloading = True

                print(f"\n📥 Baixando atualização v{self.latest_version}...")

                # Pasta do próprio app
                app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

                filename = os.path.basename(self.download_url)
                temp_file = os.path.join(app_dir, filename)

                print(f"📂 Salvando atualização em: {temp_file}")

                response = requests.get(self.download_url, stream=True, timeout=30)
                total_size = int(response.headers.get('content-length', 0))

                with open(temp_file, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            if total_size > 0:
                                progress = int((downloaded / total_size) * 100)
                                self.download_progress = progress

                                if callback:
                                    callback(progress)

                                if progress % 10 == 0:
                                    print(f"📊 Progresso: {progress}%")

                print(f"✅ Download concluído: {temp_file}")
                self._install_update(temp_file)

            except Exception as e:
                print(f"❌ Erro: {e}")
                if self.app:
                    self.app.after(0, lambda: messagebox.showerror(
                        "Erro no Download",
                        f"Não foi possível baixar a atualização:\n{e}"
                    ))

            finally:
                self.downloading = False
                self.download_progress = 0

        threading.Thread(target=download_thread, daemon=True).start()

    def _install_update(self, update_file):
        """Instala a atualização baixada"""
        try:
            print("\n🔧 Instalando atualização...")

            file_ext = os.path.splitext(update_file)[1].lower()

            if file_ext == '.exe':
                response = messagebox.askyesno(
                    "Instalar Atualização",
                    "O app será fechado e o instalador será aberto.\nContinuar?"
                )
                if response:
                    subprocess.Popen([update_file])
                    sys.exit(0)

            elif file_ext == '.zip':
                response = messagebox.askyesno(
                    "Instalar Atualização",
                    "A atualização será instalada automaticamente.\nContinuar?"
                )
                if response:
                    self._extract_and_replace(update_file)

        except Exception as e:
            print(f"❌ Erro ao instalar: {e}")
            messagebox.showerror(
                "Erro na Instalação",
                f"Não foi possível instalar a atualização:\n{e}"
            )

    def _extract_and_replace(self, zip_file):
        """Extrai e substitui arquivos da atualização"""
        try:
            print("📦 Extraindo...")

            app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            temp_extract = os.path.join(tempfile.gettempdir(), "ltk_update")

            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)

            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)

            print("📄 Substituindo arquivos...")

            batch_script = os.path.join(tempfile.gettempdir(), "update_ltk.bat")

            with open(batch_script, 'w') as f:
                f.write("@echo off\n")
                f.write("timeout /t 2 >nul\n")
                f.write(f'xcopy /s /y "{temp_extract}\\*" "{app_dir}\\"\n')
                f.write(f'rmdir /s /q "{temp_extract}"\n')
                f.write(f'del "%~f0"\n')
                f.write(f'start "" "{os.path.join(app_dir, "main.exe")}"\n')

            subprocess.Popen(['cmd', '/c', batch_script], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)

        except Exception as e:
            print(f"❌ Erro ao extrair: {e}")
            raise

    def get_release_notes(self):
        """Retorna as notas da versão"""
        return self.release_notes or "Sem notas."


# Teste standalone
if __name__ == "__main__":
    updater = Updater()
    has_update, version = updater.check_for_updates(silent=False)

    if has_update:
        print(f"\nNotas da versão {version}:")
        print(updater.get_release_notes())