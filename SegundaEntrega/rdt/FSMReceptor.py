class FSM_Receptor:
  def __init__(self):
    self.estados = {
      "estado_espera_0_baixo": self.estado_espera_0_baixo,
      "estado_espera_1_baixo": self.estado_espera_1_baixo
    }
    self.estado_atual = "estado_espera_0_baixo"

  def transicao(self, evento):
    if evento in ["recebeu_0_corretamente",
                  "recebeu_1_corretamente",
                  "corrompido_ou_0_errado",  #estava esperando 1, veio 0
                  "corrompido_ou_1_errado"   #estava esperando 0, veio 1
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_baixo(self, evento):
    if evento == "recebeu_0_corretamente":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_1_baixo"

    elif evento == "corrompido_ou_1_errado":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_0_baixo"

    return self.estado_atual

  def estado_espera_1_baixo(self, evento):
    if evento == "recebeu_1_corretamente":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_0_baixo"

    elif evento == "corrompido_ou_0_errado":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_1_baixo"

    return self.estado_atual