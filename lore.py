"""Elenco e parâmetros públicos das mecânicas do condomínio."""
PERFIS = {
    'Dona Cida (101)': dict(retrato=0, papel='Fiscal do corredor', interesse='convivencia', rigor=3),
    'Beto (401)': dict(retrato=1, papel='Pai do cachorro inocente', interesse='lixo', rigor=-4),
    'Lúcia (302)': dict(retrato=2, papel='Guardiã das encomendas', interesse='encomendas', rigor=0),
    'Júnior (203)': dict(retrato=3, papel='Ciclista desconfiado', interesse='seguranca', rigor=2),
    'Patrícia (502)': dict(retrato=4, papel='Rainha das reservas', interesse='convivencia', rigor=4),
    'Gilberto (601)': dict(retrato=5, papel='Embaixador da garagem', interesse='garagem', rigor=1),
    'Nanda (704)': dict(retrato=6, papel='Organizadora das festas', interesse='barulho', rigor=-3),
    'Rogério (805)': dict(retrato=7, papel='Especialista de tutorial', interesse='manutencao', rigor=2),
}
CONSELHEIROS = {
    'Seu Valdir': dict(retrato=8, papel='Autoridade sem fundamento'),
    'Dona Marlene': dict(retrato=9, papel='Toda crise merece uma festa'),
    'Toninho': dict(retrato=10, papel='Oportunidades e prejuízos'),
}
MELHORIAS = {
    'cameras': dict(nome='Câmeras HD', custo=1500, mensal=0, categoria=['seguranca'],
                    resumo='Metade do custo imediato em segurança. Libera consultar gravações.'),
    'portaria': dict(nome='Portaria remota', custo=2400, mensal=350, categoria=['seguranca'],
                    resumo='Libera atendimento de acessos e reduz o preço da delegação.'),
    'manutencao': dict(nome='Plano preventivo', custo=1800, mensal=200, categoria=['manutencao', 'agua'],
                    resumo='Reparos mais baratos, menos desgaste e uma solução técnica extra.'),
    'reservas': dict(nome='Reservas digitais', custo=900, mensal=80, categoria=['convivencia', 'garagem', 'barulho'],
                    resumo='Libera mediação pela agenda e reduz o custo de organizar os espaços.'),
}
PROPOSTAS = {
    'ordinaria': [
        dict(id='transparencia', titulo='Prestação de contas aberta', texto='Publicar despesas e ouvir as unidades.', custo=300, receita=0, paciencia=-4, aprovacao=12, confianca=5, apoio=12),
        dict(id='taxa', titulo='Taxa extra de manutenção', texto='Arrecadar R$ 1.800 para reforçar o caixa.', custo=0, receita=1800, paciencia=-3, aprovacao=-6, confianca=-2, apoio=-9),
        dict(id='mutirao', titulo='Mutirão voluntário organizado', texto='Delegar a organização e recuperar o fôlego.', custo=100, receita=0, paciencia=10, aprovacao=5, confianca=3, apoio=6),
    ],
    'crise': [
        dict(id='recuperacao', titulo='Plano de recuperação', texto='Investir R$ 600 e apresentar correções verificáveis.', custo=600, receita=0, paciencia=-5, aprovacao=20, confianca=10, apoio=32),
        dict(id='reparacao', titulo='Reparação às unidades', texto='Reservar R$ 1.000 para reparar danos e recuperar apoio.', custo=1000, receita=0, paciencia=-3, aprovacao=28, confianca=16, apoio=45),
        dict(id='compromisso', titulo='Compromisso público sem verba', texto='Assumir o desgaste pessoal. Exige confiança prévia dos moradores.', custo=0, receita=0, paciencia=-10, aprovacao=12, confianca=5, apoio=12),
    ],
}
MESES = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
DIAS_MESES = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def calendario(dia):
    resto = dia
    for mes, dias in enumerate(DIAS_MESES, 1):
        if resto <= dias:
            return mes, resto
        resto -= dias
    return 12, 31
