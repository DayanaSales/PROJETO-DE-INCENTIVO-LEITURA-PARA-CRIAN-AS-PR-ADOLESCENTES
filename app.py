import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3

def create_table():
    """Cria uma tabela chamada 'books' no banco de dados SQLite.

    Esta função conecta-se ao banco de dados 'books.db', cria a tabela 'books' 
    se ela ainda não existir, e define os campos para armazenar informações sobre os livros, 
    como nome, autor, gênero, idade indicada e rating.

    Returns:
        None: A função não retorna nenhum valor, apenas interage com o banco de dados 
        se necessário.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            nome_autor TEXT,
            genero TEXT,
            idade_indicada INTEGER,
            rating REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_data():
    """Insere dados iniciais na tabela 'books' caso esteja vazia inicialmente.
    
    Conecta-se ao banco de dados 'books.db' e verifica se a tabela 'books' está vazia. 
    Se não estiver, a função encerra sem inserir novos dados. Caso esteja vazia, insere 
    uma lista predefinida de livros com seus respectivos nomes, autores, gêneros, idades 
    indicadas e classificações.

    Args:
        Nenhum.

    Returns:
        None: A função não retorna nenhum valor, apenas insere dados no banco de dados 
        se necessário.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM books')
    count = c.fetchone()[0]
    if count > 0:
        conn.commit()
        conn.close()
        return
    
    books = [
        ('Harry Potter e a Pedra Filosofal', 'J.K. Rowling', 'Fantasia', 10, 4.9),
        ('Percy Jackson e o Ladrão de Raios', 'Rick Riordan', 'Fantasia', 11, 4.8),
        ('Diário de um Banana', 'Jeff Kinney', 'Ficção', 10, 4.7),
        ('As Crônicas de Nárnia', 'C.S. Lewis', 'Fantasia', 12, 4.9),
        ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Ficção', 10, 4.8),
        ('Aventuras de Tom Sawyer', 'Mark Twain', 'Aventura', 11, 4.6),
        ('Charlotte\'s Web', 'E.B. White', 'Ficção', 9, 4.7),
        ('Matilda', 'Roald Dahl', 'Ficção', 10, 4.9),
        ('O Jardim Secreto', 'Frances Hodgson Burnett', 'Ficção', 11, 4.7),
        ('Anne de Green Gables', 'L.M. Montgomery', 'Ficção', 12, 4.8),
        ('Pax', 'Sara Pennypacker', 'Aventura', 10, 4.6),
        ('A Fantástica Fábrica de Chocolate', 'Roald Dahl', 'Ficção', 10, 4.8),
        ('Wonder - Auggie e Eu', 'R.J. Palacio', 'Ficção', 12, 4.9),
        ('O Menino do Pijama Listrado', 'John Boyne', 'Ficção', 12, 4.8),
        ('A Ilha do Tesouro', 'Robert Louis Stevenson', 'Aventura', 11, 4.7),
        ('O Mágico de Oz', 'L. Frank Baum', 'Fantasia', 9, 4.6),
        ('Histórias de Sherlock Holmes', 'Arthur Conan Doyle', 'Suspense', 12, 4.7),
        ('Os Goonies', 'Steven Spielberg', 'Aventura', 11, 4.7),
        ('A Guerra dos Botões', 'Louis Pergaud', 'Aventura', 10, 4.5),
        ('James e o Pêssego Gigante', 'Roald Dahl', 'Fantasia', 9, 4.7),
        ('A Vida Secreta de Bees', 'Sue Monk Kidd', 'Ficção', 12, 4.8),
        ('Molly Moon e o Livro Hiper Hipnótico', 'Georgia Byng', 'Fantasia', 10, 4.6),
        ('A Menina que Roubava Livros', 'Markus Zusak', 'Ficção', 12, 4.9),
        ('Peter Pan', 'J.M. Barrie', 'Fantasia', 10, 4.8),
        ('Hugo Cabret', 'Brian Selznick', 'Ficção', 11, 4.7),
        ('Os Meninos da Rua Paulo', 'Ferenc Molnár', 'Ficção', 12, 4.8),
        ('Charlie e o Elevador de Vidro', 'Roald Dahl', 'Fantasia', 10, 4.7),
        ('Alice no País das Maravilhas', 'Lewis Carroll', 'Fantasia', 9, 4.9),
        ('O Leão, a Feiticeira e o Guarda-Roupa', 'C.S. Lewis', 'Fantasia', 10, 4.8),
        ('A Fada que Tinha Ideias', 'Fernanda Lopes de Almeida', 'Fantasia', 9, 4.7),
        ('O Hobbit', 'J.R.R. Tolkien', 'Fantasia', 12, 4.9),
        ('O Rei Arthur e os Cavaleiros da Távola Redonda', 'Howard Pyle', 'Aventura', 12, 4.7),
        ('Os Mistérios de Enid Blyton', 'Enid Blyton', 'Suspense', 10, 4.6),
        ('Diário de uma Garota Nada Popular', 'Rachel Renée Russell', 'Ficção', 11, 4.5),
        ('O Livro da Selva', 'Rudyard Kipling', 'Aventura', 10, 4.7),
        ('Desventuras em Série: Mau Começo', 'Lemony Snicket', 'Ficção', 11, 4.8),
        ('Artemis Fowl', 'Eoin Colfer', 'Fantasia', 12, 4.7),
        ('A Casa na Árvore de 13 Andares', 'Andy Griffiths', 'Ficção', 9, 4.5),
        ('Eragon', 'Christopher Paolini', 'Fantasia', 12, 4.8),
        ('Mulan', 'Disney', 'Aventura', 9, 4.6),
        ('Um Conto Sombrio dos Grimm', 'Adam Gidwitz', 'Fantasia', 10, 4.6),
        ('A Canção de Aquiles', 'Madeline Miller', 'Fantasia', 12, 4.9),
        ('O Tesouro da Encantada', 'Eva Ibbotson', 'Aventura', 10, 4.5),
        ('Harry Potter e a Câmara Secreta', 'J.K. Rowling', 'Fantasia', 11, 4.9),
        ('Os Guardiões da Infância: O Coelhinho da Páscoa', 'William Joyce', 'Fantasia', 9, 4.5),
        ('Os Guardiões da Infância: O Sandman', 'William Joyce', 'Fantasia', 9, 4.6),
        ('O Diário de Anne Frank', 'Anne Frank', 'História', 12, 4.9),
        ('Os Miseráveis', 'Victor Hugo', 'Ficção', 12, 4.8),
        ('A Invenção de Hugo Cabret', 'Brian Selznick', 'Aventura', 10, 4.7),
        ('O Vento nos Salgueiros', 'Kenneth Grahame', 'Fantasia', 10, 4.6),
        ('O Guia do Mochileiro das Galáxias', 'Douglas Adams', 'Ficção', 12, 4.9),
        ('Tuck Everlasting', 'Natalie Babbitt', 'Ficção', 10, 4.7),
        ('A Wrinkle in Time', 'Madeleine L\'Engle', 'Ficção', 11, 4.8),
        ('O Caso dos Dez Negrinhos', 'Agatha Christie', 'Suspense', 12, 4.9),
        ('A Lâmpada de Aladim', 'Malba Tahan', 'Fantasia', 10, 4.7),
        ('Os Karas: A Droga da Obediência', 'Pedro Bandeira', 'Suspense', 12, 4.8),
        ('Série Fábulas', 'Bill Willingham', 'Fantasia', 12, 4.7),
        ('A Chave de Casa', 'Tatiana Salem Levy', 'Ficção', 12, 4.5),
        ('O Amuleto de Samarkand', 'Jonathan Stroud', 'Fantasia', 11, 4.8),
        ('Gregor, O Guerreiro da Superfície', 'Suzanne Collins', 'Ficção', 11, 4.7),
        ('O Sobrinho do Mago', 'C.S. Lewis', 'Fantasia', 10, 4.9),
        ('A Ilha de Kansnubra e o Portal Perdido', 'Andrews Ulisses', 'Fantasia', 10, 4.6),
        ('Mágico de Oz', 'L. Frank Baum', 'Fantasia', 9, 4.9),
        ('Peter e Wendy', 'J.M. Barrie', 'Fantasia', 10, 4.8),
        ('O Segredo do Vale da Lua', 'Elizabeth Goudge', 'Ficção', 11, 4.6),
        ('O Mundo de Sofia', 'Jostein Gaarder', 'Ficção', 12, 4.9),
        ('Série O Maravilhoso Mágico de Oz', 'L. Frank Baum', 'Fantasia', 10, 4.8),
        ('A Maldição do Titã', 'Rick Riordan', 'Fantasia', 11, 4.9),
        ('A Bússola de Ouro', 'Philip Pullman', 'Fantasia', 12, 4.9),
        ('A Espada na Pedra', 'T.H. White', 'Fantasia', 11, 4.7),
        ('Os Irmãos Grimm: Contos de Fadas', 'Irmãos Grimm', 'Fantasia', 9, 4.6),
        ('A Noite Estrelada', 'Jimmy Liao', 'Ficção', 10, 4.5),
        ('O Mistério do Cinco Estrelas', 'Marcos Rey', 'Suspense', 12, 4.7),
        ('O Fantasma de Canterville', 'Oscar Wilde', 'Fantasia', 10, 4.6),
        ('Os Garotos Corvos', 'Maggie Stiefvater', 'Ficção', 12, 4.8),
        ('A Rosa do Povo', 'Carlos Drummond de Andrade', 'Ficção', 12, 4.5),
        ('O Feitiço da Lua', 'Alexandre Dumas', 'Aventura', 11, 4.8),
        ('A Bruxa de Portobello', 'Paulo Coelho', 'Ficção', 12, 4.7),
        ('O Dragão de Gelo', 'George R.R. Martin', 'Fantasia', 10, 4.6),
        ('O Cavaleiro Andante', 'George R.R. Martin', 'Fantasia', 11, 4.7),
        ('Série As Crônicas de Spiderwick', 'Holly Black', 'Fantasia', 10, 4.8),
        ('A Ilha Misteriosa', 'Júlio Verne', 'Aventura', 11, 4.9),
        ('A Canção de Roland', 'Anônimo', 'Aventura', 12, 4.5),
        ('O Alquimista', 'Paulo Coelho', 'Ficção', 12, 4.8),
        ('Sherlock Holmes: O Estudo em Vermelho', 'Arthur Conan Doyle', 'Suspense', 12, 4.7),
        ('A Casa Torta', 'Agatha Christie', 'Suspense', 12, 4.9),
        ('O Senhor dos Ladrões', 'Cornelia Funke', 'Ficção', 10, 4.8),
        ('O Pequeno Vampiro', 'Angela Sommer-Bodenburg', 'Fantasia', 9, 4.7),
        ('O Navio dos Mortos', 'Rick Riordan', 'Fantasia', 12, 4.8),
        ('Fábulas Italianas', 'Italo Calvino', 'Ficção', 12, 4.6),
        ('O Gato Malhado e a Andorinha Sinhá', 'Jorge Amado', 'Ficção', 10, 4.7),
        ('O Tigre e o Dragão', 'Wang Dulu', 'Aventura', 11, 4.5),
        ('Os 39 Degraus', 'John Buchan', 'Suspense', 12, 4.6),
        ('Contos de Beedle, o Bardo', 'J.K. Rowling', 'Fantasia', 10, 4.8),
        ('O Caçador de Pipas', 'Khaled Hosseini', 'Ficção', 12, 4.9),
        ('O Cão dos Baskervilles', 'Arthur Conan Doyle', 'Suspense', 12, 4.8),
        ('Série Artemis Fowl', 'Eoin Colfer', 'Fantasia', 12, 4.9),
        ('A Marca de Atena', 'Rick Riordan', 'Fantasia', 12, 4.8),
        ('A História do Mundo Para Crianças', 'Rosalyn Schanzer', 'História', 10, 4.7),
        ('Uma Breve História do Mundo', 'Geoffrey Blainey', 'História', 12, 4.8),
        ('A História da Arte para Crianças', 'Anthony Mason', 'História', 11, 4.6),
        ('Histórias da Pré-História', 'Alberto Moravia', 'História', 9, 4.5),
        ('O Livro das Invenções', 'Ian Graham', 'História', 10, 4.6),
        ('Grandes Exploradores', 'Philip Wilkinson', 'História', 11, 4.7),
        ('História das Olimpíadas', 'Clive Gifford', 'História', 10, 4.7),
        ('Descobridores do Passado', 'Luís da Câmara Cascudo', 'História', 12, 4.8),
        ('História Ilustrada da Roma Antiga', 'Peter Connolly', 'História', 12, 4.7),
        ('As Grandes Civilizações do Passado', 'Paul Harrison', 'História', 11, 4.8),
    ]

    c.executemany('''
        INSERT INTO books (nome, nome_autor, genero, idade_indicada, rating) VALUES (?, ?, ?, ?, ?)
    ''', books)
    conn.commit()
    conn.close()


