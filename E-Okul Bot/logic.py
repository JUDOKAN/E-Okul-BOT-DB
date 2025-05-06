import sqlite3
from config import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ogrenciler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    sinif INTEGER NOT NULL,
    sube TEXT NOT NULL,
    no INTEGER NOT NULL UNIQUE,
    kayit_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ders_notlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_no INTEGER,
    ders TEXT,
    notu INTEGER,
    tarih TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ogrenci_no) REFERENCES ogrenciler(no)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ders_programi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sinif INTEGER,
    sube TEXT,
    gun TEXT,
    saat TEXT,
    dersler TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS odevler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sinif INTEGER,
    sube TEXT,
    ders TEXT,
    kitap TEXT,
    sayfa TEXT,
    tarih TEXT,
    aciklama TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS devamsizlik (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_no INTEGER,
    tarih TEXT,
    sebep TEXT,
    FOREIGN KEY (ogrenci_no) REFERENCES ogrenciler(no)
)
''')

conn.commit()
conn.close()


