import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from coap import WhoAmI, HumidityResource


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


async def main():
   root = resource.Site()
   root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader))
   ''' whoami: Endpoint utilizado para testes. Obtém um valor qualquer (testar conectividade) '''
   root.add_resource(['whoami'], WhoAmI())
   ''' humidity: Endpoint para enviar dados de temperatura e humidade'''
   root.add_resource(['humidity'], HumidityResource())

   await aiocoap.Context.create_server_context(root)

   ''' Inicia "estuda" de conexões coap '''
   await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
   asyncio.run(main())
