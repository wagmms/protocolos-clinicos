import os, glob, re, json, html

BASE_PROJECT = '/home/wagmoraes/Projetos IA/Protocolos_Clinicos'
SNIPPETS_DIR = os.path.join(BASE_PROJECT, 'snippets')
os.makedirs(SNIPPETS_DIR, exist_ok=True)

modules = [
    {
        'id': 'go',
        'name': 'Ginecologia & Obstetrícia',
        'badge': '🌸 GO',
        'dir': os.path.join(BASE_PROJECT, '01_Ginecologia_Obstetricia')
    },
    {
        'id': 'upa',
        'name': 'Pronto Atendimento / UPA',
        'badge': '🚑 UPA Adulto',
        'dir': os.path.join(BASE_PROJECT, '02_Pronto_Atendimento_UPA')
    },
    {
        'id': 'enf',
        'name': 'Enfermaria & Internação',
        'badge': '🏥 Enfermaria',
        'dir': os.path.join(BASE_PROJECT, '03_Enfermaria_Internacao')
    },
    {
        'id': 'ped',
        'name': 'Pediatria & Puericultura',
        'badge': '👶 Pediatria',
        'dir': os.path.join(BASE_PROJECT, '04_Pediatria_Puericultura')
    }
]

all_snippets = []

for mod in modules:
    mod_files = sorted(glob.glob(f"{mod['dir']}/**/*.md", recursive=True))
    print(f"Processando {mod['name']}: {len(mod_files)} arquivos.")
    
    for f in mod_files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
            
        # Título
        title_match = re.search(r'^#\s+(.+)$', content, re.M)
        title = title_match.group(1).replace('Protocolo de Atendimento:', '').replace('Protocolo:', '').strip() if title_match else os.path.basename(f)
        
        # Atalho
        trigger_match = re.search(r'\*\*Atalho (?:Recomendado|sugerido):\*\*\s*`([^`]+)`', content, re.IGNORECASE)
        if trigger_match:
            trigger = trigger_match.group(1).strip()
        else:
            trigger = ';' + os.path.splitext(os.path.basename(f))[0].lower().replace('_', '-')
            
        # Snippet PEP
        snippet_pep = ""
        pep_match = re.search(r'##\s+📋\s*Snippet[^\n]*\n+```(?:markdown|text)?\n(.*?)\n```', content, re.DOTALL)
        if pep_match:
            snippet_pep = pep_match.group(1).strip()
        else:
            first_block = re.search(r'```(?:markdown|text)?\n(.*?)\n```', content, re.DOTALL)
            if first_block:
                snippet_pep = first_block.group(1).strip()
            else:
                snippet_pep = content.strip()
                
        # Receita Médica
        receita_match = re.search(r'##\s+💊\s*Receita[^\n]*\n+```(?:markdown|text)?\n(.*?)\n```', content, re.DOTALL)
        receita_text = receita_match.group(1).strip() if receita_match else ""
        
        # Guia de Conduta / Bolso
        guia_match = re.search(r'##\s+🎯\s*Guia de Bolso[^\n]*(.*)', content, re.DOTALL)
        guia_text = guia_match.group(1).strip() if guia_match else ""
        
        rel_path = os.path.relpath(f, BASE_PROJECT)
        subcat = os.path.basename(os.path.dirname(f)).replace('_', ' ')
        subcat_clean = re.sub(r'^\d+\s*', '', subcat)
        
        item = {
            'id': f"{mod['id']}-{len(all_snippets)+1}",
            'mod_id': mod['id'],
            'module_name': mod['name'],
            'badge': mod['badge'],
            'title': title,
            'trigger': trigger,
            'category': subcat_clean,
            'path': rel_path,
            'pep_body': snippet_pep,
            'has_receita': bool(receita_text),
            'receita_body': receita_text,
            'has_guia': bool(guia_text),
            'guia_body': guia_text
        }
        all_snippets.append(item)

print(f"\nTotal de snippets compilados: {len(all_snippets)}")

# 1. Salvar JSONs
for mod in modules:
    mod_snippets = [s for s in all_snippets if s['mod_id'] == mod['id']]
    json_path = os.path.join(SNIPPETS_DIR, f"snippets_{mod['id']}.json")
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump(mod_snippets, fh, indent=2, ensure_ascii=False)

