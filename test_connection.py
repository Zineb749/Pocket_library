from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:TonNouveauMotDePasse@localhost:3306/pocket_library")
connection = engine.connect()
print("Connexion OK")
connection.close()
