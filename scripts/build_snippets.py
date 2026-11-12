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

HAB_DIR = os.path.join(BASE_PROJECT, '05_Habilidades_Clinicas')


def extract_md_meta(content, labels):
    """Extrai campo de metadados em Markdown no formato **Campo:** valor."""
    if isinstance(labels, str):
        labels = [labels]
    pattern_labels = '|'.join(re.escape(lbl) for lbl in labels)
    m = re.search(
        rf'^\s*\*\*(?:{pattern_labels})\s*:?\*\*\s*:?\s*(.+)$',
        content,
        re.MULTILINE | re.IGNORECASE
    )
    return m.group(1).strip() if m else ''


def extract_section_body(content, heading_pattern):
    """Extrai o conteúdo de uma seção H2 (## ...) até a próxima H2 ou fim do arquivo."""
    m = re.search(
        rf'^##\s+{heading_pattern}[^\n]*\n(.*?)(?=^##\s+|\Z)',
        content,
        re.MULTILINE | re.DOTALL | re.IGNORECASE
    )
    return m.group(1).strip() if m else ''


def parse_hab_card(file_path, seq_num):
    """Faz o parsing completo de um cartão de habilidade clínica em 05_Habilidades_Clinicas/."""
    with open(file_path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(file_path))[0]

    hab_category = extract_md_meta(content, ['Categoria']) or 'Habilidades Clínicas'
    time_goal = extract_md_meta(content, ['Meta de Tempo', 'Tempo']) or '5–10 min'
    anchor = extract_md_meta(content, ['Âncora', 'Ancora'])

    # 1. Bloco Pré-Porta 30s
    pre_section = extract_section_body(content, r'(?:⚡\s*)?Pr[eé]-Porta(?:\s*30s)?')
    pre_block = re.search(r'```(?:text|markdown|md)?\s*\n(.*?)\n```', pre_section, re.DOTALL)
    pre_porta = pre_block.group(1).strip() if pre_block else pre_section.strip()

    # 2. Checklist Pós-Atendimento agrupado por ###
    chk_section = extract_section_body(content, r'(?:✅\s*)?Checklist(?:\s+P[oó]s-Atendimento)?')
    checklist_sections = []
    current_sec = None

    for raw_line in chk_section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        sec_match = re.match(r'^###\s+(.+)$', line)
        if sec_match:
            current_sec = {
                'title': sec_match.group(1).strip(),
                'items': []
            }
            checklist_sections.append(current_sec)
            continue

        item_match = re.match(r'^[-*]\s+\[\s*[xX ]?\s*\]\s+(.+)$', line)
        if item_match:
            if current_sec is None:
                current_sec = {'title': 'Checklist Geral', 'items': []}
                checklist_sections.append(current_sec)
            sec_idx = len(checklist_sections) - 1
            item_idx = len(current_sec['items'])
            current_sec['items'].append({
                'id': f'{sec_idx}-{item_idx}',
                'text': item_match.group(1).strip()
            })

    # Remove seções vazias por segurança
    checklist_sections = [s for s in checklist_sections if s['items']]
    checklist_total = sum(len(s['items']) for s in checklist_sections)

    # 3. Armadilhas & Erros Fatais
    pit_section = extract_section_body(content, r'(?:🚫\s*)?Armadilhas(?:\s*&\s*Erros(?:\s+Fatais)?)?')
    pitfalls = []
    for raw_line in pit_section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        bold_match = re.match(r'^(?:[-*]|\d+\.)\s+\*\*(.+?)\*\*\s*(.*)$', line)
        if bold_match:
            p_title = bold_match.group(1).strip().rstrip(':').strip()
            p_detail = bold_match.group(2).lstrip(':').strip()
            pitfalls.append({'title': p_title, 'detail': p_detail})
            continue
        plain_match = re.match(r'^(?:[-*]|\d+\.)\s+(.+)$', line)
        if plain_match:
            txt = plain_match.group(1).strip()
            if ':' in txt:
                p_title, p_detail = txt.split(':', 1)
                pitfalls.append({'title': p_title.strip(), 'detail': p_detail.strip()})
            else:
                pitfalls.append({'title': 'Erro Crítico', 'detail': txt})

    rel_path = os.path.relpath(file_path, BASE_PROJECT)

    return {
        'id': f'hab-{seq_num}',
        'mod_id': 'hab',
        'module_name': 'Habilidades Clínicas',
        'badge': '🧠 Habilidades',
        'title': title,
        'trigger': '',
        'all_triggers': [],
        'category': hab_category,
        'hab_category': hab_category,
        'time_goal': time_goal,
        'anchor': anchor,
        'pre_porta': pre_porta,
        'checklist_sections': checklist_sections,
        'checklist_total': checklist_total,
        'pitfalls': pitfalls,
        'pitfalls_raw': pit_section,
        'path': rel_path,
        'pep_body': '',
        'has_split': False,
        'evolucao_body': '',
        'conduta_body': '',
        'has_receita': False,
        'receita_body': '',
        'has_guia': False,
        'guia_body': ''
    }


# --- Processamento dos 90 Snippets PEP (Isolamento Estrito) ---
pep_snippets = []

for mod in modules:
    mod_files = [
        f for f in sorted(glob.glob(f"{mod['dir']}/**/*.md", recursive=True))
        if '_arquivados' not in f and not os.path.basename(f).startswith('.') and not os.path.basename(f).startswith('_')
    ]
    print(f"Processando {mod['name']}: {len(mod_files)} arquivos.")

    for f in mod_files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Título
        title_match = re.search(r'^#\s+(.+)$', content, re.M)
        title = title_match.group(1).replace('Protocolo de Atendimento:', '').replace('Protocolo:', '').strip() if title_match else os.path.basename(f)

        # Atalho
        trigger_match = re.search(r'\*\*Atalhos? (?:Recomendados?|sugeridos?):\*\*\s*`?([^`\n\r]+)`?', content, re.IGNORECASE)
        if trigger_match:
            raw_triggers = trigger_match.group(1).strip()
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
            'id': f"{mod['id']}-{len(pep_snippets)+1}",
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
        pep_snippets.append(item)

print(f"\nTotal de snippets PEP compilados: {len(pep_snippets)}")

# --- Processamento dos Cartões de Habilidades Clínicas (05_Habilidades_Clinicas) ---
hab_files = sorted(glob.glob(f"{HAB_DIR}/**/*.md", recursive=True)) if os.path.isdir(HAB_DIR) else []
hab_snippets = [parse_hab_card(f, i + 1) for i, f in enumerate(hab_files)]
print(f"Processando Habilidades Clínicas: {len(hab_snippets)} cartões.")

# 1. Salvar JSONs (PEP isolado; hab opcional separado)
for mod in modules:
    mod_snippets = [s for s in pep_snippets if s['mod_id'] == mod['id']]
    json_path = os.path.join(SNIPPETS_DIR, f"snippets_{mod['id']}.json")
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump(mod_snippets, fh, indent=2, ensure_ascii=False)

all_json_path = os.path.join(SNIPPETS_DIR, "snippets_todos.json")
with open(all_json_path, 'w', encoding='utf-8') as fh:
    json.dump(pep_snippets, fh, indent=2, ensure_ascii=False)

hab_json_path = os.path.join(SNIPPETS_DIR, "snippets_hab.json")
with open(hab_json_path, 'w', encoding='utf-8') as fh:
    json.dump(hab_snippets, fh, indent=2, ensure_ascii=False)

# 2. Salvar YAMLs do Espanso (APENAS os 90 snippets PEP; NUNCA incluir hab)
for mod in modules:
    mod_snippets = [s for s in pep_snippets if s['mod_id'] == mod['id']]
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
    fh.write(f"# Configuração Completa Espanso ({len(pep_snippets)} Modelos)\n\nmatches:\n")
    for s in pep_snippets:
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
cockpit_items = pep_snippets + hab_snippets
html_path = os.path.join(BASE_PROJECT, 'painel_rapido_snippets.html')

# Ícones SVG reutilizáveis nos cards (Minimalista)
SVG_COPY = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
SVG_CLOCK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>'
SVG_CHECK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>'
SVG_ZAP = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
SVG_ALERT = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'

cards_html = []
for idx, s in enumerate(cockpit_items):
    if s['mod_id'] == 'hab':
        checklist_items_text = ' '.join(
            it['text']
            for sec in s['checklist_sections']
            for it in sec['items']
        )
        pitfalls_text = ' '.join(
            f"{p['title']} {p['detail']}" for p in s['pitfalls']
        )
        search_keywords = (
            f"{s['title']} {s['category']} {s['module_name']} {s['anchor']} "
            f"{s['time_goal']} {s['pre_porta']} {checklist_items_text} {pitfalls_text} {s['path']}"
        ).lower()
        anchor_html = (
            f'<p class="hab-card-anchor" title="Sequência-chave">{html.escape(s["anchor"])}</p>'
            if s['anchor'] else ''
        )
        time_chip_html = (
            f'<span class="meta-time" title="Meta de tempo">{SVG_CLOCK}<span>{html.escape(s["time_goal"])}</span></span>'
            if s['time_goal'] else ''
        )
        pit_count = len(s['pitfalls'])
        pit_label = f'Erros ({pit_count})' if pit_count else 'Erros'
        cards_html.append(f"""
    <article class="card card-hab" data-mod="hab" data-idx="{idx}" data-cat="{html.escape(s['category'])}" data-search="{html.escape(search_keywords)}" style="display:none;" onclick="openInspector({idx})">
      <div class="card-head">
        <div class="card-meta">
          <span class="mod-dot mod-dot-hab"></span>
          <span class="meta-label">{html.escape(s['category'])}</span>
        </div>
        {time_chip_html}
      </div>

      <div class="card-body-block">
        <h3 class="card-title">{html.escape(s['title'])}</h3>
        {anchor_html}
      </div>

      <div class="card-footer">
        <div class="btn-group">
          <button class="btn btn-hab-pre" onclick="event.stopPropagation(); openInspector({idx}, 'preporta')" title="Abrir roteiro Pré-Porta 30s">
            {SVG_ZAP}
            <span>Pré-Porta</span>
          </button>
          <button class="btn btn-hab-chk" data-hab-chk-btn="{idx}" onclick="event.stopPropagation(); openInspector({idx}, 'checklist')" title="Abrir Checklist Pós-Atendimento">
            {SVG_CHECK}
            <span class="chk-btn-label">Checklist · {s['checklist_total']}</span>
          </button>
        </div>
        <button class="btn btn-detail btn-hab-err" onclick="event.stopPropagation(); openInspector({idx}, 'armadilhas')" title="Ver Armadilhas &amp; Erros Fatais">
          {SVG_ALERT}
          <span>{pit_label}</span>
        </button>
      </div>
    </article>
        """)
        continue

    # Botões segmentados (PEP)
    segment_buttons = [f"""
      <button class="btn btn-primary" onclick='event.stopPropagation(); copySnippet({idx})' title="Copiar evolução e conduta completas">
        {SVG_COPY}
        <span>Copiar Tudo</span>
      </button>
    """]

    if s['has_split'] and s['conduta_body']:
        segment_buttons.append(f"""
          <button class="btn btn-subtle" onclick='event.stopPropagation(); copyConduta({idx})' title="Copiar apenas a conduta / prescrição imediata">
            Conduta
          </button>
        """)

    if s['has_receita']:
        segment_buttons.append(f"""
          <button class="btn btn-subtle" onclick='event.stopPropagation(); copyReceita({idx})' title="Copiar apenas a receita estruturada">
            Receita
          </button>
        """)

    mod_label_clean = re.sub(r'^[^\wÀ-ÿ]+\s*', '', s['badge']).strip() or s['module_name']
    meta_badges = []
    if s['has_split']:
        meta_badges.append('<span class="meta-flag" title="Permite cópia separada de Anamnese e Conduta">Bipartido</span>')
    if s['has_guia']:
        meta_badges.append('<span class="meta-flag" title="Contém diretrizes e conduta clínica">Diretriz</span>')
    meta_flags_html = ('<span class="meta-sep">·</span>' + '<span class="meta-sep">·</span>'.join(meta_badges)) if meta_badges else ''

    search_keywords = f"{s['title'].lower()} {' '.join(s['all_triggers']).lower()} {s['category'].lower()} {s['module_name'].lower()} {s['path'].lower()}"
    preview_lines = []
    for raw_ln in s['pep_body'].splitlines():
        ln = raw_ln.strip()
        if not ln or re.match(r'^[=\-#_*]{3,}$', ln):
            continue
        ln = re.sub(r'^#+\s*', '', ln).rstrip('#').strip()
        if ln and ln.upper() == s['title'].upper():
            continue
        if ln:
            preview_lines.append(ln)
        if len(preview_lines) >= 3:
            break
    clean_preview = '\n'.join(preview_lines) if preview_lines else re.sub(r'\n{2,}', '\n', s['pep_body']).strip()
    preview_text = html.escape(clean_preview[:240]) + ("..." if len(clean_preview) > 240 else "")

    cards_html.append(f"""
    <article class="card card-{s['mod_id']}" data-mod="{s['mod_id']}" data-idx="{idx}" data-cat="{html.escape(s['category'])}" data-search="{html.escape(search_keywords)}" onclick="openInspector({idx})">
      <div class="card-head">
        <div class="card-meta">
          <span class="mod-dot mod-dot-{s['mod_id']}"></span>
          <span class="meta-mod">{html.escape(mod_label_clean)}</span>
          <span class="meta-sep">·</span>
          <span class="meta-label">{html.escape(s['category'])}</span>
          {meta_flags_html}
        </div>
      </div>

      <div class="card-body-block">
        <h3 class="card-title">{html.escape(s['title'])}</h3>
        <p class="card-preview-text">{preview_text}</p>
      </div>

      <div class="card-footer">
        <div class="btn-group">
          {''.join(segment_buttons)}
        </div>
        <button class="btn btn-detail" onclick="event.stopPropagation(); openInspector({idx})" title="Visualizar e personalizar">
          Abrir
        </button>
      </div>
    </article>
    """)

