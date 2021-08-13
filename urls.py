from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [

    # Index (Mostra o lucro total do Sistema)
    path('', views.index, name='index'),

    # Cadastra novo cliente (Insere um novo cliente na tabela)
    path('cadastro/', views.cadastro, name='cadastro'),
    # Login do cliente (Verifica se os campos usuario e senha correspondem a uma linha na tabela)
    path('cliente/login/', views.loginCliente, name='login-cliente'),
    # Login do usuario (Verifica se os campos usuario e senha correspondem a uma linha na tabela)
    path('fornecedor/login/', views.loginFornecedor, name='login-fornecedor'),

    # Altera para 'None' o valor de cliente ID guardado na cache do navegador
    path('cliente/logout', views.logoutCliente, name='logout-cliente'),
    # Altera para 'None' o valor de fornecedor ID guardado na cache do navegador
    path('fornecedor/logout', views.logoutFornecedor, name='logout-fornecedor'),

    # Página principal do cliente (Mostra os produtos a serem vendidos)
    path('cliente/', views.clienteView, name='cliente-view'),
    # Página do carrinho do cliente (Mostra os itens inseridos no carrinho do cliente)
    path('cliente/carrinho/', views.carrinhoView, name='carrinho'),
    # Página do histórico de compras (Mostra os itens comprados pelo cliente)
    path('cliente/historico/', views.historicoView, name='historico'),

    # Página de descrição do produto (Mostra os dados referente a um produto)
    path('produto/<int:id>', views.produtoView, name='desc-produto'),
    # Compra do produto (Insere uma nova compra do produto <int:id> para o cliente ID logado)
    path('produto/compra/<int:id>', views.compraView, name='compra-produto'),
    # Adição do produto ao carrinho (Insere um novo carrinho com produto <int:id> e cliente ID logado)
    path('produto/addCarrinho/<int:id>', views.adicionarCarrinho, name='adicionar-carrinho'),
    # Compra todos os itens presentes no carrinho (Insere novas compras do produtos no carrinho para o cliente ID logado) 
    path('produto/compra/carrinho', views.compraCarrinho, name='compra-carrinho'),
    # Deleta um produto do carrinho (Deleta um produto do carrinho do cliente ID logado)
    path('delete/carrinho/<int:id>', views.deleteCarrinho, name='delete-carrinho'),

    # Página do fornecedor (Mostra os produtos anunciados, produtos vendidos e a carteira do fornecedor ID logado)
    path('fornecedor/', views.fornecedorView, name='fornecedor-view'),
    # Página de adicionar um novo produto (Insere um novo produto na tabela)
    path('fornecedor/addProduto', views.novoProdutoView, name='novo-produto'),
    # Página de atualizar um novo produto (Atualiza a linha do produto <int:id> na tabela)
    path('fornecedor/editProduto/<int:id>', views.editProdutoView, name='edit-produto'),
]

urlpatterns += staticfiles_urlpatterns()