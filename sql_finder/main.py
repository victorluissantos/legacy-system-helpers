import os
import sys
import re

def normalize_sql(sql):
    # Deixa tudo minúsculo e remove espaços, tabs e quebras de linha
    sql = sql.lower()
    sql = re.sub(r'\s+', '', sql)
    return sql

def read_and_normalize_sql(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return normalize_sql(content)

def find_php_files(directory):
    php_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.php'):
                php_files.append(os.path.join(root, file))
    return php_files

def file_contains_query(filepath, normalized_query, debug=False):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            normalized_content = normalize_sql(content)
            if debug:
                print(f"\n[DEBUG] Arquivo: {filepath}")
                print(f"[DEBUG] Primeiros 200 chars normalizados do arquivo:\n{normalized_content[:200]}")
            return normalized_query in normalized_content
    except Exception as e:
        if debug:
            print(f"[ERRO] Falha ao ler {filepath}: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 main.py <diretorio> <arquivo_query.sql> [--debug]")
        sys.exit(1)

    directory = sys.argv[1]
    query_file = sys.argv[2]
    debug = "--debug" in sys.argv

    print("\n🔍 Buscando por trechos SQL normalizados...\n")
    print(f"📁 Diretório: {directory}")

    normalized_query = read_and_normalize_sql(query_file)
    print(f"🔎 Trecho da query normalizada (80 chars): {normalized_query[:80]}...\n")

    php_files = find_php_files(directory)
    total = len(php_files)
    encontrados = []

    for i, filepath in enumerate(php_files):
        if file_contains_query(filepath, normalized_query, debug=debug):
            encontrados.append(filepath)
        elif not debug:
            print(f"⏩ analisado: {filepath}")

    print(f"\n🧾 Total de arquivos .php analisados: {total}")
    print("📄 Arquivos que contêm a query (normalizada):")

    if encontrados:
        for path in encontrados:
            print(f"✅ {path}")
    else:
        print("⚠️ Nenhum arquivo encontrado com a query informada.")

if __name__ == "__main__":
    main()
