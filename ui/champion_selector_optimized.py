# champion_selector_optimized.py - CORRIGIDO - SEM LAG E CARREGA TODAS IMAGENS

import customtkinter as ctk
from PIL import Image
from io import BytesIO
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread, Lock
import time


class OptimizedChampionSelector:
    """Menu otimizado de seleção de campeões - SEM LAG"""
    
    # Cache global
    _IMAGE_CACHE = {}
    _CACHE_LOCK = Lock()
    _EXECUTOR = ThreadPoolExecutor(max_workers=10, thread_name_prefix="champ_img")
    _DATA_CACHE = None
    _DATA_LOCK = Lock()
    
    def __init__(self, parent, title, icon, color, callback, api_manager):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.color = color
        self.callback = callback
        self.alive = True
        self.selected_champion = None
        self.filtered_champions = []
        
        # Carregar dados
        with OptimizedChampionSelector._DATA_LOCK:
            if OptimizedChampionSelector._DATA_CACHE is None:
                OptimizedChampionSelector._DATA_CACHE = api_manager.get_champions()
            self.champions = OptimizedChampionSelector._DATA_CACHE
        
        if not self.champions:
            print("⚠️ Nenhum campeão carregado")
            return
        
        self.filtered_champions = self.champions.copy()
        self.create_window()
    
    def create_window(self):
        """Cria janela modal otimizada"""
        self.win = ctk.CTkToplevel(self.parent)
        self.win.withdraw()
        self.win.title(f"{self.icon} {self.title}")
        self.win.geometry("900x650")
        self.win.minsize(800, 500)
        self.win.resizable(True, True)
        
        self.win.configure(fg_color="#0a0f14")
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.win.transient(self.parent)
        
        try:
            self.win.iconbitmap("tiamat.ico")
        except:
            pass
        
        # Header com busca
        self.create_header()
        
        # Grid de campeões
        self.create_grid()
        
        # Footer
        self.create_footer()
        
        # Mostrar janela
        self.win.deiconify()
        self.win.lift()
        self.win.focus_force()
        self.win.grab_set()
    
    def create_header(self):
        """Cria header com barra de busca"""
        header = ctk.CTkFrame(self.win, fg_color=self.color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text=f"{self.icon} {self.title}",
            font=("Consolas", 16, "bold"),
            text_color="#0a0f14"
        ).pack()
        
        # Barra de busca
        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.pack(side="right", fill="y", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar campeão...",
            width=250,
            height=35,
            font=("Consolas", 11),
            border_width=2,
            border_color="#0a0f14",
            fg_color="#180430",
            text_color="#F0E0FF"
        )
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.filter_search)
    
    def create_grid(self):
        """Cria grid de campeões com scroll suave"""
        container = ctk.CTkFrame(self.win, fg_color="#0a0f14")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.scroll_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="#0a0f14",
            scrollbar_button_color=self.color,
            scrollbar_button_hover_color=self.color
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.champion_buttons = {}
        self.build_grid()
    

    def build_grid(self):
        """Constrói o grid de forma otimizada"""
        # Limpar widgets anteriores
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.champion_buttons.clear()
        
        # Criar linhas (5 campeões por linha)
        cols_per_row = 5
        current_row = None
        current_col_count = 0
        
        for champ in self.filtered_champions:
            # Nova linha a cada 5 campeões
            if current_col_count == 0:
                current_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=120)
                current_row.pack(fill="x", pady=5)
            
            # Criar botão do campeão
            champ_btn = self.create_champion_button(current_row, champ)
            champ_btn.pack(side="left", padx=5, expand=True, fill="both")
            
            self.champion_buttons[champ['name']] = (champ_btn, champ['icon'])
            
            current_col_count += 1
            if current_col_count >= cols_per_row:
                current_col_count = 0
        
        # Carregar TODAS as imagens em paralelo
        self.load_images_parallel()


    def create_champion_button(self, parent, champ):
        """Cria botão individual do campeão"""
        btn_frame = ctk.CTkFrame(
            parent,
            fg_color="#120326",
            corner_radius=8,
            border_width=2,
            border_color="#2a2a2a",
            cursor="hand2"
        )
        
        # Container para imagem
        img_container = ctk.CTkFrame(
            btn_frame,
            fg_color="#0a0f14",
            width=100,
            height=100,
            corner_radius=6
        )
        img_container.pack(fill="both", expand=True, padx=5, pady=5)
        img_container.pack_propagate(False)
        
        # Placeholder inicial
        placeholder = ctk.CTkLabel(
            img_container,
            text="⏳",
            font=("Consolas", 40),
            text_color=self.color
        )
        placeholder.pack(expand=True)
        img_container._placeholder = placeholder
        img_container._url = champ['icon']
        img_container._champ_name = champ['name']
        
        # Nome do campeão
        name_label = ctk.CTkLabel(
            btn_frame,
            text=champ['name'],
            font=("Consolas", 10, "bold"),
            text_color=self.color,
            height=20
        )
        name_label.pack(fill="x", padx=5, pady=(0, 5))
        
        # BIND DE CLIQUE - Aplicar a TODOS os widgets
        click_command = lambda e, name=champ['name']: self.on_champion_click(name, btn_frame)
        
        btn_frame.bind("<Button-1>", click_command)
        img_container.bind("<Button-1>", click_command)
        name_label.bind("<Button-1>", click_command)
        placeholder.bind("<Button-1>", click_command)
        
        # Efeitos hover
        hover_in = lambda e, b=btn_frame: self.on_hover(b)
        hover_out = lambda e, b=btn_frame: self.on_leave(b)
        
        btn_frame.bind("<Enter>", hover_in)
        btn_frame.bind("<Leave>", hover_out)
        img_container.bind("<Enter>", hover_in)
        img_container.bind("<Leave>", hover_out)
        
        btn_frame._img_container = img_container
        btn_frame._name_label = name_label
        btn_frame._is_selected = False
        
        return btn_frame
    
    def on_champion_click(self, champion_name, button):
        """Handle de clique no campeão"""
        if not self.alive:
            return
        
        # Desselecionar anterior
        if self.selected_champion and self.selected_champion in self.champion_buttons:
            old_btn = self.champion_buttons[self.selected_champion][0]
            old_btn._is_selected = False
            old_btn.configure(border_color="#2a2a2a", border_width=2)
        
        # Selecionar novo
        button._is_selected = True
        button.configure(border_color=self.color, border_width=3)
        self.selected_champion = champion_name
        
        # Habilitar botão confirmar
        self.confirm_btn.configure(state="normal")
        
        print(f"✅ {champion_name} selecionado")
    
    def on_hover(self, button):
        """Efeito hover"""
        if not button._is_selected:
            button.configure(border_color=self.color, border_width=2)
    
    def on_leave(self, button):
        """Remove efeito hover"""
        if not button._is_selected:
            button.configure(border_color="#2a2a2a", border_width=2)

    def load_images_parallel(self):
        """Carrega TODAS as imagens em paralelo - CORRIGIDO"""
        start_time = time.time()
        futures = {}
        
        print(f"📥 Iniciando carregamento de {len(self.champion_buttons)} imagens...")
        
        # Carregar TODAS as imagens (não apenas 10)
        for champ_name, (btn, url) in self.champion_buttons.items():
            future = self._EXECUTOR.submit(self._download_image, url)
            futures[future] = (btn, champ_name)
        
        def process_images():
            loaded = 0
            failed = 0
            
            # Timeout aumentado para 30 segundos
            for future in as_completed(futures, timeout=30):
                if not self.alive:
                    break
                
                btn, champ_name = futures[future]
                
                try:
                    photo = future.result(timeout=2)
                    if photo and self.alive:
                        self.win.after(0, lambda b=btn, p=photo, n=champ_name: self._display_image(b, p, n))
                        loaded += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
                    print(f"⚠️ Falha ao carregar {champ_name}: {e}")
            
            if self.alive:
                elapsed = time.time() - start_time
                total = loaded + failed
                print(f"✅ {loaded}/{total} imagens carregadas em {elapsed:.2f}s")
                if failed > 0:
                    print(f"⚠️ {failed} imagens falharam")
        
        Thread(target=process_images, daemon=True).start()
        
    @staticmethod
    def _download_image(url):
        """Download otimizado com cache"""
        # Verificar cache primeiro
        with OptimizedChampionSelector._CACHE_LOCK:
            if url in OptimizedChampionSelector._IMAGE_CACHE:
                return OptimizedChampionSelector._IMAGE_CACHE[url]
        
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                img_data = response.read()
            
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            
            photo = ctk.CTkImage(light_image=img, size=(100, 100))
            
            # Salvar no cache
            with OptimizedChampionSelector._CACHE_LOCK:
                OptimizedChampionSelector._IMAGE_CACHE[url] = photo
            
            return photo
        except Exception as e:
            # Retornar None em caso de erro
            return None
    
    def _display_image(self, btn, photo, champ_name):
        """Exibe imagem no botão"""
        if not self.alive or not btn.winfo_exists():
            return
        
        try:
            img_container = btn._img_container
            
            # Remover placeholder
            if hasattr(img_container, '_placeholder'):
                img_container._placeholder.destroy()
                delattr(img_container, '_placeholder')
            
            # Criar label com imagem
            img_label = ctk.CTkLabel(
                img_container,
                image=photo,
                text=""
            )
            img_label.pack(fill="both", expand=True)
            
            # IMPORTANTE: Adicionar bind de clique na imagem
            img_label.bind("<Button-1>", lambda e, name=champ_name: self.on_champion_click(name, btn))
            
            # Adicionar hover
            img_label.bind("<Enter>", lambda e, b=btn: self.on_hover(b))
            img_label.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
            
            # Manter referência da imagem
            img_label._photo_ref = photo
            
        except Exception as e:
            print(f"❌ Erro ao exibir imagem de {champ_name}: {e}")
    
    def filter_search(self, event=None):
        """Filtra campeões por busca"""
        search_text = self.search_entry.get().lower().strip()
        
        if search_text:
            self.filtered_champions = [
                c for c in self.champions
                if search_text in c['name'].lower()
            ]
        else:
            self.filtered_champions = self.champions.copy()
        
        self.build_grid()
    
    def create_footer(self):
        """Cria footer com botões"""
        footer = ctk.CTkFrame(self.win, fg_color="#0a0f14", height=50)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        # Botão Desabilitar
        disable_btn = ctk.CTkButton(
            footer,
            text="✖ Desabilitar",
            height=35,
            width=120,
            font=("Consolas", 11, "bold"),
            fg_color="#ff1744",
            hover_color="#d50000",
            command=self.disable_feature
        )
        disable_btn.pack(side="left", padx=10, pady=7)
        
        # Espaçador
        ctk.CTkFrame(footer, fg_color="transparent").pack(side="left", expand=True)
        
        # Botão Confirmar
        self.confirm_btn = ctk.CTkButton(
            footer,
            text="✓ Confirmar Seleção",
            height=35,
            width=150,
            font=("Consolas", 11, "bold"),
            fg_color=self.color,
            hover_color=self.color,
            state="disabled",
            command=self.confirm_selection
        )
        self.confirm_btn.pack(side="right", padx=10, pady=7)
    
    def confirm_selection(self):
        """Confirma e aplica a seleção"""
        if self.selected_champion:
            if self.callback(self.selected_champion):
                print(f"✅ {self.title}: {self.selected_champion} confirmado!")
                self.close()
    
    def disable_feature(self):
        """Desabilita a feature"""
        self.callback("disable")
        self.close()
    
    def close(self):
        """Fecha a janela"""
        if not self.alive:
            return
        
        self.alive = False
        
        try:
            self.win.grab_release()
            self.win.withdraw()
            self.win.destroy()
        except:
            pass
        
        self.champion_buttons.clear()
        print(f"✅ {self.title} fechado")


def preload_champion_data(api_manager):
    """Pré-carrega dados dos campeões"""
    def load():
        with OptimizedChampionSelector._DATA_LOCK:
            if OptimizedChampionSelector._DATA_CACHE is None:
                try:
                    start = time.time()
                    OptimizedChampionSelector._DATA_CACHE = api_manager.get_champions()
                    count = len(OptimizedChampionSelector._DATA_CACHE)
                    elapsed = time.time() - start
                    print(f"✅ Pré-carregado: {count} campeões em {elapsed:.2f}s")
                except Exception as e:
                    print(f"❌ Erro no pré-carregamento: {e}")
                    OptimizedChampionSelector._DATA_CACHE = []
    
    Thread(target=load, daemon=True).start()