from db import save_data
from aiocoap import Message, CHANGED
from aiocoap.resource import Resource
from aiocoap.numbers.codes import Code


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

class HumidityResource(Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                         b"with numbers to be large enough to trigger blockwise "
                         b"transfer.\n")

    def set_content(self, content):
        self.content = content
        # while len(self.content) <= 1024:
        #     self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return Message(payload=self.content)
    
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        payload=request.payload.decode()
        temperature=payload.split(" ")[0]
        humidity=payload.split(" ")[1]
        self.set_content(request.payload)
        save_data(int(temperature),int(humidity))
        return Message(code=Code.CHANGED, payload=self.content)
    
