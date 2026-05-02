class Pessoa:
    def __init__(self, nome, idade, cpf):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf

pf = Pessoa('Henrique', 31, 43572604850)
print(pf.nome)
print(pf.idade)
print(pf.cpf)