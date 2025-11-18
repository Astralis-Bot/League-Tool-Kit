
import customtkinter as ctk 
from ui .ui_config import THEME ,SIDEBAR_ITEMS 


class Sidebar (ctk .CTkFrame ):

    def __init__ (self ,master ,on_select ,colors ,theme ):
        super ().__init__ (master ,fg_color =colors ['bg_dark'],width =200 ,corner_radius =0 )
        self .pack_propagate (False )
        self .on_select =on_select 
        self .selected_item =None 
        self .colors =colors 
        self .theme =theme 

        self .logo_frame =ctk .CTkFrame (self ,fg_color =colors ['primary'],height =80 )
        self .logo_frame .pack (fill ="x")
        self .logo_frame .pack_propagate (False )

        self .logo_label =ctk .CTkLabel (
        self .logo_frame ,
        text =colors .get ('app_icon','⚡'),
        font =("Segoe UI Emoji",42 ),
        text_color =colors ['bg_dark']
        )
        self .logo_label .pack (expand =True )

        self .menu_items =[]
        for item in SIDEBAR_ITEMS :
            if 'text'in item and 'icon'in item and 'id'in item :
                btn =SidebarButton (
                self ,
                item ['icon'],
                item ['text'],
                lambda i =item :self .select_item (i ),
                colors ,
                theme 
                )
                btn .pack (fill ="x",padx =10 ,pady =5 )
                self .menu_items .append ((btn ,item ['id']))

        ctk .CTkFrame (self ,fg_color ="transparent").pack (fill ="both",expand =True )

        self .footer =ctk .CTkFrame (self ,fg_color =colors ['bg_light'],height =60 )
        self .footer .pack (fill ="x")
        self .footer .pack_propagate (False )

        self .footer_label =ctk .CTkLabel (
        self .footer ,
        text ="v2.0",
        font =("Consolas",10 ),
        text_color =colors ['text_secondary']
        )
        self .footer_label .pack (expand =True )

    def select_item (self ,item ):
        for btn ,item_id in self .menu_items :
            btn .deselect ()

        for btn ,item_id in self .menu_items :
            if item_id ==item ['id']:
                btn .select ()
                self .selected_item =item_id 
                break 

        self .on_select (item ['id'])

    def update_colors (self ,colors ):
        self .colors =colors 
        self .configure (fg_color =colors ['bg_dark'])
        self .logo_frame .configure (fg_color =colors ['primary'])
        self .logo_label .configure (
        text =colors .get ('app_icon','⚡'),
        text_color =colors ['bg_dark']
        )
        self .footer .configure (fg_color =colors ['bg_light'])
        self .footer_label .configure (text_color =colors ['text_secondary'])

        for btn ,_ in self .menu_items :
            btn .update_colors (colors )


