# Farmarcas - Sistema de Pedidos Online

## 📋 Visão Geral

O **Farmarcas** é um sistema web completo para gestão de pedidos de produtos farmacêuticos, desenvolvido em Python com Flask. O sistema permite que clientes realizem pedidos online, gerenciem carrinhos de compras e acompanhem suas promoções especiais.

### 🎯 Funcionalidades Principais

- **Autenticação de Clientes**: Login via CNPJ com integração ao banco Oracle
- **Catálogo de Produtos**: Visualização de produtos em promoção por laboratório
- **Sistema de Carrinho**: Adição, remoção e gestão de itens no carrinho
- **Gestão de Pedidos**: Criação e acompanhamento de pedidos
- **Planos de Pagamento**: Integração com sistema de planos de pagamento do cliente
- **Controle de Crédito**: Validação de limite disponível do cliente
- **Interface Responsiva**: Design moderno e adaptável para diferentes dispositivos

## 🏗️ Arquitetura do Sistema

### Tecnologias Utilizadas

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Banco de Dados**:
  - PostgreSQL (produtos, pedidos, usuários)
  - Oracle Database (clientes, planos de pagamento)
- **Conectividade**: JDBC (JayDeBeApi) para Oracle
- **Autenticação**: Sessões Flask + LocalStorage

### Estrutura de Diretórios

```
src/
├── main.py                 # Arquivo principal da aplicação
├── config.py              # Configurações do sistema
├── oracle_connection.py   # Conexão com banco Oracle
├── init_data.py          # Dados iniciais para desenvolvimento
├── .env                  # Variáveis de ambiente
├── models/               # Modelos de dados
│   ├── user.py          # Modelo de usuário
│   ├── cliente.py       # Modelo de cliente (PostgreSQL)
│   ├── item.py          # Modelo de produto
│   ├── combo.py         # Modelo de combo de produtos
│   ├── pedido.py        # Modelo de pedido
│   ├── pedido_ol.py     # Modelo de pedido OL
│   ├── brinde.py        # Modelo de brinde
│   └── oracle_models.py # Modelos para Oracle
├── routes/               # Endpoints da API
│   ├── auth.py          # Autenticação e usuários
│   ├── user.py          # Gestão de usuários
│   ├── produtos.py      # Produtos e combos
│   ├── clientes.py      # Informações do cliente
│   ├── pedidos.py       # Gestão de pedidos
│   ├── pedido_ol.py     # Pedidos OL
│   └── brindes.py       # Gestão de brindes
├── static/               # Arquivos estáticos
│   ├── *.html          # Páginas do frontend
│   ├── style.css       # Estilos CSS
│   └── *.png           # Imagens e logos
└── database/
    └── ojdbc17.jar     # Driver JDBC Oracle
```

## 🗄️ Modelo de Dados

### PostgreSQL (Produtos e Pedidos)

#### Tabelas Principais

**users**
- `id` (Integer, PK)
- `username` (String, único)
- `email` (String, único)

**cliente**
- `id` (Integer, PK)
- `nome` (String)
- `cnpj` (String, único)
- `limite_credito` (Float)
- `limite_disponivel` (Float)

**item**
- `id` (Integer)
- `id_cont` (Integer, PK)
- `nome` (String)
- `descricao` (Text)
- `preco` (Float)
- `quantidade_promocao` (Integer)
- `quantidade_max_promocao` (Integer)
- `estoque` (Integer)
- `imagem_url` (String)
- `ativo` (Boolean)
- `destaque` (Boolean)
- `promocao` (Boolean)
- `destaque_texto` (Text)
- `laboratorio` (String)
- `filial` (Integer)

**combo**
- `id` (Integer, PK)
- `nome` (String)
- `descricao` (Text)
- `preco_total` (Float)
- `imagem_url` (String)
- `ativo` (Boolean)

**combo_item**
- `id` (Integer, PK)
- `combo_id` (Integer, FK)
- `item_id` (Integer, FK)
- `quantidade` (Integer)

**pedido**
- `id` (Integer, PK)
- `cliente_id` (Integer)
- `data_pedido` (DateTime)
- `observacoes` (Text)
- `valor_total` (Float)
- `valor_total_desconto` (Float)
- `plano_pagamento` (String)
- `status` (String)
- `responsavel_id` (Integer)
- `cliente_nome` (String)

