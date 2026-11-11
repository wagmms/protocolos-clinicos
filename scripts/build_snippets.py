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
        trigger_match = re.search(r'\*\*Atalho (?:Recomendado|sugerido|sugeridos):\*\*\s*`?([^`\n\r]+)`?', content, re.IGNORECASE)
        if trigger_match:
            raw_triggers = trigger_match.group(1).strip()
            # Se houver múltiplos atalhos ex: ;mastite | ;endometrite
            first_trigger = [t.strip().strip('`') for t in re.split(r'\||,', raw_triggers) if t.strip()][0]
            trigger = first_trigger
            all_triggers = [t.strip().strip('`') for t in re.split(r'\||,', raw_triggers) if t.strip()]
        else:
            trigger = ';' + os.path.splitext(os.path.basename(f))[0].lower().replace('_', '-')
            all_triggers = [trigger]
            
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
                
        # Divisão Segmentada: Evolução vs Conduta
        split_match = re.search(r'^(#+\s*(?:PLANO\s*/\s*CONDUTA|PLANO|CONDUTA|PRESCRIÇÃO|PRESCRIÇÃO\s*MÉDICA).*)$', snippet_pep, re.M | re.IGNORECASE)
        if split_match:
            split_pos = split_match.start()
            evolucao_body = snippet_pep[:split_pos].strip()
            conduta_body = snippet_pep[split_pos:].strip()
            has_split = True
        else:
            evolucao_body = snippet_pep
            conduta_body = ""
            has_split = False

        # Receita Médica
        receita_match = re.search(r'##\s+💊\s*Receita[^\n]*\n+```(?:markdown|text)?\n(.*?)\n```', content, re.DOTALL)
        receita_text = receita_match.group(1).strip() if receita_match else ""
        
        # Guia de Conduta / Bolso
        guia_match = re.search(r'(?:##\s+🎯\s*Guia de Bolso|###\s+\[REGRAS DE CONDUTA|###\s+\[DIRETRIZES|###\s+\[PONTOS CRÍTICOS)(.*)', content, re.DOTALL)
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
            'all_triggers': all_triggers,
            'category': subcat_clean,
            'path': rel_path,
            'pep_body': snippet_pep,
            'has_split': has_split,
            'evolucao_body': evolucao_body,
            'conduta_body': conduta_body,
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
            for trg in s['all_triggers']:
                fh.write(f"  - trigger: \"{trg}\"\n")
                fh.write(f"    replace: |\n")
                for line in s['pep_body'].splitlines():
                    fh.write(f"      {line}\n")
                fh.write("\n")
                if s['has_split'] and s['conduta_body']:
                    fh.write(f"  - trigger: \"{trg}-cnd\"\n")
                    fh.write(f"    replace: |\n")
                    for line in s['conduta_body'].splitlines():
                        fh.write(f"      {line}\n")
                    fh.write("\n")
                if s['receita_body']:
                    fh.write(f"  - trigger: \"{trg}-rec\"\n")
                    fh.write(f"    replace: |\n")
                    for line in s['receita_body'].splitlines():
                        fh.write(f"      {line}\n")
                    fh.write("\n")

all_yaml_path = os.path.join(SNIPPETS_DIR, "espanso_completo.yml")
with open(all_yaml_path, 'w', encoding='utf-8') as fh:
    fh.write(f"# Configuração Completa Espanso ({len(all_snippets)} Modelos)\n\nmatches:\n")
    for s in all_snippets:
        for trg in s['all_triggers']:
            fh.write(f"  - trigger: \"{trg}\"\n")
            fh.write(f"    replace: |\n")
            for line in s['pep_body'].splitlines():
                fh.write(f"      {line}\n")
            fh.write("\n")
            if s['has_split'] and s['conduta_body']:
                fh.write(f"  - trigger: \"{trg}-cnd\"\n")
                fh.write(f"    replace: |\n")
                for line in s['conduta_body'].splitlines():
                    fh.write(f"      {line}\n")
                fh.write("\n")
            if s['receita_body']:
                fh.write(f"  - trigger: \"{trg}-rec\"\n")
                fh.write(f"    replace: |\n")
                for line in s['receita_body'].splitlines():
                    fh.write(f"      {line}\n")
                fh.write("\n")

