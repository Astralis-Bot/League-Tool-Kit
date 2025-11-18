
import customtkinter as ctk 
from ui .components import ActionCard ,FeatureCard 


class HomeView :


    def __init__ (self ,colors ,theme ):
        self .colors =colors 
        self .theme =theme 

    def create (self ,parent ,app ):

        app .ui_manager .add_title ("⚡ DASHBOARD")

        desc =ctk .CTkLabel (
        app .ui_manager .scroll_area ,
        text ="Quick access to all features with backup system",
        font =self .theme ['fonts']['small'],
        text_color =self .colors ['text_secondary']
        )
        desc .pack (anchor ="w",pady =(0 ,20 ))


        grid_container =ctk .CTkFrame (app .ui_manager .scroll_area ,fg_color ="transparent")
        grid_container .pack (fill ="both",expand =True )
        grid_container .columnconfigure (0 ,weight =1 )
        grid_container .columnconfigure (1 ,weight =1 )

        self ._create_champion_column (grid_container ,app )
        self ._create_actions_column (grid_container ,app )

        app .after (50 ,lambda :self ._restore_champion_icons (app ))

    def _create_champion_column (self ,parent ,app ):
        champ_frame =ctk .CTkFrame (parent ,fg_color ="transparent")
        champ_frame .grid (row =0 ,column =0 ,sticky ="nsew",padx =(0 ,10 ))

        ctk .CTkLabel (
        champ_frame ,
        text ="🎮 CHAMPION AUTOMATION",
        font =self .theme ['fonts']['subheading'],
        text_color =self .colors ['primary']
        ).pack (anchor ="w",pady =(0 ,10 ))

        instalock_desc =self ._get_instalock_description (app )

        instalock_card =FeatureCard (
        champ_frame ,
        "🔒 INSTALOCK",
        instalock_desc ,
        self .colors ['primary'],
        app .toggle_instalock ,
        app .open_instalock_hub ,
        self .colors ,
        self .theme ,
        is_enabled =app .instalock_enabled ,
        show_icon =True 
        )
        app .ui_manager .add_feature_card (instalock_card )

        autoban_desc =f"Selected: {app .autoban_champion }"if app .autoban_champion else "No champion selected"
        autoban_card =FeatureCard (
        champ_frame ,
        "⛔ AUTO BAN",
        autoban_desc ,
        self .colors ['secondary'],
        app .toggle_autoban ,
        app .open_autoban_hub ,
        self .colors ,
        self .theme ,
        is_enabled =app .autoban_enabled ,
        show_icon =True 
        )
        app .ui_manager .add_feature_card (autoban_card )


    def _create_actions_column (self ,parent ,app ):
        quick_frame =ctk .CTkFrame (parent ,fg_color ="transparent")
        quick_frame .grid (row =0 ,column =1 ,sticky ="nsew",padx =(10 ,0 ))

        ctk .CTkLabel (
        quick_frame ,
        text ="⚡ QUICK ACTIONS",
        font =self .theme ['fonts']['subheading'],
        text_color =self .colors ['primary']
        ).pack (anchor ="w",pady =(0 ,10 ))

        auto_accept_card =FeatureCard (
        quick_frame ,
        "✓ AUTO ACCEPT",
        "Accept matches automatically",
        self .colors ['success'],
        app .toggle_auto_accept ,
        None ,
        self .colors ,
        self .theme ,
        is_enabled =app .auto_accept .auto_accept_enabled if app .auto_accept else False ,
        show_icon =False 
        )
        app .ui_manager .add_feature_card (auto_accept_card )

        chat_card =ActionCard (
        quick_frame ,
        "💬 CHAT TOGGLE",
        "Enable/disable in-game chat",
        self .colors ['accent'],
        app .toggle_chat ,
        self .colors ,
        self .theme 
        )
        app .ui_manager .add_action_card (chat_card )

        lobby_card =ActionCard (
        quick_frame ,
        "📊 LOBBY REVEAL",
        "Open Porofessor analysis",
        self .colors ['info'],
        app .lobby_reveal ,
        self .colors ,
        self .theme 
        )
        app .ui_manager .add_action_card (lobby_card )

    def _get_instalock_description (self ,app ):
        if not app .instalock_champion :
            return "No champion selected"

        parts =[f"1st: {app .instalock_champion }"]

        if app .instalock_backup_2 :
            parts .append (f"2nd: {app .instalock_backup_2 }")

        if app .instalock_backup_3 :
            parts .append (f"3rd: {app .instalock_backup_3 }")

        return " | ".join (parts )

    def _restore_champion_icons (self ,app ):

        try :
            print ("\n"+"="*60 )
            print ("🔄 RESTAURANDO ÍCONES APÓS RECRIAR VIEW")
            print ("="*60 )

            if app .instalock_champion :
                print (f"♻️ Restaurando Instalock: {app .instalock_champion }")
                app .champion_manager .update_instalock_display (app ,app .instalock_champion )
            else :
                print ("ℹ️ Nenhum campeão Instalock para restaurar")

            if app .autoban_champion :
                print (f"♻️ Restaurando AutoBan: {app .autoban_champion }")
                app .champion_manager .update_autoban_display (app ,app .autoban_champion )
            else :
                print ("ℹ️ Nenhum campeão AutoBan para restaurar")

            print ("="*60 )
            print ("✅ RESTAURAÇÃO CONCLUÍDA")
            print ("="*60 +"\n")
        except Exception as e :
            print (f"❌ Erro ao restaurar ícones: {e }")
            import traceback 
            traceback .print_exc ()

    def update_colors (self ,colors ):

        self .colors =colors 