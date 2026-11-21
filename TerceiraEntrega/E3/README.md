# E3 – Design de Segmentação (VLANs/DHCP)

- O arquivo [`topologia-E3.pkt`](topologia-E3.pkt) é a topologia da E1 com a rede
  configurada pelo Cisco Packet Tracer.
- Os comandos completos de cada equipamento estão em [`cli/`](cli/) e a senha para
  configurar é `projetocin`.
- O endereçamento foi feito conforme a [E2](../E2/README.md).

## Ideia geral

Os 5 laboratórios compartilham os mesmos switches, mas cada um precisa funcionar como uma rede separada. Para
isso, cada lab recebe uma **VLAN** que foi arquitetada na [E1](../E1/topologia-E1.pkt).

Para um PC de um lab falar com um PC de outro lab (ou com a Internet), o tráfego passa pelo roteador **R-CIN**, que tem
um "pé" (um gateway) em cada VLAN. O R-CIN também é o resposável por distribuir os endereços IP aos PCs por **DHCP**.

Seguem abaixo os requisitos desta E3:

## 1. Lista de VLANs

Honestamente, a tabela abaixo tem praticamente as mesmas informações que a Tabela VLSM apresentada na [E2](../E2/README.md)

| VLAN | Lab   | PCs | Sub-rede (da E2) | Gateway      | IPs que o DHCP entrega        | Switches de acesso |
| ---- | ----- | --- | ---------------- | ------------ | ----------------------------- | ------------------ |
| 10   | Lab 1 | 35  | 172.20.3.0/26    | 172.20.3.1   | 172.20.3.2 até 172.20.3.62    | SW-ACC1, SW-ACC2   |
| 20   | Lab 2 | 30  | 172.20.3.64/26   | 172.20.3.65  | 172.20.3.66 até 172.20.3.126  | SW-ACC2, SW-ACC3   |
| 30   | Lab 3 | 20  | 172.20.3.128/27  | 172.20.3.129 | 172.20.3.130 até 172.20.3.158 | SW-ACC4            |
| 40   | Lab 4 | 20  | 172.20.3.160/27  | 172.20.3.161 | 172.20.3.162 até 172.20.3.190 | SW-ACC5            |
| 50   | Lab 5 | 15  | 172.20.3.192/27  | 172.20.3.193 | 172.20.3.194 até 172.20.3.222 | SW-ACC6            |

Como discutido na entrega anterior, o gateway é sempre o primeiro endereço da rede e, portanto, deve fica fora do DHCP,
para, assim, nenhum PC receber o mesmo IP do roteador.

## 2. Estratégia de DHCP

**Escolha:** os IPs dos PCs são distribuídos por DHCP, e o servidor DHCP é o próprio roteador R-CIN.

**Por que no R-CIN?** O R-CIN já está presente em todas as VLANs (é o gateway de cada uma!). Então o pedido de IP de
qualquer PC chega direto nele, sem configuração extra. Colocar o DHCP no switch core ou num servidor separado exigiria
mais endereços ou mais equipamentos.

**Comandos-chave (no R-CIN):** um _pool_ por lab. O exemplo do Lab 1 está abaixo, e os outros quatro seguem o mesmo
modelo com os valores da tabela. O texto depois de `!` é só explicação; os comandos prontos para colar no CLI dos
equipamentos estão em [`cli/`](cli/).

```
ip dhcp excluded-address 172.20.3.1        ! o gateway não é entregue a nenhum PC
ip dhcp pool LAB1
 network 172.20.3.0 255.255.255.192        ! rede do Lab 1 (/26)
 default-router 172.20.3.1                 ! gateway que o PC vai usar
 dns-server 200.200.200.2                  ! DNS da RNP
```

Cada VLAN tem seu gateway numa subinterface do R-CIN (Gi0/1.10, Gi0/1.20 … Gi0/1.50), todas no mesmo cabo que vai para
o SW-CORE. Por exemplo:

