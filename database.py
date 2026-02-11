import sqlite3

def init_db():
    """Cria o arquivo do banco e as tabelas se elas não existirem"""
    conn = sqlite3.connect('globalspeak.db')
    cursor = conn.cursor()
    
    # Tabela para salvar os dados do usuário (como o progresso das missões)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            missao_atual INTEGER DEFAULT 1
        )
    ''')
    
    # Tabela para salvar todas as mensagens trocadas (o histórico)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verifica se já existe um usuário padrão, se não, cria um
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (nome, missao_atual) VALUES (?, ?)", ("Aluno", 1))
    
    conn.commit()
    conn.close()

def salvar_mensagem(role, content):
    """Guarda uma nova mensagem (do aluno ou da IA) no banco"""
    conn = sqlite3.connect('globalspeak.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chat_history (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def carregar_historico():
    """Busca todas as mensagens guardadas para mostrar na tela ao abrir o app"""
    conn = sqlite3.connect('globalspeak.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM chat_history ORDER BY timestamp ASC')
    # Transforma os dados em uma lista que a OpenAI entende
    history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return history

def resetar_conversa():
    """Apaga o histórico se o aluno quiser começar do zero"""
    conn = sqlite3.connect('globalspeak.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history')
    conn.commit()
    conn.close()