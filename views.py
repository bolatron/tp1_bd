from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Cliente, Produto, Compra
from .forms import ClienteModelForm

from django.db import connection

def assertLogin_cliente(func):
    def inner(request, *args, **kwargs):
        if request.session.get('cliente-id') is None: 
            return redirect('/cliente/login')
        else:
            return func(request, *args, **kwargs)
    return inner


def assertLogin_fornecedor(func):
    def inner(request, *args, **kwargs):
        if request.session.get('fornecedor-id') is None: 
            return redirect('/fornecedor/login')
        else:
            return func(request, *args, **kwargs)
    return inner


def index(request):

    cursor = connection.cursor()

    cursor.execute('''  SELECT SUM(lucro)
                        FROM web_app_compra''')

    lucro_total = cursor.fetchone()[0]

    return render(request, 'tp_web/index.html', {'lucro': lucro_total})

def loginCliente(request):

    if request.method == 'POST':

        usuario = request.POST['usuario']
        senha = request.POST['senha']

        cursor = connection.cursor()
        cursor.execute('''  SELECT id
                            FROM web_app_cliente
                            WHERE web_app_cliente.usuario=%s AND web_app_cliente.senha=%s''', [usuario, senha])

        usuario_autenticado = cursor.fetchone() 
        cursor.close()
        
        request.session['cliente-id'] = usuario_autenticado

        if usuario_autenticado != None:
            return redirect('/cliente')

    return render(request, 'tp_web/login-cliente.html', {})


def loginFornecedor(request):

    if request.method == 'POST':

        usuario = request.POST['usuario']
        senha = request.POST['senha']

        cursor = connection.cursor()
        cursor.execute('''  SELECT id
                            FROM web_app_fornecedor
                            WHERE web_app_fornecedor.usuario=%s AND web_app_fornecedor.senha=%s''', [usuario, senha])

        usuario_autenticado = cursor.fetchone() 
        cursor.close()
        
        request.session['fornecedor-id'] = usuario_autenticado

        if usuario_autenticado != None:
            return redirect('/fornecedor')

    return render(request, 'tp_web/login-fornecedor.html', {})


def logoutCliente(request):
    request.session['cliente-id'] = None
    return redirect('/cliente/login')


def logoutFornecedor(request):
    request.session['fornecedor-id'] = None
    return redirect('/fornecedor/login')


def cadastro(request):

    form = ClienteModelForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
        return redirect('/cliente/login')
    
    return render(request, 'tp_web/cadastro_cliente.html', context)


@assertLogin_cliente
def clienteView(request):

    cursor = connection.cursor()

    if request.method == "POST":

        try:
            nome_produto = request.POST['p']
        except:
            nome_produto = []

        try:
            categoria = request.POST['tipo']
        except:
            categoria = []


        if nome_produto != []:
            cursor.execute('''  SELECT * 
                                FROM web_app_produto 
                                WHERE web_app_produto.nome LIKE %s AND (web_app_produto.quantidade >= 1)''', ['%' + nome_produto + '%'])

        if categoria != []:
            cursor.execute('''  SELECT *
                                FROM web_app_produto 
                                WHERE web_app_produto.tipo=%s AND (web_app_produto.quantidade >= 1)''', [categoria])

        produtos_list = cursor.fetchall()

        a = ['id', 'nome', 'descricao', 'preco', 'quantidade', 'tipo', 'f_fornecedor', 'imagem']

        prod_list =[]
        for p in produtos_list:
            prod_list.append(dict(zip(a, p)))

        context = {'produtos_list': prod_list}

    else:
        cursor.execute('''  SELECT *
                            FROM web_app_produto 
                            JOIN web_app_fornecedor
                            ON web_app_produto.f_fornecedor_id=web_app_fornecedor.id
                            WHERE (web_app_produto.quantidade >= 1)''')
    
        produtos_list = cursor.fetchall()

        a = ['id', 'nome', 'descricao', 'preco', 'quantidade', 'tipo', 'f_fornecedor', 'imagem', 'cid', 'senha', 'carteira', 'pnome', 'unome', 'fadmin', 'usuario']

        prod_list =[]
        for p in produtos_list:
            prod_list.append(dict(zip(a, p)))

        context = {'produtos_list': prod_list}

    cursor.close()
    return render(request, 'tp_web/cliente_view.html', context)


