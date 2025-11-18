
import customtkinter as ctk 


class AboutView :


    def __init__ (self ,colors ,theme ):
        self .colors =colors 
        self .theme =theme 

    def create (self ,parent ):

        container =ctk .CTkFrame (parent ,fg_color ="transparent")
        container .pack (fill ="both",expand =True )

        title =ctk .CTkLabel (
        container ,
        text ="ℹ️ ABOUT",
        font =("Consolas",24 ,"bold"),
        text_color =self .colors ['primary']
        )
        title .pack (anchor ="w",pady =(0 ,20 ))


        info_card =ctk .CTkFrame (
        container ,
        fg_color =self .colors ['bg_card'],
        corner_radius =self .theme ['radius']['lg'],
        border_width =2 ,
        border_color =self .colors ['primary']
        )
        info_card .pack (fill ="x",pady =10 ,padx =20 )


        self ._create_app_info (info_card )


        ctk .CTkFrame (
        info_card ,
        fg_color =self .colors ['bg_light'],
        height =2 
        ).pack (fill ="x",padx =20 ,pady =10 )


        self ._create_credits (info_card )


        ctk .CTkFrame (
        info_card ,
        fg_color =self .colors ['bg_light'],
        height =2 
        ).pack (fill ="x",padx =20 ,pady =10 )

        self ._create_features (info_card )

    def _create_app_info (self ,parent ):

        app_frame =ctk .CTkFrame (parent ,fg_color ="transparent")
        app_frame .pack (fill ="x",padx =20 ,pady =15 )

        header_frame =ctk .CTkFrame (app_frame ,fg_color ="transparent")
        header_frame .pack (fill ="x",pady =(0 ,10 ))

        ctk .CTkLabel (
        header_frame ,
        text =self .colors .get ('app_icon','⚡'),
        font =("Segoe UI Emoji",48 ),
        text_color =self .colors ['primary']
        ).pack (side ="left",padx =(0 ,15 ))

        name_frame =ctk .CTkFrame (header_frame ,fg_color ="transparent")
        name_frame .pack (side ="left",fill ="both",expand =True )

        ctk .CTkLabel (
        name_frame ,
        text =self .colors .get ('app_name',"LEAGUE TOOLKIT"),
        font =("Consolas",18 ,"bold"),
        text_color =self .colors ['primary'],
        anchor ="w"
        ).pack (anchor ="w")

        ctk .CTkLabel (
        name_frame ,
        text ="League Automation Toolkit v2.0",
        font =("Consolas",11 ),
        text_color =self .colors ['text_secondary'],
        anchor ="w"
        ).pack (anchor ="w",pady =(2 ,0 ))

        ctk .CTkLabel (
        app_frame ,
        text ="Advanced automation toolkit for League of Legends",
        font =("Consolas",10 ),
        text_color =self .colors ['text_secondary'],
        justify ="left"
        ).pack (anchor ="w",pady =(10 ,0 ))

    def _create_credits (self ,parent ):

        credits_frame =ctk .CTkFrame (parent ,fg_color ="transparent")
        credits_frame .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        credits_frame ,
        text ="👨‍💻 Credits & Developers",
        font =("Consolas",14 ,"bold"),
        text_color =self .colors ['primary']
        ).pack (anchor ="w",pady =(0 ,10 ))

        devs =[
        ("⚡ Younk","Lead Developer & Designer"),
        ("🔧 Gyaf","Core Developer & Architect")
        ]

        for dev_name ,dev_role in devs :
            dev_card =ctk .CTkFrame (
            credits_frame ,
            fg_color =self .colors ['bg_light'],
            corner_radius =8 
            )
            dev_card .pack (fill ="x",pady =5 )

            dev_content =ctk .CTkFrame (dev_card ,fg_color ="transparent")
            dev_content .pack (fill ="x",padx =15 ,pady =12 )

            ctk .CTkLabel (
            dev_content ,
            text =dev_name ,
            font =("Consolas",12 ,"bold"),
            text_color =self .colors ['primary']
            ).pack (anchor ="w")

            ctk .CTkLabel (
            dev_content ,
            text =dev_role ,
            font =("Consolas",9 ),
            text_color =self .colors ['text_secondary']
            ).pack (anchor ="w",pady =(2 ,0 ))

    def _create_features (self ,parent ):

        features_frame =ctk .CTkFrame (parent ,fg_color ="transparent")
        features_frame .pack (fill ="x",padx =20 ,pady =15 )

        ctk .CTkLabel (
        features_frame ,
        text ="⚡ Features",
        font =("Consolas",14 ,"bold"),
        text_color =self .colors ['primary']
        ).pack (anchor ="w",pady =(0 ,10 ))

        features_list =[
        ("🔒 Instalock","Instant champion selection with 3 backups"),
        ("⛔ Auto Ban","Automatic champion banning with 3 backups"),
        ("✓ Auto Accept","Auto-accept queue matches"),
        ("💬 Chat Toggle","Enable/disable in-game chat"),
        ("📊 Lobby Reveal","Open Porofessor analysis"),
        ("🎨 Theme Selector","Manage and import themes")
        ]

        for icon_title ,description in features_list :
            feature_item =ctk .CTkFrame (features_frame ,fg_color ="transparent")
            feature_item .pack (fill ="x",pady =3 )

            ctk .CTkLabel (
            feature_item ,
            text =icon_title ,
            font =("Consolas",11 ,"bold"),
            text_color =self .colors ['primary'],
            anchor ="w",
            width =140 
            ).pack (side ="left")

            ctk .CTkLabel (
            feature_item ,
            text =f"- {description }",
            font =("Consolas",10 ),
            text_color =self .colors ['text_secondary'],
            anchor ="w"
            ).pack (side ="left",fill ="x",expand =True )

    def update_colors (self ,colors ):

        self .colors =colors 