# E1 – Design Físico e Topologia

Arquivo: [`topologia-E1.pkt`](topologia-E1.pkt) (Cisco Packet Tracer 9.0.1), construído sobre `base-projeto-redes-2026-2.pkt`
(infraestrutura RNP/Internet mantida intacta).

## Equipamentos

| Equipamento      | Modelo    | Qtd | Nome(s)                              |
| ---------------- | --------- | --- | ------------------------------------ |
| Roteador         | 2911      | 1   | R-CIN                                |
| Switch core      | 3560-24PS | 1   | SW-CORE                              |
| Switch de acesso | 2960-24TT | 6   | SW-ACC1 … SW-ACC6                    |
| Hosts            | PC-PT     | 120 | L*n*-PC*xx* (35 + 30 + 20 + 20 + 15) |

## Justificativa do número de switches de acesso

- Total de hosts: 35 + 30 + 20 + 20 + 15 = **120**. Cada 2960-24TT tem 24 portas FastEthernet para hosts
  (as 2 portas Gigabit ficam para uplink).
- Com **5 switches** teríamos exatamente 120 portas: nenhuma porta livre, sem margem para falha de porta ou expansão.
- Os labs 1 (35) e 2 (30) passam de 24 hosts, então não cabem em um switch só. Um switch por lab mais um switch extra
  para cada lab grande daria 7 switches, acima do máximo de 6.
- Solução: **6 switches** (144 portas, 24 livres, ou 20 % de folga). As VLANs separam os labs logicamente, então o
  **SW-ACC2** pode ser compartilhado: ele recebe os hosts excedentes do Lab 1 (VLAN 10) e do Lab 2 (VLAN 20).
  Os demais switches atendem um lab cada.

## Mapeamento de portas

| Dispositivo | Porta(s)        | Modo                                 | Destino                 |
| ----------- | --------------- | ------------------------------------ | ----------------------- |
| R-CIN       | Gi0/0           | WAN (2.2.2.2/30)                     | CIN_SUPORTE Gi0/0 (RNP) |
| R-CIN       | Gi0/1           | **Trunk 802.1Q** (router-on-a-stick) | SW-CORE Gi0/1           |
| SW-CORE     | Gi0/1           | **Trunk**                            | R-CIN Gi0/1             |
| SW-CORE     | Fa0/1 – Fa0/6   | **Trunk**                            | SW-ACC1 … SW-ACC6 Gi0/1 |
| SW-ACC1     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/1           |
| SW-ACC1     | Fa0/1 – Fa0/24  | **Access** VLAN 10                   | L1-PC01 … L1-PC24       |
| SW-ACC2     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/2           |
| SW-ACC2     | Fa0/1 – Fa0/11  | **Access** VLAN 10                   | L1-PC25 … L1-PC35       |
| SW-ACC2     | Fa0/12 – Fa0/17 | **Access** VLAN 20                   | L2-PC25 … L2-PC30       |
| SW-ACC3     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/3           |
| SW-ACC3     | Fa0/1 – Fa0/24  | **Access** VLAN 20                   | L2-PC01 … L2-PC24       |
| SW-ACC4     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/4           |
| SW-ACC4     | Fa0/1 – Fa0/20  | **Access** VLAN 30                   | L3-PC01 … L3-PC20       |
| SW-ACC5     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/5           |
| SW-ACC5     | Fa0/1 – Fa0/20  | **Access** VLAN 40                   | L4-PC01 … L4-PC20       |
| SW-ACC6     | Gi0/1           | **Trunk**                            | SW-CORE Fa0/6           |
| SW-ACC6     | Fa0/1 – Fa0/15  | **Access** VLAN 50                   | L5-PC01 … L5-PC15       |

Portas livres: SW-ACC2 Fa0/18-24 (7), SW-ACC4/5 Fa0/21-24 (4 + 4), SW-ACC6 Fa0/16-24 (9), Gi0/2 de cada acesso,
SW-CORE Fa0/7-24 e Gi0/2, R-CIN Gi0/2.

VLANs planejadas: 10 = LAB1 (35), 20 = LAB2 (30), 30 = LAB3 (20), 40 = LAB4 (20), 50 = LAB5 (15).
Todos os trunks transportam as 5 VLANs.

## Cabeamento

- Straight-through: PC–switch e roteador–switch.
- Crossover: switch–switch (core ↔ acesso) e roteador–roteador (R-CIN ↔ CIN_SUPORTE).

## Estado da configuração

Nesta entrega só há o design físico: hostnames, descrições e o IP WAN fixo do enunciado (R-CIN Gi0/0 = 2.2.2.2/30).
VLANs, trunks, subinterfaces e DHCP ficam para E2/E3. Os PCs já estão em modo DHCP.

## Integrantes

| [<img src="https://avatars3.githubusercontent.com/u/149428254?v=4" width=115 height=115><br><sub>Marcos Alexandre (malb)</sub>](https://github.com/Lysanor) | [<img src="https://avatars3.githubusercontent.com/u/140253955?v=4" width=115 height=115><br><sub>Maria Clara (mcra2)</sub>](https://github.com/DianneK13) | [<img src="https://avatars3.githubusercontent.com/u/204789265?v=4" width=115 height=115><br><sub>Maria Luisa (mlas4)</sub>](https://github.com/airam00N) | [<img src="https://avatars3.githubusercontent.com/u/205706609?v=4" width=115 height=115><br><sub>Vitor Nascimento (vnb)</sub>](https://github.com/vThor27) |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------: |
