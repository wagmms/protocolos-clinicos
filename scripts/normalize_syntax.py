import glob, re

files = sorted(glob.glob('/home/wagmoraes/Projetos IA/Protocolos_Clinicos/**/*.md', recursive=True))

changed_files = 0
total_replacements = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        original = fh.read()
    
    # 1. Substituir [ ... ] por [ ]
    modified = re.sub(r'\[\s*\.\.\.\s*\]', '[ ]', original)
    # 2. Ajustar caso apareça algo como [ medidas/medicações prévias: ... ] para [medidas/medicações prévias: ]
    modified = re.sub(r'\[\s*([^\]]+?)\s*:\s*\.\.\.\s*\]', r'[\1: ]', modified)
    
    # 3. No bloco de snippet, trocar ```markdown por ```text
    modified = re.sub(r'(##\s*📋\s*Snippet[^\n]*\n+```)markdown', r'\1text', modified)

    if modified != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(modified)
        changed_files += 1

print(f'Arquivos modificados com sucesso: {changed_files}')
