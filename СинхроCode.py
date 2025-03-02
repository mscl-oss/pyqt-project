import webbrowser
import importlib
import flob
from sinchroxml import template, losepas, regchecking, ent, kilent
import flobtg
import sqlite3
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QInputDialog
from PyQt6 import uic, QtCore, QtGui, QtWidgets
import io
from main_ui import m
from pygame import mixer
import pygame
from result import *
from res1 import *
from rc_iconsmenu import *


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


rus = "йцукенгшщзхъ/фывапролджэё/ячсмитьбюё"

eng = 'qwertyuiop/asdfghjkl/zxcvbnm'

flag = True
flag1 = True
a = []

login = None
password = None
tgid = None
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
synchro = r'C:\Users\User\OneDrive\Рабочий стол\проект qt\synchro.db'  # !! ВАСИЛИЙ НИКОЛАЕВИЧ ЗДЕСЬ ВВЕДИТЕ


# ПУТЬ К МОЕЙ ДБ!!


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.i = None
        self.n = None
        self.q = None
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн
        self.reg.clicked.connect(self.regest)  # если кликнута кнопка регистрации, то запускаем функцию для вноса данных
        self.entr.clicked.connect(self.enter)  # если кликнута кнопка входа, то входим в аккаунт
        self.pushButton_4.clicked.connect(self.politic)
        self.forgpass.clicked.connect(self.forgpasss)

    def regest(self):  # функция создания аккаунта и вноса данных пользователя в таблицу
        global tgid, login, password, flag
        flag = True  # Reset the flag to True at the start of the method
        con = sqlite3.connect(synchro)
        cur = con.cursor()
        print()
        tgid = self.idtg.text()
        try:
            if len(self.name.text()) == 0:  # если пользователь не ввел имя и нажал кнопку
                raise ValueError('Василий Николаевич, введите имя!')
            elif len(self.idtg.text()) < 2 or self.idtg.text()[0] != '@':  # некорректный тгid
                raise ValueError('Василий Николаевич, введите правильный ТgID!')
            elif len(self.passw.text()) == 0:
                raise ValueError('Василий Николаевич, введите пароль!')
            if len(self.passw.text()) < 9:  # слишком короткий пароль
                raise LengthError("Пароль должен содержать 9 символов")

            if not any(char.isdigit() for char in self.passw.text()):  # пароль не содержит цифр
                raise DigitError("Пароль должен содержать хотя бы 1 цифру")

            for i in range(len(self.passw.text()) - 2):  # проверка на последовательности
                if self.passw.text()[i: i + 3].lower() in rus + eng:
                    raise SequenceError("Пароль не должен содержать 3 последовательных символа")
            if cur.execute("SELECT EXISTS(SELECT 1 FROM logs WHERE id = ?)",
                           (self.idtg.text(),)).fetchall()[0][0]:
                raise ValueError('Такой акк есть')
            con.close()

        except Exception as ve:  # выводим ошибку, если есть в label
            flag = False
            self.label_9.setText(str(ve))  # Отображаем сообщение об ошибке
            print(ve)
        if flag:  # если ошибок нет
            with open('flob.py', 'w') as file:
                file.write(f"tgidinentent = '{self.idtg.text()}'\n")
            importlib.reload(flob)
            login = self.name.text()
            tgid = self.idtg.text()
            password = self.passw.text()
            self.close()
            self.i = Regchek()  # Открываем новое окно
            self.i.show()

    def enter(self):  # запускает окно входа в акк
        # if #проверяем есть ли такой id в бд
        self.close()
        self.q = EnterEnt()
        self.q.show()

    @staticmethod
    def politic():
        webbrowser.open("https://i.pinimg.com/736x/48/4f/66/484f6645bdadf5eeb91031ca1a01ac7e.jpg")

    def forgpasss(self):  # запускает окно сброса пароля
        self.close()
        self.w = Forgetpass()
        self.w.show()


