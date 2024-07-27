
**Sobre o Projeto PyShoes**

Meu nome é Pedro Vitor, sou estudante do primeiro período (2024.1) de Bacharelado em Sistemas de Informação (BSI) na UFRN de Caicó. Este é um projeto para concluir o primeiro semestre, ministrado pelo professor Flavius Gorgônio. O sistema se chama PyShoes e é um gerenciador de lojas de calçados em Python, utilizando banco de dados em Pickle. O objetivo é implementar uma solução logística que auxilie na gestão de estoque de uma loja, cadastrando, verificando e administrando os calçados. Além disso, o sistema também cuida do cadastro de clientes, funcionários e gerenciamento das vendas.

**Funções do Sistema:**

No menu principal, você encontra três partes principais do sistema:

1. **Vendas**:
  
   *1* - **Vender Produto**: Selecione o produto através do código; em siguida os cpfs de cliente e vendedor são inseridos e verificados. Se o cpf do cliente for validado, mas não constar no banco de dados, um novo cadastro é acionado instantaneamente. Por fim, se o código compor mais de 1 produto, todos serão listados para que possa escolher o número do produto específico.

   *2*- **Checar Venda**: Exibe os dados mais importantes da venda, como nome do produto, valor, identificação dos vendedores e clientes, data da venda, etc. Código do produto, CPF do cliente ou CPF do vendedor são parâmetros que podem ser utilizados para encontar as vendas.
   - *1*- **Editar Venda**: Permite trocar o produto vendido, o cliente e o funcionário.
   - *2*- **Deletar Venda**: Exclui a venda completamente e permanetimente.
   
     *Nota: Toda manipulação de vendas afeta diretamente alguns atributos dos produtos, clientes e vendedores, como quantidade do produto, compras totais do cliente, vendas totais do vendedor e até a comissão do funcionário. Quando uma alteração é feita na venda, uma nova data aparecerá junto à anterior, indicando quando a venda foi alterada pela última vez. Se um produto que já foi vendido tiver quantidae igual à 0, ou seja, sem estoque, o símbolo "(S)" será estampado após o nome do produto na exibição da venda. Se um produto que já foi vendido for deletado do bando de dados, continuará sendo exibível; o símbolo "(D)" aparecerá na venda após o nome do produto deletado.*

   *3*- **Relatório**: Exibe todas as vendas do banco de dados.

2. **Produtos**:
   
    *1*- **Criar Produto**: Atribui diversos valores informativos ao produto, como nome, código, preço, tamanho, quantidade, marca, etc. Produtos podem ter o mesmo código, mas são diferenciados pelo atributo número, tornando a combinação código + número o identificador de um produto específico.
   
   *Nota: O número do produto é implementado automaticamente na criação com base nos números atuais de produtos que utilizam o mesmo código. Se tentar adicionar um produto com nome já existente no banco de dados, os atributos fixos serão puxados, como código, preço, marca, etc; porém valores diferentes para tamanho, cor e quantidade deverão ser preenchidos; o novo produto não vai ser salvo se suas informações forem idênticas a um já existente.*

   *2*- **Checar Produto**: Insira o código do produto e automaticamente todos os calçados de números diferentes com o determinado código serão listados.
   - *1*- **Editar Produto**: Permite editar todas as informações de um produto, exceto o código e o número.
   - *2*- **Deletar Produto**: Marca o produto como deletado.
   
     *Nota: Alterar valores fixos (nome, preço, local, marca) de um produto também irá atualizar os dados dos produtos com mesmo código. Se um produto marcado como deletador tiver suas informações reutilizadas ao cadastrar um produto novo, será reintregado podendo ter um novo valor para sua quantidade*

   *3* **Relatório**: Imprime todos os calçados do banco de dados em ordem alfabética.

5. **Pessoas**:
  
   *1*- **Adicionar Cliente**: O sistema pede o CPF do indivíduo e checa sua validade e existência no banco de dados. Se o CPF já existir, a criação é impedida, se válido, solicita os próximos dados (nome e telefone) também verificados. Após inserir os dados essenciais, o cliente é adicionado ao banco de dados.

   *2*- **Adicionar Vendedor**: O sistema pede inicialmente um CPF e checa sua validade. Se o CPF já existir como cliente, os dados de nome e telefone são puxados automaticamente para o cadastro de vendedor. Se o CPF já existir como vendedor, a criação é impedida. Todo vendedor é automaticamente registrado como cliente também.

   *3*- **Checar Pessoa**: Insira um CPF válido para exibir todos os cadastros encontrados (cliente e vendedor).
   - *1*- **Editar Pessoa**: Atualiza todos os cadastros encontrados, permitindo alterar nome e telefone.
   - *2*- **Excluir Pessoa**: Permite excluir ambos os cadastros ou somente o cadastro de vendedor.
   
      *Nota: Editar dados de clientes ou vendedores altera também os dados referenciados nas vendas. Se uma pessoa presente em alguma venda for deletada, seus dados continuarão a ser exibidos nas vendas com um símbolo "(D)", indicando que essa pessoa não está mais na base de dados. Se algum dado pessoal for alterado, o marcador "(E)" aparecerá na venda ao lado da informação mutada; uma nova data referente à edição também complementará a mudança. Clientes e vendedores possuem funções que calculam constantemente a receita de seus produtos comprados e vendidos. Os vendedores têm sua comissão calculada automaticamente com base nos produtos vendidos durante o mês (comissao igual à 3% do valor vendido no mês).*

   *4*- **Relatórios**:
    - *1*- **Clientes**: Lista todos os clientes em ordem alfabética.
    - *2*- **Funcionários**: Lista todos os funcionários em ordem alfabética.  