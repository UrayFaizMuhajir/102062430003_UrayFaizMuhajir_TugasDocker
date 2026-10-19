import os
import time

import pymysql
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "database"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "mahasiswa_db"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def init_db(retries=30, delay=2):
    for i in range(1, retries + 1):
        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS mahasiswa (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nama VARCHAR(100) NOT NULL,
                        nim VARCHAR(20) NOT NULL,
                        prodi VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
                )
            print("Database siap", flush=True)
            return
        except pymysql.MySQLError as e:
            print(f"Menunggu database ({i}/{retries}): {e}", flush=True)
            time.sleep(delay)
    raise RuntimeError("Database tidak bisa dihubungi")


init_db()


@app.route("/")
def index():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM mahasiswa ORDER BY id DESC")
        data = cur.fetchall()
    return render_template("index.html", data=data, host=os.getenv("HOSTNAME", "-"))


@app.route("/tambah", methods=["POST"])
def tambah():
    nama = request.form.get("nama", "").strip()
    nim = request.form.get("nim", "").strip()
    prodi = request.form.get("prodi", "").strip()
    if nama and nim and prodi:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO mahasiswa (nama, nim, prodi) VALUES (%s, %s, %s)", (nama, nim, prodi))
    return redirect(url_for("index"))


@app.route("/hapus/<int:mid>", methods=["POST"])
def hapus(mid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM mahasiswa WHERE id = %s", (mid,))
    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM mahasiswa")
            total = cur.fetchone()["total"]
        return jsonify(status="ok", database="connected", total_mahasiswa=total)
    except Exception as e:  # noqa: BLE001
        return jsonify(status="error", database="disconnected", detail=str(e)), 500
