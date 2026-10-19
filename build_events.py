"""Materializa o roteiro revisável em eventos.json; não roda dentro do app."""
import copy
import json
from pathlib import Path
from calendar_content import MONTHS

ROOT = Path(__file__).parent
TITLES = ['Karaokê às duas', 'Fiscal de quatro patas', 'A bicicleta invisível',
          'O primo do porteiro', 'Feira entre andares', 'Churrasqueira do gato',
          'O spa verde', 'Duas vagas e um SUV', 'Assembleia em 47 áudios',
          'Coxinha express', 'A fonte do salão', 'A sogra permanente']
RESIDENTS = ['Dona Cida (101)', 'Beto (401)', 'Lúcia (302)', 'Júnior (203)',
             'Patrícia (502)', 'Gilberto (601)', 'Nanda (704)', 'Rogério (805)']
ADVISORS = ['Seu Valdir', 'Dona Marlene', 'Toninho']
SOLUTIONS = {
    'agua': ('Suspender o uso e corrigir o problema com o responsável.', 'Isso virou parque aquático e esqueceram de avisar?', 'Registrar e multar o uso irregular após apuração.', 'A área foi organizada e o responsável foi avisado.', 'Agora estão perguntando se o pato de borracha paga taxa.'),
    'manutencao': ('Isolar o problema e agendar reparo com profissional.', 'Até o defeito está pedindo férias neste prédio.', 'Apurar a responsabilidade e cobrar o dano registrado.', 'Reparo encaminhado. Vamos acompanhar o prestador.', 'O equipamento ganhou apelido e o síndico ganhou um print.'),
    'seguranca': ('Conferir os registros e corrigir o controle de acesso.', 'Nossa segurança está trabalhando no modo decorativo.', 'Notificar e multar o descumprimento da regra de acesso.', 'Acesso conferido e orientação enviada às unidades.', 'O grupo criou uma figurinha da guarita com olhos fechados.'),
    'barulho': ('Mediar a conversa e combinar um horário permitido.', 'O prédio comprou apartamento e ganhou camarote?', 'Registrar a ocorrência e multar o barulho irregular.', 'Horário combinado. Por enquanto, dá para ouvir os próprios pensamentos.', 'O vizinho disse que vai responder em versão remix.'),
    'garagem': ('Liberar a passagem e organizar o uso com os envolvidos.', 'A garagem virou expansão imobiliária particular?', 'Registrar e multar a ocupação irregular.', 'Passagem liberada e orientação registrada.', 'Já pediram uma vaga para estacionar o sarcasmo do síndico.'),
    'encomendas': ('Conferir com o destinatário e organizar a entrega.', 'A portaria está concorrendo ao prêmio de logística freestyle.', 'Registrar e cobrar o dano de quem usou a entrega indevidamente.', 'Entrega conferida. O protocolo ficou com a portaria.', 'A transportadora não respondeu, mas os prints chegaram pontualmente.'),
    'lixo': ('Organizar a retirada e orientar o descarte correto.', 'A lixeira pediu transferência para outro condomínio.', 'Apurar o descarte e multar o responsável identificado.', 'Retirada combinada. O corredor voltou a parecer corredor.', 'A lixeira virou meme, mas alguém ainda precisa tirar o saco.'),
    'assembleia': ('Publicar as informações e votar com registro em ata.', 'Se opinião gerasse energia, a taxa seria zero.', 'Cobrar formalmente a irregularidade documentada.', 'Encaminhamento registrado em ata e enviado ao grupo.', 'Agora temos uma comissão para discutir o tom da mensagem.'),
    'convivencia': ('Conversar com os envolvidos e aplicar a regra comum.', 'Viver em condomínio é um curso que não emite diploma.', 'Notificar e multar a infração de convivência registrada.', 'Combinado registrado. Cada unidade recebeu a mesma orientação.', 'O grupo sem o síndico ganhou mais três participantes.'),
}
COSTS = {'agua': 80, 'manutencao': 90, 'seguranca': 60, 'barulho': 30,
         'garagem': 40, 'encomendas': 30, 'lixo': 60, 'assembleia': 20, 'convivencia': 40}
