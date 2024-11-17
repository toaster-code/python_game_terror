import random
import json

# Configurações do jogo
MAX_ESCOLHAS = 16
MIN_ESCOLHAS = 8
PROBABILIDADES = {
    "ruim": 75,
    "bom": 5,
    "neutro": 20
}
PENALIDADES = [10, 10, 20, 20, 20, 20, 25, 35]  # Penalidades fixas para eventos ruins
BONIFICACOES = [10, 15, 20]  # Bonificações fixas para eventos bons
NPCS = {
    "ruim": ["um vampiro!", "uma múmia!", "um monstro aterrorizante!", "um terrivel lobisomem!", "um bando de morcegos!", "um espectro do mal!", "um bando de zumbis!", "um demônio!"],
    "bom": ["um talismã", "um amuleto mágico", "uma poção revitalizante", "uma estranha pedra brilhante", "um feitiço benigno"],
    "neutro": ["um relógio antigo", "uma pintura que parece te observar", "um grande corredor vazio", "um baú trancado", "um espelho embaçado"]
}

LOCATIONS = [
    "quarto", "caverna", "adega", "biblioteca", "sótão", "corredor", "jardim", "cemitério", "entrada", "salão principal",
    "torre", "cripta", "cozinha abandonada", "galeria de arte", "laboratório antigo", "armazém", "pátio deserto",
    "claustro sombrio", "quintal devastado", "observatório"
]

ITEMS = [
    "teias de aranha", "móveis antigos", "tralhas espalhadas", "um sarcófago assustador", "quadros com olhos que te seguem",
    "um espelho empoeirado", "livros mofados caídos no chão", "uma poça de água escura", "luz fraca vindo de uma fresta",
    "pilhas de ossos", "objetos quebrados", "um altar misterioso", "uma coleção de armas enferrujadas",
    "pássaros empalhados", "um vitral destruído", "goteiras incessantes", "uma estátua sinistra", "uma lareira apagada",
    "uma pilha de cinzas", "uma máquina antiga e enferrujada"
]

EXITS = [
    "uma porta velha", "uma passagem secreta", "uma janela quebrada", "uma escada para o andar superior",
    "uma escada que leva ao porão", "uma abertura no teto", "um corredor sombrio", "uma porta de ferro enferrujada",
    "um alçapão no chão", "uma fenda na parede", "uma brecha entre os móveis", "uma cortina esvoaçante",
    "uma trilha de luz", "uma escadaria majestosa", "uma passagem estreita", "um alçapão escondido",
    "uma porta dupla", "um túnel úmido", "uma porta trancada, mas com rachaduras", "uma passagem para o jardim"
]

positive_phrases = [
    "Você encontrou {npc}. Que sorte! Sua energia aumentou em {ganho}.",
    "Você acaba de achar {npc}! Sua energia foi restaurada em {ganho}.",
    "A sorte sorriu para você, {npc} vai te ajudar na jornada! Energia recuperada: {ganho}.",
    "Você descobriu {npc}, e ganhou {ganho} de energia.",
    "Você viu {npc} que te fez se sentir revigorado! Sua energia aumentou em {ganho}.",
    "Tanta coragem merece um prêmio. Você achou {npc} e recuperou {ganho} de energia."
]

neutral_phrases = [
    "Nada de interessante aconteceu. Sua energia permanece a mesma.",
    "O que você encontrou não teve efeito sobre sua energia.",
    "Você explorou, mas não encontrou nada que impactasse sua energia.",
    "Você deu uma olhada em volta, mas nada mudou. Energia inalterada.",
    "A situação não trouxe grandes mudanças. Sua energia está estável."
]

negative_phrases = [
    "Foi assustador! Você perdeu {perda} de energia.",
    "Um susto terrível! Sua energia caiu em {perda}.",
    "O que você viu foi aterrorizante! Energia perdida: {perda}.",
    "A visão foi horrível! Você perdeu {perda} de energia.",
    "Foi terrível, você arriscou sua vida e perdeu {perda} de energia.",
    "Você recebeu um golpe inesperado! Sua energia foi reduzida em {perda}.",
    "O susto foi forte demais! Você perdeu {perda} de energia.",
    "Você quase desmaiou de tanto medo! Energia perdida: {perda}.",
    "O golpe foi direto! Sua energia caiu em {perda}.",
    "Um choque de terror! Você perdeu {perda} de energia."
]

