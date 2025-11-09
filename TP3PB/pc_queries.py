# rode ante: pip install -r requirements.txt
# para restaurar banco rode no terminal: pg_restore -U postgres -d postgres -1 dump-postgres-202511090059

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Result
import os


DB_URL = "postgresql+psycopg2://postgres:2104@localhost:5432/postgres"


engine = create_engine(DB_URL, future=True)

# As 3 consultas (strings)
INNER_SQL = """
SELECT c.id AS component_id, c.name AS component_name,
       ct.name AS type_name, v.name AS vendor_name, c.price, c.stock
FROM pc_builder.components c
INNER JOIN pc_builder.component_types ct ON c.type_id = ct.id
INNER JOIN pc_builder.vendors v ON c.vendor_id = v.id;
"""

LEFT_SQL = """
SELECT b.id AS build_id, b.name AS build_name, u.name AS user_name,
       bc.component_id, bc.quantity
FROM pc_builder.builds b
LEFT JOIN pc_builder.users u ON b.user_id = u.id
LEFT JOIN pc_builder.build_components bc ON b.id = bc.build_id
ORDER BY b.id;
"""

RIGHT_SQL = """
SELECT v.name AS vendor_name, c.id AS component_id, c.name AS component_name, c.price, c.stock
FROM pc_builder.vendors v
RIGHT JOIN pc_builder.components c ON v.id = c.vendor_id
ORDER BY c.id;
"""

def fetch_all(engine, sql):
    with engine.connect() as conn:
        result: Result = conn.execute(text(sql))
        rows = result.mappings().all()  
    return rows

def populate_dicts(rows):
    """
    Retorna um dict onde chave é um índice (0,1,2...) e valor é um dict representando a linha.
    """
    out = {}
    for idx, row in enumerate(rows):
        out[idx] = dict(row)
    return out

def populate_lists(rows):
    """
    Retorna uma lista de listas, com colunas na ordem do mapping keys.
    """
    out = []
    if not rows:
        return out
    keys = list(rows[0].keys())
    out.append(keys) 
    for row in rows:
        out.append([row[k] for k in keys])
    return out

def print_dicts(dict_object, title=None):
    if title:
        print(f"\n=== {title} (dicionários) ===")
    for k, v in dict_object.items():
        print(f"[{k}] -> {v}")

def print_lists(list_object, title=None):
    if title:
        print(f"\n=== {title} (listas) ===")
    for row in list_object:
        print(row)

def main():
    # Executa e coleta resultados
    inner_rows = fetch_all(engine, INNER_SQL)
    left_rows = fetch_all(engine, LEFT_SQL)
    right_rows = fetch_all(engine, RIGHT_SQL)

    # 5 — populando dicionários (uma estrutura por consulta)
    inner_dicts = populate_dicts(inner_rows)
    left_dicts = populate_dicts(left_rows)
    right_dicts = populate_dicts(right_rows)

    # 6 — loop imprimindo dicionários
    print_dicts(inner_dicts, title="INNER JOIN (componentes com tipo e vendor)")
    print_dicts(left_dicts, title="LEFT JOIN (builds com usuário e componentes)")
    print_dicts(right_dicts, title="RIGHT JOIN (componentes com vendor possível NULL)")

    # 7 — refazer, populando listas
    inner_lists = populate_lists(inner_rows)
    left_lists = populate_lists(left_rows)
    right_lists = populate_lists(right_rows)

    # 8 — loop imprimindo listas
    print_lists(inner_lists, title="INNER JOIN (listas)")
    print_lists(left_lists, title="LEFT JOIN (listas)")
    print_lists(right_lists, title="RIGHT JOIN (listas)")

if __name__ == "__main__":
    main()
