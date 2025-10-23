# app/errors.py

class InvalidAPIUsage(Exception):
    """
    Classe de erro personalizada para ser usada em toda a API.

    Quando esta exceção é levantada, o manipulador de erros
    registrado no Blueprint irá capturá-la e formatar uma
    resposta JSON padronizada.

    Uso:
    raise InvalidAPIUsage("O campo 'name' está faltando", status_code=400)

    Argumentos:
        message (str): A mensagem de erro para o usuário.
        status_code (int): O código de status HTTP (padrão 400).
        payload (dict, opcional): Um dicionário de detalhes extras
                                   para incluir na resposta.
    """
    status_code = 400  # Padrão é Bad Request

    def __init__(self, message, status_code=None, payload=None):
        # Chama o __init__ da classe pai (Exception)
        super().__init__(message) 
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload # 'payload' pode ser um dict com mais detalhes

    def to_dict(self):
        """
        Converte a exceção em um dicionário para a resposta JSON.
        """
        # Inicia o dicionário com o payload, se houver
        rv = dict(self.payload or ())
        # Adiciona a mensagem de erro
        rv['message'] = self.message
        return rv