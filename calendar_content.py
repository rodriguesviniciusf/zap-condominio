"""Roteiro editorial: cada linha descreve uma ocorrência própria do mandato.

Formato: categoria | assunto | mensagem | pitaco do conselho.
Os primeiros 12 dias são preservados em build_events.py.
"""
MONTHS = [
    ('Janeiro', 'Bem-vindo ao grupo', 31, '''
agua|A ducha gourmet|Instalaram uma ducha na garagem usando a mangueira do jardim. Agora tem fila de shampoo.|Cobra por espuma e chama de lava-morador.
garagem|Vaga de verão|O 603 deixou uma piscina inflável na vaga de visitante e colocou placa de profundidade.|Transforma as vagas restantes em camarotes molhados.
encomendas|Sorvete derretido|Entregaram sete caixas de picolé na portaria. A geladeira só cabe a marmita do zelador.|Distribui como sopa gelada de boas-vindas.
barulho|A aula de zumba|O terraço virou academia às seis da manhã. O instrutor usa o megafone da brigada.|Convida o prédio inteiro para sapatear em resposta.
convivencia|Varal diplomático|O varal do 201 atravessou a janela do 202. Uma cueca bloqueou a vista da sala.|Institui pedágio aéreo por peça íntima.
manutencao|Ventilador viajante|O ventilador do salão anda sozinho quando liga. Já chegou perto da mesa do conselho.|Coloca crachá e contrata como segurança móvel.
seguranca|Biometria de areia|A leitora da entrada não reconhece os moradores que voltam da praia. O chinelo entrou antes do dono.|Cadastra a sola do chinelo como documento oficial.
assembleia|Ata sem assinatura|A ata da posse só tem o desenho de um coração e a palavra boa sorte.|Completa as assinaturas com apelidos do grupo.
lixo|Casca premiada|Alguém colocou cascas de melancia no elevador para não pesar o saco. O elevador virou salada.|Faz uma feira de frutas de segunda viagem.
convivencia|Protetor solar comunitário|O 105 quer descontar o protetor solar da taxa porque emprestou na piscina.|Cria um imposto sobre bronzeado.
barulho|O grilo eletrônico|Um alarme de brinquedo imita grilo no corredor. Ninguém acha o dono e já acusaram o jardim.|Solta áudios de sapo em todas as caixas de som.
manutencao|A torneira famosa|A torneira do hall pinga no ritmo de uma música. Os moradores começaram a gravar vídeos.|Contrata empresário para o encanamento.
garagem|Barraca no subsolo|O adolescente do 701 está acampando entre duas motos porque o quarto está quente.|Anuncia o subsolo como camping com vista para o escapamento.
agua|O hidrômetro atleta|O hidrômetro gira mesmo com tudo fechado. O 302 disse que é para manter a forma.|Patrocina o aparelho em nome do condomínio.
encomendas|Óculos idênticos|Chegaram doze óculos escuros iguais sem apartamento. Todo mundo reconheceu o mais caro como seu.|Faz um desfile e entrega ao morador mais misterioso.
seguranca|O visitante tatuado|Um entregador mostrou uma tatuagem de chave e pediu para passar. Disseram que parecia convincente.|Tatua um portão no braço do zelador.
convivencia|Cadeira cativa|Dona Cida colocou uma toalha na espreguiçadeira há cinco dias e exige usucapião da sombra.|Cerca a cadeira com fita de inauguração.
assembleia|Orçamento de janeiro|A primeira prestação de contas tem mais opiniões sobre a fonte da planilha do que sobre os gastos.|Apresenta o saldo em letra invisível para ninguém reclamar.
manutencao|O toldo turista|O toldo do salão soltou uma ponta e agora aponta para a praia. Precisamos prender antes da ventania.|Amarra nele uma faixa de excursão e vende passagem.
'''),
    ('Fevereiro', 'Bloco dos inadimplentes', 28, '''
barulho|Ensaio de bloco|O bloco Unidos do Bloco B ensaia na escada. A caixa do surdo faz o sensor de presença piscar.|Coloca o sensor para marcar o compasso.
convivencia|Confete no filtro|Usaram a piscina como pista de Carnaval. O filtro está cuspindo estrelinhas douradas.|Vende o glitter filtrado como água premium.
seguranca|O mascarado do 402|Entrou um homem de fantasia dizendo ser o 402. O verdadeiro 402 está na Bahia e mandou foto.|Pede para ele sambar a senha do Wi-Fi.
lixo|Serpentina infinita|A coleta recusou um saco que desenrola serpentina até a esquina. Ninguém sabe onde termina.|Puxa até descobrir qual apartamento ganha o prêmio.
garagem|Carro alegórico|O 504 decorou o carro com uma asa de papelão. Agora ele ocupa a faixa de circulação.|Declara a garagem avenida oficial do desfile.
assembleia|Rainha da bateria|Três moradores disputam o título de rainha do bloco e todos querem verba para a faixa.|Cria três coroas e cobra taxa de reinado.
encomendas|A fantasia errada|A portaria entregou uma fantasia de pavão ao morador que esperava uma furadeira.|Convence o pavão a fazer os reparos de bico.
barulho|Apito de emergência|O apito do salva-vidas virou instrumento de ensaio. Agora ninguém sabe qual sinal vale.|Distribui vuvuzelas para diferenciar as emergências.
manutencao|Elevador purpurinado|A porta do elevador não fecha por causa de uma camada de purpurina. O técnico já está brilhando.|Promove o técnico a destaque do desfile.
convivencia|O abadá obrigatório|O conselho quer obrigar todos a comprar abadá para entrar no próprio salão.|Faz uma catraca de abraços pagos.
agua|A guerra das bisnagas|Crianças estão enchendo pistolas de água na torneira da limpeza. A faxina ficou sem mangueira.|Convoca adultos para a guerra e cobra munição.
seguranca|A senha do camarote|Vazaram a senha do portão junto com o convite do bloquinho. Tem turista procurando o camarote.|Pinta camarote na guarita e deixa a fila crescer.
lixo|Confete de boleto|Picotaram boletos para fazer confete. Agora todos dizem que a dívida desapareceu.|Apaga a planilha com borracha de carnaval.
convivencia|Romance na portaria|O 201 mandou flores para o 202 e a portaria anunciou no grupo errado. Já tem enquete de casal.|Vende patrocínio para a novela do corredor.
barulho|A marcha fúnebre|O bloco desafinado decidiu ensaiar marchinha em ritmo de velório. A síndica anterior ligou preocupada.|Faz cortejo oficial da paciência perdida.
garagem|O recuo VIP|Um morador cobra para guardar cadeiras na rampa da garagem durante o desfile da rua.|Cobra comissão e chama a rampa de lounge.
encomendas|Espuma extraviada|Chegaram caixas de espuma de festa no lugar do detergente. O zelador já abriu uma.|Batiza a faxina de pool party seca.
manutencao|O ventilador de penas|As penas das fantasias entupiram a grade do ventilador do salão. Parece uma galinha elétrica.|Coloca nome no bicho e abre visitação.
assembleia|Quórum fantasiado|Um morador trouxe cinco máscaras para representar cinco apartamentos na reunião.|Conta cada máscara como voto de confiança.
agua|Banho de mangueira|O bloco quer usar a mangueira de incêndio para refrescar os foliões. A brigada proibiu.|Desenha uma praia na parede para compensar.
convivencia|O passista do silêncio|O 303 promete dançar sem som, mas o sapato faz mais barulho que a bateria.|Ensaia com ele no teto do reclamante.
seguranca|A comissão de frente|Os convidados ficaram na entrada encenando uma comissão de frente. A fila bloqueou a calçada.|Julga a coreografia antes de liberar qualquer um.
lixo|A ressaca do salão|Sobrou um saco de confete molhado do tamanho de um sofá. A limpeza pediu reforço.|Molda o saco como poltrona e recoloca no salão.
garagem|Alegoria sem rodas|O carro alegórico virou depósito e perdeu as rodas. O dono diz que agora é escultura.|Inscreve a escultura no patrimônio do prédio.
barulho|Cinzas com tamborim|Acabou o Carnaval, mas o 402 está treinando um último solo desde ontem.|Anuncia prorrogação do feriado até ele cansar.
manutencao|O corrimão pegajoso|O corrimão está coberto de cola de fantasia. A escada segura os moradores pelo braço.|Cobra ingresso pela experiência de escalada.
assembleia|A nota da festa|A prestação do Carnaval inclui uma compra chamada alegria, sem recibo ou fornecedor.|Emite recibo assinado pelo Rei Momo.
convivencia|O bloco de desculpas|Todos querem postar desculpas ao mesmo tempo e o grupo travou com áudios de vinte minutos.|Exige desculpa cantada com acompanhamento de pandeiro.
'''),
    ('Março', 'A república das obras', 31, '''
manutencao|A furadeira pontual|O 702 liga a furadeira exatamente na primeira colherada do almoço. Deve existir um sensor de fome.|Distribui marmita para acompanhar a obra.
barulho|O martelo misterioso|O barulho vem da parede do 301, mas o apartamento está vazio. Já falaram em fantasma pedreiro.|Contrata o fantasma para terminar a pintura.
garagem|Areia de estacionamento|Descarregaram areia na vaga 14. O dono do carro só achou a antena.|Declara o carro achado arqueológico.
lixo|Entulho com etiqueta|Deixaram tijolos na coleta seletiva com a etiqueta vidro emocionalmente rígido.|Cria a lixeira de materiais temperamentais.
seguranca|O crachá de papel|O ajudante entrou com um crachá desenhado em guardanapo. O nome do síndico está escrito errado.|Carimba o guardanapo com molho de tomate.
convivencia|A varanda amarela|O 104 pintou a varanda de amarelo marca-texto. Agora o prédio parece um documento grifado.|Pinta setas apontando para as outras varandas.
manutencao|O azulejo musical|Um piso do hall faz barulho quando pisa. O zelador já tocou parabéns nele.|Monta um piano de pisos no corredor.
encomendas|Cimento no delivery|A portaria confundiu sacos de cimento com compras do mercado. O 304 recebeu cinquenta quilos.|Sugere pão de concreto na dieta do morador.
assembleia|O orçamento em áudio|O empreiteiro enviou orçamento em sete áudios, com os valores só no último e música ao fundo.|Aprova por aplausômetro dos áudios.
agua|Reforma molhada|A obra do 602 atingiu um cano. O vizinho de baixo está recebendo água pela luminária.|Chama a luminária de lustre cascata.
barulho|O corte de domingo|A serra elétrica começou no domingo. O dono disse que o material não conhece calendário.|Entrega um calendário para cada ferramenta.
garagem|O cone hereditário|O pedreiro guardou uma vaga com um cone e agora o filho dele também usa a vaga.|Emite certidão de nascimento para o cone.
convivencia|A poeira seletiva|O 501 garante que sua poeira é premium porque veio de porcelanato importado.|Cobra mais caro para respirar no quinto andar.
manutencao|Porta ao contrário|Reinstalaram a porta do salão abrindo para o lado errado. A maçaneta ficou dentro do armário.|Transforma o armário na entrada oficial.
seguranca|A escada estrangeira|Uma escada enorme apareceu na lateral do prédio. Ninguém conhece a obra que está usando.|Cobra aluguel por degrau ocupado.
lixo|O vaso aposentado|Um vaso sanitário abandonado no jardim ganhou flores. O morador exige que vire paisagismo.|Inaugura o jardim imperial do trono.
encomendas|A tinta sem dono|Chegaram vinte latas de tinta com a descrição surpresa. Todas as unidades negaram a compra.|Mistura tudo e pinta o nome do condomínio.
barulho|O piso experimental|O 802 testa o piso novo pulando de sapato. Já estamos no teste número oitenta.|Convoca uma equipe de sapateado para homologar.
manutencao|O interfone decorativo|A reforma cobriu o interfone com massa. Agora só funciona por telepatia, segundo o pintor.|Contrata um médium como ramal central.
assembleia|A comissão da cor|A comissão reduziu a escolha da fachada a quarenta tons de bege. Marcou reunião para cada tom.|Vota usando feijão como amostra de cor.
agua|O registro invertido|Trocaram as plaquinhas dos registros. Para fechar o salão é preciso abrir a churrasqueira.|Faz um mapa do tesouro para achar a água.
garagem|Elevador de carrinho|O carrinho de obra ficou preso na rampa com um monte de argamassa. Ninguém passa com compras.|Anuncia uma pista de obstáculos exclusiva.
convivencia|A planta clandestina|O 401 desenhou uma nova parede na planta usando canetinha e chamou de projeto executivo.|Aprova desde que use canetinha dourada.
seguranca|O capacete VIP|O conselho quer liberar qualquer pessoa de capacete para agilizar a reforma.|Distribui capacetes para todo visitante da rua.
manutencao|Rodapé de macarrão|O fornecedor entregou peças curvas e a instalação ficou ondulada. O hall parece lasanha.|Chama de arquitetura gastronômica e cobra visita.
lixo|O saco sem fundo|Um saco de entulho rasgou em todos os andares da escada. A trilha termina no 903.|Segue a trilha cobrando pedágio por pedra.
barulho|O teste do eco|O mestre de obras bate palmas para avaliar a acústica. Agora os moradores aplaudem o fim de cada batida.|Marca um festival de palmas sem intervalo.
encomendas|Granito de presente|A bancada de uma unidade chegou com um laço de presente e foi para a sala de festas.|Usa como bolo cenográfico de aniversário.
convivencia|A obra eterna|O 301 pediu mais dois dias pela décima vez. A reforma já tem aniversário próprio.|Compra velas e cobra cota de festa da obra.
assembleia|A vistoria criativa|O relatório da vistoria diz parece bom em todas as linhas. O rodapé é um emoji desenhado.|Substitui o laudo por uma enquete de beleza.
manutencao|A placa inaugural|Terminaram a reforma, mas a placa agradece ao síndico errado. O homenageado veio posar.|Faz duas inaugurações e cobra buffet dobrado.
'''),
    ('Abril', 'Nem todo print é prova', 30, '''
convivencia|Primeiro de abril|Postaram que a taxa vai triplicar e o 201 já anunciou a mudança. Era brincadeira do conselho.|Mantém a notícia até passar a assembleia.
seguranca|O print recortado|Um print acusa o porteiro de dormir, mas cortaram a parte que mostra a folga dele.|Proíbe fotos com mais de quatro cantos.
encomendas|O ovo gigante|Chegou um ovo de chocolate maior que o armário da portaria. Ninguém quer ajudar sem degustar.|Abre o ovo e desconta a degustação do frete.
lixo|Papel dourado|A coleta ficou cheia de embalagens metalizadas de chocolate. Um morador jurou que era ouro.|Paga a conta de luz com papel de bombom.
barulho|O coelho sonoro|Uma decoração de Páscoa toca música a cada movimento. O gato passou a noite ativando o coelho.|Coloca a decoração na frente do elevador.
convivencia|Caça ao ovo|Esconderam ovos atrás de equipamentos do condomínio. As crianças pedem chave da casa de máquinas.|Faz o prêmio final ser o livro de ocorrências.
assembleia|Ata adulterada|A ata compartilhada diz que o 302 ganhou vaga extra. A fonte muda justamente nessa frase.|Corrige distribuindo uma vaga imaginária para cada um.
agua|O filtro milagroso|O 603 vende um filtro que promete purificar a água com pensamento positivo. Quer instalar no reservatório.|Convoca meditação coletiva antes de abrir a torneira.
seguranca|Entrega por reconhecimento|Liberaram a entrada porque o visitante parecia o ator da novela. Ele veio vender antena.|Convida o vendedor para gravar a abertura do prédio.
manutencao|O QR do elevador|Colaram um QR de enquete sobre o elevador em cima do botão de emergência.|Faz a emergência depender da enquete atingir cem votos.
garagem|Placa de empréstimo|Um morador emprestou a placa de sua vaga para o primo. O primo trouxe uma van.|Divide a van em vagas menores na planilha.
barulho|O podcast de varanda|O 805 grava um podcast sobre silêncio usando três microfones na varanda.|Responde com um podcast sobre vizinhos inconvenientes.
convivencia|O grupo paralelo|Descobriram um grupo chamado Síndico Oficial 2. O administrador é o liquidificador do 401.|Nomeia a air fryer para auditar o grupo.
encomendas|Senha de chocolate|A transportadora pede uma senha que veio escrita no bombom. O destinatário comeu o papel.|Pede para ele assobiar o sabor da senha.
seguranca|O vídeo antigo|Um vídeo de invasão de outro prédio foi postado como se fosse nosso. Até a fachada é diferente.|Pinta a fachada para combinar com a notícia.
lixo|A compostagem de sofá|Colocaram espuma de sofá na composteira porque parecia macia para as minhocas.|Compra almofadas para as minhocas trabalharem sentadas.
assembleia|Voto por figurinha|Mandaram aprovar o orçamento com figurinha verde, mas cada celular mostra uma cor diferente.|Aceita qualquer figurinha com animal sorrindo.
agua|A piscina photoshopada|O anúncio de aluguel mostra uma piscina olímpica. A nossa tem oito metros e um pato de borracha.|Compra mais patos para melhorar a perspectiva.
manutencao|Manual do vizinho|O 202 fez um tutorial de conserto sem ser técnico. Agora três interfones só chiam.|Transforma o chiado em rádio comunitária.
garagem|O radar de papel|O conselho instalou uma caixa de sapato dizendo que é radar. Um morador pediu aferição.|Escreve aferido com carimbo de brinquedo.
convivencia|O feriado estendido|O 701 reservou o salão por toda a semana alegando que emendou o feriado com as férias de 2028.|Cria o feriadão permanente do sétimo andar.
barulho|O alarme da live|A live do 502 dispara o alarme de doação em volume máximo. O público descobriu e está doando centavos.|Doa um centavo a cada reclamação.
encomendas|O pacote transparente|Entregaram um pacote transparente que virou assunto de todo mundo. O destinatário pediu discrição.|Faz uma votação pública sobre a melhor embalagem.
seguranca|O uniforme genérico|Um homem com camiseta azul disse ser da manutenção. Não soube dizer de quê.|Empresta uma ferramenta para ele descobrir a profissão.
assembleia|O relatório viral|A planilha de gastos virou meme porque uma coluna se chama dinheiro que sumiu. Era desconto.|Muda o nome de todas as colunas para mistério.
lixo|Reciclagem de fofoca|O 301 colocou o mural impresso na lixeira orgânica porque disse que tinha muita mentira podre.|Cria uma coleta especial para notícia vencida.
convivencia|O selo de verificado|Dona Cida quer um selo azul no nome para suas reclamações valerem mais.|Vende selo dourado para os áudios acima de dez minutos.
manutencao|O técnico holograma|O técnico fez a vistoria por chamada de vídeo e só enxergou o teto. Mandou orçamento mesmo assim.|Projeta o orçamento no teto e considera aprovado.
garagem|A vaga no anúncio|O anúncio do 601 oferece três vagas. O apartamento só tem uma e muita autoestima.|Desenha duas vagas no folheto para completar.
assembleia|A retratação|O conselho quer apagar todas as mensagens do mês para zerar as provas das confusões.|Troca o nome do grupo e declara anistia digital.
'''),
    ('Maio', 'A paz está em manutenção', 31, '''
convivencia|O café do trabalhador|O zelador ganhou café de seis apartamentos, mas todos querem prioridade no serviço em troca.|Cria cartão fidelidade de favor com carimbo de café.
manutencao|Ferramenta de estimação|A furadeira comunitária sumiu e reapareceu com o nome Robson escrito no cabo.|Exige pensão alimentícia de quem adotou a furadeira.
garagem|A vaga de bicicleta|O 204 colocou uma bicicleta atravessada em três suportes para guardar lugar para os amigos.|Reserva o resto com desenhos de bicicletas.
agua|A conta encorpada|A conta de água veio alta. O conselho quer saber se o cafezinho do zelador foi o responsável.|Troca todos os cafés por vapor de chaleira.
barulho|A serenata ensaiada|O 501 está ensaiando serenata para domingo. O destinatário mora em outro bairro.|Transmite a serenata pelo interfone de todas as unidades.
encomendas|Flores em atacado|A portaria recebeu tantos buquês que o livro de visitantes está escondido entre rosas.|Cobra taxa de polinização por entrega.
convivencia|O almoço das mães|Cinco famílias reservaram o salão pela mesma enquete. Cada uma entendeu que tinha exclusividade.|Faz um concurso de lasanha e entrega a chave à vencedora.
lixo|A panela perdida|Jogaram uma panela quase nova na reciclagem e agora quatro pessoas dizem ser donas.|Organiza um teste de DNA do feijão.
seguranca|O motoboy paciente|O motoboy aguarda há meia hora porque o morador acha que atender entrega dá azar.|Usa o conselho como serviço de previsão do destino.
manutencao|A escada fitness|O elevador está em revisão e alguém vendeu pacote de academia na escada.|Cobra mensalidade por andar subido.
assembleia|O banco de horas|O conselho quer pagar os prestadores com horas de gratidão no grupo.|Emite vale-obrigado com prazo de três meses.
barulho|O tapete de dança|O jogo de dança do 702 registra recordes justamente depois das dez da noite.|Instala placar luminoso no apartamento de baixo.
convivencia|O crachá da sogra|A sogra do 401 ganhou crachá de administração sem ninguém aprovar.|Promove todas as sogras a diretoras do corredor.
agua|A chaleira coletiva|Ligaram seis chaleiras na copa para fazer chá de boas-vindas. A água acabou no filtro.|Abre uma cooperativa de vapor na cozinha.
garagem|O carro encapado|A capa do carro cobriu o número da vaga e metade da moto vizinha.|Entrega uma capa para a moto se defender.
seguranca|O cadastro artístico|O visitante colocou seu nome como O Ilusionista e se recusou a mostrar documento.|Pede que faça o portão desaparecer como identificação.
manutencao|O banco manco|O banco da entrada está com uma perna menor. Os moradores estão usando como balanço.|Instala cinto e vende ficha de parque.
encomendas|A televisão dobrada|Uma televisão enorme não passa pelo elevador. O entregador quer deixar na garagem.|Transforma a garagem em cinema até resolverem.
assembleia|O conselho em férias|Os três conselheiros marcaram férias ao mesmo tempo e deixaram respostas automáticas contraditórias.|Deixa os robôs de mensagem administrarem o mês.
lixo|O lixo aromático|O 602 borrifa perfume no saco de lixo para deixar no corredor até amanhã.|Cria a fragrância Resíduos do Bosque.
convivencia|O jardim de plástico|Trocaram uma planta morta por uma de plástico, mas continuam regando. O piso está molhado.|Coloca um peixe de plástico no vaso.
barulho|O violino iniciante|O 903 decidiu aprender violino e só sabe o começo da mesma música.|Pede que o prédio inteiro cante o resto.
agua|A torneira generosa|O funcionário encontrou uma torneira ligada para refrescar o ar do salão.|Instala ventilador para espalhar o frescor molhado.
seguranca|O chaveiro apressado|Um chaveiro quer abrir o apartamento sem confirmar a identidade do solicitante.|Confere a identidade perguntando a cor do sofá.
manutencao|O relógio atrasado|O relógio do hall está quarenta minutos atrasado e virou justificativa para toda infração de horário.|Atrasa os outros relógios para ninguém estar errado.
garagem|O patinete diplomático|Dois moradores disputam a tomada da garagem para carregar patinetes. Cada um trouxe extensão.|Cria um rodízio baseado na cor do capacete.
encomendas|O presente adiantado|Uma caixa marcada surpresa foi aberta para procurar o apartamento. Agora o grupo sabe do pedido de casamento.|Faz a cerimônia na portaria antes de o casal chegar.
convivencia|A comissão do abraço|O conselho propôs abraço obrigatório para reduzir conflitos. O 801 pediu dispensa por formulário.|Multa quem abraçar com pouca convicção.
assembleia|O orçamento do abraço|A campanha de convivência veio com orçamento de camisetas, banner e um animador de auditório.|Contrata uma plateia para a próxima reunião.
barulho|O silêncio patrocinado|Um morador oferece parar a música se o prédio pagar seu streaming.|Compra o plano família e coloca o condomínio inteiro.
manutencao|O plantão de maio|O técnico de plantão atende três prédios e pediu que a pane espere até segunda.|Abre uma fila de espera para defeitos.
'''),
    ('Junho', 'Arraiá do grupo silenciado', 30, '''
assembleia|A comissão da quermesse|A festa junina já tem oito coordenadores e ninguém responsável por comprar guardanapo.|Cria mais uma coordenação para coordenar os coordenadores.
convivencia|Bandeirinha territorial|As bandeirinhas atravessaram a varanda do 202. Ele quer cobrar direito de passagem.|Declara a varanda fronteira internacional.
barulho|O sanfoneiro virtual|A caixa de som repete o mesmo acorde de sanfona desde cedo. O arquivo tem oito horas.|Coloca no modo repetição até julho.
manutencao|A barraca torta|A barraca de pescaria inclina toda vez que alguém ganha um peixe. Precisa de reforço.|Equilibra colocando prêmios maiores do outro lado.
agua|O milho de molho|Deixaram todas as espigas de molho na pia da copa e bloquearam o uso da cozinha.|Renomeia a pia como lago oficial do milho.
seguranca|Convite de palha|Os convites da festa foram copiados e tem gente de outro bairro chegando de chapéu.|Reconhece morador pelo estilo do bigode postiço.
lixo|Palha até o teto|A decoração soltou palha pelo corredor. O aspirador parece um espantalho.|Inscreve o aspirador no concurso de traje típico.
encomendas|Paçoca sem fim|A compra de paçoca veio em caixas de mil unidades. A comissão leu o preço por unidade errado.|Paga os próximos fornecedores em paçoca.
garagem|O estacionamento da roça|Puseram fardos de palha delimitando vagas. Um carro ficou com decoração fixa no para-choque.|Cobra adicional de cenário rural.
convivencia|O correio elegante|O correio elegante entregou uma declaração ao apartamento errado. Dois casais pediram explicação.|Vende a continuação em capítulos no mural.
barulho|O ensaio da quadrilha|A quadrilha ensaia o olha a cobra no meio da madrugada. O cachorro acredita toda vez.|Coloca o cachorro como fiscal de répteis.
assembleia|O par do casamento|Os conselheiros disputam quem será o padre do casamento caipira. Um já cobrou cachê.|Ordena os três e faz cerimônia em revezamento.
convivencia|A ficha do beijo|A barraca do beijo foi anunciada sem consultar quem vai trabalhar nela.|Escala o interfone para mandar beijinhos gravados.
manutencao|A tomada da pipoca|A pipoqueira e a iluminação estão na mesma extensão. Quando estoura milho, a luz apaga.|Transforma o apagão em efeito de boate caipira.
agua|O quentão da pia|Despejaram uma panela de bebida açucarada na pia. Agora as formigas estão fazendo arraial.|Monta uma barraca em miniatura para elas.
lixo|O chapéu reciclável|Jogaram o chapéu premiado na coleta por engano. O vencedor quer recontagem da lixeira.|Entrega a tampa da lixeira como nova coroa.
seguranca|A senha da pescaria|Um visitante disse que a senha do portão era pescaria. Era só o nome da barraca.|Troca todas as senhas por comidas típicas.
encomendas|O balão de papel|Chegaram balões decorativos maiores que a porta do salão. A comissão não mediu a entrada.|Deixa tudo na calçada e chama de festa externa.
garagem|O cavalo mecânico|O brinquedo alugado ficou na vaga do 601. O morador pediu que o cavalo pague condomínio.|Emite boleto para o animal de plástico.
convivencia|O bingo polêmico|A prenda do bingo é uma frigideira usada e o vencedor reconheceu a própria panela.|Inclui devolução de utensílios como modalidade do bingo.
barulho|O locutor do milho|O locutor anuncia pamonha até quando ninguém está comprando. O microfone alcança outro quarteirão.|Vende espaço publicitário entre os gritos de milho.
assembleia|O empate da cocada|A votação da melhor barraca empatou. O conselho quer decidir com duelo de colher.|Faz uma final de cocada por arremesso.
manutencao|A rede comunitária|Amarraram uma rede em dois suportes decorativos. Um deles já entortou.|Limita o uso a moradores que prometam pesar pouco.
agua|O caldo interditado|A barraca de caldo usou a torneira de serviço e ninguém sabe a procedência da mangueira.|Coloca um selo caseiro de tradição no galão.
convivencia|O santo reservado|Reservaram o salão para três santos diferentes no mesmo dia e todos querem prioridade.|Divide o salão com fita e faz três festas competindo.
lixo|O tapete de amendoim|O chão do salão virou um tapete de cascas de amendoim. A limpeza pediu equipamento extra.|Declara o piso rústico e deixa até o Natal.
seguranca|O padrinho misterioso|Um convidado se apresentou como padrinho de todos os noivos da festa. Ninguém o conhece.|Dá a chave do salão como lembrança do casamento.
encomendas|A bandeja desaparecida|O fornecedor quer de volta uma bandeja que os moradores acharam que era brinde.|Faz outra com papelão e desenho de inox.
assembleia|As contas do arraiá|A comissão somou fichas de brincadeira como dinheiro arrecadado. A festa parece milionária.|Deposita as fichas na conta do condomínio.
manutencao|O desmonte de São João|As bandeirinhas ficaram presas no sensor do portão. Cada vento abre a garagem.|Usa o vento como controle remoto oficial.
'''),
    ('Julho', 'Férias para quem?', 31, '''
convivencia|O clube da escada|As crianças fundaram um clube na escada e cobram senha para adultos passarem.|Reconhece o clube e exige imposto de bala.
barulho|O campeonato portátil|O salão virou arena de videogame com narração ao vivo pelo 402. A final só acaba de madrugada.|Coloca o conselho para comentar todas as partidas.
agua|O banho de férias|O vestiário ficou com fila porque adolescentes estão usando como spa depois da piscina.|Cria uma reserva de trinta segundos por pessoa.
garagem|A pista de giz|Desenharam uma pista de corrida infantil entre as vagas. O 601 está preso no box.|Faz o carro largar em último lugar.
seguranca|O primo de temporada|O 301 trouxe doze primos de férias e cadastrou todos como João.|Diferencia cada João pela cor do chinelo.
lixo|A oficina de slime|A oficina infantil despejou slime no ralo. Agora o ralo devolve bolhas cor-de-rosa.|Vende o ralo como máquina de diversão.
encomendas|O escorregador de caixa|Chegou um brinquedo enorme. As caixas viraram escorregador na entrada antes de conferir a entrega.|Coloca um fiscal de descida no balcão.
manutencao|O balanço aposentado|O balanço do parquinho está rangendo. Um adulto diz que aguenta porque testou ontem.|Usa o peso dos conselheiros como certificado.
convivencia|O acampamento no hall|As famílias montaram barracas no hall para uma noite de aventuras. Bloquearam as passagens.|Vende lanterna e chama o corredor de floresta.
barulho|A caça ao tesouro|O prêmio da brincadeira é tocar todas as campainhas. Os adultos descobriram na quarta rodada.|Coloca a campainha do síndico valendo pontos dobrados.
assembleia|O monitor voluntário|Um voluntário ofereceu recreação e agora quer ser pago por criança que gritou.|Faz o pagamento em decibéis de aplauso.
seguranca|O crachá de dinossauro|Uma criança emprestou seu crachá de dinossauro ao tio e ele tentou usar na entrada.|Libera só se ele rugir diante da câmera.
agua|A represa da jardinagem|Fizeram uma represa de brinquedo na canaleta do jardim. A água está chegando à calçada.|Inaugura a hidrelétrica do parquinho.
garagem|O patins elétrico|O 705 ligou o patins motorizado na tomada de manutenção e prometeu devolver energia depois.|Aceita o pagamento em voltas na garagem.
encomendas|O jogo sem peças|A caixa do jogo comunitário chegou aberta. Faltam dados, regras e a metade da paz.|Deixa os conselheiros inventarem as regras durante a partida.
convivencia|A oficina de pintura|As crianças pintaram os próprios pais no mural da garagem. Um pai pediu retoque de cabelo.|Contrata os retratistas para atualizar os documentos do prédio.
manutencao|O portão astronauta|Um foguete de papelão foi preso no portão. Ele não abre sem levar a base espacial junto.|Adia as saídas até o lançamento oficial.
lixo|A geleira do freezer|A festa do sorvete deixou caixas vazias no freezer. Ninguém consegue guardar gelo de verdade.|Anuncia gelo invisível como inovação do condomínio.
barulho|O cinema comentado|A sessão infantil tem mais comentários dos adultos que som do filme.|Distribui microfones para cada poltrona.
seguranca|A excursão perdida|Uma excursão de crianças chegou ao prédio errado. O guia insiste que reconhece a piscina.|Faz visita guiada e cobra por degrau.
assembleia|O regulamento infantil|As crianças apresentaram um regimento que proíbe boletos e obriga recreio em assembleia.|Aprova e troca a tesouraria por uma caixa de brinquedos.
convivencia|O cachorro monitor|O cachorro do 401 virou mascote das férias e está recebendo petiscos de vinte pessoas.|Dá a ele a chave do armário de lanches.
agua|O aquário improvisado|Colocaram peixes de brinquedo no bebedouro. Um morador acha que a água tem cheiro de plástico.|Anuncia safári aquático no filtro.
garagem|O triciclo guinchado|O zelador guardou um triciclo perdido. O dono de quatro anos exigiu advogado.|Convoca audiência com o conselho de pelúcias.
encomendas|O kit de mágica|O kit de mágica da recreação chegou sem instruções. Toninho já ofereceu espetáculo.|Deixa ele fazer o caixa desaparecer no palco.
manutencao|A bola no refletor|Uma bola ficou presa no refletor do pátio. Estão tentando alcançar com uma vassoura curta.|Empilha as cadeiras da assembleia como torre de resgate.
lixo|O piquenique esquecido|Esqueceram a cesta do piquenique no salão fechado. O cheiro já virou assunto no elevador.|Coloca placa de queijo artesanal na porta.
barulho|A despedida das férias|A turma quer uma festa de encerramento que vai durar mais que as próprias férias.|Decreta férias da regra de silêncio.
seguranca|O visitante da saudade|Um primo que já foi embora deixou o acesso ativo e emprestou ao amigo.|Usa a saudade como critério de cadastro.
assembleia|O relatório da recreação|O relatório diz que todas as crianças foram felizes. Não menciona os três bancos riscados.|Pede que os bancos também preencham pesquisa de satisfação.
convivencia|Volta às aulas|Os pais comemoraram a volta às aulas no salão e fizeram mais bagunça que as crianças.|Dá advertência escrita na agenda dos pais.
'''),
    ('Agosto', 'Segurança de mentirinha', 31, '''
seguranca|A câmera de ponta-cabeça|A câmera da entrada mostra todo mundo de cabeça para baixo. O instalador chamou de recurso antivandalismo.|Pede aos visitantes que entrem andando de mãos.
manutencao|A fechadura falante|A fechadura eletrônica fala bem-vindo a cada tentativa errada. Já cumprimentou um estranho trinta vezes.|Grava a voz do síndico contando piadas no aparelho.
convivencia|O curso de vigilância|Seu Valdir ofereceu curso de vigilância com cenas de filmes de ação.|Contrata figurantes para simular uma fuga pela piscina.
garagem|O adesivo invisível|O adesivo de acesso ficou tão discreto que o porteiro não consegue identificar carro algum.|Cola o número do apartamento no teto de cada carro.
encomendas|O reconhecimento de pacotes|A nova regra manda fotografar todos os pacotes. Já tem álbum com compra íntima e presente surpresa.|Faz exposição de logística no mural do hall.
seguranca|A senha rimada|Toninho divulgou uma rima com a senha do portão. Todo mundo na rua aprendeu o refrão.|Lança a segunda estrofe com a senha da garagem.
barulho|O alarme teatral|O teste de alarme usa uma gravação de grito. Os moradores estão assustados e o gato se escondeu.|Põe risada gravada depois para aliviar.
assembleia|O orçamento blindado|O orçamento da guarita inclui blindagem, mas o portão ao lado segue quebrado.|Pinta o portão com tinta de tanque.
agua|O detector aquático|Compraram um sensor de vazamento e deixaram dentro de um balde cheio. Ele não para de apitar.|Coloca outro sensor para fiscalizar o primeiro.
lixo|O descarte sigiloso|O 901 rasgou documentos e entupiu a lixeira. Agora quer escolta para cada saco.|Cria o serviço secreto da coleta seletiva.
seguranca|O boné reconhecido|O porteiro liberou alguém porque reconheceu o boné. O dono do boné estava no trabalho.|Cadastra todos os acessórios como moradores.
convivencia|O almoço dos pais|O almoço de domingo lotou o salão e as crianças montaram uma fila de gravatas na entrada.|Usa a gravata como pulseira de acesso ao prédio.
garagem|A cancela emocional|A cancela abre quando quer. O fornecedor diz que pode ser sensibilidade do equipamento.|Faz uma roda de acolhimento para a cancela.
manutencao|A lanterna permanente|A iluminação da entrada falhou. O conselho sugeriu deixar uma lanterna apoiada em um vaso.|Escala o vaso como vigilante noturno.
encomendas|O pacote-isca|Seu Valdir colocou uma caixa vazia para testar furtos. O zelador reciclou e agora virou suspeito.|Instala uma isca dentro de cada isca.
seguranca|A lista de apelidos|O cadastro tem Magrão, Baixinha e Rei do Churrasco. Ninguém consegue conferir os documentos.|Emite RG com foto de churrasco para todos.
barulho|O apito do vigia|Um voluntário resolveu apitar a cada carro que entra. A garagem parece campeonato de futebol.|Faz o conselho mostrar cartão amarelo aos motoristas.
assembleia|A central de monitores|O conselho quer quatro monitores na guarita para uma câmera que aponta para o chão.|Duplica a imagem e chama de cobertura total.
seguranca|A porta segurada|O 204 segura a porta para desconhecidos por educação. Hoje entrou um vendedor atrás de três moradores.|Coloca uma placa pedindo aos desconhecidos que agradeçam.
agua|O portão molhado|O sensor do portão dispara quando lavam a calçada. O prédio entra em alerta a cada balde.|Proíbe chuva durante o expediente da portaria.
lixo|A caixa suspeita|Um papelão vazio foi tratado como encomenda suspeita. Isolaram metade da entrada com cadeiras.|Convoca coletiva para anunciar a operação Papelão.
convivencia|O vigia do sofá|Seu Valdir monitora a entrada pela janela e comenta roupa de todo mundo no grupo.|Dá a ele um programa diário de moda e segurança.
garagem|A placa trocada|O sistema leu a placa errada e abriu para um carro de aplicativo. O morador ficou do lado de fora.|Troca os nomes dos donos para combinar com o sistema.
manutencao|O interfone bilíngue|O interfone mudou de idioma depois de uma atualização. Ninguém sabe qual botão libera a entrada.|Ensina o prédio inteiro a responder por mímica.
encomendas|Entrega por telepatia|A loja marcou entrega concluída com foto de uma mão e nenhum endereço. O morador quer a compra.|Usa a foto da mão para adivinhar o apartamento.
seguranca|A ronda de patinete|Toninho propôs ronda de patinete no subsolo. Na primeira volta derrubou um cone.|Compra sirene para o patinete ficar mais respeitado.
assembleia|A senha em ata|Escreveram todas as senhas na ata e distribuíram uma cópia na caixa de correio errada.|Plastifica a ata para ela durar mais.
barulho|O curso de defesa|O curso de defesa pessoal está batendo em almofadas na parede da sala de reunião.|Inscreve as paredes no treinamento de resistência.
seguranca|O acesso por curtida|Um aplicativo prometeu liberar visitantes pelo perfil social. O fornecedor só mostrou um vídeo de propaganda.|Libera acesso a quem curtir o anúncio três vezes.
manutencao|A placa de alerta|A placa de vigilância caiu e bloqueou a visão da câmera. A câmera está vigiando a própria placa.|Compra outra câmera para vigiar o verso.
assembleia|Auditoria do cadeado|A auditoria descobriu cinco cadeados novos e nenhuma chave identificada. O conselho comemorou a segurança.|Compra cinco cadeados para guardar as chaves perdidas.
'''),
    ('Setembro', 'Flores, taxas e outras pragas', 30, '''
convivencia|A primavera antecipada|Dona Marlene plantou flores na passagem e exige que todos desviem para não amassar a felicidade.|Põe o elevador para desembarcar direto no jardim.
agua|O regador automático|O regador novo molha mais os carros que as plantas. O 502 apareceu de guarda-chuva na garagem.|Vende lavagem ecológica por aproximação.
manutencao|A poda artística|O jardineiro recebeu pedidos contraditórios e a árvore ficou parecida com um poodle.|Cobra ingresso para o zoológico vegetal.
lixo|A folha contestada|Um morador quer multar a árvore porque derruba folhas na varanda dele.|Envia a notificação para o tronco com aviso de recebimento.
barulho|O sabiá acusado|O 301 reclama do canto dos pássaros e quer horário de silêncio também para eles.|Contrata Toninho para ensinar os pássaros a sussurrar.
seguranca|O jardineiro sem agenda|Um homem apareceu para podar as plantas sem ter sido contratado. Trouxe só uma tesoura escolar.|Promove o homem a especialista em bonsai de fachada.
assembleia|A bandeira gigante|A comissão pediu uma bandeira maior que a fachada e não sabe onde prender.|Enrola o prédio inteiro e chama de presente cívico.
garagem|O carro floreira|O 203 deixou vasos sobre o capô para reservar sombra. Um vaso escorregou perto da moto.|Transforma o estacionamento em jardim suspenso de automóveis.
encomendas|Sementes misteriosas|Chegaram sementes sem identificação e o conselho quer espalhar no gramado para ver o resultado.|Planta primeiro no vaso do caixa eletrônico imaginário.
convivencia|A horta disputada|A horta comunitária tem três donos de cebolinha e ninguém disposto a regar.|Divide cada raiz em frações de condomínio.
agua|O lago de mosquito|Os pratos dos vasos estão cheios de água. Os moradores acham que a água é parte da decoração.|Cobra aluguel dos mosquitos e mantém os pratos.
manutencao|A raiz no piso|A raiz levantou uma placa da calçada. Um morador já chamou de lombada natural.|Sinaliza como trilha de aventura para pedestres.
lixo|Adubo aromático|O adubo foi guardado ao lado da entrada. As visitas estão preferindo esperar na esquina.|Vende a fragrância Campo Intenso na portaria.
barulho|O cortador dominical|A poda com máquina começou no domingo cedo. O operador diz que a grama pediu urgência.|Faz um abaixo-assinado com assinatura de cada folha.
assembleia|O orçamento do jardim|O projeto paisagístico inclui uma fonte com música e esqueceu o conserto da drenagem.|Troca o conserto por uma playlist de chuva.
seguranca|O visitante das flores|Um vendedor disse que conhece todas as plantas e usou isso para pedir acesso às unidades.|Usa a samambaia como referência cadastral.
convivencia|O banco com nome|Dona Cida colocou uma placa com seu nome no banco do jardim. Já pede silêncio na praça particular.|Batiza os outros bancos e entrega escrituras de cartolina.
garagem|A vaga sombreada|A árvore faz sombra em duas vagas. Agora existe uma tabela clandestina de aluguel por hora.|Cria o pregão oficial das sombras.
encomendas|O vaso descomunal|Um vaso comprado pela comissão não passa na porta. O vendedor disse que a medida era sem borda.|Aumenta a porta na conversa e manda insistir.
manutencao|A luz das flores|A iluminação do jardim ficou tão forte que o 101 está usando máscara de dormir às seis da tarde.|Distribui óculos escuros para todas as janelas.
agua|A mangueira sem ponta|A ponta da mangueira sumiu. Quem rega está esguichando água no caminho até o canteiro.|Chama o caminho de corredor de hidratação.
lixo|A grama reciclada|Jogaram grama cortada dentro da lixeira de papel. O saco ficou úmido e pesado.|Classifica o material como papel em formação.
convivencia|O concurso de plantas|O concurso de plantas premiou uma samambaia de plástico. O segundo lugar quer perícia.|Exige que todas as plantas façam prova escrita de fotossíntese.
barulho|O espanta-pássaro|O aparelho para espantar pássaros emite sons que incomodam mais os moradores.|Instala outro aparelho para espantar o primeiro.
assembleia|O patrocínio da horta|Toninho quer colocar propaganda de seu negócio em cada pé de alface.|Vende naming rights para a cebolinha.
seguranca|O acesso do paisagista|O prestador levou a chave do portão para fazer cópia sem avisar. A equipe pede controle.|Aceita uma foto da chave como devolução.
garagem|O bambu da discórdia|Um bambu de decoração caiu na faixa de circulação. O dono quer que os carros façam desvio.|Cria a rota turística do bambuzal subterrâneo.
encomendas|A terra do elevador|Um saco de terra rasgou na entrega. O elevador está pronto para plantar batata.|Abre uma filial da horta entre os andares.
convivencia|A colheita desigual|A horta rendeu quatro tomates. O conselho separou três para a reunião interna.|Faz um leilão de fatias com lance mínimo.
assembleia|O balanço da primavera|Gastamos mais com placas da horta que com plantas. A comissão quer imprimir o relatório em papel especial.|Imprime em folha de alface para combinar com o projeto.
'''),
    ('Outubro', 'O terror mora ao lado', 31, '''
manutencao|A lâmpada piscante|A lâmpada do corredor pisca sem parar. Seu Valdir acha que é divulgação da festa de terror.|Põe uma trilha sonora e adia o reparo.
convivencia|A teia oficial|A decoração de teia cobre o quadro de avisos. Ninguém acha os comunicados da manutenção.|Deixa só a aranha assinar os avisos.
seguranca|O esqueleto visitante|Cadastraram um esqueleto decorativo como morador e o sistema não aceita apagar o CPF inventado.|Emite segunda via do documento para o falecido de plástico.
barulho|O fantasma do áudio|Um celular escondido reproduz gemidos no corredor. O técnico do elevador foi embora assustado.|Marca uma assembleia com os espíritos do prédio.
encomendas|A abóbora premiada|A abóbora decorativa veio gigante e ocupa o balcão inteiro. As encomendas estão em volta como oferenda.|Promove a abóbora a gerente de entregas.
garagem|A vaga assombrada|Colocaram um túmulo cenográfico na vaga do 603. Ele exige uma alternativa para estacionar.|Faz o carro dividir a eternidade com a decoração.
lixo|O monstro orgânico|A abóbora de verdade começou a estragar no hall. O cheiro faz parte do susto, segundo a comissão.|Inscreve a abóbora no concurso de efeitos especiais.
agua|A piscina de poção|Querem colorir a piscina de roxo para uma festa. O fornecedor do produto não explicou se é próprio para banho.|Mistura corante até parecer suficientemente mágico.
assembleia|O orçamento do medo|A comissão pediu máquina de fumaça, mas não incluiu ventilação nem limpeza.|Resolve com leques distribuídos entre os convidados.
convivencia|O elevador do susto|Um morador fica fantasiado dentro do elevador assustando quem entra. Uma senhora desistiu de sair.|Contrata outro fantasma para cobrir o segundo elevador.
barulho|A festa dos pequenos|A festa infantil alugou um som maior que o usado na reunião do bairro.|Liga duas caixas para o som ficar equilibrado.
convivencia|Doces por apartamento|As crianças distribuíram um mapa de casas que dão doces. O 401 está marcado como território hostil.|Publica um ranking oficial dos moradores pão-duros.
seguranca|A máscara sem cadastro|Os convidados mascarados querem entrar sem mostrar o rosto porque estraga o personagem.|Usa o nome do personagem como identificação civil.
manutencao|O morcego no sensor|Um morcego de feltro preso no sensor impede a porta de fechar. O decorador pediu respeito à arte.|Deixa a porta aberta até o animal cansar.
encomendas|A caixa que grita|Um presente faz barulho ao mexer. Os funcionários não sabem se podem guardar na portaria.|Passa a caixa de mão em mão até ela perder a voz.
lixo|A oficina de abóboras|A oficina deixou sementes e restos por toda a copa. O chão parece um prato de sopa.|Serve a decoração como jantar de confraternização.
garagem|O carro teia|Envolveram o carro do 201 em barbante para uma brincadeira. Ele precisa sair para trabalhar.|Cobra taxa de escape room para liberar o carro.
agua|O caldeirão vazando|O caldeirão de decoração usa água e está vazando perto dos cabos de luz. Precisamos desligar e limpar.|Coloca uma placa de feitiço molhado e segue a festa.
assembleia|O concurso de fantasias|O jurado se inscreveu no concurso e deu nota dez para si mesmo. O prêmio saiu do caixa.|Dá a ele também o prêmio de melhor jurado.
barulho|O ensaio do uivo|O 704 ensaia uivo de lobisomem na varanda. Os cachorros do prédio estão respondendo.|Cria um coral de uivos com chamada pelo interfone.
convivencia|O espelho assustador|Colaram adesivos no espelho do hall. Um visitante tentou limpar e saiu com cola na roupa.|Anuncia o espelho como experiência interativa.
seguranca|O entregador zumbi|Um animador de festa ficou preso na entrada porque o cadastro só tem seu nome de zumbi.|Cadastra o elenco inteiro como parentes do porteiro.
manutencao|A fumaça persistente|A máquina de fumaça disparou o detector. O técnico pede suspensão do uso até vistoriar.|Coloca uma fantasia de nariz no detector.
encomendas|O chapéu de bruxa|Chegaram cinquenta chapéus quando a comissão pediu cinco. O fornecedor aceita devolução lacrada.|Nomeia todos os moradores para o conselho das bruxas.
lixo|A tinta de terror|Sobraram baldes de tinta cenográfica sem instrução de descarte. Um morador quer jogar na sarjeta.|Pinta a sarjeta e diz que faz parte do cenário.
garagem|O labirinto de caixas|Montaram um labirinto no caminho dos carros. Agora ele inclui um veículo preso de verdade.|Cobra entrada para resgatar o motorista.
convivencia|A maldição do grupo|Um áudio diz que quem não encaminhar perde o desconto da taxa. Já circulou em seis grupos.|Encaminha em nome do condomínio para garantir.
assembleia|A comissão secreta|O conselho está decidindo a festa num grupo secreto e mandando os custos para todos.|Cria um grupo ainda mais secreto para aprovar a cobrança.
barulho|O susto de madrugada|O temporizador da decoração foi configurado para três da manhã. O prédio acordou com uma risada.|Programa uma segunda risada para pedir desculpas.
seguranca|A chave do castelo|Um morador quer emprestar o controle do portão a um personagem contratado para o fim de semana.|Entrega também um mapa das portas secretas imaginárias.
convivencia|O Halloween final|A festa acabou e o conselho se recusa a tirar a fantasia na prestação de contas.|Aceita os recibos assinados por Conde Toninho.
'''),
    ('Novembro', 'Black fraude do condomínio', 30, '''
assembleia|O desconto urgente|Um fornecedor oferece desconto só até o fim do áudio. O áudio tem oito minutos.|Aprova antes de ouvir para não perder tempo.
manutencao|A lâmpada em promoção|Compraram um lote barato de lâmpadas que não cabe em nenhum soquete do prédio.|Troca os soquetes do prédio inteiro para aproveitar.
seguranca|A câmera sem imagem|A promoção de câmera veio só com a carcaça. O anúncio dizia imagem meramente ilustrativa.|Instala mesmo assim e deixa a imaginação filmar.
encomendas|A avalanche de caixas|A portaria recebeu compras de seis meses em dois dias. Não dá para alcançar o livro de entregas.|Empilha por signo do destinatário.
garagem|O robô aspirador|O robô comprado para a garagem roda em círculos no mesmo pilar. O fornecedor chama de mapeamento profundo.|Põe um crachá de vigilante e deixa patrulhar.
convivencia|O cupom coletivo|Um morador usou o cupom da compra coletiva só para o próprio apartamento. O grupo quer explicação.|Divide a economia em parcelas de elogio ao morador.
agua|A torneira inteligente|A torneira com aplicativo precisa de atualização para abrir. O pessoal da limpeza ficou esperando.|Agenda a água para o próximo lançamento do sistema.
barulho|A caixa econômica|A caixa de som da oferta não tem controle de volume. Só liga no máximo.|Compra outra para tocar uma música mais baixa por cima.
lixo|O plástico da promoção|A lixeira transbordou de plástico bolha. Os moradores estão estourando tudo no corredor.|Organiza um campeonato noturno de estalos.
assembleia|A planilha da economia|O conselho somou o valor dos descontos como dinheiro disponível e quer gastar de novo.|Abre uma conta bancária de economia imaginária.
manutencao|A garantia da garantia|O reparo barato só tem garantia se comprar outro reparo. O segundo é mais caro que o primeiro.|Compra um terceiro para garantir os outros dois.
seguranca|A fechadura social|A fechadura nova pede acesso aos contatos do celular. O vendedor disse que é para fazer amigos.|Cadastra o grupo todo como família do portão.
encomendas|O destinatário síndico|Dez moradores colocaram o nome do síndico nas compras para não ter erro. Agora todos querem prioridade.|Retira tudo e faz um amigo secreto com as caixas.
garagem|A câmera de ré perdida|O acessório comprado para o carro foi entregue e testado na guarita. Agora só mostra o balcão.|Usa como câmera oficial do troco.
convivencia|O churrasco de oferta|A compra coletiva trouxe linguiça para duzentas pessoas. A festa só tem trinta confirmados.|Faz o condomínio inteiro aderir à dieta da linguiça.
agua|O purificador parcelado|O filtro em promoção cobra assinatura para avisar quando precisa trocar a vela.|Pede aos moradores que adivinhem a validade em enquete.
barulho|O sino digital|A campainha nova toca uma propaganda antes do aviso. As entregas chegam com jingle.|Vende anúncio para a campainha da outra entrada.
lixo|A devolução sem caixa|A comissão jogou fora as embalagens antes de testar as compras. Agora quer devolver os defeitos.|Embala tudo nos panfletos de promoção do fornecedor.
assembleia|O rateio do frete|O frete da compra conjunta ficou maior que a economia. Ninguém quer admitir na reunião.|Esconde o frete na coluna de felicidade logística.
manutencao|A cadeira dobrável|As cadeiras promocionais dobram com gente sentada. O salão precisa suspender o uso.|Dá ponto extra a quem conseguir equilibrar.
seguranca|O interfone com anúncio|O interfone barato fala compre agora antes de chamar a unidade. O porteiro perdeu uma entrega.|Negocia comissão por cada visitante que comprar.
encomendas|O pacote de pedra|Uma encomenda veio com pedras no lugar do produto. O morador pede registro e ajuda com a entrega.|Usa as pedras para completar o jardim sem contar a ninguém.
garagem|O carregador universal|O carregador prometido como universal não serve em nenhum veículo do prédio.|Compra um veículo compatível para provar que funciona.
convivencia|A taxa de oportunidade|Toninho quer receber comissão porque encontrou as ofertas, inclusive as que deram errado.|Paga uma comissão extra por cada problema original.
agua|A ducha sensível|A ducha econômica desliga a cada três segundos. O fornecedor diz que é incentivo à reflexão.|Distribui roteiro de meditação entre os jatos.
barulho|O aspirador potente|O aspirador novo faz mais barulho que uma obra e não recolhe o pó fino.|Usa como sirene para anunciar a limpeza.
lixo|A montanha de isopor|As compras do salão encheram o depósito de isopor. A coleta orientou separar e agendar retirada.|Monta uma réplica do prédio para justificar a coleção.
assembleia|O parcelamento infinito|O conselho quer parcelar tudo em tantas vezes que nem o próximo mandato termina de pagar.|Declara os boletos patrimônio das futuras gerações.
seguranca|O link do desconto|Um suposto fornecedor enviou um link pedindo senha bancária para liberar cashback.|Digita a senha do portão para ver se ele aceita.
assembleia|O balanço das ofertas|A economia anunciada virou custo com devoluções. O conselho quer chamar o mês de investimento em experiência.|Imprime um diploma de comprador profissional para cada conselheiro.
'''),
    ('Dezembro', 'Só mais um mandato?', 31, '''
convivencia|A árvore do hall|A árvore de Natal ocupa a passagem e ganhou mais enfeites que espaço livre.|Pede aos moradores que passem de lado até janeiro.
manutencao|O pisca sem pausa|O pisca-pisca ficou ligado sem temporizador e o zelador não alcança a tomada.|Cria escala de moradores para ficar olhando até apagar.
assembleia|A comissão da ceia|A comissão tem cinco cardápios e ninguém conferiu o orçamento do mês.|Aprova todos e chama a diferença de espírito natalino.
encomendas|O Papai Noel logístico|A portaria virou oficina de presentes. Um morador quer que o zelador embrulhe as compras.|Dá um gorro ao zelador e inclui entrega por chaminé.
seguranca|O bom velhinho|Um homem fantasiado quer subir para entregar lembranças sem identificar os destinatários.|Libera o acesso porque o trenó deve estar em fila dupla.
garagem|A vaga do trenó|Reservaram três vagas de visitantes para uma decoração de trenó. Os visitantes chegaram antes do Natal.|Manda os carros estacionarem em formação de rena.
agua|A neve de espuma|A decoração promete neve artificial com espuma, mas está encharcando o piso do hall.|Distribui trenós de papelão para atravessar o piso.
lixo|O panetone suspeito|Uma caixa de panetone esquecida desde o ano passado reapareceu no depósito. Ninguém quer abrir.|Sorteia como prêmio surpresa da confraternização.
barulho|O coral de elevador|O coral ensaia dentro do elevador para aproveitar a acústica. Ninguém consegue chamar a cabine.|Programa uma apresentação em cada andar antes de liberar.
convivencia|O amigo invisível|O amigo secreto sorteou uma unidade vazia. O organizador quer que o síndico compre o presente dela.|Dá uma caixa vazia embrulhada e pede aplausos.
assembleia|O décimo terceiro|O conselho esqueceu uma despesa prevista e agora culpa o calendário por ter dezembro.|Tira dezembro da planilha e mantém a festa.
manutencao|A estrela inclinada|A estrela do topo da árvore está solta. Querem subir em cadeiras para consertar.|Empilha os presentes e usa como escada festiva.
encomendas|A etiqueta trocada|As etiquetas de presentes foram impressas com os nomes dos apartamentos do prédio ao lado.|Faz amigo secreto entre condomínios sem avisar.
seguranca|O fornecedor da festa|O buffet mandou uma equipe diferente da cadastrada. Precisamos confirmar antes de liberar o acesso.|Identifica os profissionais pela habilidade de enrolar guardanapo.
garagem|O lava-carro festivo|Um morador montou um lava-carro na garagem para levantar dinheiro da viagem. A fila bloqueou a saída.|Cobra pedágio de Natal e mantém o negócio.
convivencia|O presépio expandido|O presépio ganhou bonecos de moradores sem autorização. O síndico aparece de burro.|Vende miniaturas dos conselheiros para completar o estábulo.
barulho|A playlist sagrada|A mesma música natalina toca em loop no hall. O sistema esqueceu como parar.|Aumenta o volume para os moradores aprenderem mais rápido.
agua|O degelo da festa|Desligaram o freezer para usar a tomada do pisca-pisca. O gelo derreteu por toda a copa.|Serve a água como drink temático de neve líquida.
lixo|O embrulho coletivo|A oficina de embrulhos deixou fita adesiva nas mesas e no chão. A limpeza está grudando no trabalho.|Mantém as mesas colantes para segurar os pratos da ceia.
assembleia|A promessa de campanha|Seu Valdir promete taxa zero se for eleito, mas não explica como pagar os funcionários.|Imprime dinheiro do condomínio com a cara dele.
manutencao|O salão sem cadeiras|A locadora levou as cadeiras um dia antes da festa por erro na reserva. Só sobraram três.|Faz rodízio de sentar a cada refrão.
encomendas|A cesta sem destinatário|Chegou uma cesta de fim de ano para Administração. Os conselheiros acham que cada um é a administração inteira.|Sorteia a cesta entre os três sem contar aos funcionários.
seguranca|O controle emprestado|Um morador viajou e emprestou o controle a um conhecido que ninguém cadastrou.|Aceita uma selfie de férias como autorização de entrada.
convivencia|A ceia ampliada|Os convidados da ceia passaram de quarenta para noventa. A reserva e a capacidade não mudaram.|Divide cada cadeira em dois lugares na planta.
barulho|O brinde no interfone|Alguém usa o interfone para desejar boas festas a cada unidade. Já estamos no terceiro discurso.|Liga todos os ramais ao mesmo tempo para ganhar audiência.
lixo|O dia das embalagens|A área de coleta ficou coberta de caixas de presentes. O acesso precisa ser liberado.|Monta uma cidade de papelão e declara patrimônio natalino.
agua|A piscina de despedida|Uma festa de férias quer usar a piscina depois do horário. A limpeza está agendada para o mesmo período.|Faz os convidados limparem nadando em círculos.
assembleia|O balanço do mandato|Os moradores pediram contas claras. Toninho sugeriu mostrar só os meses com saldo bonito.|Imprime as despesas em branco sobre papel branco.
convivencia|A faixa da reeleição|Penduraram uma faixa de reeleição antes de o síndico confirmar candidatura. O conselho já vendeu camisetas.|Anuncia candidatura também para presidente do elevador.
manutencao|O contador da virada|O relógio da festa adianta dez minutos. Metade quer virar o ano antes para ir dormir.|Faz três viradas e cobra três cotas de festa.
assembleia|O último áudio|Chegou a última reunião do mandato. Dona Cida agradeceu em um áudio de vinte minutos e pediu só mais uma coisinha.|Aceita outro mandato sem ouvir a coisinha.
'''),
]