```
interface GigabitEthernet0/1.10
 encapsulation dot1Q 10                     ! esta subinterface atende a VLAN 10
 ip address 172.20.3.1 255.255.255.192
```

## 3. Mapeamento de Portas Trunk e Access

- **Access:** porta ligada a um PC. Pertence a uma única VLAN, a do lab daquele PC.
- **Trunk:** porta ligada a outro switch ou ao roteador. Carrega as 5 VLANs no mesmo cabo, e cada quadro leva uma
  etiqueta (802.1Q) que diz de qual VLAN ele é.

| Equipamento | Porta(s)        | Tipo   | VLAN(s) | Liga em           |
| ----------- | --------------- | ------ | ------- | ----------------- |
| R-CIN       | Gi0/1           | Trunk  | 10 a 50 | SW-CORE           |
| SW-CORE     | Gi0/1           | Trunk  | 10 a 50 | R-CIN             |
| SW-CORE     | Fa0/1 a Fa0/6   | Trunk  | 10 a 50 | SW-ACC1 a SW-ACC6 |
| SW-ACC1 a 6 | Gi0/1           | Trunk  | 10 a 50 | SW-CORE           |
| SW-ACC1     | Fa0/1 a Fa0/24  | Access | 10      | Lab 1 (PCs 1–24)  |
| SW-ACC2     | Fa0/1 a Fa0/11  | Access | 10      | Lab 1 (PCs 25–35) |
| SW-ACC2     | Fa0/12 a Fa0/17 | Access | 20      | Lab 2 (PCs 25–30) |
| SW-ACC3     | Fa0/1 a Fa0/24  | Access | 20      | Lab 2 (PCs 1–24)  |
| SW-ACC4     | Fa0/1 a Fa0/20  | Access | 30      | Lab 3             |
| SW-ACC5     | Fa0/1 a Fa0/20  | Access | 40      | Lab 4             |
| SW-ACC6     | Fa0/1 a Fa0/15  | Access | 50      | Lab 5             |

Todos os trunks carregam as cinco VLANs, então qualquer lab chega ao roteador por qualquer caminho. O SW-ACC2 é o único
switch com duas VLANs: ele recebe os PCs que não couberam no SW-ACC1 (Lab 1) e no SW-ACC3 (Lab 2).

## Testes realizados

### 1. Recebimentos dos endereços:

- _PC do Jhonny do lab 1 pede seu IP por DHCP_ e recebe **172.20.3.37/26** com gateway **172.20.3.1**, conforme o planejado.
- _PC de Macla do lab 5 pede seu IP por DHCP_ e recebe **172.20.3.206/27**, gateway **172.20.3.193**, dentro dos conformes!

### 2. Ping fora do Lab e para a Internet:

- _Ping do PC do Jhonny no Lab 1 para o PC de Macla no Lab 5_ recebeu resposta, então o R-CIN roteia direitinho entre as VLANs.
- _Ping do PC do Jhonny para a internet (o servidor RNP 200.200.200.2)_ recebeu resposta, então a rede alcança a Internet!

Para a resposta da RNP voltar até os labs, o R-CIN avisa à RNP quais redes estão atrás dele (protocolo OSPF, que a RNP
já usava).

## Integrantes

| [<img src="https://avatars3.githubusercontent.com/u/149428254?v=4" width=115 height=115><br><sub>Marcos Alexandre (malb)</sub>](https://github.com/Lysanor) | [<img src="https://avatars3.githubusercontent.com/u/140253955?v=4" width=115 height=115><br><sub>Maria Clara (mcra2)</sub>](https://github.com/DianneK13) | [<img src="https://avatars3.githubusercontent.com/u/204789265?v=4" width=115 height=115><br><sub>Maria Luisa (mlas4)</sub>](https://github.com/airam00N) | [<img src="https://avatars3.githubusercontent.com/u/205706609?v=4" width=115 height=115><br><sub>Vitor Nascimento (vnb)</sub>](https://github.com/vThor27) |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------: |