all_json_path = os.path.join(SNIPPETS_DIR, "snippets_todos.json")
with open(all_json_path, 'w', encoding='utf-8') as fh:
    json.dump(all_snippets, fh, indent=2, ensure_ascii=False)

# 2. Salvar YAMLs do Espanso
for mod in modules:
    mod_snippets = [s for s in all_snippets if s['mod_id'] == mod['id']]
    yaml_path = os.path.join(SNIPPETS_DIR, f"{mod['id']}_espanso.yml")
    with open(yaml_path, 'w', encoding='utf-8') as fh:
        fh.write(f"# Configuração Espanso: {mod['name'].upper()}\n\nmatches:\n")
        for s in mod_snippets:
            fh.write(f"  - trigger: \"{s['trigger']}\"\n")
            fh.write(f"    replace: |\n")
            for line in s['pep_body'].splitlines():
                fh.write(f"      {line}\n")
            fh.write("\n")
            if s['receita_body']:
                fh.write(f"  - trigger: \"{s['trigger']}-rec\"\n")
                fh.write(f"    replace: |\n")
                for line in s['receita_body'].splitlines():
                    fh.write(f"      {line}\n")
                fh.write("\n")

all_yaml_path = os.path.join(SNIPPETS_DIR, "espanso_completo.yml")
with open(all_yaml_path, 'w', encoding='utf-8') as fh:
    fh.write(f"# Configuração Completa Espanso ({len(all_snippets)} Modelos)\n\nmatches:\n")
    for s in all_snippets:
        fh.write(f"  - trigger: \"{s['trigger']}\"\n")
        fh.write(f"    replace: |\n")
        for line in s['pep_body'].splitlines():
            fh.write(f"      {line}\n")
        fh.write("\n")
        if s['receita_body']:
            fh.write(f"  - trigger: \"{s['trigger']}-rec\"\n")
            fh.write(f"    replace: |\n")
            for line in s['receita_body'].splitlines():
                fh.write(f"      {line}\n")
            fh.write("\n")

# 3. Cockpit Web UI/UX High-End Anti-Slop
html_path = os.path.join(BASE_PROJECT, 'painel_rapido_snippets.html')

cards_html = []
for idx, s in enumerate(all_snippets):
    has_rec_btn = ""
    if s['has_receita']:
        has_rec_btn = f"""
        <button class="btn btn-ghost" onclick='event.stopPropagation(); copyReceita({idx})' title="Copiar apenas a receita estruturada">
          💊 Receita
        </button>
        """
        
    has_guia_badge = '<span class="pill pill-guia" title="Contém guia de bolso e conduta">🎯 Conduta</span>' if s['has_guia'] else ''
    
    search_keywords = f"{s['title'].lower()} {s['trigger'].lower()} {s['category'].lower()} {s['module_name'].lower()} {s['path'].lower()}"
    preview_text = html.escape(s['pep_body'][:220]) + ("..." if len(s['pep_body']) > 220 else "")
    
    cards_html.append(f"""
    <article class="card card-{s['mod_id']}" data-mod="{s['mod_id']}" data-cat="{s['category']}" data-search="{html.escape(search_keywords)}" onclick="openInspector({idx})">
      <div class="card-top">
        <div class="tags-cluster">
          <span class="mod-pill mod-pill-{s['mod_id']}">{s['badge']}</span>
          <span class="cat-pill">{s['category']}</span>
          {has_guia_badge}
        </div>
        <button class="trigger-chip" onclick='event.stopPropagation(); copyTrigger("{s['trigger']}")' title="Clique para copiar o atalho">
          <code>{s['trigger']}</code>
          <svg class="copy-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        </button>
      </div>

      <div class="card-body-block">
        <h3 class="card-title">{html.escape(s['title'])}</h3>
        <p class="card-sub">{s['path']}</p>
        <div class="card-preview">
          <pre><code>{preview_text}</code></pre>
        </div>
      </div>

      <div class="card-footer">
        <div class="btn-group">
          <button class="btn btn-primary" onclick='event.stopPropagation(); copySnippet({idx})'>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copiar PEP
          </button>
          {has_rec_btn}
        </div>
        <button class="btn btn-detail" onclick="event.stopPropagation(); openInspector({idx})" title="Visualizar protocolo e conduta completa">
          Abrir ↗
        </button>
      </div>
    </article>
    """)

cards_joined = '\n'.join(cards_html)
snippets_json_payload = json.dumps(all_snippets, ensure_ascii=False)

