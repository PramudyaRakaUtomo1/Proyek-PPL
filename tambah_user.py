from app import app, db, User

with app.app_context():
    # Menambahkan akun Owner
    owner = User(username='admin', password='123', role='owner')
    # Menambahkan akun Kasir
    kasir = User(username='kasir', password='123', role='kasir')
    
    db.session.add(owner)
    db.session.add(kasir)
    db.session.commit()
    print("Akun Owner dan Kasir berhasil ditambahkan!")