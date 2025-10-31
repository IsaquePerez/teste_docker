# Note que o import de 'pyrfc' foi MOVIDO para dentro da função
from pydantic import BaseModel
from fastapi import HTTPException

# Modelo para receber os dados da requisição
class SAPLogin(BaseModel):
    user: str
    passwd: str
    # Adicione outros parâmetros necessários para sua automação
    # ex: numero_pedido: str

class SAPService:
    def __init__(self):
        # ATENÇÃO: Substitua pelos dados de conexão do seu servidor SAP
        # Você pode mover isso para o .env se preferir
        self.sap_params = {
            'ashost': 'SEU_SERVIDOR_SAP.com', # Servidor de aplicação SAP
            'sysnr': '00',                    # Número do sistema
            'client': '100',                  # Mandante
            'lang': 'PT'
        }

    async def run_sap_automation(self, login_data: SAPLogin):
        """
        Conecta ao SAP usando RFC e executa uma função (BAPI).
        """
        try:
            # Importa o 'pyrfc' somente quando o endpoint é chamado
            from pyrfc import Connection, ABAPApplicationError, CommunicationError
        except ImportError:
            print("ERRO: Módulo 'pyrfc' não instalado.")
            raise HTTPException(
                status_code=501, 
                detail="Integração SAP não instalada. O backend foi buildado sem a flag 'WITH_SAP=true'."
            )

        try:
            # 1. Conecta ao SAP
            print(f"Conectando ao SAP em {self.sap_params['ashost']} com usuário {login_data.user}...")
            conn = Connection(
                user=login_data.user,
                passwd=login_data.passwd,
                **self.sap_params
            )
            print("Conexão SAP estabelecida com sucesso.")

            # 2. Executa a função RFC (BAPI)
            print("Chamando função RFC...")
            result = conn.call(
                "BAPI_USER_GET_DETAIL",
                USERNAME=login_data.user
            )
            
            # 3. Processa o resultado
            print("Função RFC executada.")
            print(f"Resultado (dados do usuário): {result.get('ADDRESS')}")

            # 4. Fecha a conexão
            conn.close()
            
            return {
                "message": "Automação SAP executada com sucesso!",
                "dados_retornados": result.get('ADDRESS')
            }

        except CommunicationError as e:
            print(f"Erro de Comunicação SAP: {e}")
            raise HTTPException(status_code=500, detail=f"Erro de Comunicação SAP: {e}")
        except ABAPApplicationError as e:
            print(f"Erro de Aplicação SAP (ex: login/senha errados): {e}")
            raise HTTPException(status_code=400, detail=f"Erro de Aplicação SAP: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")