@assertLogin_cliente
def produtoView(request, id):

    cursor = connection.cursor()
    cursor.execute('''  SELECT P.id, P.nome, P.descricao, P.imagem, P.preco, P.quantidade, F.usuario
                        FROM web_app_produto AS P
                        JOIN web_app_fornecedor AS F
                        ON P.f_fornecedor_id=F.id
                        WHERE P.id=%s''', [id])

    produto = cursor.fetchone()
    cursor.close()

    a = ['id', 'nome', 'descricao', 'imagem', 'preco', 'quantidade', 'f_fornecedor']

    prod = dict(zip(a, produto))

    context = {'produto': prod}

    return render(request, 'tp_web/produto-desc.html', context)


@assertLogin_cliente
def compraView(request, id):

    cursor = connection.cursor()

    cursor.execute('''  INSERT INTO web_app_compra (data, quantidade, lucro, fproduto_id, fcliente_id)
                        SELECT  %s AS data,
                                '1' AS quantidade,
                                0.01*P.preco AS lucro,
                                %s AS fproduto_id,
                                %s AS fcliente_id
                        FROM web_app_produto AS P
                        WHERE P.id=%s ''', [timezone.now(), id, request.session['cliente-id'][0], id])

    cursor.execute('''  UPDATE web_app_produto
                        SET quantidade = quantidade - 1
                        WHERE web_app_produto.id=%s''', [id])

    cursor.execute('''  SELECT preco, f_fornecedor_id
                        FROM web_app_produto
                        WHERE web_app_produto.id=%s''', [id])

    result = cursor.fetchone()

    cursor.execute('''  UPDATE web_app_fornecedor
                        SET carteira = carteira + %s*0.99
                        WHERE web_app_fornecedor.id=%s ''', [result[0], result[1]])

    cursor.close()

    return redirect('/cliente')


@assertLogin_cliente
def carrinhoView(request):

    if request.method == 'POST':
        print(request.POST)

    cursor = connection.cursor()
    cursor.execute('''  SELECT nome, descricao, imagem, preco, quantidade, tipo, usuario, p.id
                        FROM web_app_produto AS p
                        JOIN (  SELECT *
                                FROM web_app_cliente AS c JOIN web_app_carrinho AS car
                                ON c.id=car.fcliente_id 
                                WHERE car.fcliente_id=%s) AS T ON (p.id=T.fproduto_id)''', [request.session['cliente-id'][0]])

    carrinho_list = cursor.fetchall()
    cursor.close()

    a = ['nome', 'descricao', 'imagem', 'preco', 'quantidade', 'tipo', 'usuario', 'pid']

    carr_list = []
    for item in carrinho_list:
        carr_list.append(dict(zip(a, item)))

    total = 0.0
    for produto in carr_list:
        total += produto['preco']

    context = {'carrinho_list': carr_list, 'total': total}

    return render(request, 'tp_web/carrinho.html', context)


@assertLogin_cliente
def historicoView(request):
    cursor = connection.cursor()
    cursor.execute('''  SELECT nome, imagem, preco, data, p.id, T.quantidade
                        FROM web_app_produto AS p
                        JOIN (  SELECT *
                                FROM web_app_cliente AS c JOIN web_app_compra AS com
                                ON c.id=com.fcliente_id 
                                WHERE com.fcliente_id=%s) AS T ON (p.id=T.fproduto_id)''', [request.session['cliente-id'][0]])

    historico_list = cursor.fetchall()
    cursor.close()

    a = ['nome', 'imagem', 'preco', 'data', 'pid', 'quantidade']

    comp_list = []
    for item in historico_list:
        comp_list.append(dict(zip(a, item)))

    context = {'historico_list': comp_list}

    return render(request, 'tp_web/historico.html', context)


