import os
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "shared", "database", "contacts.xlsx")
SHEET = "my_contacts"
COLUMNS = [
    "name",        # Nome do contato
    "company",     # Empresa
    "position",    # Cargo/posição
    "profile_url", # URL única do perfil (chave)
    "invited_at",  # Data do convite
    "updated_at",  # Última vez que mexeu nesse contato
]

def _now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def _ensure_file():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(DB_PATH, index=False, sheet_name=SHEET, engine="openpyxl")

def load_db() -> pd.DataFrame:
    _ensure_file()
    try:
        df = pd.read_excel(DB_PATH, sheet_name=SHEET, engine="openpyxl", dtype=str)
    except Exception:
        df = pd.DataFrame(columns=COLUMNS)
        save_db(df)
    return df

def save_db(df: pd.DataFrame):
    with pd.ExcelWriter(DB_PATH, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET)

def upsert_contact(contact: dict):
    """
    Insere ou atualiza um contato baseado no profile_url.
    contact = {"profile_url": "...", "name": "...", "company": "...", "position": "..."}
    """
    if not contact.get("profile_url"):
        raise ValueError("profile_url é obrigatório")

    df = load_db()

    # procura pelo profile_url
    mask = df["profile_url"] == contact["profile_url"]
    if mask.any():
        # atualiza contato existente
        for key in ["name", "company", "position", "invited_at"]:
            if key in contact:
                df.loc[mask, key] = contact[key]
        df.loc[mask, "updated_at"] = _now()
    else:
        # insere novo
        row = {c: "" for c in COLUMNS}
        row.update(contact)
        row["updated_at"] = _now()
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    save_db(df)

def mark_invited(profile_url: str, invited_date: str = None):
    """Marca o contato como convidado."""
    df = load_db()
    mask = df["profile_url"] == profile_url
    if not mask.any():
        return False
    df.loc[mask, "invited_at"] = invited_date or datetime.utcnow().strftime("%Y-%m-%d")
    df.loc[mask, "updated_at"] = _now()
    save_db(df)
    return True

