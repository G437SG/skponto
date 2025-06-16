from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.utils.file_utils import upload_user_photo, allowed_file, validate_file_size
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.get_by_email(email)
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.user_id
            session['user_email'] = user.email
            session['user_type'] = user.user_type
            session['user_name'] = user.name
            flash('Login realizado com sucesso!', 'success')
            
            if user.user_type == 'ADMINISTRADOR':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('dashboard.index'))
        else:
            flash('Email ou senha inválidos!', 'error')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user_type = request.form.get('user_type', 'TRABALHADOR')
        
        # Check if user already exists
        if User.get_by_email(email):
            flash('Email já cadastrado!', 'error')
            return render_template('register.html')
        
        # Handle photo upload
        photo_url = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                # Validate file
                if not allowed_file(file.filename):
                    flash('Tipo de arquivo não permitido! Use PNG, JPG, JPEG ou GIF.', 'error')
                    return render_template('register.html')
                
                if not validate_file_size(file):
                    flash('Arquivo muito grande! Máximo 16MB.', 'error')
                    return render_template('register.html')
                
                # Upload to Dropbox
                photo_url = upload_user_photo(file, email)
                if not photo_url:
                    flash('Erro ao fazer upload da foto. Tente novamente.', 'error')
                    return render_template('register.html')
        
        # Create new user
        user = User(email=email, name=name, user_type=user_type, profile_picture=photo_url)
        user.set_password(password)
        
        if user.save():
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Erro ao criar usuário. Tente novamente.', 'error')
    
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.get_by_email(session['user_email'])
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user.name = request.form['name']
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                # Validate file
                if not allowed_file(file.filename):
                    flash('Tipo de arquivo não permitido! Use PNG, JPG, JPEG ou GIF.', 'error')
                    return render_template('profile.html', user=user)
                
                if not validate_file_size(file):
                    flash('Arquivo muito grande! Máximo 16MB.', 'error')
                    return render_template('profile.html', user=user)
                
                # Upload new photo to Dropbox
                new_photo_url = upload_user_photo(file, user.email)
                if new_photo_url:
                    user.profile_picture = new_photo_url
                else:
                    flash('Erro ao fazer upload da foto. Tente novamente.', 'error')
                    return render_template('profile.html', user=user)
        
        if user.save():
            session['user_name'] = user.name  # Update session
            flash('Perfil atualizado com sucesso!', 'success')
        else:
            flash('Erro ao atualizar perfil. Tente novamente.', 'error')
    
    return render_template('profile.html', user=user)

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.get_by_email(email)
        
        if user:
            # In a real application, you would send an email here
            # For now, we'll just show a success message
            flash('Se o email existir, um link de recuperação será enviado.', 'info')
        else:
            flash('Se o email existir, um link de recuperação será enviado.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html')

@bp.route('/recover_password')
def recover_password():
    return render_template('forgot_password.html')