class Forgetpass(QMainWindow):  # окно для сброса пароля аккаунта
    def __init__(self):
        super().__init__()
        self.y = None
        self.my = None
        self.k = io.StringIO(losepas)
        uic.loadUi(self.k, self)  # Загружаем дизайн
        # кликнута кнопка - вызываем функцию
        # в функции переписываем тгid

        self.pushButton_3.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.checktg)
        self.pushButton_2.clicked.connect(self.checkcode)

    def checktg(self):  # проверка id и пароля
        con = sqlite3.connect(synchro)
        cur = con.cursor()
        global flag1
        flag1 = True  # Reset the flag to True at the start of the method
        try:
            if self.lineEdit_3.text() != self.lineEdit_4.text():
                raise ValueError('Пароли не совпадают')

            elif len(self.lineEdit_3.text()) == 0:
                raise ValueError('введите пароль!')
            elif len(self.lineEdit_3.text()) < 9:  # слишком короткий пароль
                raise LengthError("Пароль должен содержать 9 символов")

            elif not any(char.isdigit() for char in self.lineEdit_3.text()):  # пароль не содержит цифр
                raise DigitError("Пароль должен содержать хотя бы 1 цифру")

            for i in range(len(self.lineEdit_3.text()) - 2):  # проверка на последовательности
                if self.lineEdit_3.text()[i: i + 3].lower() in rus + eng:
                    raise SequenceError("Пароль не должен содержать 3 последовательных символа")
            if len(self.lineEdit.text()) < 2 or self.lineEdit.text()[0] != '@':
                # если пользователь ввел некорректный тгid и нажал кнопку.
                raise ValueError('введите верный'
                                 ' TgID')
            if not cur.execute("SELECT EXISTS(SELECT 1 FROM logs WHERE id = ?)",
                               (self.lineEdit.text(),)).fetchall()[0][0]:
                raise ValueError('Такого аккаунта нет')
            con.close()

        except Exception as ve:  # выводим ошибку, если есть в label
            flag1 = False
            self.label_4.setText(str(ve))  # Отображаем сообщение об ошибке
        if flag1:
            with open('flob.py', 'w') as file:
                file.write(f"tgidinentent = '{self.lineEdit.text()}'\n")
                self.label_4.setText(' ')
            importlib.reload(flobtg)

    def checkcode(self):  # проверка кода
        global tgid, login, password
        print(self.lineEdit_2.text())
        importlib.reload(flobtg)
        if self.lineEdit_2.text() != flobtg.tgidcode:
            self.label.setText('Неверный код!')
        else:
            self.db()

    def db(self):  # запись в дб
        with sqlite3.connect(synchro) as db:
            cursor = db.cursor()
            query = f"""UPDATE logs SET pass = ('{self.lineEdit_3.text()}') WHERE id = ('{self.lineEdit.text()}')"""
            cursor.execute(query)
        self.close()
        self.y = MainWindow()
        self.y.show()

    def back(self):
        global tgid, login, password
        tgid, login, password = None, None, None
        self.close()
        self.my = MyWidget()
        self.my.show()


class Regchek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.y = None
        self.my = None
        self.o = io.StringIO(regchecking)
        uic.loadUi(self.o, self)  # Загружаем дизайн
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.check)

    def check(self):  # проверка кода
        print(self.lineEdit.text())
        print(flobtg.tgidcode)
        print(len(self.lineEdit.text()))
        importlib.reload(flobtg)
        if len(self.lineEdit.text()) == 0 or self.lineEdit.text() != flobtg.tgidcode:
            self.label_5.setText('Неверный код!')
        else:
            self.db()

    def db(self):  # запись в дб
        print(2)
        print(tgid, login, password)
        con = sqlite3.connect(synchro)
        cur = con.cursor()
        cur.execute(f'INSERT into logs (id, name, pass) VALUES ("{tgid}", "{login}", "{password}")')
        con.commit()
        con.close()
        self.close()
        self.y = MainWindow()
        self.y.show()

    def back(self):
        global tgid, login, password
        tgid, login, password = None, None, None
        self.close()
        self.my = MyWidget()
        self.my.show()


