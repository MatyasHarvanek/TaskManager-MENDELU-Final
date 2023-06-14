import sqlite3


def create_database():
    conn = sqlite3.connect('udelej_to.db')  # Vytvoří novou databázi, pokud neexistuje

    c = conn.cursor()  # Vytvoří kurzor pro manipulaci s databází

    # Vytvoření tabulky task
    c.execute('''
        CREATE TABLE task (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            is_done BOOLEAN NOT NULL DEFAULT 0,
            user_id INTEGER,
            created_at TIMESTAMP NOT NULL
        )
    ''')

    # Vytvoření tabulky user
    c.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Přidání uživatele
    c.execute('''
        INSERT INTO user (name, password) 
        VALUES (?, ?)
    ''', ('bonifac', '1234'))

    conn.commit()  # Uložení změn
    conn.close()  # Uzavření spojení s databází

if __name__ == "__main__":
    create_database()