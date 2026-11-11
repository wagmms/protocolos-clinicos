import os, glob

BASE = '/home/wagmoraes/Projetos IA/Protocolos_Clinicos'
EXPORT_DIR = os.path.join(BASE, 'export_txt')
os.makedirs(EXPORT_DIR, exist_ok=True)

modules = [
    ('01_Ginecologia_Obstetricia', '01_Ginecologia_Obstetricia_27_Protocolos.txt', 'GINECOLOGIA E OBSTETRÍCIA'),
    ('02_Pronto_Atendimento_UPA', '02_Pronto_Atendimento_UPA_42_Protocolos.txt', 'PRONTO ATENDIMENTO / UPA ADULTO'),
    ('03_Enfermaria_Internacao', '03_Enfermaria_Internacao_10_Protocolos.txt', 'ENFERMARIA E INTERNAÇÃO HOSPITALAR'),
    ('04_Pediatria_Puericultura', '04_Pediatria_Puericultura_11_Protocolos.txt', 'PEDIATRIA E PUERICULTURA')
]

all_lines = [
    "================================================================================",
    "ACERVO COMPLETO DE PROTOCOLOS CLÍNICOS E MODELOS DE PRONTUÁRIO ELETRÔNICO (PEP)",
    "Total: 90 Protocolos Médicos Estruturados • 100% Atualizados",
    "================================================================================\n\n"
]

for folder, out_name, mod_title in modules:
    mod_path = os.path.join(BASE, folder)
    files = sorted(glob.glob(f"{mod_path}/**/*.md", recursive=True))
    
    mod_lines = [
        "================================================================================",
        f"MÓDULO: {mod_title} ({len(files)} PROTOCOLOS)",
        "================================================================================\n\n"
    ]
    
    for idx, f in enumerate(files, 1):
        with open(f, 'r', encoding='utf-8') as fh:
            text = fh.read()
        
        rel = os.path.relpath(f, BASE)
        banner = (
            f"\n\n{'#'*80}\n"
            f"# PROTOCOLO {idx:02d}/{len(files):02d} - {rel}\n"
            f"{'#'*80}\n\n"
        )
        mod_lines.append(banner + text + "\n")
        all_lines.append(banner + text + "\n")
        
    out_file = os.path.join(EXPORT_DIR, out_name)
    with open(out_file, 'w', encoding='utf-8') as fh:
        fh.write(''.join(mod_lines))
    print(f"Salvo: {out_file} ({len(files)} protocolos)")

master_out = os.path.join(EXPORT_DIR, '00_Todos_os_90_Protocolos_Completo.txt')
with open(master_out, 'w', encoding='utf-8') as fh:
    fh.write(''.join(all_lines))
print(f"Salvo arquivo mestre: {master_out}")
