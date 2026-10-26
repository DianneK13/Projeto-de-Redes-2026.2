# Entrega 2: Transferência Confiável com RDT 3.0

### Base de referência

> Baseado no modelo RDT 3.0 apresentado na disciplina e no livro Kurose & Ross (capítulo de Princípios da Transferência Confiável de Dados). As máquinas de estados do transmissor e do receptor usadas como guia estão em [`spec/transmissor_rdt3.0.png`](spec/transmissor_rdt3.0.png) e [`spec/receptor_rdt3.0.png`](spec/receptor_rdt3.0.png).

Esta entrega reaproveita a transmissão de arquivos via UDP da Entrega 1. A confiabilidade agora é implementada na camada de aplicação, em cima de um socket UDP, com numeração de sequência, ACKs, timeouts, retransmissões, um canal simulado com perdas e logs detalhados da execução.

## Instruções de Execução

0. Entre na pasta `SegundaEntrega`:
```bash
   cd SegundaEntrega
```

1. Em um terminal, inicie o servidor:
```bash
   python3 FTServer.py
```
2. Em outro terminal, execute o cliente:
```bash
   python3 FTClient.py
```
3. O cliente exibe a lista de arquivos disponíveis em `arquivos/ClientMemory/` e pede o nome do arquivo a ser enviado. Caso o nome informado não exista na lista, o cliente pede novamente. Se apenas `Enter` for pressionado, um arquivo da lista é escolhido aleatoriamente.
4. O arquivo é enviado ao servidor, que o armazena com o prefixo `servidor_` em `arquivos/ServerMemory/` e o devolve ao cliente, que o salva com o prefixo `cliente_` em `arquivos/ClientMemory/`, confirmando o recebimento.
5. Durante todo o processo, cliente e servidor imprimem no terminal os envios, ACKs, timeouts, retransmissões e as perdas e corrupções simuladas pelo canal.

> Só são usadas bibliotecas padrão do Python 3. As probabilidades de perda e de corrupção, o tempo de timeout e o limite de retransmissões podem ser ajustados nas constantes no topo da classe `RDTSocket` (`rdt/RDTSocket.py`).

## Objetivos e como concluímos cada um

### ✔︎ Simular transferência confiável usando o protocolo RDT 3.0 em camada de aplicação:

Criada a classe `RDTSocket` (em `rdt/RDTSocket.py`), que encapsula um socket UDP (`AF_INET`, `SOCK_DGRAM`) e é usada tanto pelo cliente (`FTClient.py`) quanto pelo servidor (`FTServer.py`). O método `rdtSend()` envia um pacote de dados e só avança ao receber o ACK com o número de sequência correspondente, enquanto `rdtRcv()` entrega à aplicação apenas o pacote com o número de sequência esperado e responde com um ACK. O número de sequência alterna entre 0 e 1, seguindo as máquinas de estados do transmissor e do receptor. Cada pacote carrega um cabeçalho de 4 bytes (`!BBH`) com o tipo (dados ou ACK), o número de sequência e um checksum de 16 bits, calculado como soma de palavras de 16 bits em complemento de 1. A implementação completa foi integrada no commit [ca49c70](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/ca49c70584e93f4fc53482c9959a8692354581e6).

### ✔︎ Implementar mecanismos de confiabilidade: ACKs, NAKs, timeouts e retransmissões:

- **ACKs:** o receptor confirma cada pacote correto com um ACK que carrega o mesmo número de sequência.
- **Timeouts e retransmissões:** após cada envio o emissor inicia um timer de `TIMEOUT = 0.1` segundo, controlado com `time.monotonic()` e `settimeout()`. Se o ACK não chega a tempo, o pacote é retransmitido e o timer é reiniciado, até o limite de `MAX_RETRIES = 15` retransmissões, quando o envio é abortado.
- **Pacotes corrompidos e duplicados:** o receptor confere o checksum e o número de sequência. Se o pacote chegou corrompido ou duplicado, ele é descartado e o receptor reenvia o ACK do último pacote recebido corretamente. Esse reenvio faz o papel do NAK, pois o protocolo não usa um tipo de pacote NAK separado. Se o emissor recebe um ACK corrompido ou com número de sequência errado, ele ignora e a retransmissão acontece quando o timer estoura.
- **Nome do arquivo e fim de arquivo:** o nome do arquivo e o pacote vazio que sinaliza o fim da transmissão também passam por `rdtSend()`, então também são confirmados por ACK e retransmitidos em caso de perda.