**item_pedido**
- `id` (Integer, PK)
- `pedido_id` (Integer, FK)
- `item_id` (Integer, FK)
- `quantidade` (Integer)
- `preco_unitario` (Float)
- `subtotal` (Float)
- `observacoes` (Text)

### Oracle Database (Clientes e Planos)

#### Views Utilizadas

**VW_MEGAFEIRAO_LOGCLI**
- Dados dos clientes (CNPJ, nome, limites, filial)

**VW_MEGAFEIRAO_PLPAG**
- Planos de pagamento disponíveis por cliente

## 🔌 API Endpoints

### Autenticação (`/api/auth/`)

#### `POST /api/auth/login`
Autenticação de cliente via CNPJ
```json
{
  "cnpj": "12.345.678/0001-90"
}
```

#### `POST /api/auth/logout`
Logout do cliente

#### `POST /api/auth/login/manager`
Login do administrador
```json
{
  "id": 1,
  "username": "admin"
}
```

### Produtos (`/api/produtos/`)

#### `GET /api/produtos/itens`
Lista todos os itens ativos

#### `GET /api/produtos/itens/{item_id}`
Detalhes de um item específico

#### `GET /api/produtos/combos`
Lista todos os combos ativos

#### `GET /api/produtos/combos/{combo_id}`
Detalhes de um combo específico

### Clientes (`/api/clientes/`)

#### `GET /api/clientes/cliente/info`
Informações do cliente logado

#### `GET /api/clientes/cliente/planos-pagamento`
Planos de pagamento disponíveis

### Pedidos (`/api/pedidos/`)

#### `POST /api/pedidos/pedidos`
Cria um novo pedido
```json
{
  "itens": [
    {
      "id": 1,
      "quantidade": 10,
      "tipo": "item"
    }
  ],
  "plano_pagamento": "1",
  "observacoes": "Pedido urgente",
  "responsavel_id": 1,
  "cliente_nome": "Empresa ABC",
  "valor_total_desconto": 100.00
}
```

#### `GET /api/pedidos/pedidos/{cliente_id}`
Lista pedidos de um cliente

#### `GET /api/pedidos/pedidos`
Lista todos os pedidos

#### `GET /api/pedidos/pedidos/{pedido_id}`
Detalhes de um pedido específico

### Pedidos OL (`/api/pedido-ol/`)

#### `POST /api/pedido-ol/pedido-ol`
Cria um pedido OL
```json
{
  "cnpj_codcli": 12345,
  "laboratorio": "Lab A",
  "representante_ol": "João Silva",
  "valor_pedido": 1000.00,
  "responsavel": "Maria Santos",
  "brinde_id": 1,
  "quantidade": 5
}
```

### Brindes (`/api/brindes/`)

#### `GET /api/brindes/brindes`
Lista todos os brindes

### Usuários (`/api/user/`)

#### `GET /api/user/users`
Lista todos os usuários

#### `POST /api/user/users`
Cria um novo usuário

#### `GET /api/user/users/{user_id}`
Detalhes de um usuário

#### `PUT /api/user/users/{user_id}`
Atualiza um usuário

#### `DELETE /api/user/users/{user_id}`
Remove um usuário

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- PostgreSQL
- Oracle Database (com driver JDBC)
- Java 17+ (para JDBC)

### 1. Clonagem e Dependências

```bash
# Instalar dependências Python
pip install flask flask-cors flask-sqlalchemy python-dotenv jaydebeapi jpype1 psycopg2-binary
```

### 2. Configuração do Banco de Dados

#### PostgreSQL
```sql
CREATE DATABASE app;
CREATE USER user WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE app TO user;
```

#### Oracle
Certifique-se de que o banco Oracle esteja acessível e as credenciais estejam corretas no arquivo `.env`.

### 3. Configuração das Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto conforme .envexample:

```env
# PostgreSQL
POSTGRE_HOST=localhost
POSTGRE_USER=seu_usuario
POSTGRE_DB=seu_banco
POSTGRE_PASSWORD=sua_senha

# Oracle
ORACLE_HOST=192.168.xx.xxx
ORACLE_PORT=xxxx
ORACLE_SERVICE=WINT
ORACLE_USER=xxxxxx
ORACLE_PASSWORD=xxxxxx
JDBC_JAR_PATH=src/database/ojdbc17.jar
JDBC_URL=jdbc:oracle:thin:@//ORACLE_HOST:ORACLE_PORT/ORACLE_SERVICE
JDBC_DRIVER_NAME=oracle.jdbc.driver.OracleDriver

# Java
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/bin/java
```