class EnterReg(QMainWindow):  # проверка кода при входе в акк
    def __init__(self):
        super().__init__()
        self.y = None
        self.h = io.StringIO(ent)
        self.my = None
        uic.loadUi(self.h, self)  # Загружаем дизайн
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.check)

    def check(self):
        importlib.reload(flobtg)
        if self.lineEdit.text() != flobtg.tgidcode:
            self.label_5.setText('Неверный код!')
        else:
            self.close()
            self.y = MainWindow()
            self.y.show()

    def back(self):
        global tgid, login, password
        tgid, login, password = None, None, None
        self.close()
        self.my = EnterEnt()
        self.my.show()


class EnterEnt(QMainWindow):  # вход в аккаунт и проверки существование аккаунта
    def __init__(self):
        self.ip = None
        self.my = None
        super().__init__()
        self.q = io.StringIO(kilent)
        uic.loadUi(self.q, self)  # Загружаем дизайн
        self.pushButton_2.clicked.connect(self.checktg)
        self.pushButton_3.clicked.connect(self.back)

    def back(self):  # кнопка назад
        global tgid, login, password
        tgid, login, password = None, None, None
        self.close()
        self.my = MyWidget()
        self.my.show()

    def checktg(self):  # проверка правильности тг
        global tgid
        con = sqlite3.connect(synchro)
        cur = con.cursor()
        try:

            if len(self.lineEdit_2.text()) < 2 or self.lineEdit_2.text()[0] != '@':
                # если пользователь ввел некорректный тгid и нажал кнопку.
                raise ValueError('Василий Николаевич, введите верный'
                                 ' TgID')
            if not cur.execute("SELECT EXISTS(SELECT 1 FROM logs WHERE id = ?)",
                               (self.lineEdit_2.text(),)).fetchall()[0][0]:
                raise ValueError('Такого аккаунта нет')

            else:
                with open('flob.py', 'w') as file:
                    file.write(f"tgidinentent = '{self.lineEdit_2.text()}'\n")
                importlib.reload(flobtg)
                tgid = self.lineEdit_2.text()
                self.close()
                self.ip = EnterReg()
                self.ip.show()
            con.close()
        except ValueError as j:
            self.label_3.setText(str(j))


