
from shared.database.database_manager import upsert_contact, mark_invited, load_db

# inserir/atualizar
upsert_contact({
    "profile_url": "https://linkedin.com/in/johndoe",
    "name": "John Doe",
    "company": "Tech Corp",
    "position": "Recruiter"
})

# marcar como convidado
mark_invited("https://linkedin.com/in/johndoe")

# carregar tudo
df = load_db()
print(df)