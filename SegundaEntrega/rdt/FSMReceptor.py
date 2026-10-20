class FSM_Receptor:
  def __init__(self, rdt):
    self.rdt = rdt #RDTSocket usado para enviar os ACKs
    self.estados = {
      "estado_espera_0_baixo": self.estado_espera_0_baixo,
      "estado_espera_1_baixo": self.estado_espera_1_baixo
    }
    self.estado_atual = "estado_espera_0_baixo"

  def transicao(self, evento, pacote=None):
    if evento in ["recebeu_seq0",        #pacote íntegro com seq 0
                  "recebeu_seq1",        #pacote íntegro com seq 1
                  "recebeu_corrompido"
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento, pacote)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_baixo(self, evento, pacote):
    if evento == "recebeu_seq0":
      #CÓDIGO AQUI: extract(pacote), deliver_data, make_pkt(ACK, 0, checksum), udt_send
      return "estado_espera_1_baixo"

    #corrompido ou seq 1:
    #CÓDIGO AQUI: make_pkt(ACK, 1, checksum), udt_send
    return "estado_espera_0_baixo"

  def estado_espera_1_baixo(self, evento, pacote):
    if evento == "recebeu_seq1":
      #CÓDIGO AQUI: extract(pacote), deliver_data, make_pkt(ACK, 1, checksum), udt_send
      return "estado_espera_0_baixo"

    #corrompido ou seq 0:
    #CÓDIGO AQUI: make_pkt(ACK, 0, checksum), udt_send
    return "estado_espera_1_baixo"
