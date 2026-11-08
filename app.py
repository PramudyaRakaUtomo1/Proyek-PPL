from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jotoast.db'
app.config['SECRET_KEY'] = 'jotoast_secret_123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# 1. MODEL DATABASE
# ==========================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    produk = db.relationship('Produk', backref='kategori_rel', lazy=True)

class Produk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    status_ready = db.Column(db.Boolean, default=True)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=False)

class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pemesan = db.Column(db.String(100), nullable=True)
    metode_bayar = db.Column(db.String(20), nullable=False)
    total_harga = db.Column(db.Integer, nullable=False)

# ==========================================
# 2. ROUTING LOGIN & ADMIN (Termasuk Edit & Kategori)
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username, password=password, role=role).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            
            if user.role == 'owner':
                return redirect(url_for('kelola_produk'))
            elif user.role == 'kasir':
                return redirect(url_for('kasir'))
        else:
            return render_template('login.html', error="Username atau kata sandi salah.")
    return render_template('login.html')

# --- KELOLA PRODUK ---
@app.route('/admin/produk')
def kelola_produk():
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    produk = Produk.query.all()
    return render_template('admin_produk.html', produk=produk)

@app.route('/admin/produk/tambah', methods=['GET', 'POST'])
def tambah_produk():
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    if request.method == 'POST':
        nama = request.form.get('nama')
        harga = request.form.get('harga')
        kategori_id = request.form.get('kategori_id')
        status = request.form.get('status') == 'Ready'
        
        produk_baru = Produk(nama=nama, harga=int(harga), kategori_id=kategori_id, status_ready=status)
        db.session.add(produk_baru)
        db.session.commit()
        return redirect(url_for('kelola_produk'))
        
    kategori_list = Kategori.query.all()
    return render_template('admin_tambah_produk.html', kategori=kategori_list)

# WBS 1.2.2: Fungsi UBAH Produk
@app.route('/admin/produk/edit/<int:id>', methods=['GET', 'POST'])
def edit_produk(id):
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    
    produk = Produk.query.get(id)
    if request.method == 'POST':
        produk.nama = request.form.get('nama')
        produk.harga = int(request.form.get('harga'))
        produk.kategori_id = request.form.get('kategori_id')
        produk.status_ready = request.form.get('status') == 'Ready'
        db.session.commit()
        return redirect(url_for('kelola_produk'))
        
    kategori_list = Kategori.query.all()
    return render_template('admin_edit_produk.html', produk=produk, kategori=kategori_list)

@app.route('/admin/produk/hapus/<int:id>')
def hapus_produk(id):
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    produk = Produk.query.get(id)
    if produk:
        db.session.delete(produk)
        db.session.commit()
    return redirect(url_for('kelola_produk'))

# --- WBS 1.4: KELOLA KATEGORI ---
@app.route('/admin/kategori', methods=['GET', 'POST'])
def kelola_kategori():
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nama = request.form.get('nama')
        kategori_baru = Kategori(nama=nama)
        db.session.add(kategori_baru)
        db.session.commit()
        return redirect(url_for('kelola_kategori'))
        
    kategori_list = Kategori.query.all()
    return render_template('admin_kategori.html', kategori=kategori_list)

@app.route('/admin/kategori/hapus/<int:id>')
def hapus_kategori(id):
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    kategori = Kategori.query.get(id)
    if kategori:
        db.session.delete(kategori)
        db.session.commit()
    return redirect(url_for('kelola_kategori'))
# Fungsi untuk keluar (Logout)
@app.route('/logout')
def logout():
    session.clear() # Menghapus sesi login
    return redirect(url_for('menu_online')) # Kembali ke halaman utama pelanggan
# ==========================================
# 3. ROUTING KASIR & CUSTOMER
# ==========================================
@app.route('/kasir')
def kasir():
    if session.get('role') != 'kasir':
        return redirect(url_for('login'))
    produk = Produk.query.all()
    return render_template('kasir.html', produk=produk)

@app.route('/kasir/proses_transaksi', methods=['POST'])
def proses_transaksi():
    if session.get('role') != 'kasir':
        return redirect(url_for('login'))
    metode_bayar = request.form.get('metode_bayar', 'Tunai')
    total_harga = request.form.get('total_harga', 0)
    transaksi_baru = Transaksi(nama_pemesan="Pelanggan Outlet", metode_bayar=metode_bayar, total_harga=int(total_harga))
    db.session.add(transaksi_baru)
    db.session.commit()
    return "Transaksi berhasil dicatat ke database!"

@app.route('/')
def menu_online():
    kategori_aktif = request.args.get('kategori', 'semua')
    if kategori_aktif == 'semua':
        produk = Produk.query.all()
    else:
        kategori = Kategori.query.filter_by(nama=kategori_aktif).first()
        produk = Produk.query.filter_by(kategori_id=kategori.id).all() if kategori else []
    return render_template('menu_online.html', produk=produk)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        nama_pemesan = request.form.get('nama_pemesan')
        metode_bayar = request.form.get('metode_bayar') 
        transaksi_baru = Transaksi(nama_pemesan=nama_pemesan, metode_bayar=metode_bayar, total_harga=31000)
        db.session.add(transaksi_baru)
        db.session.commit()
        return "Pesanan berhasil dibuat!"
    return render_template('checkout.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)