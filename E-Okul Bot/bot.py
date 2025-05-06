# Bot.py
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from config import TOKEN, DB_NAME

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def db_connection():
    return sqlite3.connect(DB_NAME)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    await bot.tree.sync()
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if "genel" in channel.name.lower():
                await channel.send("📚 E-Okul Sistem Botu Aktif!\nKomutlar: /kayıt /arsiv /not /guncelle /ders_programı /ödev /devamsızlık /bilgiler /sil /istatistik")

@bot.tree.command(name="kayıt")
async def kayıt(interaction: discord.Interaction, ad: str, soyad: str, sinif: int, sube: str, no: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ogrenciler (ad, soyad, sinif, sube, no) VALUES (?, ?, ?, ?, ?)", (ad, soyad, sinif, sube, no))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ {ad} {soyad} adlı öğrenci kaydedildi.")

@bot.tree.command(name="arsiv")
async def arsiv(interaction: discord.Interaction):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ad, soyad, sinif, sube, no FROM ogrenciler")
    ogrenciler = cursor.fetchall()
    conn.close()

    if not ogrenciler:
        await interaction.response.send_message("❌ Kayıtlı öğrenci yok.")
        return

    msg = "\n".join([f"{o[2]}.{o[3]} - {o[4]} | {o[0]} {o[1]}" for o in ogrenciler])
    await interaction.response.send_message(f"📚 Öğrenci Arşivi:\n{msg}")

@bot.tree.command(name="not")
async def not_gir(interaction: discord.Interaction, ogrenci_no: int, ders: str, notu: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ders_notlari (ogrenci_no, ders, notu) VALUES (?, ?, ?)", (ogrenci_no, ders, notu))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ {ogrenci_no} numaralı öğrencinin {ders} notu kaydedildi.")

@bot.tree.command(name="guncelle")
async def guncelle(interaction: discord.Interaction, no: int, ad: str, soyad: str, sinif: int, sube: str):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ogrenciler SET ad=?, soyad=?, sinif=?, sube=? WHERE no=?", (ad, soyad, sinif, sube, no))
    conn.commit()
    conn.close()
    await interaction.response.send_message("✅ Öğrenci bilgileri güncellendi.")

@bot.tree.command(name="ders_programı")
async def ders_programı(interaction: discord.Interaction, sinif: int, sube: str, gun: str, saat: str, dersler: str):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ders_programi (sinif, sube, gun, saat, dersler) VALUES (?, ?, ?, ?, ?)", (sinif, sube, gun, saat, dersler))
    conn.commit()
    conn.close()
    await interaction.response.send_message("✅ Ders programı girildi.")

@bot.tree.command(name="ödev")
async def odev(interaction: discord.Interaction, sinif: int, sube: str, ders: str, kitap: str, sayfa: str, tarih: str, aciklama: str):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO odevler (sinif, sube, ders, kitap, sayfa, tarih, aciklama) VALUES (?, ?, ?, ?, ?, ?, ?)", (sinif, sube, ders, kitap, sayfa, tarih, aciklama))
    conn.commit()
    conn.close()
    await interaction.response.send_message("✅ Ödev kaydedildi.")

@bot.tree.command(name="devamsızlık")
async def devamsizlik(interaction: discord.Interaction, ogrenci_no: int, tarih: str, sebep: str):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO devamsizlik (ogrenci_no, tarih, sebep) VALUES (?, ?, ?)", (ogrenci_no, tarih, sebep))
    conn.commit()
    conn.close()
    await interaction.response.send_message("✅ Devamsızlık eklendi.")

@bot.tree.command(name="bilgiler")
async def bilgiler(interaction: discord.Interaction, no: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ogrenciler WHERE no = ?", (no,))
    ogrenci = cursor.fetchone()
    conn.close()

    if not ogrenci:
        await interaction.response.send_message("❌ Öğrenci bulunamadı.")
        return

    await interaction.response.send_message(f"👨‍🎓 {ogrenci[1]} {ogrenci[2]}\nSınıf: {ogrenci[3]} {ogrenci[4]}\nNo: {ogrenci[5]}\nKayıt: {ogrenci[6]}")

@bot.tree.command(name="sil")
async def sil(interaction: discord.Interaction, no: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ogrenciler WHERE no = ?", (no,))
    conn.commit()
    conn.close()
    await interaction.response.send_message("✅ Öğrenci silindi.")

@bot.tree.command(name="istatistik")
async def istatistik(interaction: discord.Interaction, sinif: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ders, AVG(notu) FROM ders_notlari JOIN ogrenciler ON ders_notlari.ogrenci_no = ogrenciler.no WHERE ogrenciler.sinif = ? GROUP BY ders", (sinif,))
    veriler = cursor.fetchall()
    conn.close()

    if not veriler:
        await interaction.response.send_message("❌ Bu sınıfta not bilgisi bulunamadı.")
        return

    mesaj = "\n".join([f"{v[0]}: {round(v[1],2)}" for v in veriler])
    await interaction.response.send_message(f"📊 Sınıf {sinif} Ortalama Notlar:\n{mesaj}")

bot.run(TOKEN)