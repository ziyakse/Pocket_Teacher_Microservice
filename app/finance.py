# app/finance.py

from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, jsonify
import os

app = Flask(__name__)
# Flash mesajları (bildirimler) için gizli bir anahtar şarttır
app.secret_key = "pocket_teacher_gizli_anahtar" 

# HTML içindeki url_for('student.login') yapılarının çalışması için Blueprint tanımlıyoruz
student = Blueprint('student', __name__)

# ==========================================
# MOCK VERİLER (Demo'da dolu ve şık görünmesi için)
# ==========================================
MOCK_COURSES = [
    {"course_id": 1, "grade_level": 8, "course_name": "LGS Matematik", "progress": 60},
    {"course_id": 2, "grade_level": 8, "course_name": "LGS Fen Bilimleri", "progress": 25},
    {"course_id": 3, "grade_level": 8, "course_name": "LGS Türkçe", "progress": 0}
]

MOCK_MODULES = [
    {"module_id": 1, "module_name": "Üslü İfadeler", "progress": 100},
    {"module_id": 2, "module_name": "Kareköklü İfadeler", "progress": 50},
    {"module_id": 3, "module_name": "Veri Analizi", "progress": 0}
]

MOCK_QUESTIONS = [
    {"question_id": 1, "question_text": "2^3 + 4^2 işleminin sonucu kaçtır?", "options": '["24", "16", "20", "12"]', "difficulty_score": 1},
    {"question_id": 2, "question_text": "Aşağıdakilerden hangisi bir tam karedir?", "options": '["10", "16", "20", "24"]', "difficulty_score": 2}
]

# ==========================================
# ROUTE'LAR (SAYFA YÖNLENDİRMELERİ)
# ==========================================

@student.route('/')
def index():
    return redirect(url_for('student.login'))

@student.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        flash('Giriş başarılı! Hoş geldin.', 'success')
        return redirect(url_for('student.home'))
    return render_template('login.html')

@student.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Kayıt başarılı! Şimdi giriş yapabilirsin.', 'success')
        return redirect(url_for('student.login'))
    cities = [{"city_id": 1, "city_name": "İstanbul"}, {"city_id": 2, "city_name": "Ankara"}, {"city_id": 3, "city_name": "İzmir"}]
    return render_template('register.html', cities=cities)

@student.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash('Şifre sıfırlama linki e-postana gönderildi!', 'info')
        return redirect(url_for('student.login'))
    return render_template('forgot_password.html')

@student.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        flash('Şifren başarıyla güncellendi.', 'success')
        return redirect(url_for('student.login'))
    return render_template('reset_password.html')

@student.route('/home')
def home():
    # user_name değişkenini şablona gönderiyoruz
    return render_template('home.html', user_name="Deniz", courses=MOCK_COURSES)

@student.route('/course/<int:course_id>')
def course_detail(course_id):
    course = next((c for c in MOCK_COURSES if c["course_id"] == course_id), MOCK_COURSES[0])
    return render_template('course_detail.html', course=course, modules=MOCK_MODULES)

@student.route('/module/<int:module_id>/content')
def module_content(module_id):
    return render_template('quiz.html', module=MOCK_MODULES[0], questions=MOCK_QUESTIONS)

@student.route('/reset_module/<int:module_id>')
def reset_module(module_id):
    flash('Ünite sıfırlandı. Tekrar başarılar!', 'info')
    return redirect(url_for('student.course_detail', course_id=1))

@student.route('/achievements')
def achievements():
    badges = [
        {"name": "İlk Adım", "desc": "İlk testini çözdün.", "icon": "🥉", "locked": False},
        {"name": "Matematik Dehası", "desc": "10 Matematik testi fulledin.", "icon": "👑", "locked": True}
    ]
    return render_template('achievements.html', total_correct=15, badges=badges)

@student.route('/dashboard')
def dashboard():
    students_data = [{"name": "Ali", "last_name": "Yılmaz", "city": "İstanbul", "account_type": "Premium"}]
    return render_template('dashboard.html', 
                           total_students=120, 
                           supported_count=45, 
                           revenue=12500, 
                           transactions=[], 
                           students=students_data)

@student.route('/logout')
def logout():
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('student.login'))

# JS dosyasındaki fetch API çağrısı için uç nokta
@app.route('/api/upgrade_level/<int:module_id>', methods=['POST'])
def upgrade_level(module_id):
    return jsonify({"message": "Tebrikler! Seviye atladın. Yeni sorular daha zorlayıcı olacak."})

# Hazırladığımız tüm route'ları Flask'a kaydediyoruz
app.register_blueprint(student)

if __name__ == '__main__':
    # Container içinde tüm ağlara açılması için host 0.0.0.0 olarak kalmalı
    app.run(host='0.0.0.0', port=5000, debug=True)