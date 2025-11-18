
import json 
import os 
from typing import Dict ,Tuple 
from pathlib import Path 


class ThemeManager :


    DEFAULT_THEMES ={
    "tiamat":{
    "name":"Tiamat",
    "app_name":"TIAMAT",
    "app_icon":"⚡",
    "icon_file":"icons/tiamat.ico",

    "primary":'#B000FF',
    "secondary":'#7A00D4',
    "accent":'#FF00E5',
    "highlight":'#D633FF',
    "focus":'#9F00E6',
    "warning":'#FF0099',
    "info":'#8F4FFF',

    "bg_dark":'#05000A',
    "bg_medium":'#0D0218',
    "bg_light":'#180430',
    "bg_card":'#120326',

    "gradient_primary":"linear-gradient(135deg, #7A00D4, #B000FF)",
    "gradient_accent":"linear-gradient(135deg, #05000A, #180430)",

    "text_primary":'#F0E0FF',
    "text_secondary":'#B88FFF',
    "text_muted":'#7855B3',
    "text_dark":'#0B0015',

    "success":'#C74FFF',
    "danger":'#FF3399',

    "outline":'#1A0430',
    "border_glow":'#B000FF',
    "shadow":'#020005',

    "purple":'#9F00FF',
    "pink":'#FF00E5',
    "white":'#FFFFFF',
    "black":'#000000',
    },
    }

    REQUIRED_BASIC_FIELDS =[
    'name','app_name','app_icon',
    'primary','secondary','accent',
    'bg_dark','bg_medium','bg_light','bg_card',
    'text_primary','text_secondary','text_dark',
    'success','danger'
    ]

    OPTIONAL_FIELDS =[
    'highlight','focus','warning','info',
    'gradient_primary','gradient_accent',
    'text_muted','outline','border_glow','shadow',
    'purple','pink','white','black','icon_file'
    ]

    def __init__ (self ,config_file :str ="theme_config.json",custom_themes_dir :str ="custom_themes"):
        self .config_file =config_file 
        self .custom_themes_dir =custom_themes_dir 
        self .themes =self .DEFAULT_THEMES .copy ()

        os .makedirs (self .custom_themes_dir ,exist_ok =True )

        self .load_custom_themes ()
        self .current_theme =self .load_theme ()

    def load_custom_themes (self ):
        if not os .path .exists (self .custom_themes_dir ):
            return 

        for filename in os .listdir (self .custom_themes_dir ):
            if filename .endswith ('.json'):
                theme_path =os .path .join (self .custom_themes_dir ,filename )
                try :
                    with open (theme_path ,'r',encoding ='utf-8')as f :
                        theme_data =json .load (f )

                    if self .validate_theme (theme_data ):
                        theme_id =filename .replace ('.json','')
                        self .themes [theme_id ]=theme_data 
                        print (f"✅ Tema customizado carregado: {theme_data .get ('name',theme_id )}")
                    else :
                        print (f"⚠️ Tema inválido: {filename }")

                except Exception as e :
                    print (f"❌ Erro ao carregar tema {filename }: {e }")

    def validate_theme (self ,theme_data :Dict )->bool :
        if not isinstance (theme_data ,dict ):
            return False 

        for field in self .REQUIRED_BASIC_FIELDS :
            if field not in theme_data :
                print (f"⚠️ Campo obrigatório ausente: {field }")
                return False 

        color_fields =[
        'primary','secondary','accent',
        'bg_dark','bg_medium','bg_light','bg_card',
        'text_primary','text_secondary','text_dark',
        'success','danger'
        ]

        for field in color_fields :
            color =theme_data .get (field ,'')
            if not self .is_valid_hex_color (color ):
                print (f"⚠️ Cor inválida no campo {field }: {color }")
                return False 

        return True 

    def is_valid_hex_color (self ,color :str )->bool :
        if not isinstance (color ,str ):
            return False 

        color =color .strip ()
        if not color .startswith ('#'):
            return False 

        hex_part =color [1 :]
        if len (hex_part )not in [3 ,6 ]:
            return False 

        try :
            int (hex_part ,16 )
            return True 
        except ValueError :
            return False 

    def import_theme (self ,file_path :str )->Tuple [bool ,str ]:
        try :
            if not os .path .exists (file_path ):
                return False ,"Arquivo não encontrado"

            with open (file_path ,'r',encoding ='utf-8')as f :
                theme_data =json .load (f )

            if not self .validate_theme (theme_data ):
                return False ,"Tema inválido: campos obrigatórios ausentes ou formato incorreto"

            theme_name =theme_data .get ('name','Custom Theme')
            base_id =self .generate_theme_id (theme_name )
            theme_id =base_id 
            counter =1 

            while theme_id in self .themes :
                theme_id =f"{base_id }_{counter }"
                counter +=1 

            custom_theme_path =os .path .join (self .custom_themes_dir ,f"{theme_id }.json")
            with open (custom_theme_path ,'w',encoding ='utf-8')as f :
                json .dump (theme_data ,f ,indent =4 ,ensure_ascii =False )

            self .themes [theme_id ]=theme_data 

            return True ,f"Tema '{theme_name }' importado com sucesso!"

        except json .JSONDecodeError :
            return False ,"Erro ao ler arquivo JSON: formato inválido"
        except Exception as e :
            return False ,f"Erro ao importar tema: {str (e )}"

    def generate_theme_id (self ,theme_name :str )->str :
        theme_id =theme_name .lower ()
        theme_id =''.join (c if c .isalnum ()else '_'for c in theme_id )
        theme_id =theme_id .strip ('_')
        return theme_id or 'custom_theme'

    def delete_custom_theme (self ,theme_id :str )->Tuple [bool ,str ]:
        if theme_id in self .DEFAULT_THEMES :
            return False ,"Não é possível deletar temas padrão do sistema"

        if theme_id not in self .themes :
            return False ,"Tema não encontrado"

        try :
            theme_file =os .path .join (self .custom_themes_dir ,f"{theme_id }.json")
            if os .path .exists (theme_file ):
                os .remove (theme_file )

            del self .themes [theme_id ]

            if self .current_theme ==theme_id :
                self .apply_theme ('tiamat')

            return True ,"Tema deletado com sucesso!"

        except Exception as e :
            return False ,f"Erro ao deletar tema: {str (e )}"

    def load_theme (self )->str :
        if os .path .exists (self .config_file ):
            try :
                with open (self .config_file ,'r',encoding ='utf-8')as f :
                    config =json .load (f )
                    theme =config .get ('theme','tiamat')
                    if theme in self .themes :
                        return theme 
            except :
                pass 
        return 'tiamat'

    def save_theme (self ,theme_name :str )->bool :
        if theme_name not in self .themes :
            return False 

        try :
            with open (self .config_file ,'w',encoding ='utf-8')as f :
                json .dump ({'theme':theme_name },f ,indent =4 )
            self .current_theme =theme_name 
            return True 
        except :
            return False 

    def get_theme (self ,theme_name :str =None )->Dict [str ,str ]:
        if theme_name is None :
            theme_name =self .current_theme 

        return self .themes .get (theme_name ,self .themes ['tiamat']).copy ()

    def get_current_theme (self )->Dict [str ,str ]:
        return self .get_theme (self .current_theme )

    def get_all_themes (self )->list :
        return list (self .themes .keys ())

    def get_theme_names (self )->Dict [str ,str ]:
        return {key :self .themes [key ]['name']for key in self .themes }

    def is_custom_theme (self ,theme_id :str )->bool :
        return theme_id not in self .DEFAULT_THEMES and theme_id in self .themes 

    def apply_theme (self ,theme_name :str )->bool :
        if theme_name not in self .themes :
            return False 
        self .current_theme =theme_name 
        self .save_theme (theme_name )
        return True 