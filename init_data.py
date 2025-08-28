from src.models.user import db
from src.models.cliente import Cliente
from src.models.item import Item
from src.models.combo import Combo, ComboItem

def init_sample_data():
    """Inicializa dados de exemplo no banco de dados"""
    
    # Verificar se já existem dados
    if Cliente.query.first():
        return
    
    # Criar clientes de exemplo
    cliente1 = Cliente(
        cnpj='12.345.678/0001-90',
        nome='Empresa ABC Ltda',
        limite_credito=10000.0,
        limite_disponivel=8500.0
    )
    
    cliente2 = Cliente(
        cnpj='98.765.432/0001-10',
        nome='Comércio XYZ S.A.',
        limite_credito=15000.0,
        limite_disponivel=12000.0
    )
    
    db.session.add(cliente1)
    db.session.add(cliente2)
    
    # Criar itens de exemplo
    itens = [
        Item(nome='Produto A', descricao='Descrição do Produto A', preco=25.90, quantidade_promocao=10),
        Item(nome='Produto B', descricao='Descrição do Produto B', preco=45.50, quantidade_promocao=5),
        Item(nome='Produto C', descricao='Descrição do Produto C', preco=15.75, quantidade_promocao=20),
        Item(nome='Produto D', descricao='Descrição do Produto D', preco=89.90, quantidade_promocao=3),
        Item(nome='Produto E', descricao='Descrição do Produto E', preco=12.30, quantidade_promocao=15),
        Item(nome='Produto F', descricao='Descrição do Produto F', preco=67.80, quantidade_promocao=8)
    ]
    
    for item in itens:
        db.session.add(item)
    
    # Commit para obter os IDs
    db.session.commit()
    
    # Criar combos de exemplo
    combo1 = Combo(
        nome='Combo Básico',
        descricao='Combinação ideal para iniciantes',
        preco_total=85.00
    )
    
    combo2 = Combo(
        nome='Combo Premium',
        descricao='Nossa melhor seleção de produtos',
        preco_total=150.00
    )
    
    db.session.add(combo1)
    db.session.add(combo2)
    db.session.commit()
    
    # Adicionar itens aos combos
    combo_item1 = ComboItem(combo_id=combo1.id, item_id=itens[0].id, quantidade=2)
    combo_item2 = ComboItem(combo_id=combo1.id, item_id=itens[2].id, quantidade=3)
    
    combo_item3 = ComboItem(combo_id=combo2.id, item_id=itens[1].id, quantidade=1)
    combo_item4 = ComboItem(combo_id=combo2.id, item_id=itens[3].id, quantidade=1)
    combo_item5 = ComboItem(combo_id=combo2.id, item_id=itens[5].id, quantidade=1)
    
    db.session.add_all([combo_item1, combo_item2, combo_item3, combo_item4, combo_item5])
    db.session.commit()
    
    print("Dados de exemplo inicializados com sucesso!")

