import sqlite3
import os
from pathlib import Path

class TodoApp:
    def __init__(self):
        # Cria o diretório data se não existir
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Conecta ao banco de dados
        self.db_path = self.data_dir / 'tasks.db'
        self.conn = sqlite3.connect(str(self.db_path))
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_task(self, description):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
        self.conn.commit()
        print("\nTarefa adicionada com sucesso!")

    def view_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, description, completed FROM tasks ORDER BY created_at')
        tasks = cursor.fetchall()
        
        if not tasks:
            print("\nNenhuma tarefa encontrada!")
            return False

        print("\nLista de Tarefas:")
        for task in tasks:
            status = "✓" if task[2] else " "
            print(f"{task[0]}. [{status}] {task[1]}")
        return True

    def complete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        if cursor.rowcount > 0:
            self.conn.commit()
            print("\nTarefa marcada como concluída!")
        else:
            print("\nTarefa não encontrada!")

    def remove_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        if cursor.rowcount > 0:
            self.conn.commit()
            print("\nTarefa removida com sucesso!")
        else:
            print("\nTarefa não encontrada!")

    def close(self):
        self.conn.close()

def main():
    try:
        app = TodoApp()
        
        while True:
            print("\n=== Gerenciador de Tarefas ===")
            print("1. Adicionar Tarefa")
            print("2. Visualizar Tarefas")
            print("3. Marcar Tarefa como Concluída")
            print("4. Remover Tarefa")
            print("5. Sair")
            
            choice = input("\nEscolha uma opção (1-5): ").strip()
            
            if choice == "1":
                description = input("\nDigite a descrição da tarefa: ").strip()
                if description:
                    app.add_task(description)
                else:
                    print("\nA descrição não pode estar vazia!")
            
            elif choice == "2":
                app.view_tasks()
            
            elif choice == "3":
                if app.view_tasks():
                    try:
                        task_id = int(input("\nDigite o número da tarefa a ser marcada como concluída: "))
                        app.complete_task(task_id)
                    except ValueError:
                        print("\nPor favor, digite um número válido!")
            
            elif choice == "4":
                if app.view_tasks():
                    try:
                        task_id = int(input("\nDigite o número da tarefa a ser removida: "))
                        app.remove_task(task_id)
                    except ValueError:
                        print("\nPor favor, digite um número válido!")
            
            elif choice == "5":
                app.close()
                print("\nObrigado por usar o Gerenciador de Tarefas!")
                break
            
            else:
                print("\nOpção inválida! Por favor, escolha uma opção entre 1 e 5.")

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Por favor, tente novamente.")

if __name__ == "__main__":
    main()