class SidebarButton (ctk .CTkFrame ):

    def __init__ (self ,master ,icon ,text ,command ,colors ,theme ):
        super ().__init__ (master ,fg_color ="transparent",cursor ="hand2")
        self .command =command 
        self .is_selected =False 
        self .colors =colors 
        self .theme =theme 

        self .container =ctk .CTkFrame (
        self ,
        fg_color ="transparent",
        corner_radius =theme ['radius']['md']
        )
        self .container .pack (fill ="x",padx =5 ,pady =2 )

        content =ctk .CTkFrame (self .container ,fg_color ="transparent")
        content .pack (fill ="x",padx =12 ,pady =10 )

        self .icon_label =ctk .CTkLabel (
        content ,
        text =icon ,
        font =("Consolas",18 ),
        text_color =colors ['text_secondary'],
        width =30 
        )
        self .icon_label .pack (side ="left")

        self .text_label =ctk .CTkLabel (
        content ,
        text =text ,
        font =("Consolas",12 ,"bold"),
        text_color =colors ['text_secondary'],
        anchor ="w"
        )
        self .text_label .pack (side ="left",fill ="x",expand =True ,padx =(8 ,0 ))

        self .container .bind ("<Button-1>",lambda e :self .on_click ())
        self .icon_label .bind ("<Button-1>",lambda e :self .on_click ())
        self .text_label .bind ("<Button-1>",lambda e :self .on_click ())

        self .container .bind ("<Enter>",self .on_hover )
        self .container .bind ("<Leave>",self .on_leave )

    def on_click (self ):
        self .command ()

    def on_hover (self ,e ):
        if not self .is_selected :
            self .container .configure (fg_color =self .colors ['bg_light'])

    def on_leave (self ,e ):
        if not self .is_selected :
            self .container .configure (fg_color ="transparent")

    def select (self ):
        self .is_selected =True 
        self .container .configure (fg_color =self .colors ['bg_medium'])
        self .icon_label .configure (text_color =self .colors ['primary'])
        self .text_label .configure (text_color =self .colors ['primary'])

    def deselect (self ):
        self .is_selected =False 
        self .container .configure (fg_color ="transparent")
        self .icon_label .configure (text_color =self .colors ['text_secondary'])
        self .text_label .configure (text_color =self .colors ['text_secondary'])

    def update_colors (self ,colors ):
        self .colors =colors 
        if self .is_selected :
            self .select ()
        else :
            self .deselect ()


