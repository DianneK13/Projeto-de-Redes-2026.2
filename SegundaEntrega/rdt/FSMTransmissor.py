class FSM_Transmissor:
  def __init__(self, rdt):
    self.rdt = rdt #RDTSocket usado para enviar os pacotes
    self.estados = {
      "estado_espera_0_cima": self.estado_espera_0_cima,
      "estado_espera_1_cima": self.estado_espera_1_cima,
      "estado_espera_ACK0": self.estado_espera_ACK0,
      "estado_espera_ACK1": self.estado_espera_ACK1
    }
    self.estado_atual = "estado_espera_0_cima"

  def transicao(self, evento, dados=None):
    if evento in ["rdt_send",           #camada de cima pediu envio (seq definido pelo estado)
                  "timeout",
                  "recebeu_ACK0",
                  "recebeu_ACK1",
                  "recebeu_corrompido"
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento, dados)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_cima(self, evento, dados):
    if evento == "rdt_send":
      #CÓDIGO AQUI: make_pkt(0, dados, checksum), udt_send, start_timer
      return "estado_espera_ACK0"

    #rdt_rcv: Λ
    return "estado_espera_0_cima"

  def estado_espera_1_cima(self, evento, dados):
    if evento == "rdt_send":
      #CÓDIGO AQUI: make_pkt(1, dados, checksum), udt_send, start_timer
      return "estado_espera_ACK1"

    #rdt_rcv: Λ
    return "estado_espera_1_cima"

  def estado_espera_ACK0(self, evento, dados):
    if evento == "timeout":
      #CÓDIGO AQUI: udt_send(sndpkt), start_timer
      return "estado_espera_ACK0"

    if evento == "recebeu_ACK0":
      #CÓDIGO AQUI: stop_timer
      return "estado_espera_1_cima"

    #corrompido ou ACK1: Λ
    return "estado_espera_ACK0"

  def estado_espera_ACK1(self, evento, dados):
    if evento == "timeout":
      #CÓDIGO AQUI: udt_send(sndpkt), start_timer
      return "estado_espera_ACK1"

    if evento == "recebeu_ACK1":
      #CÓDIGO AQUI: stop_timer
      return "estado_espera_0_cima"

    #corrompido ou ACK0: Λ
    return "estado_espera_ACK1"
