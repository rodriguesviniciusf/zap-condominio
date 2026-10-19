# Zap do Condomínio

Simulador cômico de gestão para Android: sobreviva a 365 dias sem zerar a paciência ou deixar o caixa negativo.

## Jogar

No Chat, escolha conversar, debochar, multar ou ouvir um dos três Conselheiros do Caos. A resposta encerra o chamado; o botão Encerrar o dia avança o calendário. Adiar deixa uma pendência, que pode ser resolvida na aba Chamados. Cada chamado aberto custa um ponto diário de paciência e aprovação, até 12 pontos por dia.

Os conselhos têm consequências financeiras e sociais três dias depois. Câmeras custam R$ 1.500 e reduzem pela metade o custo imediato das decisões de segurança. A cada 30 dias há receita de taxas, inadimplência ligada à aprovação e despesas fixas. O mandato é salvo automaticamente no armazenamento privado do aplicativo.

## Compilar e baixar

O Actions compila em pushes e pull requests. Abra a execução concluída e baixe o artefato **ZapCondominio-APK**; extraia o ZIP para instalar o APK de teste em um Android arm64 (Android 5 ou superior). O artefato **build-log** contém o diagnóstico da compilação.

A toolchain está fixada em Ubuntu 22.04, Buildozer 1.5.0, python-for-android v2024.01.21, Cython 0.29.36, Java 17 e NDK 25b. A falha anterior acontecia no autogen da libffi com a macro LT_SYS_SYMBOL_USCORE no runner ubuntu-latest. Este é um APK debug para testes; publicação na Play Store precisa de revisão da API alvo, assinatura de release e requisitos vigentes.

## Desenvolvimento

Use Python 3.10 e `pip install kivy==2.3.0`; execute `python main.py`. As regras podem ser verificadas sem Kivy: `python -m unittest discover -s tests -v`.

## Versão 0.3 — um ano de histórias

O calendário fictício vai de janeiro a dezembro, com 365 eventos próprios, 1.460 escolhas e temas mensais. Cada dia abre sua ocorrência; não há sorteio de histórias repetidas. Cada situação oferece diplomacia, deboche, cobrança e um palpite de um dos três conselheiros. Os efeitos futuros continuam chegando após três dias.

`calendar_content.py` contém as 353 novas situações escritas em formato editorial. `build_events.py` preserva os 12 primeiros eventos e materializa o banco completo com `python build_events.py`. Esses dois arquivos ficam fora do APK; o aplicativo lê `eventos.json` diretamente.

O visual usa cartões de conversa, ilustração vetorial, avatares por iniciais, indicadores de paciência e aprovação e uma tela de início. As abas Chat, Chamados e Gestão mostram as decisões, a fila de pendências e o livro de ocorrências. O progresso fica salvo no aparelho; reiniciar exige confirmação no próprio jogo.

Saves da versão anterior mantêm o caixa, os indicadores, as consequências e os chamados antigos. Se o chamado de hoje ainda não foi respondido, ele passa a usar o roteiro do dia correto.

## Verificação visual

O job `interface` do Actions abre as telas reais do Kivy em 390×844 e 360×640, percorre respostas, pendências, compra de câmeras, fim de mandato e diálogo de reinício. As capturas ficam no artefato `telas-do-jogo`. Esse teste de desktop não substitui a instalação no aparelho Android.

As ideias para a próxima etapa estão em [IDEIAS.md](IDEIAS.md).