def add_book(nome, nome_autor, genero, idade_indicada, rating):
    """Adiciona um novo livro à tabela 'books'.

    Conecta-se ao banco de dados e insere um novo livro com os dados fornecidos 
    nos campos correspondentes.

    Args:
        nome (str): Nome do livro.
        nome_autor (str): Nome do autor do livro.
        genero (str): Gênero do livro.
        idade_indicada (int): Idade indicada para leitura do livro.
        rating (float): Classificação do livro.

    Returns:
        None: A função não retorna nenhum valor, apenas interage com o banco de dados 
        se necessário.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO books (nome, nome_autor, genero, idade_indicada, rating)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, nome_autor, genero, idade_indicada, rating))
    conn.commit()
    conn.close()


def view_books():
    """Recupera todos os livros da tabela 'books'.

    Conecta-se ao banco de dados e recupera todos os registros da tabela 'books'.

    Returns:
        list: Lista de tuplas contendo as informações dos livros, 
        onde cada tupla representa um livro.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    data = c.fetchall()
    conn.close()
    return data


def delete_book(book_id):
    """Exclui um livro da tabela 'books' com base no ID.

    Conecta-se ao banco de dados e exclui o registro que possui o ID fornecido.

    Args:
        book_id (int): ID do livro a ser excluído.

    Returns:
        None: A função não retorna nenhum valor, apenas interage com o banco de dados 
        se necessário.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()


def update_book(book_id, nome, nome_autor, genero, idade_indicada, rating):
    """Atualiza as informações de um livro existente.

    Conecta-se ao banco de dados e atualiza os detalhes de um livro específico, 
    com base no seu ID.

    Args:
        book_id (int): ID do livro a ser atualizado.
        nome (str): Novo nome do livro.
        nome_autor (str): Novo nome do autor.
        genero (str): Novo gênero do livro.
        idade_indicada (int): Nova idade indicada.
        rating (float): Novo rating.

    Returns:
        None: A função não retorna nenhum valor, apenas interage com o banco de dados 
        se necessário.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        UPDATE books
        SET nome = ?, nome_autor = ?, genero = ?, idade_indicada = ?, rating = ?
        WHERE id = ?
    ''', (nome, nome_autor, genero, idade_indicada, rating, book_id))
    conn.commit()
    conn.close()


def recommend_books(idade, genero, min_rating):
    """Recomenda livros com base na idade, gênero e classificação mínima.

    Conecta-se ao banco de dados e recupera os livros que atendem aos critérios 
    fornecidos: idade máxima indicada, gênero e classificação mínima.

    Args:
        idade (int): Idade máxima indicada.
        genero (str): Gênero do livro ou 'Todos' para qualquer gênero.
        min_rating (float): Classificação mínima desejada.

    Returns:
        list: Lista de tuplas contendo os livros que atendem aos critérios, 
        onde cada tupla representa um livro.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if genero != 'Todos':
        c.execute('''
            SELECT * FROM books WHERE idade_indicada <= ? AND genero = ? AND rating >= ?
        ''', (idade, genero, min_rating))
    else:
        c.execute('''
            SELECT * FROM books WHERE idade_indicada <= ? AND rating >= ?
        ''', (idade, min_rating))
    data = c.fetchall()
    conn.close()
    return data


# Definição dos gêneros disponíveis para seleção
generos_disponiveis = ['Ficção', 'Não Ficção', 'Fantasia', 'Romance', 'Aventura', 'Suspense', 'Ciência', 'História']

# Título do app
st.title('Catálogo de Livros')

# Criação da tabela ao inicializar o app
create_table()

# Insert dos dados
insert_data()

# Carregar o arquivo de configuração do YAML para os usuários
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Função de login
name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'Login'})

if authentication_status:
    authenticator.logout('logout', 'sidebar')
    st.sidebar.write(f'Bem-vindo, {name}!')
    # Menu lateral para navegação entre as opções
    st.sidebar.title('Menu')
    menu = st.sidebar.radio('Escolha a ação:', ['Adicionar Livro', 'Exibir Livros', 'Editar Livro', 'Excluir Livro', 'Recomendação de Livros'])

    # Condicional para a opção de adicionar livro
    if menu == 'Adicionar Livro':
        st.subheader('Adicionar Novo Livro')
        nome = st.text_input('Nome do Livro')
        nome_autor = st.text_input('Nome do Autor')
        genero = st.selectbox('Gênero', generos_disponiveis) 
        idade_indicada = st.number_input('Idade Indicada', min_value=9, max_value=12, step=1)
        rating = st.slider('Rating', min_value=0.0, max_value=5.0, step=0.1)
        
        if st.button('Adicionar Livro'):
            if not nome:
                st.error('O campo "Nome do Livro" é obrigatório.')
            elif not nome_autor:
                st.error('O campo "Nome do Autor" é obrigatório.')
            elif not genero:
                st.error('O campo "Gênero" é obrigatório.')
            elif idade_indicada < 9 or idade_indicada > 12:
                st.error('O campo "Idade Indicada" deve estar entre 9 e 12 inclusive')
            else:
                add_book(nome, nome_autor, genero, idade_indicada, rating)
                st.success(f'Livro "{nome}" adicionado com sucesso!')

    # Exibir livros
    elif menu == 'Exibir Livros':
        st.subheader('Todos os Livros')
        books = view_books()
        
        if books:
            for book in books:
                st.write(f"**Livro:** {book[1]} - **Autor:** {book[2]}")
                st.write(f"**Gênero:** {book[3]} - **Rating:** {book[5]}")
                st.write(f"**Idade Indicada:** {book[4]}")
                st.write('---')
        else:
            st.write("Nenhum livro encontrado.")

    # Editar livro
    elif menu == 'Editar Livro':
        st.subheader('Editar Livro')
        books = view_books()

        if books:
            book_options = {f"{book[0]} - {book[1]} - {book[2]}": book[0] for book in books}
            selected_option = st.selectbox('Selecione o Livro para Editar', list(book_options.keys()))
            selected_id = book_options[selected_option]

            selected_book = next((book for book in books if book[0] == selected_id), None)

            if selected_book:
                nome = st.text_input('Nome do Livro', value=selected_book[1])
                nome_autor = st.text_input('Nome do Autor', value=selected_book[2])
                genero = st.selectbox('Gênero', generos_disponiveis, index=generos_disponiveis.index(selected_book[3]))
                idade_indicada = st.number_input('Idade Indicada', value=selected_book[4], min_value=9, max_value=12, step=1)
                rating = st.slider('Rating', min_value=0.0, max_value=5.0, step=0.1, value=selected_book[5])
                
                if st.button('Atualizar Livro'):
                    if not nome:
                        st.error('O campo "Nome do Livro" é obrigatório.')
                    elif not nome_autor:
                        st.error('O campo "Nome do Autor" é obrigatório.')
                    elif not genero:
                        st.error('O campo "Gênero" é obrigatório.')
                    elif idade_indicada < 9 or idade_indicada > 12:
                        st.error('O campo "Idade Indicada" deve estar entre 9 e 12 inclusive')
                    else:
                        update_book(selected_id, nome, nome_autor, genero, idade_indicada, rating)
                        st.success(f'Livro "{selected_id}" atualizado com sucesso!')
        else:
            st.write("Nenhum livro encontrado para editar.")

    # Excluir livro
    elif menu == 'Excluir Livro':
        st.subheader('Excluir Livro')
        books = view_books()

        if books:
            book_options = {f"{book[0]} - {book[1]} - {book[2]}": book[0] for book in books}
            selected_option = st.selectbox('Selecione o Livro para Excluir', list(book_options.keys()))
            selected_id = book_options[selected_option]

            if st.button('Excluir Livro'):
                delete_book(selected_id)
                st.success(f'Livro ID {selected_id} excluído com sucesso!')
        else:
            st.write("Nenhum livro encontrado para excluir.")

    # Recomendar livros
    elif menu == 'Recomendação de Livros':
        st.subheader('Recomendação Livros')
        
        idade = st.number_input('Idade Máxima Indicada', min_value=9, max_value=12, step=1)
        genero = st.selectbox('Gênero do Livro', ['Todos']+generos_disponiveis)
        min_rating = st.slider('Rating Mínimo', min_value=0.0, max_value=5.0, step=0.1)
        
        if st.button('Obter Recomendações'):
            recommended_books = recommend_books(idade, genero, min_rating)
            
            if recommended_books:
                st.write(f"Recomendações para livros de gênero '{genero}', idade máxima '{idade}', com rating acima de '{min_rating}':")
                st.write(f'{len(recommended_books)} livro{"s" if len(recommended_books)>1 else ""} encontrado{"s" if len(recommended_books)>1 else ""}')
                st.write('---')
                for book in recommended_books:
                    st.write(f"**Livro:** {book[1]} - **Autor:** {book[2]}")
                    st.write(f"**Gênero:** {book[3]} - **Rating:** {book[5]}")
                    st.write(f"**Idade Indicada:** {book[4]}")
                    st.write('---')
            else:
                st.write("Nenhum livro encontrado com esses critérios.")

elif authentication_status == False:
    st.error('Nome de usuário ou senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira o nome de usuário e a senha')

