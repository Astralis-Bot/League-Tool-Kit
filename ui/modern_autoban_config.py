import customtkinter as ctk
from tkinter import messagebox


class ModernAutoBanConfigurator:
    """
    Configurador de Auto Ban compacto e elegante
    """

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.colors = app.colors

        # Valores atuais
        self.ban_values = {
            0: app.autoban_champion or "",
            1: getattr(app, 'autoban_backup_2', None) or "",
            2: getattr(app, 'autoban_backup_3', None) or ""
        }

        self.create_window()

    def create_window(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("⛔ Auto Ban Configuration")
        self.dialog.geometry("700x700")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Centraliza janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 350
        y = (self.dialog.winfo_screenheight() // 2) - 300
        self.dialog.geometry(f"700x700+{x}+{y}")

        self.dialog.configure(fg_color=self.colors['bg_dark'])

        # Container principal
        main = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=25, pady=25)

        self.create_header(main)
        self.create_compact_bans(main)
        self.create_footer(main)

    def create_header(self, parent):
        """Cabeçalho compacto"""
        header = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=12,
            border_width=2,
            border_color=self.colors['secondary']
        )
        header.pack(fill="x", pady=(0, 20))

        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)

        # Ícone e título lado a lado
        icon_title = ctk.CTkFrame(content, fg_color="transparent")
        icon_title.pack(side="left")

        # Ícone
        icon_circle = ctk.CTkFrame(
            icon_title,
            fg_color=self.colors['secondary'],
            width=50,
            height=50,
            corner_radius=12
        )
        icon_circle.pack(side="left", padx=(0, 15))
        icon_circle.pack_propagate(False)

        ctk.CTkLabel(
            icon_circle,
            text="⛔",
            font=("Segoe UI Emoji", 24),
            text_color="white"
        ).pack(expand=True)

        # Textos
        text_container = ctk.CTkFrame(icon_title, fg_color="transparent")
        text_container.pack(side="left")

        ctk.CTkLabel(
            text_container,
            text="Auto Ban Configuration",
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_container,
            text="Configure your champion bans with priority system",
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w")

    def create_compact_bans(self, parent):
        """Sistema compacto de bans"""
        bans_frame = ctk.CTkFrame(parent, fg_color="transparent")
        bans_frame.pack(fill="both", expand=True, pady=(0, 15))

        bans_config = [
            {
                'number': '1',
                'title': '1st Ban',
                'subtitle': 'Most hated',
                'placeholder': 'e.g., Yasuo, Zed',
                'color': self.colors['danger'],
                'index': 0
            },
            {
                'number': '2',
                'title': '2nd Ban',
                'subtitle': 'Backup ban',
                'placeholder': 'If 1st is taken (optional)',
                'color': self.colors['warning'],
                'index': 1
            },
            {
                'number': '3',
                'title': '3rd Ban',
                'subtitle': 'Final backup',
                'placeholder': 'Last resort (optional)',
                'color': self.colors['accent'],
                'index': 2
            }
        ]

        self.entry_widgets = {}

        for config in bans_config:
            self.create_compact_ban_card(bans_frame, config)

    def create_compact_ban_card(self, parent, config):
        """Card compacto de ban"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=12,
            border_width=2,
            border_color=config['color']
        )
        card.pack(fill="x", pady=6)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)

        # Linha única: número, título e campo
        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x")

        # Número e título
        left_side = ctk.CTkFrame(row, fg_color="transparent")
        left_side.pack(side="left", fill="x")

        # Número compacto
        number_circle = ctk.CTkFrame(
            left_side,
            fg_color=config['color'],
            width=32,
            height=32,
            corner_radius=8
        )
        number_circle.pack(side="left", padx=(0, 10))
        number_circle.pack_propagate(False)

        ctk.CTkLabel(
            number_circle,
            text=config['number'],
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        ).pack(expand=True)

        # Título e subtítulo
        text_frame = ctk.CTkFrame(left_side, fg_color="transparent")
        text_frame.pack(side="left")

        title_row = ctk.CTkFrame(text_frame, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkLabel(
            title_row,
            text=config['title'],
            font=("Segoe UI", 12, "bold"),
            text_color=config['color']
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            title_row,
            text=config['subtitle'],
            font=("Segoe UI", 9),
            text_color=self.colors['text_secondary']
        ).pack(side="left")

        # Campo de entrada e botão na mesma linha
        input_row = ctk.CTkFrame(content, fg_color="transparent")
        input_row.pack(fill="x", pady=(8, 0))

        entry = ctk.CTkEntry(
            input_row,
            placeholder_text=config['placeholder'],
            height=38,
            font=("Segoe UI", 11),
            fg_color=self.colors['bg_light'],
            border_color=config['color'],
            border_width=2,
            text_color=self.colors['text_primary'],
            corner_radius=8
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        entry.insert(0, self.ban_values[config['index']])

        # Atualiza valor ao digitar
        def on_change(e):
            self.ban_values[config['index']] = entry.get().strip()

        entry.bind("<KeyRelease>", on_change)
        self.entry_widgets[config['index']] = entry

        # Botão de limpar compacto
        clear_btn = ctk.CTkButton(
            input_row,
            text="✕",
            width=38,
            height=38,
            font=("Segoe UI", 14),
            fg_color=self.colors['bg_light'],
            hover_color=self.colors['danger'],
            text_color=self.colors['text_secondary'],
            corner_radius=8,
            command=lambda: self.clear_ban(config['index'])
        )
        clear_btn.pack(side="left")

        # Tips apenas no primeiro
        if config['index'] == 0:
            tips_frame = ctk.CTkFrame(
                content,
                fg_color=self.colors['bg_light'],
                corner_radius=8
            )
            tips_frame.pack(fill="x", pady=(10, 0))

            tips_content = ctk.CTkFrame(tips_frame, fg_color="transparent")
            tips_content.pack(fill="x", padx=12, pady=8)

            ctk.CTkLabel(
                tips_content,
                text="💡 Ban your most hated champion • 1st is required • System cascades if taken",
                font=("Segoe UI", 9),
                text_color=self.colors['text_secondary'],
                anchor="w"
            ).pack(anchor="w")

    def clear_ban(self, index):
        """Limpa um ban específico"""
        if index in self.entry_widgets:
            self.entry_widgets[index].delete(0, 'end')
            self.ban_values[index] = ""

    def create_footer(self, parent):
        """Rodapé compacto"""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x", pady=(15, 0))

        # Botões lado a lado
        button_container = ctk.CTkFrame(footer, fg_color="transparent")
        button_container.pack()

        # Clear All (menor)
        clear_all_btn = ctk.CTkButton(
            button_container,
            text="🗑️ Clear All",
            height=40,
            width=110,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['bg_light'],
            hover_color=self.colors['danger'],
            text_color=self.colors['text_primary'],
            corner_radius=10,
            command=self.clear_all
        )
        clear_all_btn.pack(side="left", padx=(0, 10))

        # Spacer
        ctk.CTkFrame(button_container, fg_color="transparent", width=20).pack(side="left")

        # Cancel
        cancel_btn = ctk.CTkButton(
            button_container,
            text="✖ Cancel",
            height=40,
            width=110,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['bg_light'],
            hover_color=self.colors['bg_medium'],
            text_color=self.colors['text_primary'],
            corner_radius=10,
            command=self.cancel
        )
        cancel_btn.pack(side="left", padx=(0, 10))

        # Save (destaque)
        save_btn = ctk.CTkButton(
            button_container,
            text="✓ Save Configuration",
            height=40,
            width=180,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.colors['secondary'],
            hover_color=self.colors['primary'],
            text_color="white",
            corner_radius=10,
            command=self.save_config
        )
        save_btn.pack(side="left")

    def clear_all(self):
        """Limpa todos os bans"""
        for index in self.entry_widgets:
            self.entry_widgets[index].delete(0, 'end')
            self.ban_values[index] = ""

    def save_config(self):
        """Salva configuração"""
        # Atualiza valores dos entries
        for index in self.entry_widgets:
            self.ban_values[index] = self.entry_widgets[index].get().strip()

        ban1 = self.ban_values[0].strip()
        ban2 = self.ban_values[1].strip()
        ban3 = self.ban_values[2].strip()

        # Valida ban primário
        if not ban1:
            messagebox.showerror(
                "Error",
                "Primary ban is required!\n\nPlease configure your primary ban.",
                parent=self.dialog
            )
            return

        # Configura no sistema
        if not self.app.instalock_autoban.set_auto_ban_champion(ban1):
            messagebox.showerror("Error", f"Invalid champion: {ban1}", parent=self.dialog)
            return

        self.app.autoban_champion = ban1

        # Configura backups
        self.app.autoban_backup_2 = ban2 if ban2 else None
        self.app.autoban_backup_3 = ban3 if ban3 else None

        self.app.update_feature_cards()

        print(f"\n✅ Auto Ban configured:")
        print(f"  1st: {self.app.autoban_champion}")
        print(f"  2nd: {self.app.autoban_backup_2 or 'None'}")
        print(f"  3rd: {self.app.autoban_backup_3 or 'None'}")

        messagebox.showinfo(
            "Success",
            f"Auto Ban configured successfully!\n\n"
            f"1st: {ban1}\n"
            f"2nd: {ban2 or 'None'}\n"
            f"3rd: {ban3 or 'None'}",
            parent=self.dialog
        )

        self.close()

    def cancel(self):
        self.close()

    def close(self):
        try:
            self.dialog.grab_release()
            self.dialog.destroy()
        except:
            pass


def open_modern_autoban_config(parent, app):
    ModernAutoBanConfigurator(parent, app)