class FeatureCard (ctk .CTkFrame ):

    def __init__ (self ,master ,title ,description ,color ,on_toggle ,on_configure ,colors ,theme ,is_enabled =False ,show_icon =True ):
        super ().__init__ (
        master ,
        fg_color =colors ['bg_card'],
        corner_radius =theme ['radius']['lg'],
        border_color =color ,
        border_width =2 
        )

        self .title_text =title 
        self .color =color 
        self .is_enabled =is_enabled 
        self .on_toggle =on_toggle 
        self .on_configure =on_configure 
        self .champion_icon =None 
        self .colors =colors 
        self .theme =theme 
        self .show_icon =show_icon 

        content =ctk .CTkFrame (self ,fg_color ="transparent")
        content .pack (fill ="both",expand =True ,padx =16 ,pady =14 )


        if self .show_icon :
            self .icon_frame =ctk .CTkFrame (
            content ,
            fg_color =colors ['bg_light'],
            width =50 ,
            height =50 ,
            corner_radius =8 ,
            border_width =2 ,
            border_color =color 
            )
            self .icon_frame .pack (side ="left",padx =(0 ,12 ))
            self .icon_frame .pack_propagate (False )

            self .icon_label =ctk .CTkLabel (
            self .icon_frame ,
            text ="?",
            font =("Consolas",20 ,"bold"),
            text_color =color 
            )
            self .icon_label .pack (expand =True )

            self .icon_frame .bind ("<Enter>",lambda e :self .icon_frame .configure (border_color =self .color ,border_width =3 ))
            self .icon_frame .bind ("<Leave>",lambda e :self .icon_frame .configure (border_color =self .color ,border_width =2 ))
        else :
            self .icon_frame =None 


        info =ctk .CTkFrame (content ,fg_color ="transparent")
        info .pack (side ="left",fill ="both",expand =True )

        self .title_label =ctk .CTkLabel (
        info ,
        text =title ,
        font =("Consolas",14 ,"bold"),
        text_color =color ,
        anchor ="w"
        )
        self .title_label .pack (anchor ="w")

        self .desc_label =ctk .CTkLabel (
        info ,
        text =description ,
        font =("Consolas",10 ),
        text_color =colors ['text_secondary'],
        anchor ="w"
        )
        self .desc_label .pack (anchor ="w",pady =(2 ,0 ))


        btn_frame =ctk .CTkFrame (content ,fg_color ="transparent")
        btn_frame .pack (side ="right",padx =(10 ,0 ))

        self .toggle_btn =ctk .CTkButton (
        btn_frame ,
        text ="ON"if is_enabled else "OFF",
        width =50 ,
        height =40 ,
        font =("Consolas",11 ,"bold"),
        fg_color =color if is_enabled else colors ['bg_light'],
        hover_color =color ,
        text_color =colors ['bg_dark']if is_enabled else colors ['text_primary'],
        corner_radius =8 ,
        command =self .toggle_state 
        )
        self .toggle_btn .pack (side ="left",padx =(0 ,8 ))

        if on_configure is not None :
            self .config_btn =ctk .CTkButton (
            btn_frame ,
            text ="⚙️",
            width =40 ,
            height =40 ,
            font =("Consolas",16 ),
            fg_color =colors ['bg_light'],
            hover_color =colors ['bg_medium'],
            text_color =color ,
            corner_radius =8 ,
            command =self .configure_feature 
            )
            self .config_btn .pack (side ="left")
        else :
            self .config_btn =None 

    def toggle_state (self ):
        self .is_enabled =not self .is_enabled 
        self .toggle_btn .configure (
        text ="ON"if self .is_enabled else "OFF",
        fg_color =self .color if self .is_enabled else self .colors ['bg_light'],
        text_color =self .colors ['bg_dark']if self .is_enabled else self .colors ['text_primary']
        )
        if self .on_toggle :
            self .on_toggle (self .is_enabled )

    def configure_feature (self ):
        if self .on_configure :
            self .on_configure ()

    def set_enabled (self ,enabled ):
        self .is_enabled =enabled 
        self .toggle_btn .configure (
        text ="ON"if enabled else "OFF",
        fg_color =self .color if enabled else self .colors ['bg_light'],
        text_color =self .colors ['bg_dark']if enabled else self .colors ['text_primary']
        )

    def update_description (self ,text ):
        try :
            if hasattr (self ,'desc_label')and self .desc_label .winfo_exists ():
                self .desc_label .configure (text =text )
                print (f"✅ Descrição atualizada: {text }")
        except Exception as e :
            print (f"❌ Erro ao atualizar descrição: {e }")


    def set_champion_icon (self ,icon ,champion_name ):
        if not self .show_icon or not hasattr (self ,'icon_frame')or not self .icon_frame :
            return 

        try :
            if not self .icon_frame .winfo_exists ():
                return 


            for widget in self .icon_frame .winfo_children ():
                widget .destroy ()


            img_label =ctk .CTkLabel (
            self .icon_frame ,
            image =icon ,
            text =""
            )
            img_label .pack (fill ="both",expand =True )


            self .champion_icon =icon 
            self .icon_frame ._image_ref =icon 
            img_label ._image_ref =icon 


            if not hasattr (self ,'_persistent_icon_refs'):
                self ._persistent_icon_refs =[]
            self ._persistent_icon_refs .append (icon )

            print (f"✅ Ícone definido com referências persistentes: {champion_name }")
        except Exception as e :
            print (f"❌ Erro ao definir ícone: {e }")

    def clear_champion_icon (self ):
        if not self .show_icon or not hasattr (self ,'icon_frame')or not self .icon_frame :
            return 

        try :
            if not self .icon_frame .winfo_exists ():
                return 

            for widget in self .icon_frame .winfo_children ():
                widget .destroy ()

            self .icon_label =ctk .CTkLabel (
            self .icon_frame ,
            text ="?",
            font =("Consolas",20 ,"bold"),
            text_color =self .color 
            )
            self .icon_label .pack (expand =True )

            self .champion_icon =None 
            if hasattr (self .icon_frame ,'_image_ref'):
                delattr (self .icon_frame ,'_image_ref')

            print ("✅ Ícone limpo")
        except Exception as e :
            print (f"❌ Erro ao limpar ícone: {e }")

    def update_colors (self ,colors ):
        self .colors =colors 
        self .configure (
        fg_color =colors ['bg_card'],
        border_color =self .color 
        )

        if self .show_icon and self .icon_frame :
            self .icon_frame .configure (
            fg_color =colors ['bg_light'],
            border_color =self .color 
            )

        if hasattr (self ,'title_label'):
            self .title_label .configure (text_color =self .color )
        if hasattr (self ,'desc_label'):
            self .desc_label .configure (text_color =colors ['text_secondary'])

        if hasattr (self ,'toggle_btn'):
            self .toggle_btn .configure (
            fg_color =self .color if self .is_enabled else colors ['bg_light'],
            hover_color =self .color ,
            text_color =colors ['bg_dark']if self .is_enabled else colors ['text_primary']
            )

        if hasattr (self ,'config_btn')and self .config_btn is not None :
            self .config_btn .configure (
            fg_color =colors ['bg_light'],
            hover_color =colors ['bg_medium'],
            text_color =self .color 
            )


