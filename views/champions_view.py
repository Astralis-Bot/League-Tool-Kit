
import customtkinter as ctk 
from ui .components import FeatureCard 


class ChampionsView :


    def __init__ (self ,colors ,theme ):
        self .colors =colors 
        self .theme =theme 

    def create (self ,parent ,app ):
        app .ui_manager .add_title ("🎮 CHAMPION SETTINGS")


        desc =ctk .CTkLabel (
        app .ui_manager .scroll_area ,
        text ="Configure automatic champion selection and banning with backup system",
        font =self .theme ['fonts']['small'],
        text_color =self .colors ['text_secondary']
        )
        desc .pack (anchor ="w",pady =(0 ,20 ))

        instalock_desc =self ._get_instalock_description (app )

        instalock_card =FeatureCard (
        app .ui_manager .scroll_area ,
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

        autoban_desc =self ._get_autoban_description (app )
        autoban_card =FeatureCard (
        app .ui_manager .scroll_area ,
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

        info_frame =ctk .CTkFrame (
        app .ui_manager .scroll_area ,
        fg_color =self .colors ['bg_card'],
        corner_radius =self .theme ['radius']['lg'],
        border_width =2 ,
        border_color =self .colors ['info']
        )
        info_frame .pack (fill ="x",pady =(20 ,0 ))

        info_content =ctk .CTkFrame (info_frame ,fg_color ="transparent")
        info_content .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        info_content ,
        text ="💡 Tips",
        font =self .theme ['fonts']['subheading'],
        text_color =self .colors ['info']
        ).pack (anchor ="w",pady =(0 ,10 ))

        tips =[
        "• Click the ⚙️ button to configure your champion picks",
        "• Set up to 3 backup champions for instalock",
        "• Set up to 3 backup champions for auto ban",
        "• If all picks are banned, a random champion is selected",
        "• Instalock works in blind pick and draft pick",
        "• Auto Ban only works in ranked and draft pick",
        "• Toggle ON to enable the feature"
        ]

        for tip in tips :
            ctk .CTkLabel (
            info_content ,
            text =tip ,
            font =self .theme ['fonts']['small'],
            text_color =self .colors ['text_secondary'],
            anchor ="w"
            ).pack (anchor ="w",pady =2 )

        app .after (50 ,lambda :self ._restore_champion_icons (app ))

    def _get_instalock_description (self ,app ):
        if not app .instalock_champion :
            return "No champion selected"

        parts =[f"1st: {app .instalock_champion }"]

        if app .instalock_backup_2 :
            parts .append (f"2nd: {app .instalock_backup_2 }")

        if app .instalock_backup_3 :
            parts .append (f"3rd: {app .instalock_backup_3 }")

        return " | ".join (parts )

    def _get_autoban_description (self ,app ):
        if not app .autoban_champion :
            return "No champion selected"

        parts =[f"1st: {app .autoban_champion }"]

        if hasattr (app ,'autoban_backup_2')and app .autoban_backup_2 :
            parts .append (f"2nd: {app .autoban_backup_2 }")

        if hasattr (app ,'autoban_backup_3')and app .autoban_backup_3 :
            parts .append (f"3rd: {app .autoban_backup_3 }")

        return " | ".join (parts )

    def _restore_champion_icons (self ,app ):
        try :
            if app .instalock_champion :
                app .champion_manager .update_instalock_display (app ,app .instalock_champion )

            if app .autoban_champion :
                app .champion_manager .update_autoban_display (app ,app .autoban_champion )
        except Exception as e :
            print (f"Erro ao restaurar ícones: {e }")

    def update_colors (self ,colors ):
        self .colors =colors 