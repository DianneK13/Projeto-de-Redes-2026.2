# Entrega 1: Transmissão de Arquivos com UDP

### Base de referência

> Baseado no material de "Programação de Sockets", do companion guide de Kurose & Ross [(Lab 2)](https://gaia.cs.umass.edu/kurose_ross/programming/Python_code_only/UDP_Pinger_programming_lab_only.pdf)

O código de comunicação via socket UDP foi adaptado a partir desse material de referência, com a lógica de fragmentação, reconstrução e armazenamento de arquivos implementada para atender aos requisitos deste projeto.

## Instruções de Execução

0. Entre na pasta `Primeira Entrega`:
```bash
   cd Primeira\ Entrega
```

1. Em um terminal, inicie o servidor:
```bash
   python3 UDPServer.py
```
2. Em outro terminal, execute o cliente:
```bash
   python3 UDPClient.py
```
3. O cliente exibe a lista de arquivos disponíveis em `arquivos/memória cliente/` e pede o nome do arquivo a ser enviado. Caso o nome informado não exista na lista, o cliente pede novamente.
4. O arquivo é enviado ao servidor, que o armazena com o prefixo `servidor_` em `arquivos/memória servidor/` e o devolve ao cliente, que o salva com o prefixo `cliente_` em `arquivos/memória cliente/`, confirmando o recebimento.

## Objetivos e como concluímos cada um

### ✔︎ Implementar comunicação Socket:

Criados os sockets UDP (`AF_INET`, `SOCK_DGRAM`) tanto no cliente quanto no servidor. O servidor faz `bind` na porta 12000 e fica em loop aguardando pacotes com `recvfrom`. O cliente envia mensagens com `sendto` e aguarda resposta com `recvfrom`, com timeout configurado para evitar espera indefinida. A comunicação entre os dois foi validada com um teste simples de troca de mensagens no commit [7eaaba7](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/7eaaba7b7dfdfb7399337eb6e76c346672d69e80).

### ✔︎ Gerenciar fragmentação de dados:

Implementadas as funções `enviar()` e `baixar()` (em `funcoes.py`), compartilhadas entre cliente e servidor. `enviar()` lê o arquivo em chunks de 1024 bytes e os envia via `sendto`, finalizando com um pacote vazio para sinalizar o fim da transmissão. `baixar()` recebe os pacotes em loop via `recvfrom`, escreve cada um no arquivo de destino, e para ao identificar o pacote vazio, reconstruindo o arquivo original.

### ✔︎ Trabalhar com tipos de arquivos diferentes:

O suporte a múltiplos tipos foi validado com arquivos `.txt`, `.mp3` e `.png`, disponíveis em `arquivos/memória cliente/`. A função `definir_arquivo_nome()` identifica a extensão do arquivo a partir do nome informado, permitindo que o fluxo de envio/recebimento funcione independentemente do formato.

## Integrantes

| [<img src="https://avatars3.githubusercontent.com/u/149428254?v=4" width=115 height=115><br><sub>Marcos Alexandre (malb)</sub>](https://github.com/Lysanor) | [<img src="https://avatars3.githubusercontent.com/u/140253955?v=4" width=115 height=115><br><sub>Maria Clara (mcra2)</sub>](https://github.com/DianneK13) | [<img src="https://avatars3.githubusercontent.com/u/204789265?v=4" width=115 height=115><br><sub>Maria Luisa (mlas4)</sub>](https://github.com/airam00N) | [<img src="https://avatars3.githubusercontent.com/u/205706609?v=4" width=115 height=115><br><sub>Vitor Nascimento (vnb)</sub>](https://github.com/vThor27) |
| :----------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------: |
