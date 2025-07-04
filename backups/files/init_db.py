#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados básicos do SKPONTO
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from app import create_app, db
from app.models import User, WorkClass, UserType
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializa o banco de dados com dados básicos"""
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas do banco de dados...")
        db.create_all()
        
        # Criar classes de trabalho padrão se não existirem
        if WorkClass.query.count() == 0:
            print("Criando classes de trabalho padrão...")
            
            classes = [
                {
                    'name': 'Administrador',
                    'description': 'Carga horária padrão para administradores',
                    'daily_work_hours': 8.0,
                    'lunch_hours': 1.0
                },
                {
                    'name': 'Trabalhador',
                    'description': 'Carga horária padrão para trabalhadores',
                    'daily_work_hours': 8.0,
                    'lunch_hours': 1.0
                },
                {
                    'name': 'Estagiário',
                    'description': 'Carga horária reduzida para estagiários',
                    'daily_work_hours': 6.0,
                    'lunch_hours': 1.0
                }
            ]
            
            for class_data in classes:
                work_class = WorkClass(
                    name=class_data['name'],
                    description=class_data['description'],
                    daily_work_hours=class_data['daily_work_hours'],
                    lunch_hours=class_data['lunch_hours'],
                    is_active=True
                )
                db.session.add(work_class)
            
            print("Classes de trabalho criadas com sucesso!")
        
        # Criar usuário admin padrão se não existir
        admin_user = User.query.filter_by(email='admin@skponto.com').first()
        if not admin_user:
            print("Criando usuário administrador padrão...")
            
            # Buscar a classe de trabalho de administrador
            admin_work_class = WorkClass.query.filter_by(name='Administrador').first()
            
            admin_user = User(
                nome='Administrador',
                sobrenome='do Sistema', 
                email='admin@skponto.com',
                cpf='00000000000',  # CPF temporário
                user_type=UserType.ADMIN,
                is_active=True,
                work_class_id=admin_work_class.id if admin_work_class else None
            )
            admin_user.set_password('admin123')  # Lembre-se de mudar esta senha!
            
            db.session.add(admin_user)
            print("Usuário administrador criado!")
            print("Email: admin@skponto.com")
            print("Senha: admin123")
            print("⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!")
        
        # Confirmar todas as mudanças
        db.session.commit()
        print("\n✅ Banco de dados inicializado com sucesso!")
        print("🚀 O sistema SKPONTO está pronto para uso!")

if __name__ == '__main__':
    init_database()
