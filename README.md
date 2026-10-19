# Zap do Condomínio · 0.5.0

Simulador de gestão de 365 dias para Android, feito em Python/Kivy.

## Novidades desta versão

- **Investigações:** seis casos especiais roteirizados de segurança, garagem, entregas, barulho e lixo. Surgem aleatoriamente em chamados compatíveis, sem repetir no mandato. Fontes consultadas custam R$ 60 e 2 de paciência; a primeira custa R$ 20 com câmeras. Duas fontes verificadas e conclusão correta rendem +8 de apoio e +4 de paciência. Boato não conta. Acusação incorreta ou sem provas exige retratação de R$ 200, -10 de apoio e -6 de paciência. Arquivar sem acusar custa apenas 2 de paciência. Escolher uma resposta comum encerra a investigação; cobrança sem apuração também exige retratação.
- **Panelinhas:** Liga do Sossego, Turma da Resenha e Fiscalizadores do Pix. Cada resposta altera apoios visíveis. O apoio do grupo influencia a nota de voto dos integrantes em até 6 pontos, junto com confiança e irritação pessoais. Mediação uma vez por dia: R$ 100 e 3 de paciência; +12 para o grupo ouvido e -2 para os outros.
- **Tutorial:** quatro passos na primeira entrada, com opção de pular e rever pelo menu.
- **Preferências:** sons originais curtos, vibração opcional (começa desligada), texto padrão/grande/muito grande e transição entre dias desativável. Preferências salvas separadamente do mandato.
- **Novo ícone original:** prédio e balão de conversa, integrado ao lançador Android e à marca interna.
- Saves da versão 0.4 continuam no mesmo dia, com as mesmas decisões e o mesmo gerador aleatório; novos apoios começam neutros. Saves anteriores também são migrados.

Os quatro sinais sonoros são síntese original em PCM mono, sem samples de terceiros. O ícone foi gerado para o projeto. Vibração depende do hardware e das configurações do Android; falhas de suporte não impedem jogar. O áudio pode ser desligado.

## Recursos anteriores

Simulador cômico de gestão para Android. Sobreviva a 365 dias sem falir, esgotar a paciência ou ser destituído pelos moradores.

## Mandatos aleatórios

O banco contém 365 histórias e 1.460 respostas de base. Cada dia sorteia uma história ainda não usada dentro do tema do mês. Não há uma sequência fixa de abertura. Novo mandato evita repetir o primeiro problema do mandato anterior; Continuar mantém exatamente a ocorrência e o estado do sorteio salvos.

O calendário fictício vai de janeiro a dezembro. As situações estão em eventos.json, com fonte editorial em calendar_content.py e gerador build_events.py. Os arquivos editoriais não entram no APK.

## Moradores e assembleias

Oito moradores têm confiança, irritação e memória da última interação. Conversas e melhorias ajudam; deboche, multas e conselhos ruins desgastam as relações. Esses indicadores entram no voto real de cada morador.

Há assembleias a cada 30 dias. Três dias encerrados com aprovação abaixo de 20% convocam uma assembleia de crise. São necessários cinco votos entre oito moradores para aprovar uma proposta. Se uma proposta for rejeitada na assembleia de crise, o mandato acaba por destituição. A interface mostra o apoio calculado para cada plano e os votos individuais após a decisão.

Uma conversa de reconciliação por dia custa R$ 120, recupera confiança e reduz irritação. O limite diário fica salvo.

## Melhorias e gestão pessoal

- Câmeras HD: R$ 1.500, sem mensalidade; metade dos custos imediatos em segurança e consulta às gravações.
- Portaria remota: R$ 2.400 + R$ 350/mês; solução extra para acessos e delegação mais barata.
- Plano preventivo: R$ 1.800 + R$ 200/mês; reparos mais baratos, menos desgaste e solução técnica extra.
- Reservas digitais: R$ 900 + R$ 80/mês; organização dos espaços e solução pela agenda.

As melhorias acrescentam opções utilizáveis aos eventos das categorias atendidas.

Descansar custa R$ 180 e recupera 14 pontos de paciência, com perda de dois pontos de aprovação. Delegar resolve um chamado comum por R$ 240, ou R$ 160 com portaria remota. Cada ação pode ser usada uma vez por dia; crises de conselheiros exigem decisão própria e não podem ser delegadas.

## Conselheiros e crises

Um conselho seguido pode abrir uma crise três dias depois. O jogador escolhe entre reparo definitivo, negociação e uma segunda gambiarra. Esta última abre uma segunda e última etapa em dois dias. Ignorar o prazo causa reparo emergencial mais caro, perda de paciência e aprovação.

Saves antigos mantêm os efeitos financeiros já contratados, enquanto novas escolhas usam as crises interativas.

## Visual e progresso

O jogo usa arte própria de condomínio e um elenco de 12 retratos ilustrados, interface clara com tons de papel e verde, balões, indicadores e quatro áreas: Grupo, Pautas, Gente e Prédio. As imagens estão em assets/capa.jpg e assets/elenco.jpg.

O progresso é salvo no armazenamento privado do aplicativo. Saves da versão 0.3 são migrados preservando indicadores, melhorias existentes, chamados e consequências. O novo formato também salva relações, votações, ações diárias e estado do gerador aleatório. Novo mandato pede confirmação dentro do jogo.

## Compilar, baixar e verificar

O GitHub Actions testa regras e conteúdo, abre as telas reais em 390×844 e 360×640 e compila um APK debug arm64. As capturas ficam em telas-do-jogo e o APK em ZapCondominio-APK. Baixe o ZIP do artefato e extraia o APK.

A toolchain usa Ubuntu 22.04, Python 3.10, Buildozer 1.5.0, python-for-android v2024.01.21, Cython 0.29.36, Java 17, NDK 25b e API 33. Publicação em loja exige uma etapa própria de assinatura de release e revisão da API alvo.

Para desenvolvimento: instale kivy==2.3.0, execute python main.py e use python -m unittest discover -s tests -v para testar as regras sem Kivy. O teste tests/smoke_ui.py usa Pillow e Xvfb no Linux. Instalação e interação no Android ainda precisam ser testadas no aparelho.