# главное приложение
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        f = io.StringIO(m)
        uic.loadUi(f, self)  # Load UI and set it to 'self' rather than self.ui

        # Hide the icon_only_widget
        self.is_playing = False
        self.play_sound_btn_6.clicked.connect(self.play_sound)
        self.prev_sound_btn_4.clicked.connect(self.prev_sound)
        self.next_sound_btn_4.clicked.connect(self.next_sound)
        self.add_sound_btn_4.clicked.connect(self.add_sound)
        self.remove_sound_btn_4.clicked.connect(self.remove_sound)
        self.play_sound_btn_5.clicked.connect(self.stop)
        self.listWidget_3.doubleClicked.connect(self.play_sound)

        self.volume_slider_4.setMinimum(0)
        self.volume_slider_4.setMaximum(100)
        self.volume_slider_4.setValue(50)
        self.volume_slider_4.valueChanged.connect(self.volume_reg)

        self.dir = ""
        self.sound_mixer = mixer
        self.sound_mixer.init()

        self.icon_only_widget.hide()
        self.pushButton.clicked.connect(self.new)
        self.pushButton_3.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.saveas)
        self.pushButton_4.clicked.connect(self.delete)

        self.pushButton_5.clicked.connect(self.rename)
        # Set the current index of the stackedWidget
        self.stackedWidget.setCurrentIndex(0)

    def saveas(self):  # сохранить данные файла
        if self.listWidget.currentItem():
            item = self.listWidget.currentItem()
            val = item.text()
            with open(val, "w", encoding='utf-8') as file:
                file.write(self.plainTextEdit.toPlainText())
            self.plainTextEdit.clear()

        else:
            QMessageBox.information(self, 'ошибка', f'файл не выбран')

    def open(self):  # открыть файл
        if self.listWidget.currentItem():

            item = self.listWidget.currentItem()
            val = item.text()

            with open(val, 'r', encoding='utf-8') as file:
                self.plainTextEdit.setPlainText(file.read())
        else:
            QMessageBox.information(self, 'ошибка', f'файл не выбран')

    def new(self):  # создать новый файл
        if len(self.plainTextEdit.toPlainText()) != 0:
            d, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter file name')

            if d[-4::] != '.txt':
                self.dir = d + '.txt'
            else:
                self.dir = d
            with open(self.dir, "w", encoding='utf-8') as file:
                file.write(self.plainTextEdit.toPlainText())
            self.listWidget.addItem(self.dir)
            QMessageBox.information(self, 'Успех', f'Файл успешно сохранён: {self.dir}')
            self.plainTextEdit.clear()
        else:
            QMessageBox.information(self, 'ошибка', f'файл пустой')

    def rename(self):  # переименовать файл
        if self.listWidget.currentItem():
            item = self.listWidget.currentItem()
            val = item.text()
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
            d, ok = QInputDialog.getText(self, 'Input Dialog', 'переименовать файл')
            if d[-4::] != '.txt':
                j = d + '.txt'
            else:
                j = d
            os.rename(val, j)
            self.listWidget.addItem(j)
            self.plainTextEdit.clear()

        else:
            QMessageBox.information(self, 'ошибка', f'файл не выбран')

    def delete(self):  # удалить звук

        if self.listWidget.currentItem():
            item = self.listWidget.currentItem()
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
        else:
            QMessageBox.information(self, 'ошибка', f'файл не выбран')

    def play_sound(self):  # воспроизвести звук
        print(1)
        if self.listWidget_3.currentItem():
            print(2)
            item = self.listWidget_3.currentItem()

            if item:
                filename = os.path.join(self.dir, item.text())
                self.sound_mixer.music.load(filename)
            else:
                self.listWidget_3.currentRow(0)
            self.sound_mixer.music.play()
            self.is_playing = True

    def remove_sound(self):  # удалить звук
        pygame.mixer.music.stop()

        if self.listWidget_3.currentItem():
            item = self.listWidget_3.currentItem()
            row = self.listWidget_3.row(item)
            self.listWidget_3.takeItem(row)

    def prev_sound(self):  # воспроизвести прошл.звук
        try:
            row = self.listWidget_3.currentRow()
            self.listWidget_3.setCurrentRow(row - 1)
            self.play_sound()
            self.is_playing = True
        except TypeError:
            pass

    def next_sound(self):  # воспроизвести след.звук
        try:
            row = self.listWidget_3.currentRow()
            self.listWidget_3.setCurrentRow(row + 1)
            self.play_sound()
            self.is_playing = True
        except TypeError:
            pass

    def add_sound(self):  # добавление музыки: присутствует wav файл, по причине того,что при произведении длинного mp3
        # прога крашилась

        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select wav File", "",
                                                             "Wav file (*.wav)")
        if file_name:  # Проверяем, был ли выбран файл
            if file_name.endswith(""):
                self.listWidget_3.addItem(file_name)  # Добавляем полный путь файла в listWidget
                self.dir = os.path.dirname(file_name)

    def volume_reg(self):  # регулировка громкости
        self.sound_mixer.music.set_volume(self.volume_slider_4.value() / 100)

    def stop(self):  # остановка музыки
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    #    функции для переключения окон в приложении
    def on_home_btn_1_toggled(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_home_btn_2_toggled(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_dashborad_btn_1_toggled(self):
        self.stackedWidget.setCurrentIndex(1)

    def on_dashborad_btn_2_toggled(self):
        self.stackedWidget.setCurrentIndex(1)

    def on_orders_btn_1_toggled(self):
        self.stackedWidget.setCurrentIndex(2)

    def on_orders_btn_2_toggled(self):
        self.stackedWidget.setCurrentIndex(2)

    def on_products_btn_1_toggled(self):
        self.stackedWidget.setCurrentIndex(3)

    def on_products_btn_2_toggled(self):
        self.stackedWidget.setCurrentIndex(3)

    def on_customers_btn_1_toggled(self):
        self.stackedWidget.setCurrentIndex(4)

    def on_customers_btn_2_toggled(self):
        self.stackedWidget.setCurrentIndex(4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("style.qss", "r") as style_file:  # загрузка стиля приложения
        style_str = style_file.read()
        app.setStyleSheet(style_str)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