cards_joined = '\n'.join(cards_html)
snippets_json_payload = json.dumps(cockpit_items, ensure_ascii=False).replace('</', '<\\/')

count_pep = len(pep_snippets)
count_go = len([s for s in pep_snippets if s['mod_id'] == 'go'])
count_upa = len([s for s in pep_snippets if s['mod_id'] == 'upa'])
count_enf = len([s for s in pep_snippets if s['mod_id'] == 'enf'])
count_ped = len([s for s in pep_snippets if s['mod_id'] == 'ped'])
count_hab = len(hab_snippets)

html_template = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cockpit Clínico — PEP & Habilidades</title>
  <style>
    :root {
      --bg: #0b0d11;
      --surface: #12151c;
      --surface-hover: #171b24;
      --surface-inset: #0e1117;
      --border: rgba(255, 255, 255, 0.075);
      --border-strong: rgba(255, 255, 255, 0.15);
      --text: #eceff4;
      --text-secondary: #9aa4b2;
      --text-dim: #636d7e;

      --primary: #38bdf8;
      --primary-solid: #0284c7;
      --primary-hover: #0369a1;
      --success: #34d399;
      --warning: #fbbf24;
      --danger: #f87171;

      --mod-go: #f472b6;
      --mod-upa: #38bdf8;
      --mod-enf: #34d399;
      --mod-ped: #fbbf24;
      --mod-hab: #a78bfa;
      --hab-solid: #7c3aed;

      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      --font-mono: "JetBrains Mono", "SF Mono", Menlo, Monaco, Consolas, monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 12px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { color-scheme: dark; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 14px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      line-height: 1.5;
    }
    button, input {
      font-family: inherit;
    }

    /* Topbar Minimalista */
    .topbar {
      position: sticky;
      top: 0;
      z-index: 40;
      background: rgba(11, 13, 17, 0.86);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
    }
    .topbar-content {
      max-width: 1480px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--surface);
      border: 1px solid var(--border-strong);
      color: var(--text);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .brand-text h1 {
      font-size: 0.98rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--text);
      line-height: 1.25;
    }
    .brand-text p {
      font-size: 0.72rem;
      color: var(--text-dim);
      line-height: 1.3;
    }

    /* Ferramentas do Topo */
    .top-tools {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .weight-widget {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 3px 4px 3px 10px;
      height: 34px;
    }
    .weight-label {
      font-size: 0.76rem;
      font-weight: 500;
      color: var(--text-secondary);
    }
    .weight-input {
      width: 46px;
      background: transparent;
      border: none;
      border-bottom: 1px solid var(--border-strong);
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 0.84rem;
      font-weight: 600;
      padding: 1px 2px;
      text-align: center;
      outline: none;
      font-variant-numeric: tabular-nums;
      -moz-appearance: textfield;
    }
    .weight-input::-webkit-outer-spin-button,
    .weight-input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    .weight-input:focus {
      border-bottom-color: var(--primary);
    }
    .weight-unit {
      font-size: 0.74rem;
      color: var(--text-dim);
      padding-right: 4px;
    }
    .btn-doses {
      -webkit-appearance: none;
      appearance: none;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid transparent;
      color: var(--text-secondary);
      font-size: 0.74rem;
      font-weight: 500;
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease;
    }
    .btn-doses:hover {
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }

    .btn-palette-trigger {
      -webkit-appearance: none;
      appearance: none;
      height: 34px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      font-size: 0.76rem;
      font-weight: 500;
      padding: 0 10px;
      border-radius: 8px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
    }
    .btn-palette-trigger:hover {
      background: var(--surface-hover);
      border-color: var(--border-strong);
      color: var(--text);
    }
    .kbd-shortcut {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 1px 5px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-family: var(--font-mono);
      color: var(--text-dim);
    }

    .counter-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 0 6px;
      font-size: 0.76rem;
      font-weight: 500;
      color: var(--text-secondary);
      font-variant-numeric: tabular-nums;
    }
    .counter-pill .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
      flex-shrink: 0;
    }
    .counter-pill.is-hab .dot {
      background: var(--mod-hab);
    }

    /* Container Principal */
    .app-container {
      max-width: 1480px;
      margin: 0 auto;
      padding: 20px 24px 48px;
      width: 100%;
      flex: 1;
    }

    /* Barra de Navegação & Filtros */
    .controls-panel {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 24px;
    }

    .nav-tabs {
      display: flex;
      gap: 4px;
      overflow-x: auto;
      border-bottom: 1px solid var(--border);
      scrollbar-width: none;
    }
    .nav-tabs::-webkit-scrollbar { display: none; }

    .tab-btn {
      -webkit-appearance: none;
      appearance: none;
      background-color: transparent;
      border: none;
      border-bottom: 2px solid transparent;
      color: var(--text-secondary);
      padding: 10px 14px;
      margin-bottom: -1px;
      cursor: pointer;
      font-size: 0.84rem;
      font-weight: 500;
      letter-spacing: -0.01em;
      transition: color 0.15s ease, border-color 0.15s ease;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: none;
      outline: none;
    }
    .tab-btn:hover {
      color: var(--text);
    }
    .tab-btn:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.25);
      outline-offset: -2px;
      border-radius: 6px 6px 0 0;
    }
    .tab-btn.active {
      color: var(--text);
      font-weight: 600;
      border-bottom-color: var(--text);
    }
    .tab-btn.active.tab-go { border-bottom-color: var(--mod-go); }
    .tab-btn.active.tab-upa { border-bottom-color: var(--mod-upa); }
    .tab-btn.active.tab-enf { border-bottom-color: var(--mod-enf); }
    .tab-btn.active.tab-ped { border-bottom-color: var(--mod-ped); }
    .tab-btn.active.tab-hab { border-bottom-color: var(--mod-hab); }

    .tab-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      flex-shrink: 0;
      opacity: 0.75;
    }
    .tab-btn.active .tab-dot { opacity: 1; }
    .dot-all { background: var(--text-secondary); }
    .dot-go { background: var(--mod-go); }
    .dot-upa { background: var(--mod-upa); }
    .dot-enf { background: var(--mod-enf); }
    .dot-ped { background: var(--mod-ped); }
    .dot-hab { background: var(--mod-hab); }

    .tab-count {
      font-size: 0.72rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
      font-variant-numeric: tabular-nums;
      font-weight: 500;
    }
    .tab-btn.active .tab-count {
      color: var(--text-secondary);
    }

    /* Busca & Subcategorias */
    .search-row {
      display: flex;
      gap: 12px;
      align-items: center;
      position: relative;
    }
    .search-wrapper {
      position: relative;
      flex: 1;
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }
    .search-input {
      width: 100%;
      height: 42px;
      padding: 0 72px 0 40px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.15s ease, background 0.15s ease;
    }
    .search-input::placeholder {
      color: var(--text-dim);
    }
    .search-input:focus {
      border-color: var(--border-strong);
      background: var(--surface-hover);
    }
    .search-shortcut-hint {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.03);
      font-family: var(--font-mono);
      pointer-events: none;
    }

    .subcat-chips {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .subcat-chip {
      -webkit-appearance: none;
      appearance: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-secondary);
      padding: 3px 10px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 0.73rem;
      font-weight: 500;
      line-height: 1.45;
      transition: all 0.15s ease;
    }
    .subcat-chip:hover {
      border-color: var(--border-strong);
      color: var(--text);
      background: rgba(255, 255, 255, 0.03);
    }
    .subcat-chip.active {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.22);
      color: #ffffff;
    }

    /* Grid de Cards */
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 14px;
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      transition: border-color 0.15s ease, background 0.15s ease;
      cursor: pointer;
    }
    .card:hover {
      border-color: var(--border-strong);
      background: var(--surface-hover);
    }

    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }
    .card-meta {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      font-size: 0.74rem;
      color: var(--text-secondary);
      line-height: 1.35;
      min-width: 0;
    }
    .mod-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .mod-dot-go { background: var(--mod-go); }
    .mod-dot-upa { background: var(--mod-upa); }
    .mod-dot-enf { background: var(--mod-enf); }
    .mod-dot-ped { background: var(--mod-ped); }
    .mod-dot-hab { background: var(--mod-hab); }

    .meta-mod {
      font-weight: 600;
      color: var(--text-secondary);
    }
    .meta-label {
      color: var(--text-secondary);
    }
    .meta-sep {
      color: var(--text-dim);
    }
    .meta-flag {
      color: var(--text-dim);
      font-size: 0.71rem;
    }

    .meta-time {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.72rem;
      color: var(--text-dim);
      font-variant-numeric: tabular-nums;
      text-align: right;
      line-height: 1.3;
      flex-shrink: 0;
      max-width: 170px;
    }
    .meta-time svg {
      flex-shrink: 0;
      opacity: 0.75;
    }

    .triggers-wrap {
      display: flex;
      gap: 4px;
      justify-content: flex-end;
      flex-shrink: 0;
    }
    .trigger-chip {
      -webkit-appearance: none;
      appearance: none;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      transition: border-color 0.15s ease, color 0.15s ease;
    }
    .trigger-chip:hover {
      border-color: var(--border-strong);
      color: var(--text);
    }
    .trig-more {
      color: var(--text-dim);
      font-size: 0.66rem;
    }

    .card-body-block {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .card-title {
      font-size: 0.98rem;
      font-weight: 600;
      letter-spacing: -0.015em;
      color: var(--text);
      line-height: 1.38;
    }
    .hab-card-anchor {
      padding-left: 10px;
      border-left: 2px solid rgba(167, 139, 250, 0.48);
      font-size: 0.81rem;
      color: var(--text-secondary);
      line-height: 1.48;
    }
    .card-preview-text {
      font-size: 0.79rem;
      color: var(--text-dim);
      line-height: 1.48;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      white-space: pre-line;
    }

    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      gap: 8px;
    }
    .btn-group {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    /* Botões Minimalistas */
    .btn {
      -webkit-appearance: none;
      appearance: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid transparent;
      padding: 5px 10px;
      border-radius: 7px;
      cursor: pointer;
      font-size: 0.76rem;
      font-weight: 500;
      line-height: 1.3;
      transition: all 0.15s ease;
    }
    .btn-primary {
      background: rgba(56, 189, 248, 0.12);
      color: #7dd3fc;
      border-color: rgba(56, 189, 248, 0.24);
    }
    .btn-primary:hover {
      background: rgba(56, 189, 248, 0.2);
      color: #e0f2fe;
    }
    .btn-subtle {
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-secondary);
      border-color: var(--border);
    }
    .btn-subtle:hover {
      background: rgba(255, 255, 255, 0.07);
      border-color: var(--border-strong);
      color: var(--text);
    }

    .btn-hab-pre {
      background: rgba(167, 139, 250, 0.14);
      color: #ddd6fe;
      border-color: rgba(167, 139, 250, 0.26);
    }
    .btn-hab-pre:hover {
      background: rgba(167, 139, 250, 0.24);
      color: #ffffff;
    }
    .btn-hab-chk {
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-secondary);
      border-color: var(--border);
      font-variant-numeric: tabular-nums;
    }
    .btn-hab-chk:hover {
      background: rgba(255, 255, 255, 0.07);
      border-color: var(--border-strong);
      color: var(--text);
    }
    .btn-hab-chk.complete {
      background: rgba(52, 211, 153, 0.12);
      color: #6ee7b7;
      border-color: rgba(52, 211, 153, 0.28);
    }

    .btn-detail {
      background: transparent;
      color: var(--text-dim);
      padding: 5px 8px;
    }
    .btn-detail:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.04);
    }
    .btn-hab-err:hover {
      color: #fca5a5;
      background: rgba(248, 113, 113, 0.08);
    }

    /* Drawer / Modal Inspector */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      z-index: 90;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }
    .drawer-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .drawer {
      position: fixed;
      top: 0;
      right: 0;
      bottom: 0;
      width: min(820px, 95vw);
      background: #10131a;
      border-left: 1px solid var(--border);
      z-index: 100;
      transform: translateX(100%);
      transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      box-shadow: -12px 0 36px rgba(0, 0, 0, 0.55);
    }
    .drawer-overlay.open .drawer {
      transform: translateX(0);
    }

    .drawer-header {
      padding: 18px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 14px;
      background: var(--bg);
    }
    .drawer-header h2 {
      font-size: 1.08rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--text);
      line-height: 1.35;
    }
    .drawer-header p {
      font-size: 0.72rem;
      color: var(--text-dim);
      margin-top: 3px;
      font-family: var(--font-mono);
    }
    .close-btn {
      -webkit-appearance: none;
      appearance: none;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }
    .close-btn:hover {
      background: rgba(255, 255, 255, 0.09);
      color: var(--text);
    }

    .drawer-tabs {
      display: flex;
      border-bottom: 1px solid var(--border);
      background: var(--bg);
      padding: 0 24px;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .drawer-tabs::-webkit-scrollbar { display: none; }
    .drawer-tab {
      -webkit-appearance: none;
      appearance: none;
      padding: 10px 10px;
      margin-bottom: -1px;
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-secondary);
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      background: transparent;
      white-space: nowrap;
      transition: color 0.15s ease, border-color 0.15s ease;
    }
    .drawer-tab:hover {
      color: var(--text);
    }
    .drawer-tab.active {
      color: var(--primary);
      font-weight: 600;
      border-bottom-color: var(--primary);
    }
    .drawer.drawer-hab .drawer-tab.active {
      color: var(--mod-hab);
      border-bottom-color: var(--mod-hab);
    }

    .drawer-body {
      flex: 1;
      overflow-y: auto;
      padding: 22px 24px;
    }
    .drawer-code-block {
      background: var(--surface-inset);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.81rem;
      line-height: 1.6;
      color: #cbd5e1;
      white-space: pre-wrap;
      word-break: break-word;
      user-select: text;
    }

    /* Painel Dedicado: Habilidades Clínicas */
    .hab-panel {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .hab-meta-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }
    .hab-meta-chip {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .hab-meta-label {
      font-size: 0.69rem;
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .hab-meta-val {
      font-size: 0.9rem;
      color: var(--text);
      font-weight: 600;
    }
    .hab-meta-time .hab-meta-val {
      color: #ddd6fe;
    }

    .hab-anchor-box {
      background: rgba(167, 139, 250, 0.06);
      border-left: 3px solid var(--mod-hab);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      padding: 12px 16px;
    }
    .hab-anchor-label {
      font-size: 0.69rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--mod-hab);
      margin-bottom: 4px;
    }
    .hab-anchor-text {
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text);
      line-height: 1.5;
    }

    .hab-steps-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .hab-pre-group-title {
      margin-top: 10px;
      padding: 4px 0 4px 10px;
      font-size: 0.74rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--mod-hab);
      border-left: 2px solid var(--mod-hab);
    }
    .hab-pre-step {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 11px 14px;
      font-size: 0.88rem;
      line-height: 1.55;
      color: var(--text);
    }
    .hab-pre-substep {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 9px 12px;
      margin-left: 16px;
      font-size: 0.84rem;
      line-height: 1.5;
      color: var(--text-secondary);
    }
    .hab-step-lead {
      color: #ddd6fe;
      font-weight: 600;
      margin-right: 4px;
    }
    .hab-pre-line {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.87rem;
      line-height: 1.55;
      color: var(--text-secondary);
    }

    /* Checklist Pós-Atendimento */
    .hab-progress-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .hab-progress-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }
    .hab-progress-title {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      font-weight: 600;
    }
    .hab-progress-count {
      font-size: 0.96rem;
      font-weight: 600;
      color: var(--text);
      font-variant-numeric: tabular-nums;
    }
    .hab-progress-pct {
      font-family: var(--font-mono);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--mod-hab);
      font-variant-numeric: tabular-nums;
    }
    .hab-progress-pct.done {
      color: var(--success);
    }
    .hab-progress-track {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 999px;
      overflow: hidden;
    }
    .hab-progress-fill {
      height: 100%;
      width: 0%;
      background: var(--mod-hab);
      border-radius: 999px;
      transition: width 0.22s ease, background 0.22s ease;
    }
    .hab-progress-fill.done {
      background: var(--success);
    }

    .hab-checklist-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .btn-hab-debrief {
      background: rgba(167, 139, 250, 0.16);
      color: #ede9fe;
      border-color: rgba(167, 139, 250, 0.3);
      padding: 8px 14px;
      font-size: 0.81rem;
    }
    .btn-hab-debrief:hover {
      background: rgba(167, 139, 250, 0.26);
      color: #ffffff;
    }
    .btn-hab-reset {
      background: transparent;
      color: var(--text-secondary);
      border: 1px solid var(--border);
      padding: 8px 14px;
      font-size: 0.81rem;
    }
    .btn-hab-reset:hover {
      background: rgba(255, 255, 255, 0.05);
      border-color: var(--border-strong);
      color: var(--text);
    }

    .hab-blindspots-panel {
      border-radius: var(--radius-md);
      padding: 13px 15px;
      border: 1px solid rgba(251, 191, 36, 0.22);
      background: rgba(251, 191, 36, 0.05);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .hab-blindspots-panel.all-done {
      border-color: rgba(52, 211, 153, 0.28);
      background: rgba(52, 211, 153, 0.07);
    }
    .hab-blindspots-header {
      font-size: 0.82rem;
      font-weight: 600;
      color: #fcd34d;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .hab-blindspots-panel.all-done .hab-blindspots-header {
      color: #6ee7b7;
    }
    .hab-blindspots-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
      max-height: 180px;
      overflow-y: auto;
    }
    .hab-blindspot-item {
      font-size: 0.8rem;
      color: #fef3c7;
      line-height: 1.45;
      padding: 4px 8px;
      border-radius: 5px;
      background: rgba(0, 0, 0, 0.18);
    }
    .hab-blindspot-sec {
      font-size: 0.71rem;
      color: var(--warning);
      font-weight: 600;
      margin-right: 4px;
    }

    .hab-sections-wrap {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .hab-sec-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .hab-sec-title {
      font-size: 0.82rem;
      font-weight: 600;
      color: #ddd6fe;
      padding-bottom: 8px;
      margin-bottom: 2px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .hab-sec-progress {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-dim);
      font-variant-numeric: tabular-nums;
    }
    .hab-check-item {
      display: flex;
      align-items: flex-start;
      gap: 11px;
      padding: 9px 10px;
      border-radius: 7px;
      border: 1px solid transparent;
      background: transparent;
      cursor: pointer;
      transition: background 0.14s ease, border-color 0.14s ease;
      user-select: none;
      min-height: 40px;
    }
    .hab-check-item:hover {
      background: rgba(255, 255, 255, 0.03);
    }
    .hab-check-item.checked {
      background: rgba(52, 211, 153, 0.07);
      border-color: rgba(52, 211, 153, 0.18);
    }
    .hab-check-item input[type="checkbox"] {
      width: 17px;
      height: 17px;
      margin-top: 2px;
      accent-color: #10b981;
      cursor: pointer;
      flex-shrink: 0;
    }
    .hab-check-text {
      font-size: 0.85rem;
      line-height: 1.48;
      color: var(--text);
    }
    .hab-check-item.checked .hab-check-text {
      color: #a7f3d0;
    }

    /* Armadilhas & Erros Fatais */
    .hab-pitfalls-lead {
      font-size: 0.82rem;
      color: #fecaca;
      background: rgba(248, 113, 113, 0.07);
      border: 1px solid rgba(248, 113, 113, 0.2);
      border-radius: 8px;
      padding: 10px 14px;
    }
    .hab-pitfalls-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .hab-pitfall-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--danger);
      border-radius: 8px;
      padding: 12px 15px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .hab-pitfall-title {
      font-size: 0.88rem;
      font-weight: 600;
      color: #fca5a5;
    }
    .hab-pitfall-detail {
      font-size: 0.83rem;
      color: var(--text-secondary);
      line-height: 1.52;
    }

    /* Personalizador Interativo */
    .interactive-panel {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .interactive-lead {
      font-size: 0.8rem;
      color: var(--text-secondary);
      background: rgba(56, 189, 248, 0.06);
      border: 1px solid rgba(56, 189, 248, 0.16);
      padding: 9px 12px;
      border-radius: 7px;
    }
    .interactive-rendered {
      background: var(--surface-inset);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.81rem;
      line-height: 1.6;
      color: var(--text);
      white-space: pre-wrap;
      word-break: break-word;
    }
    .choice-group {
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
      max-width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 2px 4px;
      margin: 2px 3px;
      vertical-align: baseline;
      gap: 3px;
    }
    .choice-group.is-multi {
      border-color: rgba(14, 165, 233, 0.4);
      background: rgba(14, 165, 233, 0.05);
    }
    .choice-pill {
      -webkit-appearance: none;
      appearance: none;
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-secondary);
      font-family: var(--font-sans);
      font-size: 0.73rem;
      font-weight: 500;
      padding: 2px 7px;
      border-radius: 4px;
      cursor: pointer;
      text-align: left;
      transition: all 0.12s ease;
      user-select: none;
    }
    .choice-pill:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.06);
    }
    .choice-pill.active {
      background: var(--primary-solid);
      border-color: var(--primary-solid);
      color: #ffffff;
      font-weight: 600;
    }
    .choice-group.is-multi .choice-pill.active {
      background: #0284c7;
      border-color: #38bdf8;
    }
    .choice-group.is-multi .choice-pill.active::before {
      content: "✓ ";
      font-size: 0.70rem;
      font-weight: 700;
      opacity: 0.95;
    }
    .choice-mode-btn {
      -webkit-appearance: none;
      appearance: none;
      background: rgba(255, 255, 255, 0.04);
      border: 1px dashed var(--border);
      color: var(--text-dim);
      font-family: var(--font-sans);
      font-size: 0.65rem;
      font-weight: 600;
      padding: 1px 5px;
      border-radius: 4px;
      cursor: pointer;
      margin-left: 2px;
      transition: all 0.15s ease;
      user-select: none;
    }
    .choice-mode-btn:hover {
      border-color: var(--border-strong);
      color: var(--text);
      background: rgba(255, 255, 255, 0.08);
    }
    .choice-group.is-multi .choice-mode-btn {
      border-color: #0284c7;
      color: #38bdf8;
      background: rgba(14, 165, 233, 0.12);
      font-weight: 700;
    }

    .drawer-footer {
      padding: 14px 24px;
      border-top: 1px solid var(--border);
      background: var(--bg);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .drawer-hab-meta-footer {
      font-size: 0.76rem;
      color: var(--text-secondary);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Modal Command Palette (Ctrl+K) */
    .cmd-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.72);
      backdrop-filter: blur(6px);
      z-index: 150;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 12vh;
    }
    .cmd-overlay.open {
      display: flex;
    }
    .cmd-modal {
      width: min(640px, 92vw);
      background: var(--surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-lg);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      animation: cmdPop 0.14s ease-out;
    }
    @keyframes cmdPop {
      from { transform: scale(0.97); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .cmd-search-box {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      background: var(--bg);
    }
    .cmd-search-input {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text);
      font-size: 0.96rem;
      outline: none;
    }
    .cmd-results {
      max-height: 380px;
      overflow-y: auto;
      padding: 8px;
    }
    .cmd-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 9px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.12s ease;
    }
    .cmd-item:hover, .cmd-item.active {
      background: rgba(255, 255, 255, 0.06);
    }
    .cmd-item-left {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }
    .cmd-item-title {
      font-size: 0.88rem;
      font-weight: 500;
      color: var(--text);
    }
    .cmd-item-cat {
      font-size: 0.72rem;
      color: var(--text-dim);
    }
    .cmd-item-trig {
      font-family: var(--font-mono);
      font-size: 0.73rem;
      color: var(--text-secondary);
      background: rgba(255, 255, 255, 0.04);
      padding: 2px 7px;
      border-radius: 5px;
      border: 1px solid var(--border);
      white-space: nowrap;
      flex-shrink: 0;
    }
    .cmd-item-hab-trig {
      font-family: var(--font-sans);
      color: #ddd6fe;
      background: rgba(167, 139, 250, 0.14);
      border-color: rgba(167, 139, 250, 0.28);
      font-weight: 500;
    }
    .cmd-footer {
      padding: 9px 16px;
      background: var(--bg);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: 0.71rem;
      color: var(--text-dim);
    }

    /* Modal Calculadora de Doses Rápidas */
    .doses-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.72);
      backdrop-filter: blur(4px);
      z-index: 140;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .doses-overlay.open {
      display: flex;
    }
    .doses-modal {
      width: min(680px, 94vw);
      max-height: 84vh;
      background: var(--surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
      overflow: hidden;
    }
    .doses-header {
      padding: 16px 20px;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .doses-body {
      padding: 18px 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .dose-card {
      background: var(--surface-inset);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }
    .dose-name {
      font-size: 0.84rem;
      font-weight: 600;
      color: var(--text);
    }
    .dose-rule {
      font-size: 0.73rem;
      color: var(--text-dim);
      margin-top: 2px;
    }
    .dose-calc {
      font-family: var(--font-mono);
      font-size: 0.86rem;
      font-weight: 600;
      color: var(--primary);
      text-align: right;
    }
    .dose-copy-btn {
      -webkit-appearance: none;
      appearance: none;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      font-size: 0.72rem;
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
    }
    .dose-copy-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 200;
      background: #1e293b;
      border: 1px solid var(--border-strong);
      color: #f8fafc;
      padding: 10px 16px;
      border-radius: 9px;
      font-size: 0.82rem;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
      transform: translateY(80px);
      opacity: 0;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    /* Responsivo Mobile */
    @media (max-width: 640px) {
      .topbar { padding: 10px 16px; }
      .topbar-content { gap: 10px; }
      .brand-text p, .counter-pill, .btn-palette-trigger .kbd-shortcut { display: none; }
      .app-container { padding: 14px 16px 40px; }
      .controls-panel { gap: 10px; margin-bottom: 18px; }
      .subcat-chips {
        flex-wrap: nowrap;
        overflow-x: auto;
        scrollbar-width: none;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 2px;
      }
      .subcat-chips::-webkit-scrollbar { display: none; }
      .subcat-chip { flex-shrink: 0; }
      .grid-cards { grid-template-columns: 1fr; gap: 12px; }
      .card { padding: 16px; }
      .drawer { width: 100vw; }
      .drawer-header, .drawer-tabs, .drawer-body, .drawer-footer { padding-left: 16px; padding-right: 16px; }
      .search-shortcut-hint { display: none; }
      .hab-checklist-actions { flex-direction: column; }
      .hab-checklist-actions .btn { width: 100%; justify-content: center; }
    }
  </style>
</head>
<body>

  <!-- Topbar -->
  <header class="topbar">
    <div class="topbar-content">
      <div class="brand">
        <div class="brand-icon" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
        </div>
        <div class="brand-text">
          <h1>Cockpit Clínico</h1>
          <p>PEP &amp; Habilidades • 100% Offline</p>
        </div>
      </div>

      <div class="top-tools">
        <div class="weight-widget" title="Ajuste o peso do paciente para calcular doses em tempo real">
          <span class="weight-label">Peso</span>
          <input type="number" id="quickWeightInput" class="weight-input" value="70" min="1" max="250" aria-label="Peso do paciente em kg">
          <span class="weight-unit">kg</span>
          <button class="btn-doses" onclick="openDosesModal()">Doses ▾</button>
        </div>

        <button class="btn-palette-trigger" onclick="openCmdPalette()" title="Atalho Ctrl+K">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <span>Buscar</span>
          <span class="kbd-shortcut">Ctrl+K</span>
        </button>

        <div class="counter-pill" id="counterPill">
          <span class="dot"></span>
          <span id="counterText">__TOTAL_PEP__ Protocolos</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Container -->
  <main class="app-container">

    <div class="controls-panel">
      <!-- Abas de Especialidades -->
      <nav class="nav-tabs" id="moduleTabs" aria-label="Especialidades">
        <button class="tab-btn active" data-mod="all">
          <span class="tab-dot dot-all"></span>
          <span>Geral</span>
          <span class="tab-count">__TOTAL_PEP__</span>
        </button>
        <button class="tab-btn tab-go" data-mod="go">
          <span class="tab-dot dot-go"></span>
          <span>GO</span>
          <span class="tab-count">__COUNT_GO__</span>
        </button>
        <button class="tab-btn tab-upa" data-mod="upa">
          <span class="tab-dot dot-upa"></span>
          <span>UPA Adulto</span>
          <span class="tab-count">__COUNT_UPA__</span>
        </button>
        <button class="tab-btn tab-enf" data-mod="enf">
          <span class="tab-dot dot-enf"></span>
          <span>Enfermaria</span>
          <span class="tab-count">__COUNT_ENF__</span>
        </button>
        <button class="tab-btn tab-ped" data-mod="ped">
          <span class="tab-dot dot-ped"></span>
          <span>Pediatria</span>
          <span class="tab-count">__COUNT_PED__</span>
        </button>
        <button class="tab-btn tab-hab" data-mod="hab">
          <span class="tab-dot dot-hab"></span>
          <span>Habilidades</span>
          <span class="tab-count">__COUNT_HAB__</span>
        </button>
      </nav>

      <!-- Busca e Filtros -->
      <div class="search-row">
        <div class="search-wrapper">
          <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Buscar por queixa, diagnóstico, atalho (ex: ;sepse, ;tpp, ;sca) ou droga..." autofocus>
          <span class="search-shortcut-hint">/</span>
        </div>
      </div>

      <!-- Subcategorias -->
      <div class="subcat-chips" id="subcatContainer">
        <button class="subcat-chip active" data-cat="all">Todas as Áreas</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <section class="grid-cards" id="cardsGrid">
      __CARDS_HTML__
    </section>
  </main>

  <!-- Drawer Modal Inspector -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="closeInspector()">
    <div class="drawer" id="drawerPanel" onclick="event.stopPropagation()">
      <div class="drawer-header">
        <div>
          <h2 id="drawerTitle">Título do Protocolo</h2>
          <p id="drawerPath">caminho/do/arquivo.md</p>
        </div>
        <button class="close-btn" onclick="closeInspector()" title="Fechar (Esc)" aria-label="Fechar">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <div class="drawer-tabs">
        <!-- Abas PEP -->
        <button class="drawer-tab active" id="tabPepBtn" onclick="switchDrawerTab('pep')">Snippet Completo</button>
        <button class="drawer-tab" id="tabInteractiveBtn" onclick="switchDrawerTab('interactive')">Personalizar</button>
        <button class="drawer-tab" id="tabCondutaBtn" onclick="switchDrawerTab('conduta')">Conduta</button>
        <button class="drawer-tab" id="tabRecBtn" onclick="switchDrawerTab('receita')">Receita</button>
        <button class="drawer-tab" id="tabGuiaBtn" onclick="switchDrawerTab('guia')">Diretrizes</button>

        <!-- Abas Dedicadas: Habilidades Clínicas -->
        <button class="drawer-tab" id="tabHabPreBtn" style="display:none;" onclick="switchDrawerTab('preporta')">Pré-Porta 30s</button>
        <button class="drawer-tab" id="tabHabChecklistBtn" style="display:none;" onclick="switchDrawerTab('checklist')">Checklist</button>
        <button class="drawer-tab" id="tabHabPitfallsBtn" style="display:none;" onclick="switchDrawerTab('armadilhas')">Armadilhas &amp; Erros</button>
      </div>

      <div class="drawer-body">
        <!-- Conteúdo PEP -->
        <div class="drawer-code-block" id="drawerContent"></div>
        <div class="interactive-panel" id="drawerInteractivePanel" style="display:none;">
          <div class="interactive-lead">
            Clique nas opções para personalizar. No modo <strong>☑️ Várias</strong> (comorbidades, sintomas, exames ou condutas combinadas), você pode selecionar mais de uma opção. Clique em <strong>🔘 1</strong> / <strong>☑️ Várias</strong> no chip para alternar o modo ou clique em uma opção ativa para desmarcá-la.
          </div>
          <div class="interactive-rendered" id="interactiveRendered"></div>
        </div>

        <!-- Conteúdo Habilidades Clínicas: Aba 1 (Pré-Porta 30s) -->
        <div class="hab-panel" id="habPrePanel" style="display:none;">
          <div class="hab-meta-grid">
            <div class="hab-meta-chip hab-meta-time">
              <span class="hab-meta-label">Meta de Tempo</span>
              <strong class="hab-meta-val" id="habTimeGoal"></strong>
            </div>
            <div class="hab-meta-chip">
              <span class="hab-meta-label">Área</span>
              <strong class="hab-meta-val" id="habCategoryBadge"></strong>
            </div>
          </div>
          <div class="hab-anchor-box" id="habAnchorBox">
            <div class="hab-anchor-label">Âncora Mental</div>
            <div class="hab-anchor-text" id="habAnchorText"></div>
          </div>
          <div class="hab-steps-list" id="habPreSteps"></div>
        </div>

        <!-- Conteúdo Habilidades Clínicas: Aba 2 (Checklist Pós-Atendimento) -->
        <div class="hab-panel" id="habChecklistPanel" style="display:none;">
          <div class="hab-progress-card">
            <div class="hab-progress-top">
              <div>
                <div class="hab-progress-title">Execução no Atendimento</div>
                <div class="hab-progress-count" id="habProgressCount">0/0 executados</div>
              </div>
              <div class="hab-progress-pct" id="habProgressPct">0%</div>
            </div>
            <div class="hab-progress-track">
              <div class="hab-progress-fill" id="habProgressFill"></div>
            </div>
          </div>

          <div class="hab-blindspots-panel" id="habBlindspotsPanel"></div>

          <div class="hab-checklist-actions">
            <button class="btn btn-hab-debrief" onclick="copyHabDebriefing()">
              Copiar Debriefing
            </button>
            <button class="btn btn-hab-reset" onclick="resetHabChecklist()">
              Resetar p/ Próximo Paciente
            </button>
          </div>

          <div class="hab-sections-wrap" id="habChecklistSections"></div>
        </div>

        <!-- Conteúdo Habilidades Clínicas: Aba 3 (Armadilhas & Erros Fatais) -->
        <div class="hab-panel" id="habPitfallsPanel" style="display:none;">
          <div class="hab-pitfalls-lead">
            Erros de execução que falseiam o exame, atrasam diagnóstico grave ou quebram segurança do paciente.
          </div>
          <div class="hab-pitfalls-list" id="habPitfallsList"></div>
        </div>
      </div>

      <div class="drawer-footer">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="trigger-chip" id="drawerTriggerChip" onclick="copyDrawerTrigger()">
            <code id="drawerTrigger">;atalho</code>
          </span>
          <span class="drawer-hab-meta-footer" id="drawerHabMetaFooter" style="display:none;"></span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button class="btn btn-primary" id="drawerCopyBtn" onclick="copyCurrentDrawerTab()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            <span id="drawerCopyBtnText">Copiar Texto Aberto</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Command Palette Modal (Ctrl+K) -->
  <div class="cmd-overlay" id="cmdOverlay" onclick="closeCmdPalette()">
    <div class="cmd-modal" onclick="event.stopPropagation()">
      <div class="cmd-search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="cmdSearchInput" class="cmd-search-input" placeholder="Buscar protocolo PEP, habilidade ou atalho..." autocomplete="off">
        <span class="kbd-shortcut">ESC</span>
      </div>
      <div class="cmd-results" id="cmdResults"></div>
      <div class="cmd-footer">
        <span>↑↓ navegar • Enter copia PEP ou abre Habilidade • Shift+Enter abre painel</span>
        <span id="cmdCount">__TOTAL_ALL__ itens</span>
      </div>
    </div>
  </div>

  <!-- Modal de Doses Ponderais Rápidas -->
  <div class="doses-overlay" id="dosesOverlay" onclick="closeDosesModal()">
    <div class="doses-modal" onclick="event.stopPropagation()">
      <div class="doses-header">
        <div>
          <h2 style="font-size:1rem; font-weight:600; color:var(--text);">Doses Críticas por Peso</h2>
          <p style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">Cálculo automático para <strong id="modalWeightDisplay" style="color:var(--primary);">70 kg</strong></p>
        </div>
        <button class="close-btn" onclick="closeDosesModal()" aria-label="Fechar">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <div class="doses-body" id="dosesContainer">
        <!-- Injetado dinamicamente via JS -->
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div class="toast" id="toast">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2.2"><polyline points="20 6 9 17 4 12"></polyline></svg>
    <span id="toastMsg">Texto copiado!</span>
  </div>

  <script>
    const allData = __SNIPPETS_JSON__;
    const TOTAL_PEP = __TOTAL_PEP__;
    const HAB_STORAGE_PREFIX = 'hab_checklist_v1:';

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
    const counterPill = document.getElementById('counterPill');
    const counterText = document.getElementById('counterText');
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');
    const quickWeightInput = document.getElementById('quickWeightInput');

    // Drawer elements
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerPanel = document.getElementById('drawerPanel');
    const drawerTitle = document.getElementById('drawerTitle');
    const drawerPath = document.getElementById('drawerPath');
    const drawerContent = document.getElementById('drawerContent');
    const drawerInteractivePanel = document.getElementById('drawerInteractivePanel');
    const interactiveRendered = document.getElementById('interactiveRendered');
    const drawerTriggerChip = document.getElementById('drawerTriggerChip');
    const drawerTrigger = document.getElementById('drawerTrigger');
    const drawerHabMetaFooter = document.getElementById('drawerHabMetaFooter');
    const drawerCopyBtn = document.getElementById('drawerCopyBtn');
    const drawerCopyBtnText = document.getElementById('drawerCopyBtnText');

    // Drawer tabs PEP
    const tabPepBtn = document.getElementById('tabPepBtn');
    const tabInteractiveBtn = document.getElementById('tabInteractiveBtn');
    const tabCondutaBtn = document.getElementById('tabCondutaBtn');
    const tabRecBtn = document.getElementById('tabRecBtn');
    const tabGuiaBtn = document.getElementById('tabGuiaBtn');

    // Drawer tabs & panels Habilidades
    const tabHabPreBtn = document.getElementById('tabHabPreBtn');
    const tabHabChecklistBtn = document.getElementById('tabHabChecklistBtn');
    const tabHabPitfallsBtn = document.getElementById('tabHabPitfallsBtn');
    const habPrePanel = document.getElementById('habPrePanel');
    const habTimeGoal = document.getElementById('habTimeGoal');
    const habCategoryBadge = document.getElementById('habCategoryBadge');
    const habAnchorBox = document.getElementById('habAnchorBox');
    const habAnchorText = document.getElementById('habAnchorText');
    const habPreSteps = document.getElementById('habPreSteps');
    const habChecklistPanel = document.getElementById('habChecklistPanel');
    const habProgressCount = document.getElementById('habProgressCount');
    const habProgressPct = document.getElementById('habProgressPct');
    const habProgressFill = document.getElementById('habProgressFill');
    const habBlindspotsPanel = document.getElementById('habBlindspotsPanel');
    const habChecklistSections = document.getElementById('habChecklistSections');
    const habPitfallsPanel = document.getElementById('habPitfallsPanel');
    const habPitfallsList = document.getElementById('habPitfallsList');

    // Command Palette elements
    const cmdOverlay = document.getElementById('cmdOverlay');
    const cmdSearchInput = document.getElementById('cmdSearchInput');
    const cmdResults = document.getElementById('cmdResults');
    const cmdCount = document.getElementById('cmdCount');

    // Doses Modal elements
    const dosesOverlay = document.getElementById('dosesOverlay');
    const modalWeightDisplay = document.getElementById('modalWeightDisplay');
    const dosesContainer = document.getElementById('dosesContainer');

    let toastTimer = null;
    function showToast(msg) {
      toastMsg.textContent = msg;
      toast.classList.add('show');
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('show'), 2300);
    }

    function escapeHtml(str) {
      return String(str == null ? '' : str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function copyTextToClipboard(text, successMsg) {
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(text).then(() => {
          showToast(successMsg);
        }).catch(() => {
          fallbackCopy(text, successMsg);
        });
      } else {
        fallbackCopy(text, successMsg);
      }
    }

    function fallbackCopy(text, successMsg) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        showToast(successMsg);
      } catch (err) {
        alert('Erro ao copiar: ' + err);
      }
      document.body.removeChild(ta);
    }

    function copySnippet(index) {
      const item = allData[index];
      if (!item) return;
      if (item.mod_id === 'hab') {
        openInspector(index, 'preporta');
        return;
      }
      copyTextToClipboard(item.pep_body, 'Snippet PEP completo copiado!');
    }

    function copyConduta(index) {
      const item = allData[index];
      if (!item || !item.conduta_body) return;
      copyTextToClipboard(item.conduta_body, 'Conduta / Prescrição imediata copiada!');
    }

    function copyReceita(index) {
      const item = allData[index];
      if (!item || !item.receita_body) return;
      copyTextToClipboard(item.receita_body, 'Receita de alta copiada!');
    }

    function copyTrigger(trig) {
      if (!trig) return;
      copyTextToClipboard(trig, `Atalho ${trig} copiado!`);
    }

    // --- Persistência & Helpers do Checklist de Habilidades ---
    function getHabStorageKey(item) {
      return HAB_STORAGE_PREFIX + (item.path || item.id);
    }

    function loadHabChecklistState(item) {
      try {
        const raw = localStorage.getItem(getHabStorageKey(item));
        if (!raw) return {};
        const parsed = JSON.parse(raw);
        return (parsed && typeof parsed === 'object') ? parsed : {};
      } catch (e) {
        return {};
      }
    }

    function saveHabChecklistState(item, stateObj) {
      try {
        localStorage.setItem(getHabStorageKey(item), JSON.stringify(stateObj));
      } catch (e) {
        // Ignora silenciosamente se localStorage estiver bloqueado
      }
    }

    function computeHabStats(item, stateObj) {
      const sections = item.checklist_sections || [];
      let total = 0;
      let checked = 0;
      const missed = [];

      sections.forEach(sec => {
        (sec.items || []).forEach(it => {
          total++;
          if (stateObj[it.id]) {
            checked++;
          } else {
            missed.push({ section: sec.title, text: it.text, id: it.id });
          }
        });
      });

      const pct = total > 0 ? Math.round((checked / total) * 100) : 0;
      return { total, checked, pct, missed };
    }

    function buildHabDebriefingMarkdown(item, stateObj, nowDate) {
      const d = nowDate || new Date();
      const dd = String(d.getDate()).padStart(2, '0');
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const yyyy = d.getFullYear();
      const dateStr = `${dd}/${mm}/${yyyy}`;

      const stats = computeHabStats(item, stateObj);
      const lines = [
        `### ${dateStr} — ${item.title}`,
        `- **Execução:** \`${stats.checked}/${stats.total}\` executados (${stats.pct}%)`
      ];

      if (stats.missed.length === 0) {
        lines.push(`- **Pontos Cegos / Itens Esquecidos:** Nenhum — 100% executado!`);
      } else {
        lines.push(`- **Pontos Cegos / Itens Esquecidos:**`);
        stats.missed.forEach(m => {
          lines.push(`  - [ ] [${m.section}] ${m.text}`);
        });
      }

      lines.push(`- **Contexto / Ajuste p/ próximo atendimento:**`);
      lines.push(`  - `);

      return lines.join('\n');
    }

    function syncAllHabCardBadges() {
      allData.forEach((item, idx) => {
        if (item.mod_id !== 'hab') return;
        const btn = document.querySelector(`[data-hab-chk-btn="${idx}"]`);
        if (!btn) return;
        const state = loadHabChecklistState(item);
        const stats = computeHabStats(item, state);
        const labelEl = btn.querySelector('.chk-btn-label') || btn;
        if (stats.checked > 0) {
          labelEl.textContent = `Checklist · ${stats.checked}/${stats.total}`;
          btn.classList.toggle('complete', stats.checked === stats.total && stats.total > 0);
        } else {
          labelEl.textContent = `Checklist · ${stats.total}`;
          btn.classList.remove('complete');
        }
      });
    }

    // --- Drawer Inspector ---
    function openInspector(index, initialTab) {
      const item = allData[index];
      if (!item) return;
      currentDrawerIndex = index;
      drawerTitle.textContent = item.title;
      drawerPath.textContent = item.path;

      const isHab = item.mod_id === 'hab';
      drawerPanel.classList.toggle('drawer-hab', isHab);

      // Visibilidade das abas PEP vs Habilidades
      tabPepBtn.style.display = isHab ? 'none' : 'inline-block';
      tabInteractiveBtn.style.display = isHab ? 'none' : 'inline-block';
      tabCondutaBtn.style.display = (!isHab && item.has_split) ? 'inline-block' : 'none';
      tabRecBtn.style.display = (!isHab && item.has_receita) ? 'inline-block' : 'none';
      tabGuiaBtn.style.display = (!isHab && item.has_guia) ? 'inline-block' : 'none';

      tabHabPreBtn.style.display = isHab ? 'inline-block' : 'none';
      tabHabChecklistBtn.style.display = isHab ? 'inline-block' : 'none';
      tabHabPitfallsBtn.style.display = isHab ? 'inline-block' : 'none';

      if (isHab) {
        drawerTriggerChip.style.display = 'none';
        drawerHabMetaFooter.style.display = 'inline-flex';
        drawerHabMetaFooter.textContent = `${item.time_goal || '5–10 min'} • ${item.category}`;
        const stats = computeHabStats(item, loadHabChecklistState(item));
        tabHabChecklistBtn.textContent = `Checklist (${stats.checked}/${stats.total})`;
        const targetTab = (initialTab === 'checklist' || initialTab === 'armadilhas') ? initialTab : 'preporta';
        switchDrawerTab(targetTab);
      } else {
        drawerTriggerChip.style.display = 'none';
        drawerHabMetaFooter.style.display = 'inline-flex';
        drawerHabMetaFooter.textContent = `${item.module_name} • ${item.category}`;
        switchDrawerTab(initialTab || 'pep');
      }

      drawerOverlay.classList.add('open');
    }

    function closeInspector() {
      drawerOverlay.classList.remove('open');
      currentDrawerIndex = null;
    }

    function hideAllDrawerPanels() {
      drawerContent.style.display = 'none';
      drawerInteractivePanel.style.display = 'none';
      habPrePanel.style.display = 'none';
      habChecklistPanel.style.display = 'none';
      habPitfallsPanel.style.display = 'none';
    }

    function switchDrawerTab(tab) {
      currentDrawerTab = tab;
      const item = allData[currentDrawerIndex];
      if (!item) return;

      tabPepBtn.classList.toggle('active', tab === 'pep');
      tabInteractiveBtn.classList.toggle('active', tab === 'interactive');
      tabCondutaBtn.classList.toggle('active', tab === 'conduta');
      tabRecBtn.classList.toggle('active', tab === 'receita');
      tabGuiaBtn.classList.toggle('active', tab === 'guia');

      tabHabPreBtn.classList.toggle('active', tab === 'preporta');
      tabHabChecklistBtn.classList.toggle('active', tab === 'checklist');
      tabHabPitfallsBtn.classList.toggle('active', tab === 'armadilhas');

      hideAllDrawerPanels();

      if (item.mod_id === 'hab') {
        drawerCopyBtn.classList.remove('btn-primary');
        drawerCopyBtn.classList.add('btn-hab-pre');

        if (tab === 'preporta') {
          habPrePanel.style.display = 'flex';
          drawerCopyBtnText.textContent = 'Copiar Pré-Porta 30s';
          renderHabPrePorta(item);
        } else if (tab === 'checklist') {
          habChecklistPanel.style.display = 'flex';
          drawerCopyBtnText.textContent = 'Copiar Debriefing';
          renderHabChecklist(item);
        } else if (tab === 'armadilhas') {
          habPitfallsPanel.style.display = 'flex';
          drawerCopyBtnText.textContent = 'Copiar Armadilhas';
          renderHabPitfalls(item);
        }
        return;
      }

      drawerCopyBtn.classList.remove('btn-hab-pre');
      drawerCopyBtn.classList.add('btn-primary');
      drawerCopyBtnText.textContent = 'Copiar Texto Aberto';

      if (tab === 'interactive') {
        drawerInteractivePanel.style.display = 'flex';
        renderInteractive(item.pep_body);
      } else {
        drawerContent.style.display = 'block';
        if (tab === 'pep') {
          drawerContent.textContent = item.pep_body;
        } else if (tab === 'conduta') {
          drawerContent.textContent = item.conduta_body || 'Sem seção de conduta separada.';
        } else if (tab === 'receita') {
          drawerContent.textContent = item.receita_body || 'Sem receita específica associada.';
        } else if (tab === 'guia') {
          drawerContent.textContent = item.guia_body || 'Sem guia de conduta adicional.';
        }
      }
    }

    // --- Renderização das 3 Abas de Habilidades Clínicas ---
    function renderHabPrePorta(item) {
      habTimeGoal.textContent = item.time_goal || '5–10 min';
      habCategoryBadge.textContent = item.hab_category || item.category || 'Habilidades Clínicas';

      if (item.anchor) {
        habAnchorBox.style.display = 'block';
        habAnchorText.textContent = item.anchor;
      } else {
        habAnchorBox.style.display = 'none';
      }

      habPreSteps.innerHTML = '';
      const raw = (item.pre_porta || '').trim();
      if (!raw) {
        habPreSteps.innerHTML = '<div class="hab-pre-line">Sem bloco Pré-Porta definido.</div>';
        return;
      }

      const lines = raw.split('\n');
      lines.forEach(line => {
        const trimmed = line.trim();
        if (!trimmed) return;

        // Sub-item indentado com "- " ou "• "
        const subMatch = trimmed.match(/^[-•]\s+(.+)$/);
        if (subMatch) {
          const subText = subMatch[1];
          const card = document.createElement('div');
          card.className = 'hab-pre-substep';
          const labelMatch = subText.match(/^([^:]{2,55}:)\s+(.+)$/);
          if (labelMatch && !labelMatch[1].includes('http')) {
            const lead = document.createElement('strong');
            lead.className = 'hab-step-lead';
            lead.textContent = labelMatch[1];
            card.appendChild(lead);
            card.appendChild(document.createTextNode(' ' + labelMatch[2]));
          } else {
            card.textContent = subText;
          }
          habPreSteps.appendChild(card);
          return;
        }

        // Destaque especial para alerta final iniciando com >>>
        if (trimmed.startsWith('>>>')) {
          const h = document.createElement('div');
          h.className = 'hab-pre-group-title';
          h.textContent = trimmed.replace(/^>+\s*/, '');
          habPreSteps.appendChild(h);
          return;
        }

        // Subcabeçalho puro terminado em ":" (ex: "EXAME OBSTÉTRICO:" ou "4. AUSCULTA (...):")
        if (trimmed.endsWith(':') && trimmed.length <= 100 && !trimmed.includes('http')) {
          const h = document.createElement('div');
          h.className = 'hab-pre-group-title';
          h.textContent = trimmed.slice(0, -1);
          habPreSteps.appendChild(h);
          return;
        }

        // Passo numerado/letra (1. / A. / ESTAÇÃO) ou rótulo curto antes de ":"
        const stepMatch = trimmed.match(/^((?:(?:\d+|[A-E])\.\s+[^:]{1,70}|[^:]{2,55}):)\s+(.+)$/);
        if (stepMatch && !stepMatch[1].includes('http')) {
          const card = document.createElement('div');
          card.className = 'hab-pre-step';
          const lead = document.createElement('strong');
          lead.className = 'hab-step-lead';
          lead.textContent = stepMatch[1];
          card.appendChild(lead);
          card.appendChild(document.createTextNode(' ' + stepMatch[2]));
          habPreSteps.appendChild(card);
          return;
        }

        const plain = document.createElement('div');
        plain.className = 'hab-pre-line';
        plain.textContent = trimmed;
        habPreSteps.appendChild(plain);
      });
    }

    function updateHabChecklistView(item, stateObj) {
      const stats = computeHabStats(item, stateObj);

      habProgressCount.textContent = `${stats.checked}/${stats.total} executados`;
      habProgressPct.textContent = `${stats.pct}%`;
      const isComplete = stats.total > 0 && stats.checked === stats.total;
      habProgressPct.classList.toggle('done', isComplete);
      habProgressFill.style.width = `${stats.pct}%`;
      habProgressFill.classList.toggle('done', isComplete);

      tabHabChecklistBtn.textContent = `Checklist (${stats.checked}/${stats.total})`;

      // Painel ao vivo de Pontos Cegos / Itens Esquecidos
      if (stats.total === 0) {
        habBlindspotsPanel.classList.remove('all-done');
        habBlindspotsPanel.innerHTML = '<div class="hab-blindspots-header">Nenhum item de checklist encontrado neste cartão.</div>';
      } else if (stats.missed.length === 0) {
        habBlindspotsPanel.classList.add('all-done');
        habBlindspotsPanel.innerHTML = `
          <div class="hab-blindspots-header">
            <span>Nenhum ponto cego — todos os ${stats.total} itens executados.</span>
          </div>
        `;
      } else {
        habBlindspotsPanel.classList.remove('all-done');
        const listItems = stats.missed.map(m => (
          `<li class="hab-blindspot-item"><span class="hab-blindspot-sec">[${escapeHtml(m.section)}]</span> - [ ] ${escapeHtml(m.text)}</li>`
        )).join('');
        habBlindspotsPanel.innerHTML = `
          <div class="hab-blindspots-header">
            <span>Pontos Cegos / Itens Esquecidos (${stats.missed.length})</span>
            <span style="font-size:0.72rem; font-weight:500; opacity:0.85;">Ao vivo</span>
          </div>
          <ul class="hab-blindspots-list">${listItems}</ul>
        `;
      }

      // Atualizar contadores por seção
      const secCards = habChecklistSections.querySelectorAll('.hab-sec-card');
      (item.checklist_sections || []).forEach((sec, sIdx) => {
        const card = secCards[sIdx];
        if (!card) return;
        const secChecked = sec.items.filter(it => Boolean(stateObj[it.id])).length;
        const progEl = card.querySelector('.hab-sec-progress');
        if (progEl) progEl.textContent = `${secChecked}/${sec.items.length}`;
      });

      syncAllHabCardBadges();
    }

    function renderHabChecklist(item) {
      const stateObj = loadHabChecklistState(item);
      habChecklistSections.innerHTML = '';

      (item.checklist_sections || []).forEach(sec => {
        const secCard = document.createElement('div');
        secCard.className = 'hab-sec-card';

        const secHeader = document.createElement('div');
        secHeader.className = 'hab-sec-title';
        secHeader.innerHTML = `
          <span>${escapeHtml(sec.title)}</span>
          <span class="hab-sec-progress">0/${sec.items.length}</span>
        `;
        secCard.appendChild(secHeader);

        sec.items.forEach(it => {
          const isChecked = Boolean(stateObj[it.id]);
          const row = document.createElement('label');
          row.className = 'hab-check-item' + (isChecked ? ' checked' : '');

          const cb = document.createElement('input');
          cb.type = 'checkbox';
          cb.checked = isChecked;
          cb.dataset.itemId = it.id;

          const txtSpan = document.createElement('span');
          txtSpan.className = 'hab-check-text';
          txtSpan.textContent = it.text;

          cb.addEventListener('change', () => {
            const latest = loadHabChecklistState(item);
            if (cb.checked) {
              latest[it.id] = true;
            } else {
              delete latest[it.id];
            }
            saveHabChecklistState(item, latest);
            row.classList.toggle('checked', cb.checked);
            updateHabChecklistView(item, latest);
          });

          row.appendChild(cb);
          row.appendChild(txtSpan);
          secCard.appendChild(row);
        });

        habChecklistSections.appendChild(secCard);
      });

      updateHabChecklistView(item, stateObj);
    }

    function copyHabDebriefing() {
      const item = allData[currentDrawerIndex];
      if (!item || item.mod_id !== 'hab') return;
      const stateObj = loadHabChecklistState(item);
      const md = buildHabDebriefingMarkdown(item, stateObj, new Date());
      copyTextToClipboard(md, 'Debriefing copiado! Cole em 00_DIARIO_PONTOS_CEGOS.md');
    }

    function resetHabChecklist() {
      const item = allData[currentDrawerIndex];
      if (!item || item.mod_id !== 'hab') return;
      saveHabChecklistState(item, {});
      renderHabChecklist(item);
      showToast('Checklist resetado para o próximo paciente!');
    }

    function renderHabPitfalls(item) {
      habPitfallsList.innerHTML = '';
      const list = item.pitfalls || [];
      if (list.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'hab-pre-line';
        empty.textContent = item.pitfalls_raw || 'Nenhuma armadilha cadastrada.';
        habPitfallsList.appendChild(empty);
        return;
      }

      list.forEach(p => {
        const card = document.createElement('div');
        card.className = 'hab-pitfall-card';
        card.innerHTML = `
          <div class="hab-pitfall-title">${escapeHtml(p.title)}</div>
          ${p.detail ? `<div class="hab-pitfall-detail">${escapeHtml(p.detail)}</div>` : ''}
        `;
        habPitfallsList.appendChild(card);
      });
    }

    function isLikelyMultiGroup(lineText, options) {
      if (!options || options.length <= 1) return false;

      const lowerOpts = options.map(o => o.toLowerCase().trim());
      const allJoined = lowerOpts.join(' | ');

      // Pares ou trios estritamente mutuamente exclusivos
      const strictSingles = [
        /^(sim\s*\|\s*não|não\s*\|\s*sim)$/i,
        /^(m\s*\|\s*f|f\s*\|\s*m)$/i,
        /^(masculino\s*\|\s*feminino|feminino\s*\|\s*masculino)$/i,
        /^(beg\s*\|\s*reg\s*\|\s*meg|beg\s*\|\s*reg)$/i,
        /^(normal\s*\|\s*alterada?)$/i,
        /^(não reagente\s*\|\s*reagente|reagente\s*\|\s*não reagente)$/i,
        /^(direito\s*\|\s*esquerdo|msd\s*\|\s*mse|mid\s*\|\s*mie)$/i,
        /^(cefálica\s*\|\s*pélvica)$/i,
        /^manter\s*\|\s*suspender/i
      ];

      for (const rx of strictSingles) {
        if (rx.test(allJoined)) return false;
      }

      // Contexto da linha: comorbidades, sintomas, exames, condutas, etc.
      const lineLower = (lineText || '').toLowerCase();
      const multiKeywords = [
        'comorbidade', 'antecedente', 'sintoma', 'queixa', 'alergia',
        'exame', 'conduta', 'prescri', 'procedimento', 'solicitar',
        'retirar', 'orienta', 'risco', 'achado', 'droga', 'medicamento',
        'dispositivo', 'diagnóstico secundário'
      ];
      if (multiKeywords.some(k => lineLower.includes(k))) return true;

      // Siglas ou termos clínicos comuns em listas combináveis
      const multiTerms = ['has', 'dm', 'dac', 'drc', 'dpoc', 'cardiopatia', 'neoplasia', 'tc', 'usg', 'rx', 'ecg', 'dipirona', 'tosse', 'febre', 'dispneia'];
      if (lowerOpts.some(o => multiTerms.includes(o) || multiTerms.some(t => o.startsWith(t + ' ') || o.endsWith(' ' + t)))) {
        return true;
      }

      // Se tiver 4 ou mais opções e não for escala estrita, tende a ser lista de opções
      if (options.length >= 4) return true;

      return false;
    }

    // Renderização do Personalizador Interativo (PEP)
    function renderInteractive(rawText) {
      interactiveRendered.innerHTML = '';

      const lines = rawText.split('\n');
      const frag = document.createDocumentFragment();

      lines.forEach(line => {
        const lineDiv = document.createElement('div');
        const parts = line.split(/(\[[^\]]+?\s*\/\s*[^\]]+?\])/g);

        parts.forEach(part => {
          if (part.startsWith('[') && part.endsWith(']') && part.includes('/')) {
            const inner = part.slice(1, -1);
            const options = inner.split('/').map(o => o.trim()).filter(Boolean);

            if (options.length === 0) {
              lineDiv.appendChild(document.createTextNode(part));
              return;
            }

            const groupSpan = document.createElement('span');
            groupSpan.className = 'choice-group';

            const defaultMulti = isLikelyMultiGroup(line, options);
            if (defaultMulti) {
              groupSpan.classList.add('is-multi');
            }

            // Botão para alternar modo (🔘 1 / ☑️ Várias)
            const modeBtn = document.createElement('button');
            modeBtn.type = 'button';
            modeBtn.className = 'choice-mode-btn';
            modeBtn.title = 'Alternar entre seleção única ou múltipla neste campo';

            function syncModeBtn() {
              const isM = groupSpan.classList.contains('is-multi');
              modeBtn.textContent = isM ? '☑️ Várias' : '🔘 1';
            }
            syncModeBtn();

            modeBtn.onclick = (e) => {
              e.stopPropagation();
              const wasMulti = groupSpan.classList.contains('is-multi');
              if (wasMulti) {
                groupSpan.classList.remove('is-multi');
                // Se mudou para 1 opção e tinha várias selecionadas, preserva apenas a primeira
                const actives = Array.from(groupSpan.querySelectorAll('.choice-pill.active'));
                if (actives.length > 1) {
                  actives.slice(1).forEach(b => b.classList.remove('active'));
                }
              } else {
                groupSpan.classList.add('is-multi');
              }
              syncModeBtn();
            };

            // Criar pílulas de opção
            options.forEach((opt, oIdx) => {
              const btn = document.createElement('button');
              btn.type = 'button';
              btn.className = 'choice-pill' + (oIdx === 0 ? ' active' : '');
              btn.textContent = opt;

              btn.onclick = (e) => {
                e.stopPropagation();
                const isMultiMode = groupSpan.classList.contains('is-multi');
                const isActive = btn.classList.contains('active');
                const optLower = opt.toLowerCase();
                const isNegation = optLower.startsWith('nega') || optLower === 'hígido' || optLower === 'nenhum' || optLower === 'sem queixas';

                if (isMultiMode) {
                  // MODO MÚLTIPLO: toggle direto
                  if (isActive) {
                    btn.classList.remove('active');
                  } else {
                    btn.classList.add('active');
                    // Se clicou em Nega/Hígido, desmarca itens positivos
                    if (isNegation) {
                      groupSpan.querySelectorAll('.choice-pill').forEach(b => {
                        if (b !== btn) b.classList.remove('active');
                      });
                    } else {
                      // Se clicou em item positivo, desmarca Nega/Hígido
                      groupSpan.querySelectorAll('.choice-pill').forEach(b => {
                        const bLow = b.textContent.toLowerCase();
                        if (bLow.startsWith('nega') || bLow === 'hígido' || bLow === 'nenhum' || bLow === 'sem queixas') {
                          b.classList.remove('active');
                        }
                      });
                    }
                  }
                } else {
                  // MODO ÚNICO:
                  if (isActive) {
                    // Clicar no selecionado desmarca (permite deixar vazio)
                    btn.classList.remove('active');
                  } else {
                    groupSpan.querySelectorAll('.choice-pill').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                  }
                }
              };

              groupSpan.appendChild(btn);
            });

            groupSpan.appendChild(modeBtn);
            lineDiv.appendChild(groupSpan);
          } else {
            lineDiv.appendChild(document.createTextNode(part));
          }
        });

        frag.appendChild(lineDiv);
      });

      interactiveRendered.appendChild(frag);
    }

    function copyCurrentDrawerTab() {
      const item = allData[currentDrawerIndex];
      if (!item) return;

      if (item.mod_id === 'hab') {
        if (currentDrawerTab === 'preporta') {
          const text = `${item.title}\nMeta: ${item.time_goal}\nÂncora: ${item.anchor}\n\n${item.pre_porta}`.trim();
          copyTextToClipboard(text, 'Bloco Pré-Porta 30s copiado!');
        } else if (currentDrawerTab === 'checklist') {
          copyHabDebriefing();
        } else if (currentDrawerTab === 'armadilhas') {
          const text = (item.pitfalls || []).map(p => `- ${p.title}: ${p.detail}`).join('\n') || item.pitfalls_raw;
          copyTextToClipboard(text, 'Armadilhas & Erros Fatais copiados!');
        }
        return;
      }

      if (currentDrawerTab === 'interactive') {
        let text = "";
        interactiveRendered.childNodes.forEach(lineNode => {
          let lineText = "";
          lineNode.childNodes.forEach(child => {
            if (child.classList && child.classList.contains('choice-group')) {
              const actives = Array.from(child.querySelectorAll('.choice-pill.active'));
              if (actives.length > 0) {
                lineText += actives.map(a => a.textContent.trim()).join(', ');
              } else {
                lineText += "";
              }
            } else {
              lineText += child.textContent;
            }
          });
          text += lineText + "\n";
        });
        copyTextToClipboard(text.trim(), 'Texto personalizado copiado!');
      } else {
        copyTextToClipboard(drawerContent.textContent, 'Conteúdo copiado com sucesso!');
      }
    }

    function copyDrawerTrigger() {
      const trig = drawerTrigger.textContent;
      copyTrigger(trig);
    }

    // Subcategorias Dinâmicas
    function updateSubcategories() {
      subcatContainer.innerHTML = '<button class="subcat-chip active" data-cat="all">Todas as Áreas</button>';
      const cats = new Set();
      cards.forEach(c => {
        if ((activeModule === 'all' && c.dataset.mod !== 'hab') || c.dataset.mod === activeModule) {
          cats.add(c.dataset.cat);
        }
      });
      Array.from(cats).sort().forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'subcat-chip';
        btn.dataset.cat = cat;
        btn.textContent = cat;
        subcatContainer.appendChild(btn);
      });
      activeSubcat = 'all';
    }

    // Filtragem Principal (Aba Geral mostra APENAS os 90 PEP; aba Habilidades mostra os cartões hab)
    function filterCards() {
      const q = searchInput.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(c => {
        const matchSearch = !q || c.dataset.search.includes(q);
        const matchMod = (activeModule === 'all') ? (c.dataset.mod !== 'hab') : (c.dataset.mod === activeModule);
        const matchCat = (activeSubcat === 'all') || (c.dataset.cat === activeSubcat);

        if (matchSearch && matchMod && matchCat) {
          c.style.display = 'flex';
          visible++;
        } else {
          c.style.display = 'none';
        }
      });

      counterPill.classList.toggle('is-hab', activeModule === 'hab');
      if (activeModule === 'hab') {
        counterText.textContent = `${visible} ${visible === 1 ? 'Habilidade' : 'Habilidades'}`;
      } else if (activeModule === 'all' && !q && activeSubcat === 'all') {
        counterText.textContent = `${visible} Protocolos`;
      } else {
        counterText.textContent = `${visible} Filtrados`;
      }
    }

    searchInput.addEventListener('input', filterCards);

    moduleTabs.addEventListener('click', (e) => {
      const btn = e.target.closest('.tab-btn');
      if (!btn) return;
      moduleTabs.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (btn.scrollIntoView) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
      activeModule = btn.dataset.mod;
      searchInput.placeholder = activeModule === 'hab'
        ? 'Buscar habilidade, manobra, ECG, RX, SPIKES, Leopold, protocolo...'
        : 'Buscar por queixa, diagnóstico, atalho (ex: ;sepse, ;tpp, ;sca, ;fasthug) ou droga...';
      updateSubcategories();
      filterCards();
    });

    subcatContainer.addEventListener('click', (e) => {
      if (e.target.classList.contains('subcat-chip')) {
        subcatContainer.querySelectorAll('.subcat-chip').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        activeSubcat = e.target.dataset.cat;
        filterCards();
      }
    });

    // Command Palette Modal (Ctrl+K)
    function openCmdPalette() {
      cmdOverlay.classList.add('open');
      cmdSearchInput.value = '';
      cmdSearchInput.focus();
      updateCmdResults('');
    }

    function closeCmdPalette() {
      cmdOverlay.classList.remove('open');
    }

    function activateCmdItem(item, forceOpen) {
      const idx = allData.indexOf(item);
      if (item.mod_id === 'hab' || forceOpen) {
        openInspector(idx);
      } else {
        copySnippet(idx);
      }
      closeCmdPalette();
    }

    function updateCmdResults(query) {
      const q = query.toLowerCase().trim();
      cmdMatches = allData.filter(item => {
        if (!q) return true;
        return item.title.toLowerCase().includes(q) ||
               (item.all_triggers || []).some(t => t.toLowerCase().includes(q)) ||
               item.category.toLowerCase().includes(q) ||
               item.module_name.toLowerCase().includes(q) ||
               (item.anchor && item.anchor.toLowerCase().includes(q));
      }).slice(0, 15);

      cmdResults.innerHTML = '';
      cmdActiveIndex = 0;

      if (cmdMatches.length === 0) {
        cmdResults.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-dim); font-size:0.86rem;">Nenhum protocolo ou habilidade encontrada.</div>';
        cmdCount.textContent = '0 resultados';
        return;
      }

      cmdMatches.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'cmd-item' + (idx === 0 ? ' active' : '');
        const isHab = item.mod_id === 'hab';
        const dotEl = `<span class="mod-dot mod-dot-${escapeHtml(item.mod_id)}"></span>`;
        const subtitle = isHab
          ? `${item.module_name} • ${item.category}${item.time_goal ? ' • ' + item.time_goal : ''}`
          : `${item.module_name} • ${item.category}`;
        const rightTag = isHab
          ? '<span class="cmd-item-trig cmd-item-hab-trig">Habilidade</span>'
          : `<span class="cmd-item-trig">${escapeHtml(item.category)}</span>`;

        div.innerHTML = `
          <div class="cmd-item-left">
            ${dotEl}
            <div>
              <div class="cmd-item-title">${escapeHtml(item.title)}</div>
              <div class="cmd-item-cat">${escapeHtml(subtitle)}</div>
            </div>
          </div>
          ${rightTag}
        `;
        div.onclick = () => activateCmdItem(item, false);
        cmdResults.appendChild(div);
      });

      cmdCount.textContent = `${cmdMatches.length} de ${allData.length} itens`;
    }

    cmdSearchInput.addEventListener('input', (e) => {
      updateCmdResults(e.target.value);
    });

    // Navegação no Command Palette por teclado
    cmdSearchInput.addEventListener('keydown', (e) => {
      const items = cmdResults.querySelectorAll('.cmd-item');
      if (items.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        items[cmdActiveIndex].classList.remove('active');
        cmdActiveIndex = (cmdActiveIndex + 1) % items.length;
        items[cmdActiveIndex].classList.add('active');
        items[cmdActiveIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        items[cmdActiveIndex].classList.remove('active');
        cmdActiveIndex = (cmdActiveIndex - 1 + items.length) % items.length;
        items[cmdActiveIndex].classList.add('active');
        items[cmdActiveIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (cmdMatches[cmdActiveIndex]) {
          activateCmdItem(cmdMatches[cmdActiveIndex], e.shiftKey);
        }
      }
    });

    // Modal de Doses Ponderais Rápidas
    function openDosesModal() {
      const weight = parseFloat(quickWeightInput.value) || 70;
      modalWeightDisplay.textContent = `${weight} kg`;
      renderDoses(weight);
      dosesOverlay.classList.add('open');
    }

    function closeDosesModal() {
      dosesOverlay.classList.remove('open');
    }

    function renderDoses(w) {
      const doses = [
        {
          name: 'Ressuscitação na Sepse (30 mL/kg)',
          rule: '30 mL/kg de Ringer Lactato aquecido nas primeiras 3 horas',
          calc: `${Math.round(w * 30)} mL de Ringer Lactato EV rápido`,
          copy: `${Math.round(w * 30)} mL de Ringer Lactato EV em 3 horas`
        },
        {
          name: 'Dengue Grupo C - Fase de Expansão (10 mL/kg/h)',
          rule: '10 mL/kg/hora nas primeiras 2 horas',
          calc: `${Math.round(w * 10)} mL/hora`,
          copy: `SF 0,9% ou Ringer Lactato: infundir ${Math.round(w * 10)} mL/hora nas primeiras 2 horas.`
        },
        {
          name: 'Alteplase (rt-PA) no AVC Isquêmico (0,9 mg/kg)',
          rule: '0,9 mg/kg (máx 90mg) • 10% em bólus 1 min + 90% em 60 min',
          calc: `${Math.min(90, (w * 0.9)).toFixed(1)} mg total (${(Math.min(90, w * 0.9) * 0.1).toFixed(1)} mg bólus + ${(Math.min(90, w * 0.9) * 0.9).toFixed(1)} mg em 1h)`,
          copy: `Alteplase (rt-PA) para peso ${w} kg: Dose total: ${Math.min(90, (w * 0.9)).toFixed(1)} mg EV. Administrar ${(Math.min(90, w * 0.9) * 0.1).toFixed(1)} mg em bólus EV em 1 min e ${(Math.min(90, w * 0.9) * 0.9).toFixed(1)} mg em BIC em 60 min.`
        },
        {
          name: 'Enoxaparina Terapêutica Plena (1 mg/kg 12/12h)',
          rule: '1 mg/kg SC de 12/12h (idade < 75 anos e ClCr > 30)',
          calc: `${Math.round(w)} mg SC 12/12h`,
          copy: `Enoxaparina ${Math.round(w)} mg SC de 12/12 horas.`
        },
        {
          name: 'Enoxaparina Terapêutica Idoso >= 75 anos (0,75 mg/kg 12/12h)',
          rule: '0,75 mg/kg SC de 12/12h sem bólus EV',
          calc: `${(w * 0.75).toFixed(0)} mg SC 12/12h`,
          copy: `Enoxaparina ${(w * 0.75).toFixed(0)} mg SC de 12/12 horas.`
        },
        {
          name: 'Dipirona Gotas (1 gota/kg)',
          rule: '1 gota/kg até máximo de 40 gotas (1g) por tomada',
          calc: `${Math.min(40, Math.round(w))} gotas VO`,
          copy: `Dipirona gotas: Tomar ${Math.min(40, Math.round(w))} gotas via oral de 6/6 horas SOS se dor ou febre.`
        },
        {
          name: 'Paracetamol Gotas 200mg/mL (1 gota/kg)',
          rule: '1 gota/kg (máx 35-40 gotas / 750mg) por tomada',
          calc: `${Math.min(37, Math.round(w))} gotas VO`,
          copy: `Paracetamol gotas (200 mg/mL): Tomar ${Math.min(37, Math.round(w))} gotas via oral de 6/6 horas SOS se febre.`
        },
        {
          name: 'Sequência Rápida de Intubação: Etomidato (0,3 mg/kg)',
          rule: '0,3 mg/kg EV em bólus',
          calc: `${(w * 0.3).toFixed(1)} mg EV`,
          copy: `Etomidato: ${(w * 0.3).toFixed(1)} mg EV em bólus rápido.`
        },
        {
          name: 'Sequência Rápida de Intubação: Succinilcolina (1,2 mg/kg)',
          rule: '1,0 a 1,5 mg/kg EV em bólus',
          calc: `${Math.round(w * 1.2)} mg EV`,
          copy: `Succinilcolina: ${Math.round(w * 1.2)} mg EV em bólus rápido.`
        },
        {
          name: 'Sequência Rápida de Intubação: Fentanil (2 mcg/kg)',
          rule: '1 a 2 mcg/kg EV lento',
          calc: `${Math.round(w * 2)} mcg (${(w * 2 / 50).toFixed(1)} mL) EV`,
          copy: `Fentanil: ${Math.round(w * 2)} mcg (${(w * 2 / 50).toFixed(1)} mL) EV lento.`
        }
      ];

      dosesContainer.innerHTML = '';
      doses.forEach(d => {
        const card = document.createElement('div');
        card.className = 'dose-card';
        const left = document.createElement('div');
        left.innerHTML = `<div class="dose-name">${escapeHtml(d.name)}</div><div class="dose-rule">${escapeHtml(d.rule)}</div>`;
        const right = document.createElement('div');
        right.style.cssText = 'display:flex; align-items:center; gap:10px;';
        const calcDiv = document.createElement('div');
        calcDiv.className = 'dose-calc';
        calcDiv.textContent = d.calc;
        const copyBtn = document.createElement('button');
        copyBtn.className = 'dose-copy-btn';
        copyBtn.textContent = 'Copiar';
        copyBtn.onclick = () => copyTextToClipboard(d.copy, 'Dose copiada!');
        right.appendChild(calcDiv);
        right.appendChild(copyBtn);
        card.appendChild(left);
        card.appendChild(right);
        dosesContainer.appendChild(card);
      });
    }

    quickWeightInput.addEventListener('input', () => {
      const w = parseFloat(quickWeightInput.value) || 70;
      modalWeightDisplay.textContent = `${w} kg`;
      renderDoses(w);
    });

    // Atalhos Globais de Teclado
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openCmdPalette();
        return;
      }

      if (e.key === '/' && document.activeElement !== searchInput && document.activeElement !== cmdSearchInput && document.activeElement !== quickWeightInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      } else if (e.key === 'Escape') {
        if (cmdOverlay.classList.contains('open')) {
          closeCmdPalette();
        } else if (dosesOverlay.classList.contains('open')) {
          closeDosesModal();
        } else if (drawerOverlay.classList.contains('open')) {
          closeInspector();
        } else if (searchInput.value) {
          searchInput.value = '';
          filterCards();
        }
      }
    });

    // Inicialização
    updateSubcategories();
    filterCards();
    syncAllHabCardBadges();
  </script>
</body>
</html>
"""

html_page = (
    html_template
    .replace('__TOTAL_PEP__', str(count_pep))
    .replace('__TOTAL_ALL__', str(len(cockpit_items)))
    .replace('__COUNT_GO__', str(count_go))
    .replace('__COUNT_UPA__', str(count_upa))
    .replace('__COUNT_ENF__', str(count_enf))
    .replace('__COUNT_PED__', str(count_ped))
    .replace('__COUNT_HAB__', str(count_hab))
    .replace('__CARDS_HTML__', cards_joined)
    .replace('__SNIPPETS_JSON__', snippets_json_payload)
)

with open(html_path, 'w', encoding='utf-8') as fh:
    fh.write(html_page)
index_path = os.path.join(BASE_PROJECT, 'index.html')
with open(index_path, 'w', encoding='utf-8') as fh:
    fh.write(html_page)
print(f"Cockpit Web UI/UX High-End salvo com sucesso em {html_path} e {index_path}!")
