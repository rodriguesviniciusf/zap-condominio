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

Próximas expansões possíveis: assembleias com votações, manutenção preventiva, moradores com memória das decisões e eventos sazonais. O banco inicial contém 12 situações e 48 respostas; eventos são reutilizados ao longo do mandato.