# Classe para gerenciar o labirinto
class Labirinto:
    def __init__(self):
        self.arvore = self.gerar_labirinto()

    def gerar_labirinto(self):
        caminho = []
        total_passos = random.randint(MIN_ESCOLHAS, MAX_ESCOLHAS)
        for _ in range(total_passos):
            # cada passo, um conjunto de escolhas, onde uma é sempre neutra.
            num_escolhas_extras = random.choice([1]*5 + [2]*3 + [3]*2 + [4])
            escolhas = [self._gerar_evento() for _ in range(num_escolhas_extras)]
            # adiciona escolha neutra
            escolhas.append("neutro")
            # embaralhar as escolhas
            random.shuffle(escolhas)
            # adiciona ao caminho
            caminho.append(escolhas)
        return caminho

    def _gerar_evento(self):
        tipo = random.choices(
            ["ruim", "bom", "neutro"],
            weights=[PROBABILIDADES["ruim"], PROBABILIDADES["bom"], PROBABILIDADES["neutro"]]
        )[0]
        return tipo

    def obter_evento(self, etapa, escolha):
        tipo = self.arvore[etapa][escolha - 1]
        return tipo, random.choice(NPCS[tipo])

    def gerar_texto_evento(self, num_opcoes):
        local = random.choice(LOCATIONS)
        item = random.choice(ITEMS)
        saidas = random.sample(EXITS, k=num_opcoes)
        saidas_texto = "\n".join(f"{i + 1}. {saida}" for i, saida in enumerate(saidas))
        text = f"Você entrou em um {local} cheio de {item}. O lugar parece perigoso. " \
               f"Você encontra algumas opções:\n{saidas_texto}\n"
        return text

    def exibir_arvore_opcoes(self):
        """
        Exibe a árvore de escolhas de maneira hierárquica e legível.
        Cada nível mostra as escolhas possíveis e o tipo de evento associado.

        :param arvore: Lista de listas representando a árvore do labirinto.
                    Cada sublista contém os tipos de eventos ("ruim", "bom", "neutro").
        """
        def formatar_evento(tipo):
            if tipo == "ruim":
                return "[RUIM 🛑]"
            elif tipo == "bom":
                return "[BOM ✨]"
            else:
                return "[NEUTRO ⚪]"

        def mostrar_nivel(nivel, profundidade=0):
            prefixo = "    " * profundidade  # Espaçamento para representar a hierarquia
            for idx, evento in enumerate(nivel, start=1):
                print(f"{prefixo}Escolha {idx}: {formatar_evento(evento)}")

        print("Labirinto\n")
        for i, nivel in enumerate(self.arvore):
            print(f"Nível {i + 1}:")
            mostrar_nivel(nivel, profundidade=i)
            print()


# Classe principal do jogo
class Jogo:
    def __init__(self):
        self.labirinto = Labirinto()
        self.energia = 100
        self.etapa_atual = 0

    def num_choices(self, etapa):
        """Display the choices at the current etapa"""
        return len(self.labirinto.arvore[etapa])

    def introduzir_jogo(self):
        print("Você acorda dentro de uma mansão assombrada.")
        print("Seu objetivo é escapar antes que sua energia acabe!")
        print("Cada passo pode revelar algo inesperado...\n")

    def mostrar_escolhas(self, num_opcoes):
        return self.labirinto.gerar_texto_evento(num_opcoes)

    def processar_escolha(self, escolha):
        tipo, npc = self.labirinto.obter_evento(self.etapa_atual, escolha)
        print(f"Você acabou de encontrar {npc}!")
        if tipo == "ruim":
            perda = random.choice(PENALIDADES)
            self.energia -= perda
            print(random.choice(negative_phrases).format(perda=perda))
        elif tipo == "bom":
            ganho = random.choice(BONIFICACOES)
            self.energia += ganho
            print(random.choice(positive_phrases).format(npc=npc, ganho=ganho))
        else:
            print(random.choice(neutral_phrases))

        self.etapa_atual += 1

    def jogar(self):
        self.introduzir_jogo()
        while self.energia > 0 and self.etapa_atual < len(self.labirinto.arvore):
            num_escolhas = len(self.labirinto.arvore[self.etapa_atual]) #numero de escolhas possiveis na geração do labirinto
            texto_evento = self.mostrar_escolhas(num_escolhas)
            while True:
                print(texto_evento)
                escolha = int(input("Escolha um caminho (digite o número): "))
                if (1 <= escolha <= num_escolhas):
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            self.processar_escolha(escolha)
            print(f"Energia restante: {self.energia}\n")

        if self.energia <= 0:
            print("Sua energia acabou. Você não conseguiu escapar da mansão...")
            if (distancia:=len(self.labirinto.arvore)-self.etapa_atual) <=3:
                print("Você morreu a {distancia} passos do final. Faltou pouco!")
            elif len(self.labirinto.arvore)/2 <= distancia > 3:
                print("Você morreu no meio do caminho. Esperava mais de você. Uma pena...")
            elif len(self.labirinto.arvore)/2 > distancia > len(self.labirinto.arvore)/4:
                print("Você virou comida rapidinho! Deveria ter desistido enquanto podia. Descanse em paz.")
            else:
                print("Uau! Um novo recorde. A morte te levou rapidinho.")


        else:
            print("Você abre a porta e sente o ar fresco da liberdade! Sua escolha levou diretamente à saída da mansão!")
            print("Parabéns! Você escapou da mansão assombrada com vida!")

        print("\nMapa completo do labirinto:")
        self.labirinto.exibir_arvore_opcoes()

    def resetar_jogo(self):
        """Reseta o estado do jogo para uma nova simulação."""
        self.energia = 100
        self.etapa_atual = 0

    def salvar_jogo(self, nome_arquivo):
        estado = {
            "energia": self.energia,
            "etapa_atual": self.etapa_atual,
            "labirinto": self.labirinto.arvore
        }
        with open(nome_arquivo, "w") as f:
            json.dump(estado, f)
        print("Jogo salvo com sucesso!")

    def carregar_jogo(self, nome_arquivo):
        try:
            with open(nome_arquivo, "r") as f:
                estado = json.load(f)
            self.energia = estado["energia"]
            self.etapa_atual = estado["etapa_atual"]
            self.labirinto.arvore = estado["labirinto"]
            print("Jogo carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo de jogo não encontrado.")


