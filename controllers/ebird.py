import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Avistamento, Especie
from utils import db
from flask_login import login_required, current_user

BASE = "https://api.ebird.org/v2"
_cache = {"especies": None}


def carregar_especies_brasil(api_key):
    if _cache["especies"] is not None:
        return _cache["especies"]

    headers = {"X-eBirdApiToken": api_key}

    r = requests.get(f"{BASE}/product/spplist/BR", headers=headers, timeout=30)
    r.raise_for_status()
    codigos_br = set(r.json())

    r = requests.get(
        f"{BASE}/ref/taxonomy/ebird",
        headers=headers,
        params={"fmt": "json", "cat": "species", "locale": "pt_BR"},
        timeout=60,
    )
    r.raise_for_status()

    especies = [
        {
            "codigo": t["speciesCode"],
            "nome": t["comName"],
            "cientifico": t["sciName"],
        }
        for t in r.json()
        if t["speciesCode"] in codigos_br
    ]
    especies.sort(key=lambda e: e["nome"])

    _cache["especies"] = especies
    return especies