@assertLogin_cliente
def deleteCarrinho(request, id):

    cursor = connection.cursor()
    cursor.execute('''  DELETE FROM web_app_carrinho
                        WHERE web_app_carrinho.fcliente_id=%s AND web_app_carrinho.fproduto_id=%s''', [request.session['cliente-id'][0], id])

    cursor.close()

    return redirect('/cliente/carrinho')


@assertLogin_cliente
def compraCarrinho(request):

    cursor = connection.cursor()
    cursor.execute('''  INSERT INTO web_app_compra (data, quantidade, lucro, fproduto_id, fcliente_id)
                        SELECT  %s AS data,
                                '1' AS quantidade,
                                0.01*P.preco AS lucro,
                                C.fproduto_id,
                                %s AS fcliente_id
                        FROM web_app_carrinho AS C
                        JOIN web_app_produto AS P
                        ON C.fproduto_id=P.id AND C.fcliente_id=%s;''', [timezone.now(), request.session['cliente-id'][0], request.session['cliente-id'][0]])

    cursor.execute('''  SELECT fproduto_id
                        FROM web_app_carrinho
                        WHERE web_app_carrinho.fcliente_id=%s''', [request.session['cliente-id'][0]])

    ids_produto = cursor.fetchall()

    for id in ids_produto:
        cursor.execute('''  UPDATE web_app_produto
                            SET quantidade = quantidade - 1
                            WHERE web_app_produto.id=%s''', [id[0]])

        cursor.execute('''  SELECT preco, f_fornecedor_id
                            FROM web_app_produto
                            WHERE web_app_produto.id=%s''', [id[0]])

        result = cursor.fetchone()

        cursor.execute('''  UPDATE web_app_fornecedor
                            SET carteira = carteira + %s*0.99
                            WHERE web_app_fornecedor.id=%s ''', [result[0], result[1]])

    cursor.execute('''  DELETE FROM web_app_carrinho
                        WHERE web_app_carrinho.fcliente_id=%s''', [request.session['cliente-id'][0]])

    cursor.close()

    return redirect('/cliente')


@assertLogin_cliente
def adicionarCarrinho(request, id):
    
    cursor = connection.cursor()
    cursor.execute('''  INSERT INTO web_app_carrinho (fproduto_id, fcliente_id)
                        SELECT P.id, %s AS fcliente_id
                        FROM web_app_produto AS P
                        WHERE P.id=%s''', [request.session['cliente-id'][0], id])

    cursor.close()

    return redirect('/cliente/carrinho')


@assertLogin_fornecedor
def novoProdutoView(request):

    CASA_LAR = "CASA"
    ELETRONICO = "ELET"
    INFANTIL = "INFA"
    ROUPA = "ROUP"

    TIPOS_PRODUTO = [
        (CASA_LAR, 'Casa/Lar'),
        (ELETRONICO, 'Eletrônicos'),
        (INFANTIL, 'Produtos Infantis'),
        (ROUPA, 'Roupas'),
    ]

    context = {}
    cursor = connection.cursor()

    if request.method == 'POST':

        nome = request.POST['nome']
        descricao = request.POST['descricao']
        imagem = request.FILES['imagem'].name
        preco = request.POST['preco']
        quantidade = request.POST['quantidade']
        tipo = request.POST['tipo']

        cursor.execute('''  INSERT INTO web_app_produto (nome, descricao, imagem, preco, quantidade, tipo, f_fornecedor_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)''', [nome, descricao, imagem, preco, quantidade, tipo, request.session['fornecedor-id'][0]])

        return redirect('/fornecedor')

    else:
        cursor.execute('''  SELECT usuario
                            FROM web_app_fornecedor''')

        fornecedores = cursor.fetchall()

        cursor.close()

        context = {'fornecedores': fornecedores, 'tipos_produto': TIPOS_PRODUTO}
    
    return render(request, 'tp_web/novo-produto.html', context)