### ✔︎ Gerenciar perda de pacotes:

O método `udtSend()` simula um canal não confiável. Antes de cada envio, ele sorteia um número com `random.random()` e, com probabilidade `LOSS_PROB = 0.1`, descarta o pacote sem enviá-lo. Com probabilidade `CORRUPT_PROB = 0.1`, inverte os bits de um byte aleatório do pacote, o que faz o checksum falhar no receptor. A simulação vale para pacotes de dados e para ACKs, nos dois lados da comunicação. O gerador foi adicionado no commit [8c843f2](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/8c843f20f69278c81d6ff113e33e553240c6fbd1).

### ✔︎ Manter funcionalidades básicas: envio, armazenamento e devolução de arquivos:

A leitura e a escrita de arquivos ficam em `util/FileReader.py` e `util/FileWriter.py`, separadas da lógica do protocolo no commit [5a8f9f3](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/5a8f9f3243c16edb8c9f01581194765d8ad04405). O cliente (`FTClient`) envia primeiro o nome do arquivo e depois o conteúdo, em blocos de 1020 bytes de dados (1024 bytes do pacote menos os 4 bytes do cabeçalho), finalizando com um pacote vazio. O servidor (`FTServer`) grava o arquivo em `arquivos/ServerMemory/` com o prefixo `servidor_` e o devolve ao cliente pelo mesmo protocolo, e o cliente o salva em `arquivos/ClientMemory/` com o prefixo `cliente_`. Como os arquivos são lidos e escritos em modo binário, a transferência funciona independentemente do formato, e os exemplos disponíveis em `arquivos/ClientMemory/` incluem arquivos `.txt`, `.mp3` e `.png`.

### ✔︎ Garantir transparência operacional:

Cliente e servidor imprimem logs de tudo o que acontece em tempo de execução, identificados pelos prefixos `[envio]`, `[recepção]` e `[canal]`. Eles mostram o envio de cada pacote com número de sequência e tamanho, a chegada de ACKs, os timeouts com a contagem de retransmissões (por exemplo, `1/15`), os pacotes perdidos ou corrompidos pelo canal simulado, os duplicados descartados e o reenvio do último ACK. Um exemplo do formato:

```
[envio] DATA seq=0 (1020 bytes)
[canal] DATA 0 PERDIDO
[envio] TIMEOUT!!!!!!!!!!!!!! seq=0, retransmitindo (1/15)
[envio] ACK 0 chegou.
```

As mensagens de alto nível ficam com os prefixos `(cliente)` e `(servidor)`, e o servidor exibe uma animação enquanto aguarda um cliente. Os logs foram detalhados no commit [7f4e107](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/7f4e10738c636170b03626d335692e228226a577) e a animação de espera foi adicionada no commit [e4471b9](https://github.com/DianneK13/Projeto-de-Redes-2026.2/commit/e4471b9dac232290a5b3da8cc74c3219ac9fb06d).

## Integrantes

| [<img src="https://avatars3.githubusercontent.com/u/149428254?v=4" width=115 height=115><br><sub>Marcos Alexandre (malb)</sub>](https://github.com/Lysanor) | [<img src="https://avatars3.githubusercontent.com/u/140253955?v=4" width=115 height=115><br><sub>Maria Clara (mcra2)</sub>](https://github.com/DianneK13) | [<img src="https://avatars3.githubusercontent.com/u/204789265?v=4" width=115 height=115><br><sub>Maria Luisa (mlas4)</sub>](https://github.com/airam00N) | [<img src="https://avatars3.githubusercontent.com/u/205706609?v=4" width=115 height=115><br><sub>Vitor Nascimento (vnb)</sub>](https://github.com/vThor27) |
| :----------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------: |
