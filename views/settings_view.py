
import customtkinter as ctk 
from ui .theme .theme_switcher_ui import ThemeSettingsView 


class SettingsView :


    def __init__ (self ,colors ,theme ):
        self .colors =colors 
        self .theme =theme 

    def create (self ,parent ,on_theme_change ):

        grid =ctk .CTkFrame (parent ,fg_color ="transparent")
        grid .pack (fill ="both",expand =True )


        title =ctk .CTkLabel (
        grid ,
        text ="⚙️ SETTINGS",
        font =("Consolas",20 ,"bold"),
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w",pady =(0 ,20 ))

        theme_view =ThemeSettingsView (
        grid ,
        on_theme_change =on_theme_change ,
        fg_color =self .colors ['bg_medium']
        )
        theme_view .pack (fill ="both",expand =True )

    def update_colors (self ,colors ):

        self .colors =colors 