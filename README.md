# setrem-iot-application
Este repositório representa a aplicação responsável por exibir em gráficos os dados coletados dos NodeMCUs (sensores).

A aplicação é composta por:
- API python: receber os dados
- MySQL: Guardar os dados recebidos via API
- Grafana: Exibição dos dados através de Dashboard

## Onde executar?
Inicialmente estamos subindo o recurso via Docker Compose em um servidor local. Porém, da forma que foi estruturado, podemos provisionar esta aplicação em qualquer Kubernets, seja ele na nuvem ou não.
