Nome: Rafael Gomes de Castro
Data: 04/12/2020

### Considerações iniciais
- O presente projeto foi desenvolvido com o intuito de ser avaliado no processo seletivo da Focus NF-e.
- Tal projeto foi desenvolvido em Python 3.8.2. A escolha dessa linguagem deve-se à facilidade de manipualação de arquivos e desenvolvimento rápido.
- O código foi desenvolvido e testado em ambiente Linux (Linux Mint 20).
- Toda a manipulação dos dados foi feita usando diretamente o sistema de arquivos.
- Não é necessária nenhuma alteração nos dados dos arquivos de entrada fornecidos. Apenas para evitar o uso de bibliotecas de terceiros, optei por corverter o arquivo Produtos.xlsx para o formato CSV (Produtos.csv). Tal conversão é feita externamente ao programa e encontra-se em "data/Produtos.csv".
	- Caso houvesse apenas 1 dia para realizar a tarefa, eu optaria por alterações manuais nas informações do arquivo Produtos.csv, deixando-o mais padronizado, e utilizaria um sevidor de banco de dados para agilizar as consultas. Acredito não ser uma boa ideia padronizar o arquivo exemplo.txt pois não seria uma técnica eficiente em produção, já que as mensagens provindas dos usuários necessitariam de padronização manual também.
- **Execução**: 
	- `$ git clone https://github.com/rafaelGomesCastro/focus_nfe.git`
	- `$ cd focus_nfe-main/`
	- `$ python3 src/main.py`

### Diretórios e arquivos
- data/:
	- data/exemplo.txt: arquivo contendo as solicitações dos clientes;
	- data/Produtos.csv: arquivo contendo as informações dos produtos em estoque convertido para CSV;
	- data/Produtos.xlsx: arquivo original contendo as informações dos produtos em estoque.
- src/:
	- src/main.py: script Python que lê os arquivos de entrada e gera o arquivo CSV resultante
- result/:
	- result/result.txt: resultado da execução do algoritmo. A cada execução, esse arquivo será sobrescrito.
- README.md: esse relatório.

### Metodologia
- Após uma análise dos dados, optei por selecionar as palavras-chaves de cada pedido e procurar na descrição dos produtos uma entrada que contenha tais palavras-chaves. Percebi que utilizando no máximo 3 palavras-chaves é o suficiente para indentificar cada produto.
- Inicialmente, fiz a leitura dos arquivos de entrada (data/exemplo.txt e data/Produtos.csv), bem como a limpeza dos dados. Tal limpeza compreende o processo de remoção de acentos e cedilhas; deixar todas as letras minúsculas; padrinizar unidades de medida (ex.: kg, g, und); remoção de sinais de pontuação, hífens e porcentagem; remoção de stopwords (de, e, com, em); remoção de espaços duplicados; remoção do plural das palavras. Após a leitura, os dados de entrada estarão armazenados em vetores distintos (uma para os dados do data/exemplo.txt e outro para os dados do data/Produtos.csv)
- Em seguida, criei um dicionário que armazena a frequência de aparição de cada palavra utilizada para descrever os produtos. Para cada pedido, utilizo esse dicionário para selecionar as 3 (três) palavras com menor frequência. Quanto menor a frequência de uma palavra, mais fácil de identificar o produto solicitado.
- Identificada a descrição do produto que corresponde ao pedido feito, extraí as informações necessárias (detalhadas na próxima seção desse relatório) e criei o arquivo de resultado.

### Resultado
- Ao final da execução, o script gera o arquivo "result/result.csv". Tal arquivo contém os seguintes campos:
	1. id_cliente: identificação numérica do cliente;
	2. nome_cliente: nome do cliente;
	3. desc_pedido: descrição do pedido;
	4. desc_estoque: descrição do estoque encontrado para cada um dos pedidos solicitados;
	5. fornecedor: nome do fornecedor do produto encontrado;
	6. preco: valor de cada produto;
	7. quantidade_solicitada: quantidade solicitada de cada produto;
	8. total: cálculo do valor a ser recebido por cada pedido.

### Decisões de implementação
- Palavras com erros de digitação e sem outra palavra que ajudasse na identificação: classifiquei-as como "Produto não encontrado" para não correr o risco de enviar ao cliente um produto errado;
- Mesmo produto, mesmo preço, mas fornecedores diferentes: optei por selecionar o primeiro fornecedor que aparece na busca;
- Pedidos sem especificação de quantidade: assumi que era equivalente a uma unidade (dependendo do produto, uma unidade pode ser 1kg, 300g, 1 maço, ...).
