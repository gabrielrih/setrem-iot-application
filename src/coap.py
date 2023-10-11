from db import save_data
from aiocoap import Message, CHANGED
from aiocoap.resource import Resource
from aiocoap.numbers.codes import Code


''' Classe de teste de um GET no protocolo COAP '''
class WhoAmI(Resource):
    async def render_get(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]
        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)
        
        claims = list(request.remote.authenticated_claims)
        if claims:
             text.append("Authenticated claims of the client: %s." % ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")
            
        return Message(content_format=0,
                               payload="\n".join(text).encode('utf8'))

''' Implementação do endpoint "humidity" do protocolo coap
    Recebe dados de temperatura e humidade (separados por espaço) e salva na base de dados (MySQL)
'''
class HumidityResource(Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                         b"with numbers to be large enough to trigger blockwise "
                         b"transfer.\n")

    def set_content(self, content):
        self.content = content

    ''' Método get para pegar o último resultado gravado'''
    async def render_get(self, request):
        return Message(payload=self.content)
    
    ''' Método PUT para receber dados e salvar na database '''
    async def render_put(self, request):
        ''' O payload vem em bytes
            Usamos o decode para converter para string
        '''
        payload=request.payload.decode()
        ''' O payload é composto por temperatura e humidade separados por whitespace
            Exemplo, b'12 50'
            O split é justamente para os valores em duas variáveis diferentes
        '''
        temperature=payload.split(" ")[0]
        humidity=payload.split(" ")[1]
        self.set_content(request.payload)
        ''' Salva na base de dados'''
        save_data(int(temperature),int(humidity))
        return Message(code=Code.CHANGED, payload=self.content)