class ActionCard (ctk .CTkFrame ):

    def __init__ (self ,master ,title ,description ,color ,command ,colors ,theme ):
        super ().__init__ (
        master ,
        fg_color =colors ['bg_card'],
        corner_radius =theme ['radius']['lg'],
        border_color =color ,
        border_width =2 ,
        cursor ="hand2"
        )

        self .command =command 
        self .color =color 
        self .colors =colors 
        self .theme =theme 
        self ._is_processing =False 

        content =ctk .CTkFrame (self ,fg_color ="transparent")
        content .pack (fill ="both",expand =True ,padx =16 ,pady =14 )

        info =ctk .CTkFrame (content ,fg_color ="transparent")
        info .pack (side ="left",fill ="both",expand =True )

        self .title_label =ctk .CTkLabel (
        info ,
        text =title ,
        font =("Consolas",14 ,"bold"),
        text_color =color ,
        anchor ="w"
        )
        self .title_label .pack (anchor ="w")

        self .desc_label =ctk .CTkLabel (
        info ,
        text =description ,
        font =("Consolas",10 ),
        text_color =colors ['text_secondary'],
        anchor ="w"
        )
        self .desc_label .pack (anchor ="w",pady =(2 ,0 ))

        self .action_btn =ctk .CTkButton (
        content ,
        text ="▶",
        width =40 ,
        height =40 ,
        font =("Consolas",16 ,"bold"),
        fg_color =color ,
        hover_color =colors ['primary'],
        text_color =colors ['bg_dark'],
        corner_radius =8 ,
        command =self .on_click 
        )
        self .action_btn .pack (side ="right")

        self .bind ("<Enter>",self .on_hover )
        self .bind ("<Leave>",self .on_leave )
        self .bind ("<Button-1>",lambda e :self .on_click ())

    def on_click (self ):
        if self ._is_processing :
            return 

        if self .command :
            self ._is_processing =True 

            original_color =self .action_btn .cget ("fg_color")
            self .action_btn .configure (fg_color =self .colors ['bg_light'])
            self .configure (border_width =3 )

            try :
                self .command ()
            finally :
                self .after (300 ,lambda :self ._reset_button (original_color ))

    def _reset_button (self ,original_color ):
        try :
            self .action_btn .configure (fg_color =original_color )
            self .configure (border_width =2 )
            self ._is_processing =False 
        except :
            pass 

    def on_hover (self ,e ):
        if not self ._is_processing :
            self .configure (border_width =3 )

    def on_leave (self ,e ):
        if not self ._is_processing :
            self .configure (border_width =2 )

    def update_colors (self ,colors ):
        self .colors =colors 
        self .configure (
        fg_color =colors ['bg_card'],
        border_color =self .color 
        )

        if hasattr (self ,'title_label'):
            self .title_label .configure (text_color =self .color )
        if hasattr (self ,'desc_label'):
            self .desc_label .configure (text_color =colors ['text_secondary'])

        if hasattr (self ,'action_btn'):
            self .action_btn .configure (
            fg_color =self .color ,
            hover_color =colors ['primary'],
            text_color =colors ['bg_dark']
            )


