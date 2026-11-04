from dotenv import load_dotenv
load_dotenv()

import os
from app import app
from models import Especie
from utils import db
from controllers.ebird import carregar_especies_brasil

with app.app_context():
    lista = carregar_especies_brasil(os.getenv("EBIRD_API_KEY"))

    existentes = {e.nome_cientifico for e in Especie.query.all()}

    novas = 0
    for e in lista:
        if e["cientifico"] in existentes:
            continue
        db.session.add(
            Especie(
                nome_comum=e["nome"],
                nome_cientifico=e["cientifico"],
                fk_id_status_conservacao=None,
            )
        )
        novas += 1

    db.session.commit()
    print(f"{novas} espécies adicionadas.")