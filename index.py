from flask import Flask, render_template,request,redirect,url_for,session,url_for , make_response, send_file
from fpdf import FPDF
from datetime import datetime, time
import mysql.connector
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'Raynnard'

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'db_klinik_rawat_inap_rio'
}   
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def Id_Otomatis(prefix, nama_tabel, kolom_id):
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT MAX(CAST(SUBSTRING({kolom_id}, LENGTH('{prefix}_') + 1) AS UNSIGNED)) as data_terakhir FROM {nama_tabel} WHERE {kolom_id} LIKE '{prefix}_%'")
        data_terakhir = cursor.fetchone()
        cursor.close()
        conn.close()
        
        Data = data_terakhir['data_terakhir'] if data_terakhir['data_terakhir'] else 0
        new_num = Data + 1
        return f"{prefix}_{new_num:04d}"
    except Exception as e:
        return f"{prefix}_0001"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = "SELECT * FROM user_rio WHERE username = %s AND password = %s"
        conn = get_db_connection()
        cursor = conn.cursor(dictionary = True)
        cursor.execute(query,(username, password))
        user = cursor.fetchone()

        if user:
            session['loginM'] = True
            session["user"] = user["username"]
            return redirect("/dashboard")
        else:
            return "<h3>Login gagal</h3><a href='/'>Coba Lagi</a>"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'loginM' not in session:
        return redirect(url_for('login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `transaksi_rio` t JOIN pasien_rio p ON t.id_pasien_rio=p.id_pasien_rio JOIN rawat_inap_rio r ON t.id_rawat_rio = r.id_rawat_rio JOIN kamar_rio k ON r.id_kamar_rio = k.id_kamar_rio")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template("dashboard.html",transaksi=result)

    except Exception as e:
        return f"Gagal koneksi ke database: {e}"

@app.route('/pasien', methods=['POST', 'GET'])
def pasien():
    if 'loginM' not in session:
        return redirect(url_for('login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `pasien_rio`")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template("pasien.html",transaksi=result)

    except Exception as e:
        return f"Gagal koneksi ke database: {e}"


@app.route('/input', methods=['POST', 'GET'])
def index():
    if 'loginM' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        id_pasien_rio = request.form['id_pasien_rio']
        id_rawat_rio = request.form['id_rawat_rio']
        total_biaya_rio = request.form['total_biaya_rio']
        status_pembayaran_rio = request.form['status_pembayaran_rio']
        tgl_transaksi_rio = request.form['tgl_transaksi_rio']

        id_transaksi = Id_Otomatis('T','transaksi_rio','id_transaksi')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO `transaksi_rio` 
                     (`id_transaksi`, `id_pasien_rio`,`id_rawat_rio`, `total_biaya_rio`, `status_pembayaran_rio`, `tgl_transaksi_rio`) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (id_transaksi, id_pasien_rio,id_rawat_rio, total_biaya_rio, status_pembayaran_rio, tgl_transaksi_rio)
            cursor.execute(sql, val)
            conn.commit()
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            return f"Error: {err}. Pastikan ID Pasien '{id_pasien_rio}' sudah terdaftar."
        finally:
            cursor.close()
            conn.close()
    
    elif request.method == "GET":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_pasien_rio, nama_rio FROM pasien_rio")
        data = cursor.fetchall()
        cursor.execute("SELECT id_rawat_rio FROM rawat_inap_rio")
        rawat = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("index.html", data=data,rawat=rawat)


@app.route('/hapus_transaksi/<string:id>', methods=['POST']) 
def hapus_transaksi(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_query = "DELETE FROM transaksi_rio WHERE id_transaksi  = %s"
    cursor.execute(sql_query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/edit_transaksi/<string:id>', methods=['GET', 'POST'])
def edit_transaksi(id):
    if 'loginM' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_transaksi = request.form['id_transaksi']
        id_pasien_rio = request.form['id_pasien_rio']
        total_biaya_rio = request.form['total_biaya_rio']
        status_pembayaran_rio = request.form['status_pembayaran_rio']
        tgl_transaksi_rio = request.form['tgl_transaksi_rio']
 
        sql_query = "UPDATE transaksi_rio SET id_transaksi  = %s, id_pasien_rio  = %s, total_biaya_rio = %s, status_pembayaran_rio = %s ,tgl_transaksi_rio = %s WHERE id_transaksi  = %s"
        cursor.execute(sql_query, (id_transaksi, id_pasien_rio, total_biaya_rio, status_pembayaran_rio,tgl_transaksi_rio, id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transaksi_rio WHERE id_transaksi = %s", (id,))
        s = cursor.fetchone()
        cursor.execute("SELECT id_pasien_rio, nama_rio FROM pasien_rio")
        pasien = cursor.fetchall()
        cursor.close()
        conn.close()
        if s is None:
            return "transaksi tidak ditemukan"
        return render_template('edit-transaksi.html', g=s,pasien=pasien)

@app.route('/cetak')
def cetak():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien_rio, nama_rio, alamat_rio, kontak FROM pasien_rio ORDER BY id_pasien_rio ASC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "",size=12)
    pdf.cell(200, 10, txt="Data Pasien Klinik", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "",size=10)
    pdf.set_fill_color(200, 220, 0)
    pdf.cell(30, 10, txt="Id Pasien:",border=1, ln=0,fill=True)
    pdf.cell(50, 10, txt="Nama Pasien:",border=1, ln=0,fill=True)
    pdf.cell(80, 10, txt="Alamat:",border=1, ln=0,fill=True)
    pdf.cell(30, 10, txt="No. Kontak:",border=1, ln=1,fill=True)

    pdf.set_fill_color(200, 220, 255)
    for d in data:
        pdf.cell(30, 10, txt=d['id_pasien_rio'], border=1)
        pdf.cell(50, 10, txt=d['nama_rio'], border=1)
        pdf.cell(80, 10, txt=d['alamat_rio'], border=1)
        pdf.cell(30, 10, txt=d['kontak'], border=1, ln=1)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Data_Pasien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mimetype="application/pdf"
    )


if __name__ == '__main__':
    app.run(debug=True)