class StatusBar (ctk .CTkFrame ):

    def __init__ (self ,master ,get_status_callback ,colors ,theme ):
        super ().__init__ (
        master ,
        fg_color =colors ['bg_dark'],
        corner_radius =0 ,
        height =50 
        )
        self .pack_propagate (False )
        self .get_status =get_status_callback 
        self .colors =colors 
        self .theme =theme 

        content =ctk .CTkFrame (self ,fg_color ="transparent")
        content .pack (fill ="both",expand =True ,padx =20 )

        self .indicators =ctk .CTkFrame (content ,fg_color ="transparent")
        self .indicators .pack (side ="left",fill ="y")

        self .status_text =ctk .CTkLabel (
        self .indicators ,
        text ="● All systems operational",
        font =("Consolas",10 ,"bold"),
        text_color =colors ['success']
        )
        self .status_text .pack (side ="left",pady =15 )

        self .info_frame =ctk .CTkFrame (content ,fg_color ="transparent")
        self .info_frame .pack (side ="left",fill ="y",padx =20 )

        self .info_text =ctk .CTkLabel (
        self .info_frame ,
        text ="",
        font =("Consolas",9 ),
        text_color =colors ['text_secondary']
        )
        self .info_text .pack (side ="left",pady =15 )

        btn_frame =ctk .CTkFrame (content ,fg_color ="transparent")
        btn_frame .pack (side ="right",fill ="y")

        self .refresh_btn =ctk .CTkButton (
        btn_frame ,
        text ="🔄",
        width =40 ,
        height =30 ,
        font =("Consolas",14 ),
        fg_color =colors ['bg_light'],
        hover_color =colors ['bg_medium'],
        text_color =colors ['primary'],
        corner_radius =6 ,
        command =self .refresh_status 
        )
        self .refresh_btn .pack (side ="left",padx =5 ,pady =10 )

        self .after (3000 ,self .auto_refresh )

    def refresh_status (self ):
        try :
            status =self .get_status ()

            active_modules =[]

            if status .get ('auto_accept',False ):
                active_modules .append ("Auto Accept")

            if status .get ('instalock'):
                active_modules .append (f"Instalock ({status ['instalock']})")

            if status .get ('auto_ban'):
                active_modules .append (f"Auto Ban ({status ['auto_ban']})")

            active_count =len (active_modules )

            if active_count >0 :
                self .status_text .configure (
                text =f"● {active_count } módulo(s) ativo(s)",
                text_color =self .colors ['success']
                )

                details =" | ".join (active_modules )
                self .info_text .configure (text =details )
            else :
                self .status_text .configure (
                text ="● Aguardando ativação",
                text_color =self .colors ['text_secondary']
                )
                self .info_text .configure (text ="Nenhum módulo ativo")

            chat_state =status .get ('chat','unknown')
            if chat_state !='unknown':
                current_info =self .info_text .cget ("text")
                if current_info and current_info !="Nenhum módulo ativo":
                    self .info_text .configure (
                    text =f"{current_info } | Chat: {chat_state }"
                    )

        except Exception as e :
            self .status_text .configure (
            text ="● Erro ao atualizar status",
            text_color =self .colors ['warning']
            )
            self .info_text .configure (text ="")

    def auto_refresh (self ):
        if self .winfo_exists ():
            self .refresh_status ()
            self .after (3000 ,self .auto_refresh )

    def update_colors (self ,colors ):
        self .colors =colors 
        self .configure (fg_color =colors ['bg_dark'])

        if hasattr (self ,'status_text'):
            current_text =self .status_text .cget ("text")
            status_color =colors ['success']if "ativo"in current_text else colors ['text_secondary']
            self .status_text .configure (text_color =status_color )

        if hasattr (self ,'info_text'):
            self .info_text .configure (text_color =colors ['text_secondary'])

        if hasattr (self ,'refresh_btn'):
            self .refresh_btn .configure (
            fg_color =colors ['bg_light'],
            hover_color =colors ['bg_medium'],
            text_color =colors ['primary']
            )