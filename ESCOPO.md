# Escopo do projeto

  

## Objetivo Principal

Desenvolver uma aplicação capaz de reconhecer produtos similares com base em características customizáveis, especificamente:

- Cor

- Estampa

- Modelagem

  

A aplicação permitirá que os usuários busquem produtos similares ajustando a ênfase em cada uma dessas características conforme suas preferências.

  

## Abordagens Propostas

**Abordagem 1**: Embedding Único com Subespaços para Cada Pilar de Informação

Gerar um único embedding que represente o produto completo e, posteriormente, identificar subespaços dentro desse embedding que correspondam a cada pilar de informação (cor, estampa e modelagem). A ideia é começar do mesmo ponto, com um mesmo embedding inicial para cada pilar, e a partir daí reduzir e projetar até chegar em um vetor que represente uma característica isolada.

  
Vantagens:

- Simplificação na representação do produto.
  
- Facilita a análise da interdependência entre diferentes características.

Desvantagens:

Pode ser desafiador isolar características específicas devido à interconexão das informações no embedding.

  

**Abordagem 2**: Vetores de embedding segregados para Cada Pilar de Informação

Descrição: Criar vetores de embedding independentes para cada característica (cor, estampa e modelagem) e combinar esses embeddings para representar o produto completo.  Uma possibilidade é realizar finetunning do modelo para cada pilar, com imagens estratégicas correspondentes.
  

Vantagens:

Permite uma manipulação mais precisa de cada característica.

Facilita a personalização das recomendações com base nas preferências do usuário.

  

Desvantagens:  
Caso seja necessário retreinar para cada pilar, o processo aumentará signitivamente a complexidade. Além de que características correlacionadas podem gerar redundância e prejudicar a eficiência dos modelos. Há ainda o risco de perda de contexto global ao focar em atributos isolados.
## Metodologia
### Montagem da Base de Dados Inicial

Descrição: Construir uma base de dados composta por pares de descrições textuais e imagens de produtos.
  

Atividades:

Coleta de imagens de produtos de fontes diversas.  

Extração ou criação de descrições textuais detalhadas para cada produto.

Organização e armazenamento dos pares descrição + imagem em um banco de dados estruturado.

  

### Geração de embeddings com o Modelo CLIP  

Descrição: Utilizar o modelo CLIP para gerar embeddings a partir da base de dados montada.

  
Atividades:

Pré-processamento das imagens e textos para adequação ao modelo CLIP.

Validação da qualidade dos embeddings gerados (analisar se conseguimos identificar os produtos com descrições textuais)

### Identificação do Subespaço de Cor

#### Teste com PCA na Descrição da Cor

Descrição: Aplicar Análise de Componentes Principais (PCA) nos embeddings gerados a partir das descrições de cor para identificar padrões e variações cromáticas.

  

Atividades:

Extração das descrições de cor das descrições textuais dos produtos.

Geração dos embeddings correspondentes.

Aplicação do PCA para redução de dimensionalidade e identificação de componentes principais relacionados à cor.

  

  

##### Inclusão de Cores Sólidas (Imagens)

Descrição: Incluir embeddings gerados a partir de imagens de cores sólidas para enriquecer a representação cromática.

  

  

Atividades:

Criação de imagens com cores puras correspondentes às cores presentes nos produtos.

Geração dos embeddings dessas imagens.

Integração desses embeddings com os embeddings dos produtos e repetição do teste de PCA.

  

  

##### Teste com PLS com a Cor como Target

Descrição: Utilizar Partial Least Squares (PLS) para definir a cor como variável target e ajustar os embeddings para maximizar a correlação com os valores de cor.

  

  

Atividades:

Definição das variáveis de cor como targets a partir das descrições textuais
  
Aplicação do PLS nos embeddings para identificar direções que melhor representam a variação de cor.

Comparação dos resultados com os obtidos pelo PCA.

  

  

#### Ponderação dos Subespaços

Descrição: Avaliar e ajustar a importância relativa de cada subespaço (cor, estampa, modelagem) na representação final dos embeddings.
   

Atividades:

Análise da variância explicada por cada subespaço.  

Ajuste de pesos para cada característica conforme a relevância desejada.

Testes de desempenho da aplicação com diferentes ponderações.

  

### Identificação dos outros Subespaços

Explorar diferentes técnicas e abordagens, usando o conhecimento experimental adquirido no processo de identificar o subespaço da cor, para identificar os subespaços de estampa e modelagem correspondentes ao produto.

  

## Pontos a Considerar

5.1 Necessidade de Fine-Tuning do Modelo  

Descrição: Avaliar se é necessário realizar um fine-tuning do modelo CLIP com um dataset específico para melhorar a representação das características customizáveis.
  

Atividades:

Análise da performance do CLIP pré-treinado nos dados do projeto.

Realização de fine-tuning se a performance não atender aos requisitos.

Reavaliação dos embeddings após o fine-tuning.

  
  

## Resultados Esperados

Desenvolvimento de Embeddings Eficientes: Criação de embeddings que representem de forma eficaz as características de cor, estampa e modelagem dos produtos.
  

Identificação de Subespaços Significativos: Capacidade de isolar e manipular subespaços específicos para cada característica, permitindo recomendações personalizadas.


Aplicação Funcional: Uma aplicação funcional que receba fotos ou descrições textuais de uma roupa e retorne imagens de produtos semelhantes com critérios customizáveis, como priorizar a cor ou combinar diferentes características (exemplo: rotornar o produto com a mesma modelagem mas em uma cor diferente).

  

## Aplicação Final

  

### Funcionalidades

Entrada de Dados:

  

Upload de fotos de produtos.

  

Inserção de descrições textuais.

  

Personalização de Busca:

  

  

Ajuste de ênfase em características específicas (cor, estampa, modelagem).

  
  

Resultados:

  

Exibição de produtos similares conforme os critérios definidos.

  

Opções de filtragem e ordenação dos resultados.

  

  

## Conclusão

  

Este projeto visa criar uma solução inovadora para o reconhecimento de produtos similares com base em características personalizáveis, utilizando técnicas avançadas de machine learning e modelos de embedding como o CLIP. Através de uma abordagem estruturada e detalhada, espera-se desenvolver uma aplicação robusta que atenda às necessidades do usuário final e proporcione uma experiência de busca e recomendação de produtos mais eficiente e personalizada.