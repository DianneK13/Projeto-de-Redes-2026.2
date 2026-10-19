class FSM_Transmissor:
  def __init__(self):
    self.estados = {
      "estado_espera_0_cima": self.estado_espera_0_cima,
      "estado_espera_1_cima": self.estado_espera_1_cima,
      "estado_espera_ACK0": self.estado_espera_ACK0,
      "estado_espera_ACK1": self.estado_espera_ACK1
    }
    self.estado_atual = "estado_espera_0_cima"

  def transicao(self, evento):
    if evento in ["recebeu_dados_0",
                  "recebeu_dados_1",
                  "timeout",
                  "recebeu_ACK0",
                  "recebeu_ACK1"  
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_cima(self, evento):
    if evento == "recebeu_dados_0":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_ACK0"

    return self.estado_atual

  def estado_espera_1_cima(self, evento):
    if evento == "recebeu_dados_1":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_ACK1"

    return self.estado_atual

  def estado_espera_ACK0(self, evento):
    if evento == "timeout":
      #CÓDIGO
      self.estado_atual = "estado_espera_ACK0"

    elif evento == "recebeu_ACK0":
      #CÓDIGO
      self.estado_atual = "estado_espera_1_cima"

    return self.estado_atual

  def estado_espera_ACK1(self, evento):
    if evento == "timeout":
      #CÓDIGO
      self.estado_atual = "estado_espera_ACK1"

    elif evento == "recebeu_ACK1":
      #CÓDIGO
      self.estado_atual = "estado_espera_0_cima"

    return self.estado_atual