# 3. Cockpit Web UI/UX High-End Anti-Slop
html_path = os.path.join(BASE_PROJECT, 'painel_rapido_snippets.html')

cards_html = []
for idx, s in enumerate(all_snippets):
    # Botões segmentados
    segment_buttons = []
    
    # 1. Copiar Completo
    segment_buttons.append(f"""
      <button class="btn btn-primary" onclick='event.stopPropagation(); copySnippet({idx})' title="Copiar evolução e conduta completas">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        Copiar Tudo
      </button>
    """)
    
    # 2. Copiar Conduta (se houver divisão)
    if s['has_split'] and s['conduta_body']:
        segment_buttons.append(f"""
          <button class="btn btn-cnd" onclick='event.stopPropagation(); copyConduta({idx})' title="Copiar apenas a conduta / prescrição imediata">
            💉 Conduta
          </button>
        """)
        
    # 3. Copiar Receita
    if s['has_receita']:
        segment_buttons.append(f"""
          <button class="btn btn-rec" onclick='event.stopPropagation(); copyReceita({idx})' title="Copiar apenas a receita estruturada">
            💊 Receita
          </button>
        """)
        
    has_guia_badge = '<span class="pill pill-guia" title="Contém diretrizes e conduta clínica">🎯 Conduta</span>' if s['has_guia'] else ''
    has_split_badge = '<span class="pill pill-split" title="Permite cópia separada de Anamnese e Conduta">⚡ Bipartido</span>' if s['has_split'] else ''
    
    search_keywords = f"{s['title'].lower()} {' '.join(s['all_triggers']).lower()} {s['category'].lower()} {s['module_name'].lower()} {s['path'].lower()}"
    preview_text = html.escape(s['pep_body'][:220]) + ("..." if len(s['pep_body']) > 220 else "")
    
    trigger_chips_html = " ".join([
        f"""<button class="trigger-chip" onclick='event.stopPropagation(); copyTrigger("{t}")' title="Copiar atalho"><code>{t}</code><svg class="copy-icon" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>"""
        for t in s['all_triggers']
    ])

    cards_html.append(f"""
    <article class="card card-{s['mod_id']}" data-mod="{s['mod_id']}" data-cat="{s['category']}" data-search="{html.escape(search_keywords)}" onclick="openInspector({idx})">
      <div class="card-top">
        <div class="tags-cluster">
          <span class="mod-pill mod-pill-{s['mod_id']}">{s['badge']}</span>
          <span class="cat-pill">{s['category']}</span>
          {has_split_badge}
          {has_guia_badge}
        </div>
        <div class="triggers-wrap">
          {trigger_chips_html}
        </div>
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
          {''.join(segment_buttons)}
        </div>
        <button class="btn btn-detail" onclick="event.stopPropagation(); openInspector({idx})" title="Visualizar e personalizar">
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
      background: rgba(9, 13, 22, 0.92);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
    }}
    .topbar-content {{
      max-width: 1540px;
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
      font-size: 1.08rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #fff;
    }}
    .brand-text p {{
      font-size: 0.74rem;
      color: var(--text-muted);
    }}

    /* Top Actions & Calculadora de Peso */
    .top-tools {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .weight-widget {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 4px 10px;
    }}
    .weight-label {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .weight-input {{
      width: 58px;
      background: #090d16;
      border: 1px solid #334155;
      color: #38bdf8;
      font-family: var(--font-mono);
      font-size: 0.88rem;
      font-weight: 700;
      padding: 3px 6px;
      border-radius: 5px;
      text-align: center;
      outline: none;
    }}
    .weight-input:focus {{
      border-color: #38bdf8;
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }}
    .weight-unit {{
      font-size: 0.78rem;
      color: var(--text-dim);
      font-weight: 600;
    }}
    .btn-doses {{
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #38bdf8;
      font-size: 0.74rem;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn-doses:hover {{
      background: rgba(56, 189, 248, 0.22);
    }}

    .btn-palette-trigger {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      color: #e2e8f0;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 7px;
      transition: all 0.15s;
    }}
    .btn-palette-trigger:hover {{
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }}
    .kbd-shortcut {{
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 1px 5px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-family: var(--font-mono);
      color: #94a3b8;
    }}

    .counter-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
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
      max-width: 1540px;
      margin: 0 auto;
      padding: 20px 24px;
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
      grid-template-columns: repeat(auto-fill, minmax(390px, 1fr));
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
      align-items: flex-start;
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
    .pill-split {{
      background: rgba(56, 189, 248, 0.1);
      color: #38bdf8;
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(56, 189, 248, 0.25);
    }}

    .triggers-wrap {{
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }}
    .trigger-chip {{
      background: #090d16;
      border: 1px solid #334155;
      color: #fbbf24;
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 0.78rem;
      font-family: var(--font-mono);
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
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
      gap: 6px;
    }}
    .btn-group {{
      display: flex;
      align-items: center;
      gap: 5px;
      flex-wrap: wrap;
    }}

    /* Botões */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: none;
      padding: 6px 11px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.78rem;
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
    .btn-cnd {{
      background: rgba(56, 189, 248, 0.14);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .btn-cnd:hover {{
      background: rgba(56, 189, 248, 0.25);
    }}
    .btn-rec {{
      background: rgba(13, 148, 136, 0.14);
      color: #2dd4bf;
      border: 1px solid rgba(13, 148, 136, 0.3);
    }}
    .btn-rec:hover {{
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
      background: rgba(0, 0, 0, 0.72);
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
      width: min(840px, 94vw);
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
      overflow-x: auto;
    }}
    .drawer-tab {{
      padding: 10px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      border-bottom: 2px solid transparent;
      cursor: pointer;
      background: none;
      border-top: none;
      border-left: none;
      border-right: none;
      white-space: nowrap;
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

    /* Personalizador Interativo */
    .interactive-panel {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .interactive-lead {{
      font-size: 0.82rem;
      color: #94a3b8;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.2);
      padding: 8px 12px;
      border-radius: 6px;
    }}
    .interactive-rendered {{
      background: #070a12;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      line-height: 1.6;
      color: #e2e8f0;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .choice-group {{
      display: inline-flex;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 2px;
      margin: 0 3px;
      vertical-align: baseline;
    }}
    .choice-pill {{
      background: transparent;
      border: none;
      color: #94a3b8;
      font-family: var(--font-sans);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.12s;
    }}
    .choice-pill:hover {{
      color: #fff;
    }}
    .choice-pill.active {{
      background: #0284c7;
      color: #fff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }}

    .drawer-footer {{
      padding: 14px 20px;
      border-top: 1px solid var(--border);
      background: #090d16;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    /* Modal Command Palette (Ctrl+K) */
    .cmd-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(6px);
      z-index: 150;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 12vh;
    }}
    .cmd-overlay.open {{
      display: flex;
    }}
    .cmd-modal {{
      width: min(680px, 92vw);
      background: #0f172a;
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      animation: cmdPop 0.15s ease-out;
    }}
    @keyframes cmdPop {{
      from {{ transform: scale(0.96); opacity: 0; }}
      to {{ transform: scale(1); opacity: 1; }}
    }}
    .cmd-search-box {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      background: #090d16;
    }}
    .cmd-search-input {{
      flex: 1;
      background: transparent;
      border: none;
      color: #fff;
      font-size: 1.05rem;
      outline: none;
    }}
    .cmd-results {{
      max-height: 400px;
      overflow-y: auto;
      padding: 8px;
    }}
    .cmd-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.12s;
    }}
    .cmd-item:hover, .cmd-item.active {{
      background: rgba(56, 189, 248, 0.15);
    }}
    .cmd-item-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .cmd-item-title {{
      font-size: 0.92rem;
      font-weight: 600;
      color: #fff;
    }}
    .cmd-item-cat {{
      font-size: 0.74rem;
      color: var(--text-dim);
    }}
    .cmd-item-trig {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: #fbbf24;
      background: rgba(0, 0, 0, 0.3);
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid #334155;
    }}
    .cmd-footer {{
      padding: 8px 16px;
      background: #090d16;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      color: var(--text-dim);
    }}

    /* Modal Calculadora de Doses Rápidas */
    .doses-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 140;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .doses-overlay.open {{
      display: flex;
    }}
    .doses-modal {{
      width: min(720px, 94vw);
      max-height: 85vh;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 16px 40px rgba(0,0,0,0.6);
      overflow: hidden;
    }}
    .doses-header {{
      padding: 14px 20px;
      background: #090d16;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .doses-body {{
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .dose-card {{
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .dose-name {{
      font-size: 0.86rem;
      font-weight: 700;
      color: #fff;
    }}
    .dose-rule {{
      font-size: 0.74rem;
      color: var(--text-dim);
    }}
    .dose-calc {{
      font-family: var(--font-mono);
      font-size: 0.95rem;
      font-weight: 700;
      color: #38bdf8;
      text-align: right;
    }}
    .dose-copy-btn {{
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      font-size: 0.72rem;
      padding: 4px 8px;
      border-radius: 5px;
      cursor: pointer;
    }}
    .dose-copy-btn:hover {{
      background: rgba(56, 189, 248, 0.2);
    }}

    /* Toast Notification */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 200;
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

      <div class="top-tools">
        <!-- Calculadora de Peso -->
        <div class="weight-widget" title="Ajuste o peso do paciente para calcular doses em tempo real">
          <span class="weight-label">⚖️ Peso:</span>
          <input type="number" id="quickWeightInput" class="weight-input" value="70" min="1" max="250">
          <span class="weight-unit">kg</span>
          <button class="btn-doses" onclick="openDosesModal()">Doses Ponderais ▾</button>
        </div>

        <!-- Botão Command Palette -->
        <button class="btn-palette-trigger" onclick="openCmdPalette()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <span>Buscar</span>
          <span class="kbd-shortcut">Ctrl+K</span>
        </button>

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
          <input type="text" id="searchInput" class="search-input" placeholder="Buscar por queixa, diagnóstico, atalho (ex: ;sepse, ;tpp, ;sca, ;fasthug) ou droga..." autofocus>
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
        <button class="drawer-tab active" id="tabPepBtn" onclick="switchDrawerTab('pep')">📋 Snippet Completo</button>
        <button class="drawer-tab" id="tabInteractiveBtn" onclick="switchDrawerTab('interactive')">⚡ Personalizar & Chips</button>
        <button class="drawer-tab" id="tabCondutaBtn" onclick="switchDrawerTab('conduta')">💉 Apenas Conduta</button>
        <button class="drawer-tab" id="tabRecBtn" onclick="switchDrawerTab('receita')">💊 Receita de Alta</button>
        <button class="drawer-tab" id="tabGuiaBtn" onclick="switchDrawerTab('guia')">🎯 Diretrizes</button>
      </div>

      <div class="drawer-body">
        <div class="drawer-code-block" id="drawerContent"></div>
        <div class="interactive-panel" id="drawerInteractivePanel" style="display:none;">
          <div class="interactive-lead">
            ⚡ <strong>Personalização Rápida:</strong> Clique nas opções nos chips abaixo para selecionar a conduta desejada antes de copiar para o prontuário.
          </div>
          <div class="interactive-rendered" id="interactiveRendered"></div>
        </div>
      </div>

      <div class="drawer-footer">
        <div style="display:flex; align-items:center; gap:6px;">
          <span class="trigger-chip" id="drawerTriggerChip" onclick="copyDrawerTrigger()">
            <code id="drawerTrigger">;atalho</code>
          </span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button class="btn btn-primary" id="drawerCopyBtn" onclick="copyCurrentDrawerTab()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copiar Texto Aberto
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Command Palette Modal (Ctrl+K) -->
  <div class="cmd-overlay" id="cmdOverlay" onclick="closeCmdPalette()">
    <div class="cmd-modal" onclick="event.stopPropagation()">
      <div class="cmd-search-box">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="cmdSearchInput" class="cmd-search-input" placeholder="Buscar protocolo, queixa ou atalho... (Enter para copiar, Esc para fechar)" autocomplete="off">
        <span class="kbd-shortcut">ESC</span>
      </div>
      <div class="cmd-results" id="cmdResults"></div>
      <div class="cmd-footer">
        <span>↑↓ para navegar • Enter para copiar PEP • Shift+Enter para abrir</span>
        <span id="cmdCount">91 disponíveis</span>
      </div>
    </div>
  </div>

  <!-- Modal de Doses Ponderais Rápidas -->
  <div class="doses-overlay" id="dosesOverlay" onclick="closeDosesModal()">
    <div class="doses-modal" onclick="event.stopPropagation()">
      <div class="doses-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:1.3rem;">⚖️</span>
          <div>
            <h2 style="font-size:1.05rem; font-weight:700; color:#fff;">Calculadora de Doses Críticas por Peso</h2>
            <p style="font-size:0.76rem; color:var(--text-muted);">Cálculo automático baseado no peso atual: <strong id="modalWeightDisplay" style="color:#38bdf8;">70 kg</strong></p>
          </div>
        </div>
        <button class="close-btn" onclick="closeDosesModal()">✕</button>
      </div>

      <div class="doses-body" id="dosesContainer">
        <!-- Injetado dinamicamente via JS -->
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
    let cmdActiveIndex = 0;
    let cmdMatches = [];

    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.card');
    const moduleTabs = document.getElementById('moduleTabs');
    const subcatContainer = document.getElementById('subcatContainer');
    const counterText = document.getElementById('counterText');
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');
    const quickWeightInput = document.getElementById('quickWeightInput');

    // Drawer elements
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerTitle = document.getElementById('drawerTitle');
    const drawerPath = document.getElementById('drawerPath');
    const drawerContent = document.getElementById('drawerContent');
    const drawerInteractivePanel = document.getElementById('drawerInteractivePanel');
    const interactiveRendered = document.getElementById('interactiveRendered');
    const drawerTrigger = document.getElementById('drawerTrigger');
    const tabPepBtn = document.getElementById('tabPepBtn');
    const tabInteractiveBtn = document.getElementById('tabInteractiveBtn');
    const tabCondutaBtn = document.getElementById('tabCondutaBtn');
    const tabRecBtn = document.getElementById('tabRecBtn');
    const tabGuiaBtn = document.getElementById('tabGuiaBtn');

    // Command Palette elements
    const cmdOverlay = document.getElementById('cmdOverlay');
    const cmdSearchInput = document.getElementById('cmdSearchInput');
    const cmdResults = document.getElementById('cmdResults');
    const cmdCount = document.getElementById('cmdCount');

    // Doses Modal elements
    const dosesOverlay = document.getElementById('dosesOverlay');
    const modalWeightDisplay = document.getElementById('modalWeightDisplay');
    const dosesContainer = document.getElementById('dosesContainer');

    function showToast(msg) {{
      toastMsg.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2200);
    }}

    function copySnippet(index) {{
      const item = allData[index];
      navigator.clipboard.writeText(item.pep_body).then(() => {{
        showToast('Snippet PEP completo copiado!');
      }}).catch(err => alert('Erro: ' + err));
    }}

    function copyConduta(index) {{
      const item = allData[index];
      if (!item.conduta_body) return;
      navigator.clipboard.writeText(item.conduta_body).then(() => {{
        showToast('Conduta / Prescrição imediata copiada!');
      }}).catch(err => alert('Erro: ' + err));
    }}

    function copyReceita(index) {{
      const item = allData[index];
      if (!item.receita_body) return;
      navigator.clipboard.writeText(item.receita_body).then(() => {{
        showToast('Receita de alta copiada!');
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

      // Abas condicionais
      tabCondutaBtn.style.display = item.has_split ? 'inline-block' : 'none';
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
      tabInteractiveBtn.classList.toggle('active', tab === 'interactive');
      tabCondutaBtn.classList.toggle('active', tab === 'conduta');
      tabRecBtn.classList.toggle('active', tab === 'receita');
      tabGuiaBtn.classList.toggle('active', tab === 'guia');

      if (tab === 'interactive') {{
        drawerContent.style.display = 'none';
        drawerInteractivePanel.style.display = 'flex';
        renderInteractive(item.pep_body);
      }} else {{
        drawerContent.style.display = 'block';
        drawerInteractivePanel.style.display = 'none';

        if (tab === 'pep') {{
          drawerContent.textContent = item.pep_body;
        }} else if (tab === 'conduta') {{
          drawerContent.textContent = item.conduta_body || 'Sem seção de conduta separada.';
        }} else if (tab === 'receita') {{
          drawerContent.textContent = item.receita_body || 'Sem receita específica associada.';
        }} else if (tab === 'guia') {{
          drawerContent.textContent = item.guia_body || 'Sem guia de conduta adicional.';
        }}
      }}
    }}

    // Renderização do Personalizador Interativo
    function renderInteractive(rawText) {{
      interactiveRendered.innerHTML = '';
      
      // Quebrar por linhas para manter formatação
      const lines = rawText.split('\\n');
      const frag = document.createDocumentFragment();

      lines.forEach((line, lIdx) => {{
        const lineDiv = document.createElement('div');
        
        // Identificar padrões de escolha [ Opção 1 / Opção 2 ]
        const parts = line.split(/(\\[[^\\]]+?\\s*\\/\\s*[^^\\]]+?\\])/g);
        
        parts.forEach((part, pIdx) => {{
          if (part.startsWith('[') && part.endsWith(']') && part.includes('/')) {{
            const inner = part.slice(1, -1);
            const options = inner.split('/').map(o => o.trim());
            
            const groupSpan = document.createElement('span');
            groupSpan.className = 'choice-group';
            
            options.forEach((opt, oIdx) => {{
              const btn = document.createElement('button');
              btn.className = 'choice-pill' + (oIdx === 0 ? ' active' : '');
              btn.textContent = opt;
              btn.onclick = () => {{
                groupSpan.querySelectorAll('.choice-pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
              }};
              groupSpan.appendChild(btn);
            }});
            lineDiv.appendChild(groupSpan);
          }} else {{
            lineDiv.appendChild(document.createTextNode(part));
          }}
        }});

        frag.appendChild(lineDiv);
      }});

      interactiveRendered.appendChild(frag);
    }}

    function copyCurrentDrawerTab() {{
      if (currentDrawerTab === 'interactive') {{
        // Obter o texto renderizado substituindo os grupos pelas escolhas ativas
        let text = "";
        interactiveRendered.childNodes.forEach(lineNode => {{
          let lineText = "";
          lineNode.childNodes.forEach(child => {{
            if (child.classList && child.classList.contains('choice-group')) {{
              const active = child.querySelector('.choice-pill.active');
              lineText += active ? active.textContent : "";
            }} else {{
              lineText += child.textContent;
            }}
          }});
          text += lineText + "\\n";
        }});
        navigator.clipboard.writeText(text.trim()).then(() => {{
          showToast('Texto personalizado copiado!');
        }});
      }} else {{
        const text = drawerContent.textContent;
        navigator.clipboard.writeText(text).then(() => {{
          showToast('Conteúdo copiado com sucesso!');
        }});
      }}
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

    // Filtragem Principal
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

    // Command Palette Modal (Ctrl+K)
    function openCmdPalette() {{
      cmdOverlay.classList.add('open');
      cmdSearchInput.value = '';
      cmdSearchInput.focus();
      updateCmdResults('');
    }}

    function closeCmdPalette() {{
      cmdOverlay.classList.remove('open');
    }}

    function updateCmdResults(query) {{
      const q = query.toLowerCase().trim();
      cmdMatches = allData.filter(item => {{
        if (!q) return true;
        return item.title.toLowerCase().includes(q) ||
               item.all_triggers.some(t => t.toLowerCase().includes(q)) ||
               item.category.toLowerCase().includes(q) ||
               item.module_name.toLowerCase().includes(q);
      }}).slice(0, 15);

      cmdResults.innerHTML = '';
      cmdActiveIndex = 0;

      if (cmdMatches.length === 0) {{
        cmdResults.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-dim); font-size:0.86rem;">Nenhum protocolo encontrado.</div>';
        cmdCount.textContent = '0 resultados';
        return;
      }}

      cmdMatches.forEach((item, idx) => {{
        const div = document.createElement('div');
        div.className = 'cmd-item' + (idx === 0 ? ' active' : '');
        div.innerHTML = `
          <div class="cmd-item-left">
            <span>${{item.badge.split(' ')[0]}}</span>
            <div>
              <div class="cmd-item-title">${{item.title}}</div>
              <div class="cmd-item-cat">${{item.module_name}} • ${{item.category}}</div>
            </div>
          </div>
          <span class="cmd-item-trig">${{item.trigger}}</span>
        `;
        div.onclick = () => {{
          copySnippet(allData.indexOf(item));
          closeCmdPalette();
        }};
        cmdResults.appendChild(div);
      }});

      cmdCount.textContent = `${{cmdMatches.length}} de ${{allData.length}} protocolos`;
    }}

    cmdSearchInput.addEventListener('input', (e) => {{
      updateCmdResults(e.target.value);
    }});

    // Navegação no Command Palette por teclado
    cmdSearchInput.addEventListener('keydown', (e) => {{
      const items = cmdResults.querySelectorAll('.cmd-item');
      if (items.length === 0) return;

      if (e.key === 'ArrowDown') {{
        e.preventDefault();
        items[cmdActiveIndex].classList.remove('active');
        cmdActiveIndex = (cmdActiveIndex + 1) % items.length;
        items[cmdActiveIndex].classList.add('active');
        items[cmdActiveIndex].scrollIntoView({{ block: 'nearest' }});
      }} else if (e.key === 'ArrowUp') {{
        e.preventDefault();
        items[cmdActiveIndex].classList.remove('active');
        cmdActiveIndex = (cmdActiveIndex - 1 + items.length) % items.length;
        items[cmdActiveIndex].classList.add('active');
        items[cmdActiveIndex].scrollIntoView({{ block: 'nearest' }});
      }} else if (e.key === 'Enter') {{
        e.preventDefault();
        if (cmdMatches[cmdActiveIndex]) {{
          const item = cmdMatches[cmdActiveIndex];
          if (e.shiftKey) {{
            openInspector(allData.indexOf(item));
          }} else {{
            copySnippet(allData.indexOf(item));
          }}
          closeCmdPalette();
        }}
      }}
    }});

    // Modal de Doses Ponderais Rápidas
    function openDosesModal() {{
      const weight = parseFloat(quickWeightInput.value) || 70;
      modalWeightDisplay.textContent = `${{weight}} kg`;
      renderDoses(weight);
      dosesOverlay.classList.add('open');
    }}

    function closeDosesModal() {{
      dosesOverlay.classList.remove('open');
    }}

    function renderDoses(w) {{
      const doses = [
        {{
          name: 'Ressuscitação na Sepse (30 mL/kg)',
          rule: '30 mL/kg de Ringer Lactato aquecido nas primeiras 3 horas',
          calc: `${{Math.round(w * 30)}} mL de Ringer Lactato EV rápido`,
          copy: `${{Math.round(w * 30)}} mL de Ringer Lactato EV em 3 horas`
        }},
        {{
          name: 'Dengue Grupo C - Fase de Expansão (10 mL/kg/h)',
          rule: '10 mL/kg/hora nas primeiras 2 horas',
          calc: `${{Math.round(w * 10)}} mL/hora`,
          copy: `SF 0,9% ou Ringer Lactato: infundir ${{Math.round(w * 10)}} mL/hora nas primeiras 2 horas.`
        }},
        {{
          name: 'Alteplase (rt-PA) no AVC Isquêmico (0,9 mg/kg)',
          rule: '0,9 mg/kg (máx 90mg) • 10% em bólus 1 min + 90% em 60 min',
          calc: `${{Math.min(90, (w * 0.9)).toFixed(1)}} mg total (${{(Math.min(90, w * 0.9) * 0.1).toFixed(1)}} mg bólus + ${{(Math.min(90, w * 0.9) * 0.9).toFixed(1)}} mg em 1h)`,
          copy: `Alteplase (rt-PA) para peso ${{w}} kg: Dose total: ${{Math.min(90, (w * 0.9)).toFixed(1)}} mg EV. Administrar ${{(Math.min(90, w * 0.9) * 0.1).toFixed(1)}} mg em bólus EV em 1 min e ${{(Math.min(90, w * 0.9) * 0.9).toFixed(1)}} mg em BIC em 60 min.`
        }},
        {{
          name: 'Enoxaparina Terapêutica Plena (1 mg/kg 12/12h)',
          rule: '1 mg/kg SC de 12/12h (idade < 75 anos e ClCr > 30)',
          calc: `${{Math.round(w)}} mg SC 12/12h`,
          copy: `Enoxaparina ${{Math.round(w)}} mg SC de 12/12 horas.`
        }},
        {{
          name: 'Enoxaparina Terapêutica Idoso >= 75 anos (0,75 mg/kg 12/12h)',
          rule: '0,75 mg/kg SC de 12/12h sem bólus EV',
          calc: `${{(w * 0.75).toFixed(0)}} mg SC 12/12h`,
          copy: `Enoxaparina ${{(w * 0.75).toFixed(0)}} mg SC de 12/12 horas.`
        }},
        {{
          name: 'Dipirona Gotas (1 gota/kg)',
          rule: '1 gota/kg até máximo de 40 gotas (1g) por tomada',
          calc: `${{Math.min(40, Math.round(w))}} gotas VO`,
          copy: `Dipirona gotas: Tomar ${{Math.min(40, Math.round(w))}} gotas via oral de 6/6 horas SOS se dor ou febre.`
        }},
        {{
          name: 'Paracetamol Gotas 200mg/mL (1 gota/kg)',
          rule: '1 gota/kg (máx 35-40 gotas / 750mg) por tomada',
          calc: `${{Math.min(37, Math.round(w))}} gotas VO`,
          copy: `Paracetamol gotas (200 mg/mL): Tomar ${{Math.min(37, Math.round(w))}} gotas via oral de 6/6 horas SOS se febre.`
        }},
        {{
          name: 'Sequência Rápida de Intubação: Etomidato (0,3 mg/kg)',
          rule: '0,3 mg/kg EV em bólus',
          calc: `${{(w * 0.3).toFixed(1)}} mg EV`,
          copy: `Etomidato: ${{(w * 0.3).toFixed(1)}} mg EV em bólus rápido.`
        }},
        {{
          name: 'Sequência Rápida de Intubação: Succinilcolina (1,2 mg/kg)',
          rule: '1,0 a 1,5 mg/kg EV em bólus',
          calc: `${{Math.round(w * 1.2)}} mg EV`,
          copy: `Succinilcolina: ${{Math.round(w * 1.2)}} mg EV em bólus rápido.`
        }},
        {{
          name: 'Sequência Rápida de Intubação: Fentanil (2 mcg/kg)',
          rule: '1 a 2 mcg/kg EV lento',
          calc: `${{Math.round(w * 2)}} mcg (${{(w * 2 / 50).toFixed(1)}} mL) EV`,
          copy: `Fentanil: ${{Math.round(w * 2)}} mcg (${{(w * 2 / 50).toFixed(1)}} mL) EV lento.`
        }}
      ];

      dosesContainer.innerHTML = '';
      doses.forEach(d => {{
        const card = document.createElement('div');
        card.className = 'dose-card';
        card.innerHTML = `
          <div>
            <div class="dose-name">${{d.name}}</div>
            <div class="dose-rule">${{d.rule}}</div>
          </div>
          <div style="display:flex; align-items:center; gap:10px;">
            <div class="dose-calc">${{d.calc}}</div>
            <button class="dose-copy-btn" onclick='navigator.clipboard.writeText("${{d.copy}}").then(() => showToast("Dose copiada!"))'>Copiar</button>
          </div>
        `;
        dosesContainer.appendChild(card);
      }});
    }}

    quickWeightInput.addEventListener('input', () => {{
      const w = parseFloat(quickWeightInput.value) || 70;
      modalWeightDisplay.textContent = `${{w}} kg`;
      renderDoses(w);
    }});

    // Atalhos Globais de Teclado
    window.addEventListener('keydown', (e) => {{
      // Ctrl+K ou Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openCmdPalette();
        return;
      }}
      
      // / para focar a busca se não estiver em outro input
      if (e.key === '/' && document.activeElement !== searchInput && document.activeElement !== cmdSearchInput && document.activeElement !== quickWeightInput) {{
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }} else if (e.key === 'Escape') {{
        if (cmdOverlay.classList.contains('open')) {{
          closeCmdPalette();
        }} else if (dosesOverlay.classList.contains('open')) {{
          closeDosesModal();
        }} else if (drawerOverlay.classList.contains('open')) {{
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
print(f"Cockpit Web UI/UX High-End salvo com sucesso em {html_path} e {index_path}!")
