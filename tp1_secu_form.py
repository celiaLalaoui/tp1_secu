import hashlib
import sys
import re
import bcrypt
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulaire de connexion")
        self.resize(500, 500)

        logo_label = QLabel(self)
        pixmap = QPixmap("logo.png").scaledToWidth(75)
        logo_label.setPixmap(pixmap)
        logo_label.setGeometry(60, 80, 75, 75)  

        self.title_label = QLabel(self)
        self.title_label.setText('Formulaire de connexion')
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.title_label.setGeometry(200, 100, 200, 30)  

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setGeometry(125, 200, 250, 30)  

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(125, 250, 250, 30)  

        self.button_login = QPushButton("Se connecter", self)
        self.button_login.setGeometry(150, 300, 100, 30)  
        self.button_login.clicked.connect(self.login)

        self.button_register = QPushButton("S'inscrire", self)
        self.button_register.setGeometry(200, 350, 100, 30)  
        self.button_register.clicked.connect(self.show_register_dialog)

        self.button_reset = QPushButton("Reset", self)
        self.button_reset.setGeometry(260, 300, 100, 30)  
        self.button_reset.clicked.connect(self.reset_form)

        self.load_users_data()

       

    def load_users_data(self):
        try:
            self.db = pd.read_excel('users.xlsx')
        except FileNotFoundError:
            self.db = pd.DataFrame(columns=['email', 'password'])

    def save_users_data(self):
        self.db.to_excel('users.xlsx', index=False)

    def login(self):
        email = self.email_input.text()
        pwd = self.password_input.text()

        if not email or not pwd:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir l'adresse email et le mot de passe.")
            return

        password = self.hash_password(pwd)
        
      

        user = self.db[self.db['email'].str.strip() == email.strip()]
        if not user.empty:
            recup_password = user.iloc[0]['password']
           
            if password == recup_password :
                QMessageBox.information(self, "Connexion réussie", "Bienvenue!")
               
            else:
                QMessageBox.warning(self, "Erreur", "Adresse email ou mot de passe incorrect.")
              
        else:
            QMessageBox.warning(self, "Erreur", "Adresse email ou mot de passe incorrect.")
            

    def reset_form(self):
        self.email_input.setText("")
        self.password_input.setText("")

    def show_register_dialog(self):
        dialog = RegisterDialog(self)
        dialog.exec_()

    def hash_password(self, password):
        password_utf8 = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_utf8).hexdigest()
        return hashed_password

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inscription")
        self.resize(500, 500)

        layout = QVBoxLayout()

        logo = QLabel(self)
        pixmap = QPixmap("logo.png").scaledToWidth(75)
        logo.setPixmap(pixmap)
        logo.setGeometry(60, 80, 75, 75)  

        self.titre_label = QLabel(self)
        self.titre_label.setText("Formulaire d'inscription")
        self.titre_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.titre_label.setGeometry(200, 100, 200, 30)  

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setGeometry(150,200,250,30)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(150,250,250,30)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirmer mot de passe")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setGeometry(150,300,250,30)

        self.button_register = QPushButton("S'inscrire", self)
        self.button_register.clicked.connect(self.register)
        self.button_register.setGeometry(150,350,250,30)

      

        self.setLayout(layout)

    def register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        parent = self.parent()

        if email in parent.db['email'].values:
            QMessageBox.warning(self, "Erreur", "Cette adresse email existe déjà.")
            return

        if password == confirm_password:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                QMessageBox.warning(self, "Erreur", "Veuillez saisir une adresse e-mail valide.")
                return

            if len(password) < 12:
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins 12 caractères.")
                return
            if not re.search(r"\d", password):
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins un chiffre.")
                return
            if not re.search(r"[A-Z]", password):
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins une majuscule.")
                return
            if not re.search(r"[@$!%*?&]", password):
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins un caractère spécial.")
                return

            hashed_password = parent.hash_password(password)

            parent.db = parent.db._append({'email': email, 'password': hashed_password}, ignore_index=True)
            parent.save_users_data()  
            QMessageBox.information(self, "Inscription réussie", "Utilisateur enregistré avec succès.")
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