### 4. Inicialização da Aplicação

```bash
# Executar a aplicação
python main.py

# A aplicação estará disponível em:
# http://localhost:5001
```

## 📱 Interface do Usuário

### Páginas Principais

1. **Login** (`index.html`)
   - Autenticação via CNPJ
   - Validação de cliente no Oracle

2. **Página Inicial** (`home.html`)
   - Catálogo de produtos em promoção
   - Filtros por laboratório
   - Sistema de carrinho

3. **Página Mix** (`mix-home.html`)
   - Produtos não promocionais
   - Visualização alternativa

4. **Checkout** (`checkout.html`)
   - Finalização do pedido
   - Seleção de plano de pagamento
   - Confirmação do pedido

5. **Gerenciamento** (`manage.html`, `manage-home.html`)
   - Interface administrativa
   - Gestão de pedidos e produtos

### Funcionalidades do Frontend

- **Sistema de Carrinho**: Adição/remover itens, cálculo automático de totais
- **Filtros Dinâmicos**: Por laboratório e busca por nome
- **Validação em Tempo Real**: Quantidades mínimas/máximas
- **Responsividade**: Adaptável para desktop e mobile
- **Persistência**: Dados salvos no LocalStorage

## 🔧 Funcionalidades Avançadas

### Sistema de Descontos Automáticos

- **3%** de desconto para pedidos acima de R$ 2.000,00
- **4%** de desconto para pedidos acima de R$ 4.000,00
- **5%** de desconto para pedidos acima de R$ 5.000,00
- **10% adicional** para produtos específicos (CATARINENSE, GEOLAB, etc.)

### Controle de Crédito

- Validação automática do limite disponível
- Bloqueio de pedidos que excedem o crédito
- Status automático: APROVADO/BLOQUEADO

### Gestão de Estoque

- Controle de quantidade em estoque
- Validação de disponibilidade antes da venda
- Atualização automática do estoque após pedido

### Sistema Multi-Filial

- Suporte a diferentes filiais (MG/BA)
- Preços diferenciados por filial
- Produtos específicos por localização

## 🔒 Segurança

- **Autenticação**: Validação via CNPJ no banco Oracle
- **Sessões**: Controle de sessão do lado servidor
- **CORS**: Configurado para permitir origens específicas
- **Validação**: Sanitização de dados de entrada
- **Logs**: Registro detalhado de operações

## 📊 Monitoramento e Logs

O sistema inclui logging abrangente:

- Conexões com bancos de dados
- Operações de autenticação
- Criação de pedidos
- Erros e exceções
- Operações administrativas

## 🚀 Deploy

### Produção

```bash
# Configurar variáveis de produção no .env
# Configurar servidor web (nginx/apache)
# Configurar SSL/TLS
# Configurar monitoramento
```

### Docker (Recomendado)

```dockerfile
FROM python:3.9-slim-bullseye

# Instalar Java
RUN apt-get update && apt-get install -y default-jre

# Copiar arquivos
COPY . /app
WORKDIR /app

# Instalar dependências
RUN pip install -r requirements.txt

# Expor porta
EXPOSE 5001

# Executar
CMD ["python", "src/main.py"]
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de Conexão Oracle**
   - Verificar credenciais no `.env`
   - Confirmar disponibilidade do banco Oracle
   - Verificar driver JDBC

2. **Erro de Conexão PostgreSQL**
   - Verificar credenciais e permissões
   - Confirmar que o banco está rodando

3. **Problemas de JVM**
   - Instalar Java 17+
   - Configurar JAVA_HOME corretamente
   - Verificar permissões do diretório

## 📈 Melhorias Futuras

- [ ] Implementar cache Redis
- [ ] Adicionar testes automatizados
- [ ] Implementar API REST completa
- [ ] Dashboard administrativo
- [ ] Notificações por email
- [ ] Integração com sistemas externos
- [ ] API mobile

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, entre em contato com a equipe de desenvolvimento.

---

**Farmarcas** - Sistema de Pedidos Online
Desenvolvido para otimizar o processo de vendas e gestão de pedidos farmacêuticos.