count_go = len([s for s in all_snippets if s['mod_id'] == 'go'])
count_upa = len([s for s in all_snippets if s['mod_id'] == 'upa'])
count_enf = len([s for s in all_snippets if s['mod_id'] == 'enf'])
count_ped = len([s for s in all_snippets if s['mod_id'] == 'ped'])

html_page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cockpit de Protocolos Clínicos & PEP</title>
  <style>
    :root {{
      --bg: #090d16;
      --surface: #0f172a;
      --card-bg: #131b2e;
      --card-hover: #18233c;
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(56, 189, 248, 0.4);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #0284c7;
      --primary-hover: #0369a1;
      --success: #10b981;
      --accent: #f59e0b;
      
      --mod-go: #ec4899;
      --mod-upa: #38bdf8;
      --mod-enf: #10b981;
      --mod-ped: #f59e0b;
      
      --font-sans: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      --font-mono: "JetBrains Mono", "SF Mono", Menlo, Monaco, Consolas, monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
    }}

    /* Topbar */
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 40;
      background: rgba(9, 13, 22, 0.88);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
    }}
    .topbar-content {{
      max-width: 1480px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      width: 34px;
      height: 34px;
      border-radius: 9px;
      background: linear-gradient(135deg, #0284c7, #0ea5e9);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }}
    .brand-text h1 {{
      font-size: 1.12rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #fff;
    }}
    .brand-text p {{
      font-size: 0.76rem;
      color: var(--text-muted);
    }}

    .top-stats {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .counter-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #e2e8f0;
    }}
    .counter-pill .dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 8px var(--success);
    }}

    /* Container Principal */
    .app-container {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 24px;
      width: 100%;
      flex: 1;
    }}

    /* Barra de Navegação & Filtros */
    .controls-panel {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 22px;
    }}

    .nav-tabs {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 4px;
      border-bottom: 1px solid var(--border);
      scrollbar-width: none;
    }}
    .nav-tabs::-webkit-scrollbar {{ display: none; }}
    
    .tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.88rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      transition: all 0.18s ease;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .tab-btn:hover {{
      background: rgba(255, 255, 255, 0.04);
      color: #fff;
    }}
    .tab-btn.active {{
      background: rgba(2, 132, 199, 0.12);
      border-color: rgba(56, 189, 248, 0.35);
      color: #38bdf8;
    }}
    .tab-count {{
      background: rgba(255, 255, 255, 0.08);
      font-size: 0.72rem;
      padding: 2px 7px;
      border-radius: 12px;
      font-weight: 700;
    }}

    .tab-btn.active.tab-go {{
      background: rgba(236, 72, 153, 0.12);
      border-color: rgba(236, 72, 153, 0.35);
      color: #f472b6;
    }}
    .tab-btn.active.tab-upa {{
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.35);
      color: #38bdf8;
    }}
    .tab-btn.active.tab-enf {{
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.35);
      color: #34d399;
    }}
    .tab-btn.active.tab-ped {{
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.35);
      color: #fbbf24;
    }}

    /* Search & Subcategorias */
    .search-row {{
      display: flex;
      gap: 12px;
      align-items: center;
      position: relative;
    }}
    .search-wrapper {{
      position: relative;
      flex: 1;
    }}
    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      padding: 12px 14px 12px 42px;
      border-radius: 9px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: white;
      font-size: 0.94rem;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{
      border-color: #38bdf8;
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
      background: #111a30;
    }}
    .search-shortcut-hint {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-dim);
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: var(--font-mono);
      pointer-events: none;
    }}

    .subcat-chips {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      max-height: 72px;
      overflow-y: auto;
      scrollbar-width: thin;
    }}
    .subcat-chip {{
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.76rem;
      font-weight: 500;
      transition: all 0.15s;
    }}
    .subcat-chip:hover, .subcat-chip.active {{
      background: #1e293b;
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}
    .subcat-chip.active {{
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
    }}

    /* Grid de Cards */
    .grid-cards {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 16px;
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 11px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
      cursor: pointer;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.35);
      background: var(--card-hover);
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}
    .tags-cluster {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .mod-pill {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.02em;
    }}
    .mod-pill-go {{ background: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.25); }}
    .mod-pill-upa {{ background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }}
    .mod-pill-enf {{ background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }}
    .mod-pill-ped {{ background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.25); }}
    
    .cat-pill {{
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .pill-guia {{
      background: rgba(245, 158, 11, 0.1);
      color: #fbbf24;
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(245, 158, 11, 0.25);
    }}

    .trigger-chip {{
      background: #090d16;
      border: 1px solid #334155;
      color: #fbbf24;
      padding: 2px 8px;
      border-radius: 5px;
      font-size: 0.8rem;
      font-family: var(--font-mono);
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .trigger-chip:hover {{
      border-color: #fbbf24;
      background: rgba(251, 191, 36, 0.08);
    }}

    .card-body-block {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .card-title {{
      font-size: 1.02rem;
      font-weight: 600;
      letter-spacing: -0.015em;
      color: #f1f5f9;
      line-height: 1.35;
    }}
    .card-sub {{
      font-size: 0.7rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }}
    .card-preview {{
      background: #090d16;
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 0.74rem;
      color: var(--text-muted);
      overflow: hidden;
      max-height: 80px;
      margin-top: 6px;
    }}
    .card-preview pre {{
      white-space: pre-wrap;
      word-break: break-word;
      font-family: var(--font-mono);
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .btn-group {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Botões */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.8rem;
      font-weight: 600;
      transition: all 0.18s ease;
      font-family: var(--font-sans);
    }}
    .btn-primary {{
      background: var(--primary);
      color: white;
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}
    .btn-ghost {{
      background: rgba(13, 148, 136, 0.15);
      color: #2dd4bf;
      border: 1px solid rgba(13, 148, 136, 0.3);
    }}
    .btn-ghost:hover {{
      background: rgba(13, 148, 136, 0.25);
    }}
    .btn-detail {{
      background: transparent;
      color: var(--text-dim);
      padding: 6px 8px;
    }}
    .btn-detail:hover {{
      color: #fff;
    }}

    /* Drawer / Modal Inspector */
    .drawer-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 90;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }}
    .drawer-overlay.open {{
      opacity: 1;
      pointer-events: auto;
    }}

    .drawer {{
      position: fixed;
      top: 0;
      right: 0;
      bottom: 0;
      width: min(800px, 92vw);
      background: #0d1424;
      border-left: 1px solid var(--border);
      z-index: 100;
      transform: translateX(100%);
      transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      box-shadow: -10px 0 30px rgba(0,0,0,0.5);
    }}
    .drawer-overlay.open .drawer {{
      transform: translateX(0);
    }}

    .drawer-header {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      background: #090d16;
    }}
    .drawer-header h2 {{
      font-size: 1.15rem;
      letter-spacing: -0.02em;
      color: #fff;
      line-height: 1.3;
    }}
    .drawer-header p {{
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 2px;
      font-family: var(--font-mono);
    }}
    .close-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: none;
      color: var(--text-muted);
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .close-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .drawer-tabs {{
      display: flex;
      border-bottom: 1px solid var(--border);
      background: #0b1120;
      padding: 0 16px;
    }}
    .drawer-tab {{
      padding: 10px 16px;
      font-size: 0.84rem;
      font-weight: 600;
      color: var(--text-muted);
      border-bottom: 2px solid transparent;
      cursor: pointer;
      background: none;
      border-top: none;
      border-left: none;
      border-right: none;
    }}
    .drawer-tab.active {{
      color: #38bdf8;
      border-bottom-color: #38bdf8;
    }}

    .drawer-body {{
      flex: 1;
      overflow-y: auto;
      padding: 20px;
    }}
    .drawer-code-block {{
      background: #070a12;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      line-height: 1.55;
      color: #cbd5e1;
      white-space: pre-wrap;
      word-break: break-word;
      user-select: text;
    }}

    .drawer-footer {{
      padding: 14px 20px;
      border-top: 1px solid var(--border);
      background: #090d16;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Toast Notification */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 120;
      background: #0284c7;
      color: white;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      transform: translateY(80px);
      opacity: 0;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }}
    .toast.show {{
      transform: translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>

  <!-- Topbar -->
  <header class="topbar">
    <div class="topbar-content">
      <div class="brand">
        <div class="brand-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
        </div>
        <div class="brand-text">
          <h1>Cockpit de Atendimento & Protocolos</h1>
          <p>Prontuário Eletrônico (PEP) • 100% Offline</p>
        </div>
      </div>

      <div class="top-stats">
        <div class="counter-pill" id="counterPill">
          <span class="dot"></span>
          <span id="counterText">{len(all_snippets)} Protocolos Prontos</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Container -->
  <main class="app-container">
    
    <div class="controls-panel">
      <!-- Abas de Especialidades -->
      <nav class="nav-tabs" id="moduleTabs">
        <button class="tab-btn active" data-mod="all">
          <span>🌐 Geral</span>
          <span class="tab-count">{len(all_snippets)}</span>
        </button>
        <button class="tab-btn tab-go" data-mod="go">
          <span>🌸 GO</span>
          <span class="tab-count">{count_go}</span>
        </button>
        <button class="tab-btn tab-upa" data-mod="upa">
          <span>🚑 UPA Adulto</span>
          <span class="tab-count">{count_upa}</span>
        </button>
        <button class="tab-btn tab-enf" data-mod="enf">
          <span>🏥 Enfermaria</span>
          <span class="tab-count">{count_enf}</span>
        </button>
        <button class="tab-btn tab-ped" data-mod="ped">
          <span>👶 Pediatria</span>
          <span class="tab-count">{count_ped}</span>
        </button>
      </nav>

      <!-- Busca e Filtros -->
      <div class="search-row">
        <div class="search-wrapper">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Buscar por queixa, diagnóstico, atalho (ex: ;bva, ;sca, ;fasthug) ou droga..." autofocus>
          <span class="search-shortcut-hint">/ para buscar</span>
        </div>
      </div>

      <!-- Subcategorias -->
      <div class="subcat-chips" id="subcatContainer">
        <button class="subcat-chip active" data-cat="all">Todas as Áreas</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <section class="grid-cards" id="cardsGrid">
      {cards_joined}
    </section>
  </main>

  <!-- Drawer Modal Inspector -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="closeInspector()">
    <div class="drawer" onclick="event.stopPropagation()">
      <div class="drawer-header">
        <div>
          <h2 id="drawerTitle">Título do Protocolo</h2>
          <p id="drawerPath">caminho/do/arquivo.md</p>
        </div>
        <button class="close-btn" onclick="closeInspector()" title="Fechar (Esc)">✕</button>
      </div>

      <div class="drawer-tabs">
        <button class="drawer-tab active" id="tabPepBtn" onclick="switchDrawerTab('pep')">📋 Snippet PEP</button>
        <button class="drawer-tab" id="tabRecBtn" onclick="switchDrawerTab('receita')">💊 Receita Estruturada</button>
        <button class="drawer-tab" id="tabGuiaBtn" onclick="switchDrawerTab('guia')">🎯 Guia & Condutas</button>
      </div>

      <div class="drawer-body">
        <div class="drawer-code-block" id="drawerContent"></div>
      </div>

      <div class="drawer-footer">
        <span class="trigger-chip" id="drawerTriggerChip" onclick="copyDrawerTrigger()">
          <code id="drawerTrigger">;atalho</code>
        </span>
        <button class="btn btn-primary" id="drawerCopyBtn" onclick="copyCurrentDrawerTab()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          Copiar Texto Aberto
        </button>
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div class="toast" id="toast">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    <span id="toastMsg">Texto copiado!</span>
  </div>

  <script>
    const allData = {snippets_json_payload};

    let activeModule = 'all';
    let activeSubcat = 'all';
    let currentDrawerIndex = null;
    let currentDrawerTab = 'pep';

    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.card');
    const moduleTabs = document.getElementById('moduleTabs');
    const subcatContainer = document.getElementById('subcatContainer');
    const counterText = document.getElementById('counterText');
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');

    // Drawer elements
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerTitle = document.getElementById('drawerTitle');
    const drawerPath = document.getElementById('drawerPath');
    const drawerContent = document.getElementById('drawerContent');
    const drawerTrigger = document.getElementById('drawerTrigger');
    const tabPepBtn = document.getElementById('tabPepBtn');
    const tabRecBtn = document.getElementById('tabRecBtn');
    const tabGuiaBtn = document.getElementById('tabGuiaBtn');

    function showToast(msg) {{
      toastMsg.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2200);
    }}

    function copySnippet(index) {{
      const item = allData[index];
      navigator.clipboard.writeText(item.pep_body).then(() => {{
        showToast('Snippet para PEP copiado!');
      }}).catch(err => alert('Erro: ' + err));
    }}

    function copyReceita(index) {{
      const item = allData[index];
      if (!item.receita_body) return;
      navigator.clipboard.writeText(item.receita_body).then(() => {{
        showToast('Receita copiada!');
      }}).catch(err => alert('Erro: ' + err));
    }}

    function copyTrigger(trig) {{
      navigator.clipboard.writeText(trig).then(() => {{
        showToast(`Atalho ${{trig}} copiado!`);
      }});
    }}

    // Drawer Inspector
    function openInspector(index) {{
      currentDrawerIndex = index;
      const item = allData[index];
      drawerTitle.textContent = item.title;
      drawerPath.textContent = item.path;
      drawerTrigger.textContent = item.trigger;

      // Abas de receita e guia
      tabRecBtn.style.display = item.has_receita ? 'inline-block' : 'none';
      tabGuiaBtn.style.display = item.has_guia ? 'inline-block' : 'none';

      switchDrawerTab('pep');
      drawerOverlay.classList.add('open');
    }}

    function closeInspector() {{
      drawerOverlay.classList.remove('open');
      currentDrawerIndex = null;
    }}

    function switchDrawerTab(tab) {{
      currentDrawerTab = tab;
      const item = allData[currentDrawerIndex];
      tabPepBtn.classList.toggle('active', tab === 'pep');
      tabRecBtn.classList.toggle('active', tab === 'receita');
      tabGuiaBtn.classList.toggle('active', tab === 'guia');

      if (tab === 'pep') {{
        drawerContent.textContent = item.pep_body;
      }} else if (tab === 'receita') {{
        drawerContent.textContent = item.receita_body || 'Sem receita específica associada.';
      }} else if (tab === 'guia') {{
        drawerContent.textContent = item.guia_body || 'Sem guia de conduta adicional.';
      }}
    }}

    function copyCurrentDrawerTab() {{
      const text = drawerContent.textContent;
      navigator.clipboard.writeText(text).then(() => {{
        showToast('Conteúdo copiado com sucesso!');
      }});
    }}

    function copyDrawerTrigger() {{
      const trig = drawerTrigger.textContent;
      copyTrigger(trig);
    }}

    // Subcategorias Dinâmicas
    function updateSubcategories() {{
      subcatContainer.innerHTML = '<button class="subcat-chip active" data-cat="all">Todas as Áreas</button>';
      const cats = new Set();
      cards.forEach(c => {{
        if (activeModule === 'all' || c.dataset.mod === activeModule) {{
          cats.add(c.dataset.cat);
        }}
      }});
      Array.from(cats).sort().forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'subcat-chip';
        btn.dataset.cat = cat;
        btn.textContent = cat;
        subcatContainer.appendChild(btn);
      }});
      activeSubcat = 'all';
    }}

    // Filtragem
    function filterCards() {{
      const q = searchInput.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(c => {{
        const matchSearch = !q || c.dataset.search.includes(q);
        const matchMod = (activeModule === 'all') || (c.dataset.mod === activeModule);
        const matchCat = (activeSubcat === 'all') || (c.dataset.cat === activeSubcat);

        if (matchSearch && matchMod && matchCat) {{
          c.style.display = 'flex';
          visible++;
        }} else {{
          c.style.display = 'none';
        }}
      }});
      counterText.textContent = `${{visible}} Protocolos Filtrados`;
    }}

    searchInput.addEventListener('input', filterCards);

    moduleTabs.addEventListener('click', (e) => {{
      const btn = e.target.closest('.tab-btn');
      if (!btn) return;
      moduleTabs.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeModule = btn.dataset.mod;
      updateSubcategories();
      filterCards();
    }});

    subcatContainer.addEventListener('click', (e) => {{
      if (e.target.classList.contains('subcat-chip')) {{
        subcatContainer.querySelectorAll('.subcat-chip').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        activeSubcat = e.target.dataset.cat;
        filterCards();
      }}
    }});

    // Atalhos de Teclado
    window.addEventListener('keydown', (e) => {{
      if (e.key === '/' && document.activeElement !== searchInput) {{
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }} else if (e.key === 'Escape') {{
        if (drawerOverlay.classList.contains('open')) {{
          closeInspector();
        }} else if (searchInput.value) {{
          searchInput.value = '';
          filterCards();
        }}
      }}
    }});

    // Inicialização
    updateSubcategories();
  </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as fh:
    fh.write(html_page)
index_path = os.path.join(BASE_PROJECT, 'index.html')
with open(index_path, 'w', encoding='utf-8') as fh:
    fh.write(html_page)
print(f"Cockpit Web UI/UX High-End salvo em {html_path} e {index_path}")
