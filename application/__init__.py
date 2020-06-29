from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
from application import routes
from application.models import Patient_Medicine
# login = login_details()
# login = login_details(email="admintest@abc.com", password= "pbkdf2:sha256:150000$5Z8xbxQE$4375b860d474875365dc4fddf0889bbc54463d1b647429b48bcdba29308f1a6e",accesslevel =1)
# db.session.add(login)
# login1 = login_details(email="pharmatest@abc.com", password= "pbkdf2:sha256:150000$hQUIEwnK$75d7b749c9364e4de8e2036713b4caa3ad74ede106b875993fec8318e84b5cfd",accesslevel =2)
# db.session.add(login1)
# login2 =  login_details(email="diagtest@abc.com", password= "pbkdf2:sha256:150000$OQBLvnNk$0fc8a720ad70f1832f0f2bece87c7b26f0c8a5cf2d6d8a5ebb95d63b791064ef",accesslevel =3)
# db.session.add(login2)
# db.session.commit()
#admintest, pharmatest,diagtest
# pbkdf2:sha256:150000$5Z8xbxQE$4375b860d474875365dc4fddf0889bbc54463d1b647429b48bcdba29308f1a6e
# pbkdf2:sha256:150000$hQUIEwnK$75d7b749c9364e4de8e2036713b4caa3ad74ede106b875993fec8318e84b5cfd
# pbkdf2:sha256:150000$OQBLvnNk$0fc8a720ad70f1832f0f2bece87c7b26f0c8a5cf2d6d8a5ebb95d63b791064ef
# medicine = Medicine(medicine_name="Crocine", medicine_rate = 10, medicine_quantity = 100)
# db.session.add(medicine)
# medicine = Medicine(medicine_name="VicksAction-500", medicine_rate = 15, medicine_quantity = 100)
# db.session.add(medicine)
# medicine = Medicine(medicine_name="Benidryl", medicine_rate = 50, medicine_quantity = 100)
# db.session.add(medicine)
# db.session.commit()
# test = Patient_Medicine(patient_id=1,medicine_id=1,quantity_issued=5)
# db.session.add(test)
# test = Patient_Medicine(patient_id=1,medicine_id=2,quantity_issued=6)
# db.session.add(test)
# db.session.commit()
