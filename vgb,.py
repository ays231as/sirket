import sqlite3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem


class GezginGemiSirketi:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Y_GEMİ (
                                ID INTEGER PRIMARY KEY,
                                GEMİ_AD TEXT NOT NULL,
                                GEMİ_AGIRLIK REAL NOT NULL,
                                YAPIM_YILI INTEGER NOT NULL,
                                YOLCU_KAPASİTE INTEGER NOT NULL
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS K_GEMİ (
                                ID INTEGER PRIMARY KEY,
                                GEMİ_AD TEXT NOT NULL,
                                GEMİ_AGİRLİK REAL NOT NULL,
                                YAPIM_YILI INTEGER NOT NULL,
                                KONTEYNER_SAYISI_KAPASİTE INTEGER NOT NULL,
                                MAX_AGİRLİK INTEGER NOT NULL
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS P_GEMİ (
                                ID INTEGER PRIMARY KEY,
                                GEMİ_AD TEXT NOT NULL,
                                GEMİ_AGIRLIK REAL NOT NULL,
                                YAPIM_YILI INTEGER NOT NULL,
                                PETROL_KAPASİTE INTEGER NOT NULL

                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Seferler (
                                SEFER_ID INTEGER PRIMARY KEY,
                                GEMİ_ID INTEGER NOT NULL UNIQUE,
                                IDK INTEGER NOT NULL UNIQUE,
                                KAPTAN_SAYISI TEXT NOT NULL,

                                YOLA_CIKIS_TARİHİ TEXT NOT NULL,
                                DONUS_TARİHİ TEXT,
                                GİDİLEN_LİMAN TEXT NOT NULL,
                                GIDILEN_ULKE TEXT NOT NULL,
                                FOREIGN KEY (GEMİ_ID) REFERENCES Gemiler (ID)
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Sefer_Limanlari (
                                SEFER_ID INTEGER NOT NULL,
                                LİMAN_AD TEXT NOT NULL,
                                FOREIGN KEY (SEFER_ID) REFERENCES Seferler (ID)
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Limanlar (
                                LİMAN_AD TEXT NOT NULL,
                                ULKE_AD TEXT NOT NULL,
                                NUFUS INTEGER,
                                PASAPORT_VARYOK INTEGER,
                                DEMİRLEME_UCRETİ REAL,
                                PRIMARY KEY (LİMAN_AD, ULKE_AD)
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Kaptanlar (
                                IDK INTEGER PRIMARY KEY,
                                KAPTAN_AD TEXT NOT NULL,
                                KAPTAN_SOYAD TEXT NOT NULL,
                                ADRES TEXT,
                                VATANDASLIK TEXT,
                                DOGUM_TARİHİ TEXT,
                                İSE_GİRİS_TARİHİ TEXT,
                                KAPTAN_LİSANS TEXT

                                )''')

    def gemi_ekle_Y(self, ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, YOLCU_KAPASİTE):
        self.cursor.execute('''INSERT INTO Y_GEMİ (ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI,YOLCU_KAPASİTE) 
                                VALUES (?, ?, ?, ?, ?)''', (ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, YOLCU_KAPASİTE))
        self.conn.commit()
        print("Gemi eklendi.")

    def gemi_sil_Y(self, ID):
        self.cursor.execute('DELETE FROM Y_GEMİ WHERE ID = ?', (ID,))
        self.conn.commit()
        print("Gemi silindi.")

    def gemi_guncelle_Y(self, ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, YOLCU_KAPASİTE):
        self.cursor.execute("UPDATE Y_GEMİ SET GEMİ_AD=?,GEMİ_AGIRLIK=?,YAPIM_YILI=?,YOLCU_KAPASİTE=? WHERE ID=?",
                            (GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, YOLCU_KAPASİTE, ID))
        self.conn.commit()
        print("Gemi güncellendi.")

    def gemi_listele_Y(self):
        self.cursor.execute("SELECT * FROM Y_GEMİ")
        gemiler = self.cursor.fetchall()
        return gemiler

    def gemi_ekle_K(self, ID, GEMİ_AD, GEMİ_AGİRLİK, YAPIM_YILI, KONTEYNER_SAYISI_KAPASİTE, MAX_AGİRLİK):
        self.cursor.execute('''INSERT INTO K_GEMİ (ID, GEMİ_AD, GEMİ_AGİRLİK, YAPIM_YILI,KONTEYNER_SAYISI_KAPASİTE,MAX_AGİRLİK) 
                                VALUES (?, ?, ?, ?, ?,?)''',
                            (ID, GEMİ_AD, GEMİ_AGİRLİK, YAPIM_YILI, KONTEYNER_SAYISI_KAPASİTE, MAX_AGİRLİK))
        self.conn.commit()

    def gemi_sil_K(self, ID):
        self.cursor.execute("DELETE FROM K_GEMİ WHERE ID=?", (ID,))
        self.conn.commit()
        print("Gemi silindi.")

    def gemi_guncelle_K(self, ID, GEMİ_AD, GEMİ_AGİRLİK, YAPIM_YILI, KONTEYNER_SAYISI_KAPASİTE, MAX_AGİRLİK):
        self.cursor.execute(
            "UPDATE K_GEMİ SET GEMİ_AD=?,GEMİ_AGİRLİK=?,YAPIM_YILI=?,KONTEYNER_SAYISI_KAPASİTE=?,MAX_AGİRLİK=? WHERE ID=?",
            (GEMİ_AD, GEMİ_AGİRLİK, YAPIM_YILI, KONTEYNER_SAYISI_KAPASİTE, MAX_AGİRLİK, ID))
        self.conn.commit()

    def gemi_listele_K(self):
        self.cursor.execute("SELECT * FROM K_GEMİ")
        gemiler = self.cursor.fetchall()
        return gemiler

    def gemi_ekle_P(self, ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, PETROL_KAPASİTE):
        self.cursor.execute('''INSERT INTO P_GEMİ (ID,GEMİ_AD,GEMİ_AGIRLIK,YAPIM_YILI,PETROL_KAPASİTE) 
                                VALUES (?, ?, ?, ?, ?)''', (ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, PETROL_KAPASİTE))
        self.conn.commit()
        print("Gemi eklendi.")

    def gemi_sil_P(self, ID):
        self.cursor.execute('DELETE FROM P_GEMİ WHERE ID = ?', (ID,))
        self.conn.commit()
        print("Gemi silindi.")

    def gemi_guncelle_P(self, ID, GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, PETROL_KAPASİTE):
        self.cursor.execute("UPDATE P_GEMİ SET GEMİ_AD=?,GEMİ_AGIRLIK=?,YAPIM_YILI=?,PETROL_KAPASİTE=? WHERE ID=?",
                            (GEMİ_AD, GEMİ_AGIRLIK, YAPIM_YILI, PETROL_KAPASİTE, ID))
        self.conn.commit()
        print("Gemi güncellendi.")

    def gemi_listele_P(self):
        self.cursor.execute("SELECT * FROM P_GEMİ")
        gemiler = self.cursor.fetchall()
        return gemiler

    def sefer_ekle(self, SEFER_ID, GEMİ_ID, IDK, KAPTAN_SAYISI, YOLA_CIKIS_TARİHİ, DONUS_TARİHİ, GİDİLEN_LİMAN,
                   GIDILEN_ULKE):
        self.cursor.execute('''INSERT INTO Seferler (SEFER_ID,GEMİ_ID,IDK ,KAPTAN_SAYISI,  YOLA_CIKIS_TARİHİ, DONUS_TARİHİ, GİDİLEN_LİMAN,GIDILEN_ULKE) 
                                VALUES (?, ?, ?, ?, ?, ?,?,?)''', (
        SEFER_ID, GEMİ_ID, IDK, KAPTAN_SAYISI, YOLA_CIKIS_TARİHİ, DONUS_TARİHİ, GİDİLEN_LİMAN, GIDILEN_ULKE))
        self.conn.commit()
        print("Sefer eklendi.")

    def sefer_guncelle(self, SEFER_ID, GEMİ_ID, IDK, KAPTAN_SAYISI, YOLA_CIKIS_TARİHİ, DONUS_TARİHİ, GİDİLEN_LİMAN,
                       GIDILEN_ULKE):
        self.cursor.execute(
            "UPDATE Seferler SET  GEMİ_ID=?,IDK=?,  KAPTAN_SAYISI=?, YOLA_CIKIS_TARİHİ=?, DONUS_TARİHİ=?, GİDİLEN_LİMAN=? , GIDILEN_ULKE=? WHERE SEFER_ID=? ",
            (GEMİ_ID, IDK, KAPTAN_SAYISI, YOLA_CIKIS_TARİHİ, DONUS_TARİHİ, GİDİLEN_LİMAN, GIDILEN_ULKE, SEFER_ID))

        self.conn.commit()
        print("Sefer güncellendi.")

    def sefer_sil(self, SEFER_ID):
        self.cursor.execute('''DELETE FROM Seferler WHERE SEFER_ID = ?''', (SEFER_ID,))
        self.conn.commit()

        print("Sefer silindi.")

    def sefer_listele(self):
        self.cursor.execute("SELECT * FROM Seferler")
        seferler = self.cursor.fetchall()
        return seferler

    def liman_ekle(self, LİMAN_AD, ULKE_AD, NUFUS=None, PASAPORT_VARYOK=0, DEMİRLEME_ÜCRETİ=None):
        self.cursor.execute('''INSERT INTO Limanlar (LİMAN_AD, ULKE_AD, NUFUS, PASAPORT_VARYOK, DEMİRLEME_UCRETİ) 
                                VALUES (?, ?, ?, ?, ?)''',
                            (LİMAN_AD, ULKE_AD, NUFUS, PASAPORT_VARYOK, DEMİRLEME_ÜCRETİ))
        self.conn.commit()
        print("Liman eklendi.")

    def liman_guncelle(self, LİMAN_AD, ULKE_AD, NUFUS=None, PASAPORT_VARYOK=0, DEMİRLEME_ÜCRETİ=None):
        self.cursor.execute(
            "UPDATE Limanlar SET NUFUS=?,PASAPORT_VARYOK=?,DEMİRLEME_UCRETİ=? WHERE ULKE_AD=? AND LİMAN_AD=?",
            (NUFUS, PASAPORT_VARYOK, DEMİRLEME_ÜCRETİ, ULKE_AD, LİMAN_AD))
        self.conn.commit()

    def liman_sil(self, LİMAN_AD, ULKE_AD):
        self.cursor.execute('''DELETE FROM Limanlar WHERE LİMAN_AD = ? AND ULKE_AD=?''', (LİMAN_AD, ULKE_AD))
        self.conn.commit()
        print("Liman silindi.")

    def liman_listele(self):
        self.cursor.execute("SELECT * FROM Limanlar")
        seferler = self.cursor.fetchall()
        return seferler

    def kaptan_ekle(self, IDK, KAPTAN_AD, KAPTAN_SOYAD, ADRES=None, VATANDASLIK=None, DOGUM_TARİHİ=None,
                    İSE_GİRİS_TARİHİ=None, KAPTAN_LİSANS=None):
        self.cursor.execute('''INSERT INTO Kaptanlar (IDK,KAPTAN_AD, KAPTAN_SOYAD, ADRES, VATANDASLIK, DOGUM_TARİHİ, İSE_GİRİS_TARİHİ, KAPTAN_LİSANS) 
                                VALUES (?, ?, ?, ?, ?, ?, ?,?)''', (
        IDK, KAPTAN_AD, KAPTAN_SOYAD, ADRES, VATANDASLIK, DOGUM_TARİHİ, İSE_GİRİS_TARİHİ, KAPTAN_LİSANS))
        self.conn.commit()
        print("Kaptan eklendi.")

    def kaptan_guncelle(self, IDK, KAPTAN_AD, KAPTAN_SOYAD, ADRES=None, VATANDASLIK=None, DOGUM_TARİHİ=None,
                        İSE_GİRİS_TARİHİ=None, KAPTAN_LİSANS=None):
        self.cursor.execute(
            "UPDATE Kaptanlar SET KAPTAN_AD=?, KAPTAN_SOYAD=?, ADRES=?, VATANDASLIK=?, DOGUM_TARİHİ=?, İSE_GİRİS_TARİHİ=?, KAPTAN_LİSANS=? WHERE IDK=?",
            (KAPTAN_AD, KAPTAN_SOYAD, ADRES, VATANDASLIK, DOGUM_TARİHİ, İSE_GİRİS_TARİHİ, KAPTAN_LİSANS, IDK))
        self.conn.commit()

    def kaptan_sil(self, IDK):
        self.cursor.execute('''DELETE FROM Kaptanlar WHERE IDK = ?''', (IDK,))
        self.conn.commit()
        print("Kaptan silindi.")

    def kaptan_listele(self):
        self.cursor.execute("SELECT * FROM Kaptanlar")
        seferler = self.cursor.fetchall()
        return seferler

    def __del__(self):
        self.conn.close()


sirket = GezginGemiSirketi("sirket.db")


class Ui_Dialog(object):
    def sefer_ekle_buton(self):
        try:

            if self.sefer_sec_ekle.isChecked():
                sirket.sefer_ekle(int(self.sefer_id.text()), self.sefer_gemi_seri_no.text(),
                                  self.sefer_kaptan_id.text(), self.sefer_kaptan_sayisi.text(),
                                  self.yola_cikis_tarih.text(), self.donus_tarihi.text(),
                                  self.sefer_gidilen_liman.text(), self.sefer_gidilen_ulke.text())
                self.tablo_yukleme()
            if self.sefer_gec_guncelle.isChecked():
                sirket.sefer_guncelle(int(self.sefer_id.text()), self.sefer_gemi_seri_no.text(),
                                      self.sefer_kaptan_id.text(), self.sefer_kaptan_sayisi.text(),
                                      self.yola_cikis_tarih.text(), self.donus_tarihi.text(),
                                      self.sefer_gidilen_liman.text(), self.sefer_gidilen_ulke.text())
                self.tablo_yukleme()
        except ValueError:
            pass
        except sqlite3.IntegrityError:
            pass

    def gemi_ekle_buton(self):

        try:
            if self.gemiler_sec_ekle.isChecked():

                if self.K1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(False)
                    self.gemiler_yolcu_kapasite.setEnabled(False)
                    self.gemiler_k_sayi_kapasite.setEnabled(True)
                    self.gemiler_konteyner_max_agirlik.setEnabled(True)
                    sirket.gemi_ekle_K(int(self.gemiler_id.text()), self.gemiler_ad.text(), self.gemiler_agirlik.text(),
                                       self.gemiler_yapim_yil.text(), self.gemiler_k_sayi_kapasite.text(),
                                       self.gemiler_konteyner_max_agirlik.text())

                elif self.Y1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(False)
                    self.gemiler_yolcu_kapasite.setEnabled(True)
                    self.gemiler_k_sayi_kapasite.setEnabled(False)
                    self.gemiler_konteyner_max_agirlik.setEnabled(False)
                    sirket.gemi_ekle_Y(int(self.gemiler_id.text()), self.gemiler_ad.text(), self.gemiler_agirlik.text(),
                                       self.gemiler_yapim_yil.text(), self.gemiler_yolcu_kapasite.text())
                elif self.P1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(True)
                    self.gemiler_yolcu_kapasite.setEnabled(False)
                    self.gemiler_k_sayi_kapasite.setEnabled(False)
                    self.gemiler_konteyner_max_agirlik.setEnabled(False)
                    sirket.gemi_ekle_P(int(self.gemiler_id.text()), self.gemiler_ad.text(), self.gemiler_agirlik.text(),
                                       self.gemiler_yapim_yil.text(), self.gemiler_petrol_kapasite.text())
                self.tablo_yukleme()
            if self.gemiler_sec_guncelle.isChecked():
                if self.K1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(False)
                    self.gemiler_yolcu_kapasite.setEnabled(False)
                    self.gemiler_k_sayi_kapasite.setEnabled(True)
                    self.gemiler_konteyner_max_agirlik.setEnabled(True)
                    sirket.gemi_guncelle_K(int(self.gemiler_id.text()), self.gemiler_ad.text(),
                                           self.gemiler_agirlik.text(), self.gemiler_yapim_yil.text(),
                                           self.gemiler_k_sayi_kapasite.text(),
                                           self.gemiler_konteyner_max_agirlik.text())
                elif self.Y1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(False)
                    self.gemiler_yolcu_kapasite.setEnabled(True)
                    self.gemiler_k_sayi_kapasite.setEnabled(False)
                    self.gemiler_konteyner_max_agirlik.setEnabled(False)
                    sirket.gemi_guncelle_Y(int(self.gemiler_id.text()), self.gemiler_ad.text(),
                                           self.gemiler_agirlik.text(), self.gemiler_yapim_yil.text(),
                                           self.gemiler_yolcu_kapasite.text())
                elif self.P1.isChecked():
                    self.gemiler_petrol_kapasite.setEnabled(True)
                    self.gemiler_yolcu_kapasite.setEnabled(False)
                    self.gemiler_k_sayi_kapasite.setEnabled(False)
                    self.gemiler_konteyner_max_agirlik.setEnabled(False)
                    sirket.gemi_guncelle_P(int(self.gemiler_id.text()), self.gemiler_ad.text(),
                                           self.gemiler_agirlik.text(), self.gemiler_yapim_yil.text(),
                                           self.gemiler_petrol_kapasite.text())
                self.tablo_yukleme()
        except sqlite3.IntegrityError:
            pass
        except ValueError:
            pass

    def gemiler_sil(self):

        if self.Y2.isChecked():
            sirket.gemi_sil_Y(self.silinecek_gemiler_id.text())
        elif self.P2.isChecked():
            sirket.gemi_sil_P(self.silinecek_gemiler_id.text())
        elif self.K2.isChecked():
            sirket.gemi_sil_K(self.silinecek_gemiler_id.text())
        self.tablo_yukleme()

    def sefer_sil_butonn(self):
        sirket.sefer_sil(self.silinecek_sefer_id.text())
        self.tablo_yukleme()

    def liman_ekle_guncelle_buton(self):
        if self.liman_sec_ekle.isChecked():
            sirket.liman_ekle(self.liman_ad.text(), self.ulke_ad.text(), self.liman_nufus.text(),
                              self.pasaport_v_y.text(), self.liman_demirleme_ucret.text())
            self.tablo_yukleme()
        if self.liman_sec_guncelle.isChecked():
            sirket.liman_guncelle(self.liman_ad.text(), self.ulke_ad.text(), self.liman_nufus.text(),
                                  self.pasaport_v_y.text(), self.liman_demirleme_ucret.text())
            self.tablo_yukleme()

    def liman_sil_butonn(self):
        veri = self.silinecek_liman_ulke.text().split(",")

        sirket.liman_sil(veri[0], veri[1])
        self.tablo_yukleme()

    def kaptan_sill(self):
        sirket.kaptan_sil(self.silinecek_k_m_buton.text())
        self.tablo_yukleme()

    def tablo_yukleme(self):
        sefer = sirket.sefer_listele()
        gemiK = sirket.gemi_listele_K()
        gemiP = sirket.gemi_listele_P()
        gemiY = sirket.gemi_listele_Y()
        liman = sirket.liman_listele()
        kaptan = sirket.kaptan_listele()
        try:

            for row_index, row_data in enumerate(sefer):

                self.sefer_tablosu.insertRow(self.sefer_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.sefer_tablosu.setItem(row_index, column_index, item)

            for row_index, row_data in enumerate(gemiK):

                self.konteyner_tablosu.insertRow(self.konteyner_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.konteyner_tablosu.setItem(row_index, column_index, item)
            for row_index, row_data in enumerate(gemiP):

                self.petrol_tablosu.insertRow(self.petrol_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.petrol_tablosu.setItem(row_index, column_index, item)
            for row_index, row_data in enumerate(gemiY):

                self.yolcu_tablosu.insertRow(self.yolcu_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.yolcu_tablosu.setItem(row_index, column_index, item)
            for row_index, row_data in enumerate(liman):

                self.liman_tablosu.insertRow(self.liman_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.liman_tablosu.setItem(row_index, column_index, item)
            for row_index, row_data in enumerate(kaptan):

                self.kaptan_murettebat_tablosu.insertRow(self.kaptan_murettebat_tablosu.rowCount())
                for column_index, veri in enumerate(row_data):
                    item = QTableWidgetItem(str(veri))
                    self.kaptan_murettebat_tablosu.setItem(row_index, column_index, item)
        except ValueError:
            pass

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1265, 925)
        self.seferler = QtWidgets.QLabel(Dialog)
        self.seferler.setGeometry(QtCore.QRect(60, 20, 101, 16))
        self.seferler.setObjectName("seferler")
        self.petrol_gemileri = QtWidgets.QLabel(Dialog)
        self.petrol_gemileri.setGeometry(QtCore.QRect(400, 10, 111, 16))
        self.petrol_gemileri.setObjectName("petrol_gemileri")
        self.limanlar = QtWidgets.QLabel(Dialog)
        self.limanlar.setGeometry(QtCore.QRect(740, 10, 81, 20))
        self.limanlar.setObjectName("limanlar")
        self.kaptanlar_ve_murettabatlar = QtWidgets.QLabel(Dialog)
        self.kaptanlar_ve_murettabatlar.setGeometry(QtCore.QRect(890, 10, 201, 21))
        self.kaptanlar_ve_murettabatlar.setObjectName("kaptanlar_ve_murettabatlar")
        self.sefer_sec_ekle = QtWidgets.QRadioButton(Dialog)
        self.sefer_sec_ekle.setGeometry(QtCore.QRect(60, 40, 95, 20))
        self.sefer_sec_ekle.setObjectName("sefer_sec_ekle")
        self.sefer_gec_guncelle = QtWidgets.QRadioButton(Dialog)
        self.sefer_gec_guncelle.setGeometry(QtCore.QRect(60, 90, 95, 20))
        self.sefer_gec_guncelle.setObjectName("sefer_gec_guncelle")
        self.gemiler_sec_ekle = QtWidgets.QRadioButton(Dialog)
        self.gemiler_sec_ekle.setGeometry(QtCore.QRect(410, 40, 95, 20))
        self.gemiler_sec_ekle.setObjectName("gemiler_sec_ekle")
        self.gemiler_sec_guncelle = QtWidgets.QRadioButton(Dialog)
        self.gemiler_sec_guncelle.setGeometry(QtCore.QRect(410, 90, 95, 20))
        self.gemiler_sec_guncelle.setObjectName("gemiler_sec_guncelle")
        self.liman_sec_guncelle = QtWidgets.QRadioButton(Dialog)
        self.liman_sec_guncelle.setGeometry(QtCore.QRect(750, 90, 95, 20))
        self.liman_sec_guncelle.setObjectName("liman_sec_guncelle")
        self.guncelle = QtWidgets.QRadioButton(Dialog)
        self.guncelle.setGeometry(QtCore.QRect(930, 90, 95, 20))
        self.guncelle.setObjectName("guncelle")
        self.liman_sec_ekle = QtWidgets.QRadioButton(Dialog)
        self.liman_sec_ekle.setGeometry(QtCore.QRect(750, 50, 95, 20))
        self.liman_sec_ekle.setObjectName("liman_sec_ekle")
        self.ekle = QtWidgets.QRadioButton(Dialog)
        self.ekle.setGeometry(QtCore.QRect(930, 50, 95, 20))
        self.ekle.setObjectName("ekle")
        self.sefer_ekle_guncelle = QtWidgets.QPushButton(Dialog)
        self.sefer_ekle_guncelle.setGeometry(QtCore.QRect(60, 440, 111, 28))
        self.sefer_ekle_guncelle.setObjectName("sefer_ekle_guncelle")
        self.sefer_ekle_guncelle.clicked.connect(self.sefer_ekle_buton)
        self.kayit_sil_2 = QtWidgets.QLabel(Dialog)
        self.kayit_sil_2.setGeometry(QtCore.QRect(80, 490, 101, 16))
        self.kayit_sil_2.setObjectName("kayit_sil_2")
        self.sefer_sil_buton = QtWidgets.QPushButton(Dialog)
        self.sefer_sil_buton.setGeometry(QtCore.QRect(70, 600, 93, 28))
        self.sefer_sil_buton.setObjectName("sefer_sil_buton")
        self.sefer_sil_buton.clicked.connect(self.sefer_sil_butonn)
        self.gemiler_ekle_guncelle = QtWidgets.QPushButton(Dialog)
        self.gemiler_ekle_guncelle.setGeometry(QtCore.QRect(400, 450, 121, 28))
        self.gemiler_ekle_guncelle.setObjectName("gemiler_ekle_guncelle")
        self.gemiler_ekle_guncelle.clicked.connect(self.gemi_ekle_buton)
        self.kayit_silme_2 = QtWidgets.QLabel(Dialog)
        self.kayit_silme_2.setGeometry(QtCore.QRect(430, 490, 91, 16))
        self.kayit_silme_2.setObjectName("kayit_silme_2")
        self.gemiler_sil_buton = QtWidgets.QPushButton(Dialog)
        self.gemiler_sil_buton.setGeometry(QtCore.QRect(420, 600, 93, 28))
        self.gemiler_sil_buton.setObjectName("gemiler_sil_buton")
        self.gemiler_sil_buton.clicked.connect(self.gemiler_sil)
        self.liman_ekle_guncelle = QtWidgets.QPushButton(Dialog)
        self.liman_ekle_guncelle.setGeometry(QtCore.QRect(740, 350, 121, 28))
        self.liman_ekle_guncelle.setObjectName("liman_ekle_guncelle")
        self.liman_ekle_guncelle.clicked.connect(self.liman_ekle_guncelle_buton)
        self.kayt_silme = QtWidgets.QLabel(Dialog)
        self.kayt_silme.setGeometry(QtCore.QRect(760, 490, 91, 16))
        self.kayt_silme.setObjectName("kayt_silme")
        self.liman_sil_buton = QtWidgets.QPushButton(Dialog)
        self.liman_sil_buton.setGeometry(QtCore.QRect(750, 600, 93, 28))
        self.liman_sil_buton.setObjectName("liman_sil_buton")
        self.liman_sil_buton.clicked.connect(self.liman_sil_butonn)
        self.kaptan_ekle_guncelle = QtWidgets.QPushButton(Dialog)
        self.kaptan_ekle_guncelle.setGeometry(QtCore.QRect(930, 460, 111, 28))
        self.kaptan_ekle_guncelle.setObjectName("kaptan_ekle_guncelle")
        self.kaptan_ekle_guncelle.clicked.connect(self.kaptan_guncelle_ekle)
        self.kayit_silme = QtWidgets.QLabel(Dialog)
        self.kayit_silme.setGeometry(QtCore.QRect(940, 510, 91, 16))
        self.kayit_silme.setObjectName("kayit_silme")
        self.kaptan_sil_buton = QtWidgets.QPushButton(Dialog)
        self.kaptan_sil_buton.setGeometry(QtCore.QRect(940, 600, 93, 28))
        self.kaptan_sil_buton.setObjectName("kaptan_sil_buton")
        self.kaptan_sil_buton.clicked.connect(self.kaptan_sill)
        self.sefer_tablosu = QtWidgets.QTableWidget(Dialog)
        self.sefer_tablosu.setGeometry(QtCore.QRect(10, 650, 181, 192))
        self.sefer_tablosu.setObjectName("sefer_tablosu")
        self.sefer_tablosu.setColumnCount(8)
        self.sefer_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.sefer_tablosu.setHorizontalHeaderItem(7, item)

        self.yolcu_tablosu = QtWidgets.QTableWidget(Dialog)
        self.yolcu_tablosu.setGeometry(QtCore.QRect(200, 650, 171, 192))
        self.yolcu_tablosu.setObjectName("yolcu_tablosu")
        self.yolcu_tablosu.setColumnCount(5)
        self.yolcu_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.yolcu_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcu_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcu_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcu_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcu_tablosu.setHorizontalHeaderItem(4, item)
        self.petrol_tablosu = QtWidgets.QTableWidget(Dialog)
        self.petrol_tablosu.setGeometry(QtCore.QRect(380, 650, 201, 192))
        self.petrol_tablosu.setObjectName("petrol_tablosu")
        self.petrol_tablosu.setColumnCount(5)
        self.petrol_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.petrol_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrol_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrol_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrol_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrol_tablosu.setHorizontalHeaderItem(4, item)
        self.konteyner_tablosu = QtWidgets.QTableWidget(Dialog)
        self.konteyner_tablosu.setGeometry(QtCore.QRect(590, 650, 211, 192))
        self.konteyner_tablosu.setObjectName("konteyner_tablosu")
        self.konteyner_tablosu.setColumnCount(6)
        self.konteyner_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteyner_tablosu.setHorizontalHeaderItem(5, item)
        self.liman_tablosu = QtWidgets.QTableWidget(Dialog)
        self.liman_tablosu.setGeometry(QtCore.QRect(810, 650, 201, 192))
        self.liman_tablosu.setObjectName("liman_tablosu")
        self.liman_tablosu.setColumnCount(5)
        self.liman_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.liman_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.liman_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.liman_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.liman_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.liman_tablosu.setHorizontalHeaderItem(4, item)
        self.kaptan_murettebat_tablosu = QtWidgets.QTableWidget(Dialog)
        self.kaptan_murettebat_tablosu.setGeometry(QtCore.QRect(1020, 650, 231, 192))
        self.kaptan_murettebat_tablosu.setObjectName("kaptan_murettebat_tablosu")
        self.kaptan_murettebat_tablosu.setColumnCount(9)
        self.kaptan_murettebat_tablosu.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptan_murettebat_tablosu.setHorizontalHeaderItem(8, item)
        self.gemiler_id = QtWidgets.QLineEdit(Dialog)
        self.gemiler_id.setGeometry(QtCore.QRect(400, 150, 113, 20))
        self.gemiler_id.setObjectName("gemiler_id")
        self.gemiler_ad = QtWidgets.QLineEdit(Dialog)
        self.gemiler_ad.setGeometry(QtCore.QRect(400, 200, 113, 20))
        self.gemiler_ad.setObjectName("gemiler_ad")
        self.gemiler_agirlik = QtWidgets.QLineEdit(Dialog)
        self.gemiler_agirlik.setGeometry(QtCore.QRect(400, 250, 113, 20))
        self.gemiler_agirlik.setObjectName("gemiler_agirlik")
        self.gemiler_yapim_yil = QtWidgets.QLineEdit(Dialog)
        self.gemiler_yapim_yil.setGeometry(QtCore.QRect(400, 300, 113, 20))
        self.gemiler_yapim_yil.setObjectName("gemiler_yapim_yil")
        self.gemiler_yolcu_kapasite = QtWidgets.QLineEdit(Dialog)
        self.gemiler_yolcu_kapasite.setGeometry(QtCore.QRect(400, 340, 113, 20))
        self.gemiler_yolcu_kapasite.setObjectName("gemiler_yolcu_kapasite")
        self.gemiler_petrol_kapasite = QtWidgets.QLineEdit(Dialog)
        self.gemiler_petrol_kapasite.setGeometry(QtCore.QRect(290, 380, 113, 20))
        self.gemiler_petrol_kapasite.setObjectName("gemiler_petrol_kapasite")
        self.gemiler_k_sayi_kapasite = QtWidgets.QLineEdit(Dialog)
        self.gemiler_k_sayi_kapasite.setGeometry(QtCore.QRect(530, 380, 151, 20))
        self.gemiler_k_sayi_kapasite.setObjectName("gemiler_k_sayi_kapasite")
        self.silinecek_gemiler_id = QtWidgets.QLineEdit(Dialog)
        self.silinecek_gemiler_id.setGeometry(QtCore.QRect(420, 540, 113, 20))
        self.silinecek_gemiler_id.setObjectName("silinecek_gemiler_id")
        self.gemiler_konteyner_max_agirlik = QtWidgets.QLineEdit(Dialog)
        self.gemiler_konteyner_max_agirlik.setGeometry(QtCore.QRect(532, 420, 141, 20))
        self.gemiler_konteyner_max_agirlik.setObjectName("gemiler_konteyner_max_agirlik")
        self.kaptan_ad = QtWidgets.QLineEdit(Dialog)
        self.kaptan_ad.setGeometry(QtCore.QRect(930, 160, 113, 20))
        self.kaptan_ad.setObjectName("kaptan_ad")
        self.kaptan_soyad = QtWidgets.QLineEdit(Dialog)
        self.kaptan_soyad.setGeometry(QtCore.QRect(930, 200, 113, 20))
        self.kaptan_soyad.setObjectName("kaptan_soyad")
        self.kaptan_adres = QtWidgets.QLineEdit(Dialog)
        self.kaptan_adres.setGeometry(QtCore.QRect(930, 240, 113, 20))
        self.kaptan_adres.setObjectName("kaptan_adres")
        self.id_k_m = QtWidgets.QLineEdit(Dialog)
        self.id_k_m.setGeometry(QtCore.QRect(930, 120, 113, 20))
        self.id_k_m.setObjectName("id_k_m")
        self.kaptan_dogum_Tarih = QtWidgets.QLineEdit(Dialog)
        self.kaptan_dogum_Tarih.setGeometry(QtCore.QRect(930, 280, 113, 20))
        self.kaptan_dogum_Tarih.setObjectName("kaptan_dogum_Tarih")
        self.kaptan_ise_giris = QtWidgets.QLineEdit(Dialog)
        self.kaptan_ise_giris.setGeometry(QtCore.QRect(930, 320, 113, 20))
        self.kaptan_ise_giris.setObjectName("kaptan_ise_giris")
        self.kaptan_vatandaslik = QtWidgets.QLineEdit(Dialog)
        self.kaptan_vatandaslik.setGeometry(QtCore.QRect(930, 350, 113, 20))
        self.kaptan_vatandaslik.setObjectName("kaptan_vatandaslik")
        self.kaptan_gorev = QtWidgets.QLineEdit(Dialog)
        self.kaptan_gorev.setGeometry(QtCore.QRect(930, 390, 113, 20))
        self.kaptan_gorev.setObjectName("kaptan_gorev")
        self.kaptan_lisans = QtWidgets.QLineEdit(Dialog)
        self.kaptan_lisans.setGeometry(QtCore.QRect(930, 420, 113, 20))
        self.kaptan_lisans.setObjectName("kaptan_lisans")
        self.silinecek_k_m_buton = QtWidgets.QLineEdit(Dialog)
        self.silinecek_k_m_buton.setGeometry(QtCore.QRect(930, 540, 113, 20))
        self.silinecek_k_m_buton.setObjectName("silinecek_k_m_buton")
        self.liman_ad = QtWidgets.QLineEdit(Dialog)
        self.liman_ad.setGeometry(QtCore.QRect(740, 140, 113, 20))
        self.liman_ad.setObjectName("liman_ad")
        self.ulke_ad = QtWidgets.QLineEdit(Dialog)
        self.ulke_ad.setGeometry(QtCore.QRect(740, 180, 113, 20))
        self.ulke_ad.setObjectName("ulke_ad")
        self.liman_nufus = QtWidgets.QLineEdit(Dialog)
        self.liman_nufus.setGeometry(QtCore.QRect(740, 220, 113, 20))
        self.liman_nufus.setObjectName("liman_nufus")
        self.pasaport_v_y = QtWidgets.QLineEdit(Dialog)
        self.pasaport_v_y.setGeometry(QtCore.QRect(740, 260, 113, 20))
        self.pasaport_v_y.setObjectName("pasaport_v_y")
        self.liman_demirleme_ucret = QtWidgets.QLineEdit(Dialog)
        self.liman_demirleme_ucret.setGeometry(QtCore.QRect(740, 300, 113, 20))
        self.liman_demirleme_ucret.setObjectName("liman_demirleme_ucret")
        self.silinecek_liman_ulke = QtWidgets.QLineEdit(Dialog)
        self.silinecek_liman_ulke.setGeometry(QtCore.QRect(702, 540, 171, 20))
        self.silinecek_liman_ulke.setObjectName("silinecek_liman_ulke")
        self.silinecek_sefer_id = QtWidgets.QLineEdit(Dialog)
        self.silinecek_sefer_id.setGeometry(QtCore.QRect(70, 540, 113, 20))
        self.silinecek_sefer_id.setObjectName("silinecek_sefer_id")
        self.sefer_gemi_seri_no = QtWidgets.QLineEdit(Dialog)
        self.sefer_gemi_seri_no.setGeometry(QtCore.QRect(60, 400, 113, 20))
        self.sefer_gemi_seri_no.setObjectName("sefer_gemi_seri_no")
        self.sefer_kaptan_id = QtWidgets.QLineEdit(Dialog)
        self.sefer_kaptan_id.setGeometry(QtCore.QRect(60, 360, 113, 20))
        self.sefer_kaptan_id.setObjectName("sefer_kaptan_id")
        self.sefer_gidilen_ulke = QtWidgets.QLineEdit(Dialog)
        self.sefer_gidilen_ulke.setGeometry(QtCore.QRect(60, 320, 113, 20))
        self.sefer_gidilen_ulke.setObjectName("sefer_gidilen_ulke")
        self.sefer_gidilen_liman = QtWidgets.QLineEdit(Dialog)
        self.sefer_gidilen_liman.setGeometry(QtCore.QRect(60, 280, 113, 20))
        self.sefer_gidilen_liman.setObjectName("sefer_gidilen_liman")
        self.donus_tarihi = QtWidgets.QLineEdit(Dialog)
        self.donus_tarihi.setGeometry(QtCore.QRect(60, 240, 113, 20))
        self.donus_tarihi.setObjectName("donus_tarihi")
        self.yola_cikis_tarih = QtWidgets.QLineEdit(Dialog)
        self.yola_cikis_tarih.setGeometry(QtCore.QRect(60, 200, 113, 20))
        self.yola_cikis_tarih.setObjectName("yola_cikis_tarih")
        self.sefer_id = QtWidgets.QLineEdit(Dialog)
        self.sefer_id.setGeometry(QtCore.QRect(60, 160, 113, 20))
        self.sefer_id.setObjectName("sefer_id")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(320, 510, 101, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Y2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.Y2.setObjectName("Y2")
        self.verticalLayout.addWidget(self.Y2)
        self.K2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.K2.setObjectName("K2")
        self.verticalLayout.addWidget(self.K2)
        self.P2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.P2.setObjectName("P2")
        self.verticalLayout.addWidget(self.P2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(410, 370, 94, 81))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.K1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.K1.setObjectName("K1")
        self.verticalLayout_2.addWidget(self.K1)
        self.K1.toggled.connect(self.control)
        self.Y1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.Y1.setObjectName("Y1")
        self.verticalLayout_2.addWidget(self.Y1)
        self.Y1.toggled.connect(self.control)
        self.P1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.P1.setObjectName("P1")
        self.verticalLayout_2.addWidget(self.P1)
        self.P1.toggled.connect(self.control)
        self.sefer_kaptan_sayisi = QtWidgets.QLineEdit(Dialog)
        self.sefer_kaptan_sayisi.setGeometry(QtCore.QRect(180, 360, 113, 20))
        self.sefer_kaptan_sayisi.setObjectName("sefer_kaptan_sayisi")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.tablo_yukleme()

    def kaptan_guncelle_ekle(self):
        try:
            if self.ekle.isChecked():
                sirket.kaptan_ekle(int(self.id_k_m.text()), self.kaptan_ad.text(), self.kaptan_soyad.text(),
                                   self.kaptan_adres.text(), self.kaptan_vatandaslik.text(),
                                   self.kaptan_dogum_Tarih.text(), self.kaptan_ise_giris.text(),
                                   self.kaptan_lisans.text())
            if self.guncelle.isChecked():
                sirket.kaptan_guncelle(int(self.id_k_m.text()), self.kaptan_ad.text(), self.kaptan_soyad.text(),
                                       self.kaptan_adres.text(), self.kaptan_vatandaslik.text(),
                                       self.kaptan_dogum_Tarih.text(), self.kaptan_ise_giris.text(),
                                       self.kaptan_lisans.text())
            self.tablo_yukleme()
        except ValueError:
            pass
        except sqlite3.IntegrityError:
            pass

    def control(self):
        if self.K1.isChecked():
            self.gemiler_petrol_kapasite.setEnabled(False)
            self.gemiler_yolcu_kapasite.setEnabled(False)
            self.gemiler_k_sayi_kapasite.setEnabled(True)
            self.gemiler_konteyner_max_agirlik.setEnabled(True)

        elif self.Y1.isChecked():
            self.gemiler_petrol_kapasite.setEnabled(False)
            self.gemiler_yolcu_kapasite.setEnabled(True)
            self.gemiler_k_sayi_kapasite.setEnabled(False)
            self.gemiler_konteyner_max_agirlik.setEnabled(False)
        elif self.P1.isChecked():
            self.gemiler_petrol_kapasite.setEnabled(True)
            self.gemiler_yolcu_kapasite.setEnabled(False)
            self.gemiler_k_sayi_kapasite.setEnabled(False)
            self.gemiler_konteyner_max_agirlik.setEnabled(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.seferler.setText(_translate("Dialog", "SEFERLER"))
        self.petrol_gemileri.setText(_translate("Dialog", "GEMİLER"))
        self.limanlar.setText(_translate("Dialog", "LİMANLAR"))
        self.kaptanlar_ve_murettabatlar.setText(_translate("Dialog", "KAPTANLAR_VE_MURETTABATLAR"))
        self.sefer_sec_ekle.setText(_translate("Dialog", "EKLE"))
        self.sefer_gec_guncelle.setText(_translate("Dialog", "GUNCELLE"))
        self.gemiler_sec_ekle.setText(_translate("Dialog", "EKLE"))
        self.gemiler_sec_guncelle.setText(_translate("Dialog", "GUNCELLE"))
        self.liman_sec_guncelle.setText(_translate("Dialog", "GUNCELLE"))
        self.guncelle.setText(_translate("Dialog", "GUNCELLE"))
        self.liman_sec_ekle.setText(_translate("Dialog", "EKLE"))
        self.ekle.setText(_translate("Dialog", "EKLE"))
        self.sefer_ekle_guncelle.setText(_translate("Dialog", "EKLE_GUNCELLE"))
        self.kayit_sil_2.setText(_translate("Dialog", "KAYİT_SİL"))
        self.sefer_sil_buton.setText(_translate("Dialog", "SEFER_SİL"))
        self.gemiler_ekle_guncelle.setText(_translate("Dialog", "EKLE_GUNCELLE"))
        self.kayit_silme_2.setText(_translate("Dialog", "KAYİT_SİLME"))
        self.gemiler_sil_buton.setText(_translate("Dialog", "GEMİ_SİL"))
        self.liman_ekle_guncelle.setText(_translate("Dialog", "EKLE_GUNCELLE"))
        self.kayt_silme.setText(_translate("Dialog", "KAYIT_SİLME"))
        self.liman_sil_buton.setText(_translate("Dialog", "LİMAN_SİL"))
        self.kaptan_ekle_guncelle.setText(_translate("Dialog", "EKLE_GUNCELLE"))
        self.kayit_silme.setText(_translate("Dialog", "KAYİT_SİLME"))
        self.kaptan_sil_buton.setText(_translate("Dialog", "KAPTAN_SİL"))
        item = self.sefer_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "SEFER İD"))
        item = self.sefer_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "GEMİ SERİ NO"))
        item = self.sefer_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "KAPTAN İD"))
        item = self.sefer_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "KAPTAN_SAYISI"))

        item = self.sefer_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "YOLA CİKİS TARİH"))
        item = self.sefer_tablosu.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "DONUS TARİH"))
        item = self.sefer_tablosu.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "GİDİLEN LİMAN"))
        item = self.sefer_tablosu.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "GIDILEN ULKE"))
        item = self.yolcu_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "GEMİ İD"))
        item = self.yolcu_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "GEMİ AD"))
        item = self.yolcu_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "GEMİ AGİRLİK"))
        item = self.yolcu_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "YAPİM YİLİ"))
        item = self.yolcu_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "YOLCU KAPASİTE"))
        item = self.petrol_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "GEMİ İD"))
        item = self.petrol_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "GEMİ AD"))
        item = self.petrol_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "GEMİ AGİRLİK"))
        item = self.petrol_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", " YAPİM_YİLİ"))
        item = self.petrol_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", " PETROL KAPASİTE"))
        item = self.konteyner_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "GEMİ İD"))
        item = self.konteyner_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "GEMİ AD"))
        item = self.konteyner_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "GEMİ AGİRLİK"))
        item = self.konteyner_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "YAPİM YİL"))
        item = self.konteyner_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "KONTEYNER SAYI KAPASİTE"))
        item = self.konteyner_tablosu.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "MAX AGİRLİK"))
        item = self.liman_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "LIMAN AD"))
        item = self.liman_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "ULKE AD"))
        item = self.liman_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "NUFUS"))
        item = self.liman_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "PASAPORT VAR/YOK"))
        item = self.liman_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "DEMİRLEME UCRETİ"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "İD_K_M"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "KAPTAN İD"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "KAPTAN SOYAD"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "ADRES"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "New Column"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "İSE GİRİS TARİH"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "VATANDASLIK"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "GOREV"))
        item = self.kaptan_murettebat_tablosu.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "KAPTAN_LİSANS"))
        self.gemiler_id.setText(_translate("Dialog", "GEMİ İD"))
        self.gemiler_ad.setText(_translate("Dialog", "GEMİ AD"))
        self.gemiler_agirlik.setText(_translate("Dialog", "GEMİ AGİRLİK"))
        self.gemiler_yapim_yil.setText(_translate("Dialog", "YAPİM YİL"))
        self.gemiler_yolcu_kapasite.setText(_translate("Dialog", "YOLCU KAPASİTE"))
        self.gemiler_petrol_kapasite.setText(_translate("Dialog", "PETROL KAPASİTE"))
        self.gemiler_k_sayi_kapasite.setText(_translate("Dialog", "KONTEYNER SAYI KAPASİTE"))
        self.silinecek_gemiler_id.setText(_translate("Dialog", "SİLİNECEK GEMİ İD"))
        self.gemiler_konteyner_max_agirlik.setText(_translate("Dialog", "MAX AGİRLİK"))
        self.kaptan_ad.setText(_translate("Dialog", "KAPTAN AD"))
        self.kaptan_soyad.setText(_translate("Dialog", "KAPTAN SOYAD"))
        self.kaptan_adres.setText(_translate("Dialog", "ADRES"))
        self.id_k_m.setText(_translate("Dialog", "İD_K_M"))
        self.kaptan_dogum_Tarih.setText(_translate("Dialog", "DOGUM TARİHİ"))
        self.kaptan_ise_giris.setText(_translate("Dialog", "İSE GİRİS TARİHİ"))
        self.kaptan_vatandaslik.setText(_translate("Dialog", "VATANDASLIK"))
        self.kaptan_gorev.setText(_translate("Dialog", "GOREV"))
        self.kaptan_lisans.setText(_translate("Dialog", "KAPTAN_LİSANS"))
        self.silinecek_k_m_buton.setText(_translate("Dialog", "SİLİNECEK_K_M İD"))
        self.liman_ad.setText(_translate("Dialog", "LIMAN AD"))
        self.ulke_ad.setText(_translate("Dialog", "ULKE AD"))
        self.liman_nufus.setText(_translate("Dialog", "NUFUS"))
        self.pasaport_v_y.setText(_translate("Dialog", "PASAPORT VAR/YOK"))
        self.liman_demirleme_ucret.setText(_translate("Dialog", "DEMİRLEME UCRETİ"))
        self.silinecek_liman_ulke.setText(_translate("Dialog", "SİLİNECEK LİMAN AD,ULKE AD"))
        self.silinecek_sefer_id.setText(_translate("Dialog", "SİLİNECEK SEFER İD"))
        self.sefer_gemi_seri_no.setText(_translate("Dialog", "GEMİ SERİ NO"))
        self.sefer_kaptan_id.setText(_translate("Dialog", "KAPTAN İD"))
        self.sefer_gidilen_ulke.setText(_translate("Dialog", "GİDİLEN ULKE"))
        self.sefer_gidilen_liman.setText(_translate("Dialog", "GİDİLEN LİMAN"))
        self.donus_tarihi.setText(_translate("Dialog", "DONUS TARİHİ"))
        self.yola_cikis_tarih.setText(_translate("Dialog", "YOLA CİKİS TARİHİ"))
        self.sefer_id.setText(_translate("Dialog", "SEFER İD"))
        self.Y2.setText(_translate("Dialog", "YOLCU G"))
        self.K2.setText(_translate("Dialog", "KONTEYNER G"))
        self.P2.setText(_translate("Dialog", "PETROL G"))
        self.K1.setText(_translate("Dialog", "KONTEYNER G"))
        self.Y1.setText(_translate("Dialog", "YOLCU G"))
        self.P1.setText(_translate("Dialog", "PETROL G"))
        self.sefer_kaptan_sayisi.setText(_translate("Dialog", "KAPTAN SAYISI"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())