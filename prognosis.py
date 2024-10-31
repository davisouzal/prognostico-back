def calcular_pontuacao(encefalopatia, ascite, inr, bilirrubina, albumina):
    pontuacao = 0

    if encefalopatia == 0:
        pontuacao += 1
    elif encefalopatia in [1, 2]:
        pontuacao += 2
    else:
        pontuacao += 3

    if ascite == 0:
        pontuacao += 1
    elif ascite == 1:
        pontuacao += 2
    else:
        pontuacao += 3

    if inr < 1.7:
        pontuacao += 1
    elif 1.7 <= inr <= 2.3:
        pontuacao += 2
    else:
        pontuacao += 3

    if bilirrubina < 2:
        pontuacao += 1
    elif 2 <= bilirrubina <= 3:
        pontuacao += 2
    else:
        pontuacao += 3

    if albumina > 3.5:
        pontuacao += 1
    elif 2.8 <= albumina <= 3.5:
        pontuacao += 2
    else:
        pontuacao += 3

    if 5 <= pontuacao <= 6:
        classe = 'Classe A'
    elif 7 <= pontuacao <= 9:
        classe = 'Classe B'
    else:
        classe = 'Classe C'

    return classe, pontuacao

def obter_prognostico(classe, pontuacao):
    if classe == 'Classe A':
        sobrevida_1_ano = 100
        sobrevida_2_anos = 85
        mortalidade_perioperatoria = 10
        recomendacao = (
            "Recomenda-se monitoramento contínuo, "
            "ajuste de terapias conforme necessário e acompanhamento periódico para manter a condição estável."
        )
    elif classe == 'Classe B':
        sobrevida_1_ano = 81
        sobrevida_2_anos = 57
        mortalidade_perioperatoria = 30
        recomendacao = (
            "É recomendada cautela em decisões cirúrgicas e otimização agressiva do tratamento clínico para melhorar o prognóstico e reduzir complicações."
        )
    else:
        sobrevida_1_ano = 45
        sobrevida_2_anos = 35
        mortalidade_perioperatoria = 10
        recomendacao = (
            "A gestão clínica deve focar em cuidados paliativos "
            "ou intervenções muito cautelosas, evitando cirurgias de grande porte, e uma abordagem centrada na qualidade de vida e no controle dos sintomas é indicada."
        )

    return {
        "classe": classe,
        "pontuacao": pontuacao,
        "sobrevida_1_ano": sobrevida_1_ano,
        "sobrevida_2_anos": sobrevida_2_anos,
        "mortalidade_perioperatoria": mortalidade_perioperatoria,
        "recommendations": recomendacao.format(pontuacao=pontuacao)
    }

def obter_prognostico_humanizado(classe):
    if classe == 'Classe A':
        prognostico = (
            "Com base na sua pontuação, você está na Classe A. Isso significa que suas chances de "
            "sobreviver por mais de um ano são muito boas, cerca de 100%. Além disso, sua chance de viver "
            "por dois anos é em torno de 85%. Caso precise de uma cirurgia abdominal, o risco de complicações "
            "é relativamente baixo, com uma mortalidade de aproximadamente 10%."
        )
    elif classe == 'Classe B':
        prognostico = (
            "Sua pontuação coloca você na Classe B. Isso indica que suas chances de sobreviver por um ano são "
            "em torno de 81%, e há uma chance de 57% de viver por dois anos. O risco de complicações "
            "em uma cirurgia abdominal aumenta um pouco, com uma mortalidade em torno de 30%."
        )
    else:
        prognostico = (
            "Você se encontra na Classe C. Isso significa que suas chances de sobreviver por um ano caem para "
            "cerca de 45%, e para dois anos, em torno de 35%. Caso precise de uma cirurgia abdominal, o risco "
            "ainda permanece significativo, com uma mortalidade de aproximadamente 10%."
        )
    return prognostico