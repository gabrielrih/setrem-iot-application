#- chamar o URL coap:skgsgdgfdpg/temperatura
#- pegar o dados e gravar em variável
#- gravar no banco MySQL

import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from coap import WhoAmI, HumidityResource


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


async def main():
   # Resource tree creation
   root = resource.Site()
   root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader))
   root.add_resource(['whoami'], WhoAmI())
   root.add_resource(['humidity'], HumidityResource())

   await aiocoap.Context.create_server_context(root)

   # Run forever
   await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
   asyncio.run(main())