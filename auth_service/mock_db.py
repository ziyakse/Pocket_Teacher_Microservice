# auth_service/mock_db.py

MOCK_USERS_DB = {
    "denis@example.com": {
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQG8.F.q", # Şifre: 123
        "name": "Denis",
        "role": "student"
    },
    "ali@example.com": {
        "password": "$2b$12$N9uXyB11rQ1Hn.p0A8yCbe7I/gC.J0ZJbF5Q0PqXpM2Mh8N0J.SjK", # Şifre: password123
        "name": "Ali",
        "role": "student"
    },
    "ayse@example.com": {
        "password": "$2b$12$D2M/PjD7wV6A5d/Q1O3n/O0S0R5U9X6f/Z5uF6l/U8I7C6J3E1T.K", # Şifre: admin
        "name": "Ayşe",
        "role": "premium_student"
    }
}