
import customtkinter as ctk 


class StatusView :


    def __init__ (self ,colors ,theme ):
        self .colors =colors 
        self .theme =theme 

    def create (self ,parent ,get_status_data ):

        grid =ctk .CTkFrame (parent ,fg_color ="transparent")
        grid .pack (fill ="both",expand =True )

        title =ctk .CTkLabel (
        grid ,
        text ="📊 SYSTEM STATUS",
        font =("Consolas",20 ,"bold"),
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w",pady =(0 ,20 ))

        status_frame =ctk .CTkFrame (grid ,fg_color ="transparent")
        status_frame .pack (fill ="both",expand =True )


        status =get_status_data ()


        self ._create_active_modules_card (status_frame ,status )

        self ._create_chat_status_card (status_frame ,status )


        self ._create_system_info_card (status_frame )

    def _create_active_modules_card (self ,parent ,status ):

        active_card =ctk .CTkFrame (
        parent ,
        fg_color =self .colors ['bg_card'],
        corner_radius =self .theme ['radius']['lg'],
        border_width =2 ,
        border_color =self .colors ['success']
        )
        active_card .pack (fill ="x",pady =10 )

        active_header =ctk .CTkFrame (active_card ,fg_color ="transparent")
        active_header .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        active_header ,
        text ="✅ Active Modules",
        font =("Consolas",16 ,"bold"),
        text_color =self .colors ['success']
        ).pack (anchor ="w")

        modules_frame =ctk .CTkFrame (active_card ,fg_color ="transparent")
        modules_frame .pack (fill ="x",padx =30 ,pady =(0 ,15 ))

        has_active =False 

        if status .get ('auto_accept'):
            self ._add_status_item (modules_frame ,"⚡ Auto Accept","ACTIVE",self .colors ['success'])
            has_active =True 

        if status .get ('instalock'):
            self ._add_status_item (modules_frame ,"🔒 Instalock",status ['instalock'],self .colors ['primary'])
            has_active =True 

        if status .get ('auto_ban'):
            self ._add_status_item (modules_frame ,"⛔ Auto Ban",status ['auto_ban'],self .colors ['secondary'])
            has_active =True 


        if not has_active :
            ctk .CTkLabel (
            modules_frame ,
            text ="No modules currently active",
            font =("Consolas",10 ),
            text_color =self .colors ['text_secondary']
            ).pack (anchor ="w",pady =5 )

    def _create_chat_status_card (self ,parent ,status ):

        chat_card =ctk .CTkFrame (
        parent ,
        fg_color =self .colors ['bg_card'],
        corner_radius =self .theme ['radius']['lg'],
        border_width =2 ,
        border_color =self .colors ['accent']
        )
        chat_card .pack (fill ="x",pady =10 )

        chat_content =ctk .CTkFrame (chat_card ,fg_color ="transparent")
        chat_content .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        chat_content ,
        text ="💬 Chat Status",
        font =("Consolas",16 ,"bold"),
        text_color =self .colors ['accent']
        ).pack (anchor ="w",pady =(0 ,10 ))

        chat_state =status .get ('chat','unknown')

        status_text =f"Chat is currently {chat_state .upper ()}"
        status_color =self .colors ['success']if chat_state .lower ()=='enabled'else self .colors ['warning']

        ctk .CTkLabel (
        chat_content ,
        text =status_text ,
        font =("Consolas",12 ),
        text_color =status_color 
        ).pack (anchor ="w")

    def _create_system_info_card (self ,parent ):
        info_card =ctk .CTkFrame (
        parent ,
        fg_color =self .colors ['bg_card'],
        corner_radius =self .theme ['radius']['lg'],
        border_width =2 ,
        border_color =self .colors ['info']
        )
        info_card .pack (fill ="x",pady =10 )

        info_content =ctk .CTkFrame (info_card ,fg_color ="transparent")
        info_content .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        info_content ,
        text ="🔧 System Information",
        font =("Consolas",16 ,"bold"),
        text_color =self .colors ['info']
        ).pack (anchor ="w",pady =(0 ,10 ))

        info_items =[
        ("Application","League Toolkit v2.0"),
        ("Connection","LCU Connected"),
        ("Status","All systems operational"),
        ("Update Check","Automatic"),
        ]

        for label ,value in info_items :
            item_frame =ctk .CTkFrame (info_content ,fg_color ="transparent")
            item_frame .pack (fill ="x",pady =3 )

            ctk .CTkLabel (
            item_frame ,
            text =f"{label }:",
            font =("Consolas",11 ,"bold"),
            text_color =self .colors ['text_primary']
            ).pack (side ="left")

            ctk .CTkLabel (
            item_frame ,
            text =value ,
            font =("Consolas",10 ),
            text_color =self .colors ['text_secondary']
            ).pack (side ="left",padx =(10 ,0 ))

    def _add_status_item (self ,parent ,title ,value ,color ):

        item =ctk .CTkFrame (parent ,fg_color ="transparent")
        item .pack (fill ="x",pady =5 )

        ctk .CTkLabel (
        item ,
        text =title ,
        font =("Consolas",12 ,"bold"),
        text_color =color 
        ).pack (side ="left")

        ctk .CTkLabel (
        item ,
        text =f"→ {value }",
        font =("Consolas",10 ),
        text_color =self .colors ['text_secondary']
        ).pack (side ="left",padx =(10 ,0 ))

    def update_colors (self ,colors ):

        self .colors =colors 