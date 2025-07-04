"""
SKPONTO - Sistema de Controle de Ponto
Aplicação principal Flask
"""

import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import (User, TimeRecord, MedicalAttestation, Notification, 
                       SecurityLog, SystemConfig, UserType, AttestationType,
                       AttestationStatus, NotificationType, WorkClass)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Contexto do shell Flask"""
    return {
        'db': db,
        'User': User,
        'TimeRecord': TimeRecord,
        'MedicalAttestation': MedicalAttestation,
        'Notification': Notification,
        'SecurityLog': SecurityLog,
        'SystemConfig': SystemConfig,
        'UserType': UserType,
        'AttestationType': AttestationType,
        'AttestationStatus': AttestationStatus,
        'NotificationType': NotificationType,
        'WorkClass': WorkClass
    }

if __name__ == '__main__':
    with app.app_context():
        # Criar tabelas se não existirem
        db.create_all()
        
        # Verificar se existe pelo menos um admin
        admin_exists = User.query.filter_by(user_type=UserType.ADMIN).first()
        if not admin_exists:
            print("⚠️  AVISO: Nenhum administrador encontrado!")
            print("Execute: flask create-admin")
            print("Para criar o primeiro administrador do sistema.")
    
    # Configuração para desenvolvimento
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug)
