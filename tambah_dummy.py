from app import app, db, Kategori, Produk

with app.app_context():
    # 1. Bersihkan data menu lama agar tidak dobel (tidak menghapus akun user)
    Produk.query.delete()
    Kategori.query.delete()
    db.session.commit()

    # 2. Buat Kategori
    kat_ricebowl = Kategori(nama='Ricebowl')
    kat_tost = Kategori(nama='Tost')
    kat_kopi = Kategori(nama='Kopi')
    db.session.add_all([kat_ricebowl, kat_tost, kat_kopi])
    db.session.commit()

    # 3. Masukkan Data Dummy
    data_dummy = [
        Produk(nama='Ricebowl Ayam Geprek', harga=15000, status_ready=True, kategori_id=kat_ricebowl.id),
        Produk(nama='Ricebowl Sapi Lada Hitam', harga=22000, status_ready=True, kategori_id=kat_ricebowl.id),
        Produk(nama='Ricebowl Sambal Matah', harga=17000, status_ready=False, kategori_id=kat_ricebowl.id),
        
        Produk(nama='Tost Coklat Keju', harga=12000, status_ready=True, kategori_id=kat_tost.id),
        Produk(nama='Tost Telur Smoked Beef', harga=16000, status_ready=True, kategori_id=kat_tost.id),
        Produk(nama='Tost Selai Kacang', harga=10000, status_ready=True, kategori_id=kat_tost.id),
        
        Produk(nama='Kopi Susu Gula Aren', harga=12000, status_ready=True, kategori_id=kat_kopi.id),
        Produk(nama='Kopi Americano', harga=8000, status_ready=True, kategori_id=kat_kopi.id),
        Produk(nama='Es Matcha Latte', harga=15000, status_ready=True, kategori_id=kat_kopi.id)
    ]
    
    db.session.add_all(data_dummy)
    db.session.commit()
    print("Berhasil! Data dummy lengkap telah dimasukkan ke database.")