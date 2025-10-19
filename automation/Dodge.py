from core import Rengar

def dodge():
    """Executa o dodge da fila"""
    try:
        rengar = Rengar()
        
        # Endpoint correto para fazer dodge
        response = rengar.lcu_request(
            "POST",
            "/lol-matchmaking/v1/ready-check/decline",
            ""
        )
        
        if response.status_code in [200, 204]:
            print("✅ Dodge executado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao fazer dodge: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar dodge: {e}")
        return False