@assertLogin_fornecedor
def editProdutoView(request, id):

    CASA_LAR = "CASA"
    ELETRONICO = "ELET"
    INFANTIL = "INFA"
    ROUPA = "ROUP"

    TIPOS_PRODUTO = {
        CASA_LAR: 'Casa/Lar',
        ELETRONICO: 'Eletrônicos',
        INFANTIL: 'Produtos Infantis',
        ROUPA: 'Roupas',
    }

    context = {}
    cursor = connection.cursor()

    if request.method == 'POST':

        nome = request.POST['nome']
        descricao = request.POST['descricao']
        imagem = request.FILES['imagem'].name
        preco = request.POST['preco']
        quantidade = request.POST['quantidade']
        tipo = request.POST['tipo']

        cursor.execute('''  UPDATE web_app_produto
                            SET nome = %s,
                                descricao = %s,
                                imagem = %s,
                                preco = %s,
                                quantidade = %s,
                                tipo = %s,
                                f_fornecedor_id = %s
                            WHERE web_app_produto.id=%s''', [nome, descricao, imagem, preco, quantidade, tipo, request.session['fornecedor-id'][0], id])

        return redirect('/fornecedor')

    else:
        cursor.execute('''  SELECT usuario
                            FROM web_app_fornecedor''')

        fornecedores = cursor.fetchall()

        cursor.execute('''  SELECT *
                            FROM web_app_produto
                            WHERE web_app_produto.id=%s''', [id])

        produto = cursor.fetchone()
        cursor.close()
        
        a = ['id', 'nome', 'descricao', 'imagem', 'preco', 'quantidade', 'f_fornecedor_id', 'tipo']

        print(produto)

        context = {'fornecedores': fornecedores, 'tipos_produto': TIPOS_PRODUTO, 'produto': dict(zip(a, produto))}
    
    return render(request, 'tp_web/edit-produto.html', context)


@assertLogin_fornecedor
def fornecedorView(request):

    cursor = connection.cursor()

    cursor.execute('''  SELECT carteira
                        FROM web_app_fornecedor AS F
                        WHERE F.id=%s''', [request.session['fornecedor-id'][0]])
    
    carteira = cursor.fetchone()[0]

    if request.method == 'POST':
        try:
            if request.POST['produtos-vendidos'] == 'Produtos vendidos':
                produtos_vendidos = True
        except:
            produtos_vendidos = False
        
        try:
            if request.POST['produtos-anunciados'] == 'Produtos anunciados':
                produtos_anunciados = True
        except:
            produtos_anunciados = False
    else:
        produtos_vendidos = False
        produtos_anunciados = True

    if (produtos_anunciados == True):
        cursor.execute('''  SELECT *
                            FROM web_app_produto AS P
                            WHERE P.f_fornecedor_id=%s''', [request.session['fornecedor-id'][0]])

        produtos_list = cursor.fetchall()

        a = ['pid', 'nome', 'descricao', 'preco', 'quantidade', 'tipo', 'fid', 'imagem']

        prod_list = []
        for item in produtos_list:
            prod_list.append(dict(zip(a, item)))

        context = { 'produtos_list': prod_list,
                    'carteira': carteira}

    if (produtos_vendidos == True):
        cursor.execute('''  SELECT C.fcliente_id, C.data, C.quantidade, P.preco-C.lucro, P.id, P.nome, P.descricao, P.imagem, P.preco, P.tipo, P.f_fornecedor_id
                            FROM web_app_compra AS C
                            JOIN web_app_produto AS P
                            WHERE C.fproduto_id=P.id AND P.f_fornecedor_id=%s''', [request.session['fornecedor-id'][0]])

        produtos_list = cursor.fetchall()

        a = ['cid', 'data', 'quantidade_comprada', 'lucro', 'pid', 'nome', 'descricao', 'imagem', 'preco', 'tipo', 'fid']

        prod_list = []
        for item in produtos_list:
            prod_list.append(dict(zip(a, item)))

        context = { 'produtos_list': prod_list, 
                    'pa': produtos_anunciados,
                    'produtos_vendidos': produtos_vendidos,
                    'carteira': carteira
                    }

    cursor.close()
    return render(request, 'tp_web/fornecedor_view.html', context)