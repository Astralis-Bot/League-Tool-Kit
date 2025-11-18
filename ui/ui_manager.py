
import customtkinter as ctk 
from ui .ui_config import COLORS ,THEME 
from ui .components import Sidebar ,StatusBar 


class UIManager :

    def __init__ (self ,app ,colors =None ,theme =None ):
        self .app =app 
        self .colors =colors or COLORS 
        self .theme =theme or THEME 
        self .components ={}
        self .feature_cards =[]
        self .action_cards =[]
        self .main_frame =None 
        self .content_frame =None 
        self .scroll_area =None 
        self .header_frame =None 
        self .status_bar =None 
        self .sidebar =None 

        self .instalock_card =None 
        self .autoban_card =None 

    def create_main_layout (self ):

        self .main_frame =ctk .CTkFrame (
        self .app ,
        fg_color =self .colors ['bg_dark']
        )
        self .main_frame .pack (fill ="both",expand =True )

        self .sidebar =Sidebar (
        self .main_frame ,
        self .app .switch_category ,
        self .colors ,
        self .theme 
        )
        self .sidebar .pack (side ="left",fill ="y")
        self .components ['sidebar']=self .sidebar 

        self .content_frame =ctk .CTkFrame (
        self .main_frame ,
        fg_color =self .colors ['bg_medium']
        )
        self .content_frame .pack (side ="left",fill ="both",expand =True )

        self .create_header ()

        self .scroll_area =ctk .CTkScrollableFrame (
        self .content_frame ,
        fg_color =self .colors ['bg_medium'],
        corner_radius =0 
        )
        self .scroll_area .pack (
        fill ="both",
        expand =True ,
        padx =self .theme ['spacing']['lg'],
        pady =self .theme ['spacing']['lg']
        )
        self .components ['scroll_area']=self .scroll_area 

        self .status_bar =StatusBar (
        self .content_frame ,
        self .app .get_status_data ,
        self .colors ,
        self .theme 
        )
        self .status_bar .pack (side ="bottom",fill ="x")
        self .components ['status_bar']=self .status_bar 

    def create_header (self ):
        self .header_frame =ctk .CTkFrame (
        self .content_frame ,
        fg_color =self .colors ['bg_dark'],
        height =80 
        )
        self .header_frame .pack (fill ="x",padx =20 ,pady =(20 ,0 ))
        self .header_frame .pack_propagate (False )

        left_container =ctk .CTkFrame (self .header_frame ,fg_color ="transparent")
        left_container .pack (side ="left",fill ="y")


        icon_label =ctk .CTkLabel (
        left_container ,
        text =self .colors .get ('app_icon','⚡'),
        font =("Segoe UI Emoji",42 ),
        text_color =self .colors ['primary']
        )
        icon_label .pack (side ="left",padx =(5 ,15 ))
        self .components ['header_icon']=icon_label 


        text_container =ctk .CTkFrame (left_container ,fg_color ="transparent")
        text_container .pack (side ="left",fill ="y",pady =10 )


        title =ctk .CTkLabel (
        text_container ,
        text =self .colors .get ('app_name',"LEAGUE TOOLKIT"),
        font =("Consolas",22 ,"bold"),
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w")
        self .components ['header_title']=title 


        subtitle =ctk .CTkLabel (
        text_container ,
        text ="League Automation Toolkit v2.0",
        font =("Consolas",10 ),
        text_color =self .colors ['text_secondary']
        )
        subtitle .pack (anchor ="w")


        right_container =ctk .CTkFrame (self .header_frame ,fg_color ="transparent")
        right_container .pack (side ="right",fill ="y",pady =15 )


        badge =ctk .CTkLabel (
        right_container ,
        text ="● ONLINE",
        font =("Consolas",12 ,"bold"),
        text_color =self .colors ['bg_dark'],
        fg_color =self .colors ['success'],
        corner_radius =8 
        )
        badge .pack (side ="right",padx =5 ,ipadx =15 ,ipady =6 )
        self .components ['status_badge']=badge 


        connection =ctk .CTkLabel (
        right_container ,
        text ="⚡ LCU Connected",
        font =("Consolas",10 ),
        text_color =self .colors ['text_secondary']
        )
        connection .pack (side ="right",padx =(0 ,15 ))

    def clear_scroll_area (self ):

        for widget in self .scroll_area .winfo_children ():
            widget .destroy ()
        self .feature_cards =[]
        self .action_cards =[]

    def add_title (self ,text ):

        title =ctk .CTkLabel (
        self .scroll_area ,
        text =text ,
        font =self .theme ['fonts']['title'],
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w",pady =(0 ,self .theme ['spacing']['md']))
        return title 

    def add_section_title (self ,text ):

        title =ctk .CTkLabel (
        self .scroll_area ,
        text =text ,
        font =self .theme ['fonts']['heading'],
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w",pady =(self .theme ['spacing']['lg'],self .theme ['spacing']['md']))
        return title 

    def add_spacing (self ,height =20 ):

        spacer =ctk .CTkFrame (
        self .scroll_area ,
        fg_color ="transparent",
        height =height 
        )
        spacer .pack ()

    def add_feature_card (self ,card ):

        card .pack (fill ="x",pady =self .theme ['spacing']['md'])
        self .feature_cards .append (card )


        if "Instalock"in card .title_text or "instalock"in card .title_text .lower ():
            self .instalock_card =card 
        elif "Auto Ban"in card .title_text or "autoban"in card .title_text .lower ():
            self .autoban_card =card 

        return card 

    def add_action_card (self ,card ):

        card .pack (fill ="x",pady =self .theme ['spacing']['md'])
        self .action_cards .append (card )
        return card 

    def update_colors (self ,colors ):

        self .colors =colors 


        self .app .configure (fg_color =colors ['bg_dark'])
        self .main_frame .configure (fg_color =colors ['bg_dark'])
        self .content_frame .configure (fg_color =colors ['bg_medium'])
        self .scroll_area .configure (fg_color =colors ['bg_medium'])
        self .header_frame .configure (fg_color =colors ['bg_dark'])


        if self .sidebar :
            self .sidebar .update_colors (colors )

        if self .status_bar :
            self .status_bar .update_colors (colors )

        if 'header_icon'in self .components :
            self .components ['header_icon'].configure (
            text =colors .get ('app_icon','⚡'),
            text_color =colors ['primary']
            )

        if 'header_title'in self .components :
            self .components ['header_title'].configure (
            text =colors .get ('app_name',"LEAGUE TOOLKIT"),
            text_color =colors ['primary']
            )

        if 'status_badge'in self .components :
            self .components ['status_badge'].configure (
            text_color =colors ['bg_dark'],
            fg_color =colors ['success']
            )


        for card in self .feature_cards :
            if hasattr (card ,'update_colors'):
                card .update_colors (colors )

        for card in self .action_cards :
            if hasattr (card ,'update_colors'):
                card .update_colors (colors )