# Função para realizar o teste de Monte Carlo com probabilidade de sobrevivência
def monte_carlo_test_with_survival(jogo, num_simulations=1000):
    resultados = {
        "ruim": 0,
        "bom": 0,
        "neutro": 0,
        "sobreviveu": 0,
        "morreu": 0
    }

    for _ in range(num_simulations):
        jogo.resetar_jogo()  # Reset the game for each run
        num_etapas = len(jogo.labirinto.arvore)
        while jogo.energia > 0 and jogo.etapa_atual < num_etapas:
            num_choices = jogo.num_choices(jogo.etapa_atual)
            choice = random.choice(range(num_choices))
            tipo, npc = jogo.labirinto.obter_evento(jogo.etapa_atual, choice)  # Get the first event for simplicity
            if tipo == "ruim":
                perda = random.choice(PENALIDADES)
                jogo.energia -= perda
                resultados["ruim"] += 1
            elif tipo == "bom":
                ganho = random.choice(BONIFICACOES)
                jogo.energia += ganho
                resultados["bom"] += 1
            else:
                resultados["neutro"] += 1

            # passou uma etapa
            if jogo.energia <= 0:
                resultados["morreu"] += 1
                break
            else:
                jogo.etapa_atual +=1

        if jogo.energia > 0:
            resultados["sobreviveu"] += 1

    # Calcular as probabilidades
    probabilidades = {key: (count) for key, count in resultados.items()}

    # Exibir os resultados
    print(f"Resultados de {num_simulations} simulações de Monte Carlo:")
    print(f"Numero médio de eventos 'ruim' por partida: {probabilidades['ruim']/num_simulations:.2f}")
    print(f"Numero médio de eventos 'bom': por partida: {probabilidades['bom']/num_simulations:.2f}")
    print(f"Numero médio de eventos 'neutro': por partida: {probabilidades['neutro']/num_simulations:.2f}")
    print(f"Probabilidade de sobrevivência: {probabilidades['sobreviveu']*100/num_simulations:.2f}%")
    print(f"Probabilidade de morte: {probabilidades['morreu']*100/num_simulations:.2f}%")


# Início do jogo
if __name__ == "__main__":
    jogo = Jogo()
    carregar = input("Deseja carregar um jogo salvo? (s/n): ")
    if carregar.lower() == "s":
        jogo.carregar_jogo("jogo_salvo.json")
        jogo.jogar()
    else:
        print("New game. Shuffling the game...\n")
        while True:
            jogo.jogar()
            print("#####################")
            print("Statistics:\n")
            monte_carlo_test_with_survival(jogo, num_simulations=10000)
            print("#####################")
            replay = input("Deseja jogar novamente? (s/n): ")
            if replay.lower() == "s":
                jogo.resetar_jogo()
            else:
                print("Quit...")
                salvar = input("Deseja salvar o jogo? (s/n): ")
                if salvar.lower() == "s":
                    jogo.salvar_jogo("jogo_salvo.json")
                print("Bye.")
                break

