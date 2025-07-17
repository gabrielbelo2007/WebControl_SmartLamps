# Controle Web de Lâmpadas Inteligentes
### Este repositório contém o código para uma aplicação web simples que permite o controle de lâmpadas inteligentes Intelbras através de uma página HTML, utilizando a integração com a API da Tuya Smart.
> Pode se usar outros modelos de lâmpadas que possuam compatibilidade com a Tuya Inc.

---
## Funcionalidade

- **Controle de Lâmpadas Smart**: Liga e desliga lâmpadas inteligentes (nessa configuração as lâmpadas são ligadas na cor vermelha).
- **Interface Web Simples**: Uma página HTML intuitiva para fácil interação.
- **Integração com Tuya Smart API**: Comunicação com as lâmpadas via API da Tuya.
- **SmartLife**: Funciona através do aplicativo mobile *SmartLife*.

## Tecnologias Utilizadas

- **Backend**: Python com FastAPI
- **Frontend**: HTML, CSS
- **Servidor Web**: Uvicorn (Possibilita testes locais)
- **Variáveis de Ambiente**: python-dotenv

## Como Configurar e Rodar o Projeto

- Pré-requisitos

  - Python 3.x instalado
  - Servidor com suporte para backend em Python
  - Conta de desenvolvedor Tuya Smart
  - Dispositivos compatíveis com Tuya/SmartLife

## Instalação
- Clone o repositório:

```Bash
git clone https://github.com/gabrielbelo2007/webcontrol_smartlamps.git
Navegue até o diretório do projeto:
```

```Bash
cd webcontrol_smartlamps
```

- Crie e ative um ambiente virtual (opcional, mas recomendado):

```Bash
python -m venv lampadas
# No Windows
.\lampadas\Scripts\Activate.ps1
# No macOS/Linux
source lampadas/bin/activate
```

- Instale as dependências:

```Bash
pip install -r requirements.txt
Configuração da API Tuya Smart
Crie um arquivo .env na raiz do projeto com suas credenciais da API Tuya
```

```Python
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_DEVICE_ID=your_device_id
```
> Substitua your_access_id, your_access_secret e your_device_id pelas suas informações.

- Execução Local
  
```Bash

uvicorn main:app --reload
A aplicação estará disponível em http://127.0.0.1:8000.
```

## Uso
Acesse a URL da aplicação no seu navegador (localmente ou após o deploy). A página HTML simples fornecerá os controles para interagir com suas lâmpadas inteligentes.

> **Detalhes da Integração com a API Tuya:**
  A aplicação utiliza a API oficial da Tuya Smart para enviar comandos às lâmpadas. Certifique-se de que seus dispositivos smarts estejam configurados corretamente no aplicativo SmartLife e vinculados à sua conta de desenvolvedor Tuya.

Para mais informações sobre a API da Tuya, consulte a [Documentação Oficial da Tuya Open API](https://developer.tuya.com/en/docs/iot/applying-for-api-group-permissions?id=Ka6vf012u6q76).

