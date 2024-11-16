# Criando dicionários com o conjunto de atributos para cada grupo de produto

VESTIDO_CARAC = "\
COMPRIMENTO_SAIA: CALCANHAR, MEIO_CANELA, JOELHO, MEIO_COXA, MINI;\
COMPRIMENTO_MANGA: COMPRIDA, TRES_QUARTOS, MEIA_MANGA, CURTA, ALÇA, SEM_MANGA;\
TIPO_MANGA: N/A, REGULAR, BISPO, DECOTE_NO_OMBRO, BORBOLETA, KIMONO, FLARE, BUFANTE, FLUTTER, SINO, FLAUTA, CIGANA, FENDA, MANGA_DOBRADA, LACO, AMPLA;\
MODELAGEM_SAIA: REGULAR, LAPIS, GODÊ, ENVELOPE, EVASÊ, PLISSADA, BALONÊ, SEREIA, COM_BABADOS, TRANSPASSADA, PREGUEADA, ASSIMETRICA;\
FENDA_PERNA: SIM, N/A;\
DECOTE_OU_GOLA: V, HALTER, QUADRADA, POLO, ENVELOPE, GOLA_ALTA, OMBRO_A_OMBRO, REDONDA, CORACAO, TOMARA_QUE_CAIA, RETO, U, OMBRO_UNICO, CAPUZ, CANOA, TRANSPASSADO, DEGAGÊ;\
AMARRACAO: SIM_NA_SAIA, SIM_NO_BUSTO, N/A;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ESTRELA, CORACAO, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, ANIMALPRINT_TIGRE, FOLHAGEM, TROPICAL, CAMUFLAGEM, TIE_DYE, DEGRADE, MARMORIZADA, MINIMALISTA, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"

CALCA_CARAC = "\
COMPRIMENTO: CALCANHAR, MEIO_CANELA, JOELHO, MEIO_COXA, MINI;\
TIPO_CINTURA: ALTA, MEDIA, BAIXA;\
MODELAGEM: RETA, SKINNY, FLARE, PANTALONA, MOM, CARGO, BOYFRIEND, CLOCHARD, CROPPED, JOGGER, SLIM, SOLTA, ASSIMETRICA;\
TIPO_BARRA: RETA, DOBRADA, DESFIADA, ASSIMETRICA, COM_BABADOS, AJUSTADA, EVASÊ;\
AMARRACAO: SIM_NA_LATERAL, SIM_NA_FRENTE, N/A;\
FENDA_PERNA: SIM, N/A;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO, JEANS;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ESTRELA, CORACAO, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, ANIMALPRINT_TIGRE, FOLHAGEM, TROPICAL, CAMUFLAGEM, TIE_DYE, DEGRADE, MARMORIZADA, MINIMALISTA, ABSTRATO, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"

SAIA_CARAC = "\
COMPRIMENTO: CALCANHAR, MEIO_CANELA, JOELHO, MEIO_COXA, MINI;\
MODELAGEM: REGULAR, LAPIS, GODÊ, ENVELOPE, EVASÊ, PLISSADA, BALONÊ, SEREIA, COM_BABADOS, TRANSPASSADA, PREGUEADA, ASSIMETRICA;\
TIPO_CINTURA: ALTA, MEDIA, BAIXA;\
TIPO_BARRA: RETA, DESFIADA, ASSIMETRICA, COM_BABADOS, AJUSTADA, EVASÊ, PREGUEADA;\
AMARRACAO: SIM_NA_LATERAL, SIM_NA_FRENTE, N/A;\
FENDA_PERNA: SIM, N/A;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO, JEANS;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ESTRELA, CORACAO, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, ANIMALPRINT_TIGRE, FOLHAGEM, TROPICAL, CAMUFLAGEM, TIE_DYE, DEGRADE, MARMORIZADA, MINIMALISTA, ABSTRATO, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"

BLUSA_CARAC = "\
COMPRIMENTO: LONGA, MEDIA, CURTA, CROPPED;\
MODELAGEM: SOLTA, AJUSTADA, EVASÊ, RETA, ASSIMETRICA;\
COMPRIMENTO_MANGA: COMPRIDA, TRES_QUARTOS, MEIA_MANGA, CURTA, ALÇA, SEM_MANGA;\
TIPO_MANGA: N/A, REGULAR, BISPO, DECOTE_NO_OMBRO, BORBOLETA, KIMONO, FLARE, BUFANTE, FLUTTER, SINO, FLAUTA, CIGANA, FENDA, MANGA_DOBRADA, LACO, AMPLA;\
DECOTE_OU_GOLA: V, HALTER, QUADRADA, POLO, ENVELOPE, GOLA_ALTA, OMBRO_A_OMBRO, REDONDA, CORACAO, TOMARA_QUE_CAIA, RETO, U, OMBRO_UNICO, CAPUZ, CANOA, TRANSPASSADO, DEGAGÊ;\
AMARRACAO: SIM_NA_LATERAL, SIM_NA_FRENTE, N/A;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ESTRELA, CORACAO, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, ANIMALPRINT_TIGRE, FOLHAGEM, TROPICAL, CAMUFLAGEM, TIE_DYE, DEGRADE, MARMORIZADA, MINIMALISTA, ABSTRATO, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"

SHORT_CARAC = "\
COMPRIMENTO: LONGO, MEDIO, CURTO, MINI;\
MODELAGEM: RETA, SOLTA, AJUSTADA, EVASÊ, CARGO, CLOCHARD, MOM, BOYFRIEND, SKINNY, ASSIMETRICA, ESPORTIVO;\
TIPO_CINTURA: ALTA, MEDIA, BAIXA;\
TIPO_BARRA: RETA, DESFIADA, DOBRADA, ASSIMETRICA, AJUSTADA, EVASÊ, PREGUEADA;\
AMARRACAO: SIM_NA_LATERAL, SIM_NA_FRENTE, N/A;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO, JEANS;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, CAMUFLAGEM, TIE_DYE, DEGRADE, MINIMALISTA, ABSTRATO, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"

BLAZER_CARAC = "\
COMPRIMENTO: LONGO, MEDIO, CURTO, CROPPED;\
MODELAGEM: RETA, AJUSTADA, OVERSIZED, ASSIMETRICA, SOLTA;\
COMPRIMENTO_MANGA: CURTA, TRES_QUARTOS, COMPRIDA;\
TIPO_MANGA: REGULAR, BUFANTE, KIMONO, DOBRADA, AMPLA;\
COR_PREDOMINANTE: PRETO, AZUL, VERDE, AMARELO, VERMELHO, ROSA, BEGE, LARANJA, ROXO, BRANCO, OFF_WHITE, MARROM, CINZA, MULTICOLORIDO;\
LOCALIZACAO_ESTAMPA: N/A, LOCALIZADA, ROUPA_INTEIRA;\
ZOOM_ESTAMPA: N/A, GRANDE, MEDIO, PEQUENO;\
ESTAMPA: SEM_ESTAMPA, FLORAL, LISTRADO_VERTICAL, LISTRADO_HORIZONTAL, LISTRADO_OUTRO, POA, XADREZ, ESTRELA, CORACAO, ANIMALPRINT_ONCA, ANIMALPRINT_COBRA, ANIMALPRINT_ZEBRA, ANIMALPRINT_TIGRE, FOLHAGEM, TROPICAL, CAMUFLAGEM, TIE_DYE, DEGRADE, MARMORIZADA, MINIMALISTA, ABSTRATO, GEOMETRICO, ESTAMPA_ETNICA;\
ESTILO: CASUAL, SOCIAL, ESPORTIVO, FESTIVO, BASICO;"