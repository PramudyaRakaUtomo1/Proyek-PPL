from app import app, db, Kategori, Produk

with app.app_context():
    # 1. Tambahkan Kategori
    kat_ricebowl = Kategori(nama='Ricebowl')
    kat_tost = Kategori(nama='Tost')
    kat_kopi = Kategori(nama='Kopi')
    
    db.session.add_all([kat_ricebowl, kat_tost, kat_kopi])
    db.session.commit()

    # 2. Tambahkan Produk
    p1 = Produk(nama='Ricebowl Ayam', harga=15000, status_ready=True, kategori_id=kat_ricebowl.id)
    p2 = Produk(nama='Tost Coklat', harga=10000, status_ready=True, kategori_id=kat_tost.id)
    p3 = Produk(nama='Tost Telur Keju', harga=12000, status_ready=False, kategori_id=kat_tost.id)
    p4 = Produk(nama='Kopi Susu', harga=8000, status_ready=True, kategori_id=kat_kopi.id)
    
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    
    print("Data Kategori dan Produk berhasil ditambahkan!")