AFTERMATH = {
    'agua': 'A brincadeira virou desperdício e deixou uma limpeza extra para pagar.',
    'manutencao': 'A gambiarra precisou ser desfeita antes de chamar um profissional de verdade.',
    'seguranca': 'O plano confundiu o controle de acesso e exigiu revisão dos cadastros.',
    'barulho': 'A resposta virou um evento ainda mais barulhento. Vieram queixas e limpeza extra.',
    'garagem': 'A circulação ficou pior e foi necessário organizar uma retirada emergencial.',
    'encomendas': 'O improviso gerou devoluções, embalagens novas e pedidos de ressarcimento.',
    'lixo': 'O acúmulo ficou maior. A coleta extra não aceitou pagamento em boas intenções.',
    'assembleia': 'O conselho precisou convocar outra reunião e refazer todos os registros.',
    'convivencia': 'A piada virou discussão coletiva, sujeira e uma rodada de reparos.',
}


def build():
    previous = json.loads((ROOT / 'eventos.json').read_text(encoding='utf-8'))
    events = copy.deepcopy(previous[:12])
    for i, event in enumerate(events):
        event.update(titulo=TITLES[i], mes=1, dia_mes=i+1, capitulo=MONTHS[0][1], conselheiro=ADVISORS[i % 3])
        for j, option in enumerate(event['opcoes']):
            option['tipo'] = ['passiva', 'debochada', 'multa', 'conselho'][j]
    for month, (name, chapter, length, rows) in enumerate(MONTHS, 1):
        lines = [line.strip() for line in rows.splitlines() if line.strip()]
        expected = length - 12 if month == 1 else length
        if len(lines) != expected:
            raise ValueError(f'{name}: {len(lines)} ocorrências, esperadas {expected}.')
        for day_month, line in enumerate(lines, 13 if month == 1 else 1):
            category, title, message, advice = [part.strip() for part in line.split('|')]
            day = len(events) + 1
            solutions = SOLUTIONS[category]
            advisor = ADVISORS[(day-1) % 3]
            cost = COSTS[category] + ((day // 7) % 3) * 10
            penalty = 350 + (month * 35) + ((day * 47) % 500)
            event = dict(id=f'dia-{day:03d}', dia=day, mes=month, dia_mes=day_month,
                         capitulo=chapter, titulo=title, categoria=category,
                         remetente=RESIDENTS[(day * 3) % len(RESIDENTS)],
                         mensagem=message, conselheiro=advisor,
                         conselheiro_pitaco=f'{advisor}: {advice}')
            event['opcoes'] = [
                dict(tipo='passiva', texto=solutions[0], paciencia_sindico=-1, caixa_condominio=-cost,
                     aprovacao=3, resposta_morador=f'{title}: {solutions[3]}'),
                dict(tipo='debochada', texto=solutions[1], paciencia_sindico=4, caixa_condominio=0,
                     aprovacao=-6, resposta_morador=f'{title}: {solutions[4]}'),
                dict(tipo='multa', texto=solutions[2], paciencia_sindico=-2, caixa_condominio=150,
                     aprovacao=-4, resposta_morador=f'{title}: cobrança registrada. O responsável pediu acesso às provas antes de recorrer.'),
                dict(tipo='conselho', texto=advice, paciencia_sindico=8, caixa_condominio=-100,
                     aprovacao=-3, resposta_morador=f'{advisor} assumiu o plano de {title.lower()}. O grupo está aplaudindo... por enquanto.',
                     consequencia=dict(texto=f'{title} — {AFTERMATH[category]} Prejuízo: R$ {penalty}.',
                                       caixa=-penalty, paciencia=-12, aprovacao=-10))
            ]
            events.append(event)
    assert len(events) == 365
    assert len({event['mensagem'] for event in events}) == 365
    (ROOT / 'eventos.json').write_text(json.dumps(events, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'{len(events)} eventos / {sum(len(e["opcoes"]) for e in events)} escolhas / 12 meses')


if __name__ == '__main__':
    build()
