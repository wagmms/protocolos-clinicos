import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const htmlPath = path.resolve(process.cwd(), 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

function extractScriptAndRun() {
  const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);
  assert.ok(scriptMatch, 'Script block must exist in index.html');

  // Minimal DOM mock to run index.html script in Node VM
  const makeEl = () => ({
    style: {},
    dataset: {},
    classList: {
      _set: new Set<string>(),
      add(...cls: string[]) { cls.forEach(c => this._set.add(c)); },
      remove(...cls: string[]) { cls.forEach(c => this._set.delete(c)); },
      toggle(c: string, force?: boolean) {
        if (force === undefined) {
          if (this._set.has(c)) this._set.delete(c);
          else this._set.add(c);
        } else if (force) {
          this._set.add(c);
        } else {
          this._set.delete(c);
        }
      },
      contains(c: string) { return this._set.has(c); }
    },
    innerHTML: '',
    textContent: '',
    value: '',
    children: [] as any[],
    childNodes: [] as any[],
    appendChild(child: any) { this.children.push(child); return child; },
    addEventListener() {},
    setAttribute() {},
    getAttribute() { return ''; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    focus() {},
    select() {}
  });

  const elements: Record<string, any> = {};
  const getEl = (id: string) => {
    if (!elements[id]) elements[id] = makeEl();
    return elements[id];
  };

  const vibrateCalls: any[] = [];
  const mockCards = Array.from({ length: 93 }, (_, idx) => {
    const el = makeEl();
    el.dataset = {
      mod: idx < 16 ? 'go' : idx < 57 ? 'upa' : idx < 66 ? 'enf' : idx < 74 ? 'ped' : 'hab',
      cat: 'Categoria Teste',
      search: ''
    };
    el.style = { display: idx < 74 ? 'flex' : 'none' };
    el.scrollIntoView = () => {};
    return el;
  });

  const sandbox: any = {
    window: {
      innerWidth: 1440,
      addEventListener() {},
      scrollTo() {}
    },
    document: {
      activeElement: null,
      documentElement: {
        style: {
          _props: {} as Record<string, string>,
          setProperty(k: string, v: string) { this._props[k] = v; }
        }
      },
      getElementById: getEl,
      querySelector: () => makeEl(),
      querySelectorAll: (sel: string) => (sel === '.card' ? mockCards : []),
      createElement: () => makeEl(),
      createDocumentFragment: () => makeEl(),
      createTextNode: (t: string) => ({ textContent: t }),
      body: makeEl(),
      execCommand: () => true
    },
    navigator: {
      vibrate: (pattern: number[]) => {
        vibrateCalls.push(pattern);
        return true;
      },
      clipboard: {
        writeText: async () => {}
      }
    },
    localStorage: {
      getItem: () => null,
      setItem: () => {}
    },
    performance,
    setTimeout,
    clearTimeout,
    console
  };

  vm.createContext(sandbox);
  vm.runInContext(scriptMatch[1], sandbox);
  const runExpr = (expr: string) => vm.runInContext(expr, sandbox);
  return { sandbox, elements, vibrateCalls, runExpr, mockCards };
}

test('Prompt 1: Semantic search maps tags_sintomas and ranks Asma, DPOC, and EAP at top for "falta de ar"', () => {
  const { sandbox, runExpr } = extractScriptAndRun();
  const allData = runExpr('allData');
  assert.equal(allData.length, 93, 'All 93 protocols (74 PEP + 19 Habilidades) must be preserved');

  const pepCount = Array.from(allData).filter((x: any) => x.mod_id !== 'hab').length;
  const habCount = Array.from(allData).filter((x: any) => x.mod_id === 'hab').length;
  assert.equal(pepCount, 74, 'Must have exactly 74 PEP protocols');
  assert.equal(habCount, 19, 'Must have exactly 19 Habilidades Clínicas cards');

  const t0 = performance.now();
  sandbox.window.searchCommandPalette('falta de ar');
  const elapsed = performance.now() - t0;

  assert.ok(elapsed < 16, `Search latency (${elapsed.toFixed(2)}ms) must be under 16ms`);

  const matches = runExpr('cmdMatches');
  assert.ok(matches.length >= 3, 'Must return at least 3 matches for "falta de ar"');

  const top3Ids = Array.from(matches.slice(0, 3), (m: any) => m.item.id);
  assert.deepEqual(top3Ids, ['upa-32', 'upa-33', 'upa-34'], 'Top 3 protocols for "falta de ar" must be Asma (upa-32), DPOC (upa-33), and EAP (upa-34)');

  matches.slice(0, 3).forEach((m: any) => {
    assert.equal(m.matchedSymptom, 'falta de ar');
    assert.equal(m.isTopHighlight, true);
  });
});

test('Prompt 1: Semantic search handles "dor no peito", "dor de cabeça", "sangramento", and "febre"', () => {
  const { sandbox, runExpr } = extractScriptAndRun();

  sandbox.window.searchCommandPalette('dor no peito');
  let matches = runExpr('cmdMatches');
  assert.equal(matches[0].item.id, 'upa-30', 'Dor Torácica / SCA must be #1 for "dor no peito"');
  assert.equal(matches[0].matchedSymptom, 'dor no peito');

  sandbox.window.searchCommandPalette('dor de cabeça');
  matches = runExpr('cmdMatches');
  assert.equal(matches[0].item.id, 'upa-35', 'Cefaleia Aguda must be #1 for "dor de cabeça"');
  assert.equal(matches[0].matchedSymptom, 'dor de cabeça');

  sandbox.window.searchCommandPalette('sangramento');
  matches = runExpr('cmdMatches');
  assert.ok(['go-10', 'upa-27'].includes(matches[0].item.id), 'HPP or HDA must be at the top for "sangramento"');
  assert.equal(matches[0].matchedSymptom, 'sangramento');

  sandbox.window.searchCommandPalette('febre');
  matches = runExpr('cmdMatches');
  assert.equal(matches[0].item.id, 'upa-53', 'Sepse must be #1 for "febre"');
  assert.equal(matches[0].matchedSymptom, 'febre');
});

test('Prompt 3: Mobile thumb-zone bottom bar, 48x48 touch targets, haptics, 1s emerald state, and 1.8s Toast', () => {
  assert.ok(htmlContent.includes('id="mobileBottomBar"'), 'Mobile floating bottom bar must exist');
  assert.ok(htmlContent.includes('Ctrl+K Busca'), 'Mobile bottom bar must contain Ctrl+K Busca');
  assert.ok(htmlContent.includes('Voltar ao Topo'), 'Mobile bottom bar must contain Voltar ao Topo');
  assert.ok(htmlContent.includes('min-height: 48px'), '48px min-height must be enforced in mobile CSS');
  assert.ok(htmlContent.includes('min-width: 48px'), '48px min-width must be enforced in mobile CSS');

  const { elements, vibrateCalls, runExpr } = extractScriptAndRun();
  runExpr('copyConduta(0)');
  assert.equal(vibrateCalls.length, 1, 'navigator.vibrate must be called on copyConduta');
  assert.deepEqual(Array.from(vibrateCalls[0]), [40], 'navigator.vibrate([40]) must be triggered');
  assert.equal(elements.toastMsg.textContent, '✅ Conduta copiada com sucesso!');
});

test('Desktop Workstation Refactor, Column Resizers & Weight Calculator Exclusion', () => {
  // Verify workstation grid CSS & anti-slop clinical palette
  assert.ok(htmlContent.includes('grid-template-columns: var(--sidebar-width, 232px) var(--list-width, 460px) 6px minmax(360px, 1fr)'), 'Must define workstation columns with fixed sidebar and resizable list splitter');
  assert.equal(htmlContent.includes('id="resizerSidebar"'), false, 'First column must be fixed in width without #resizerSidebar');
  assert.ok(htmlContent.includes('id="resizerList"'), 'Must include #resizerList drag splitter');
  assert.ok(htmlContent.includes('.power-action-btn'), 'Must style .power-action-btn in top-right cockpit bar');
  assert.ok(htmlContent.includes('#0b0e14'), 'Must include #0b0e14 deep clinical slate');
  assert.ok(htmlContent.includes('#111620'), 'Must include #111620 clinical surface');
  assert.ok(htmlContent.includes('#182030'), 'Must include #182030 elevated surface');
  assert.ok(htmlContent.includes('#10b981'), 'Must include #10b981 Monitor Green');
  assert.ok(htmlContent.includes('#f59e0b'), 'Must include #f59e0b Alert Amber');
  assert.ok(htmlContent.includes('#ef4444'), 'Must include #ef4444 Critical Red');
  assert.ok(htmlContent.includes('#0284c7'), 'Must include #0284c7 Technical Cyan');

  // Verify Weight Calculator is completely removed
  assert.equal(htmlContent.includes('quickWeightInput'), false, 'quickWeightInput must be completely removed');
  assert.equal(htmlContent.includes('dosesOverlay'), false, 'dosesOverlay must be completely removed');
  assert.equal(htmlContent.includes('openDosesModal'), false, 'openDosesModal must be completely removed');
  assert.equal(htmlContent.includes('Calculadora Peso'), false, 'Calculadora Peso button must be removed');

  // Verify J/K navigation, 1/2/3 copy, column resizing, and Modo Consulta vs Modo Treino
  const { sandbox, elements, runExpr } = extractScriptAndRun();
  assert.equal(runExpr('selectedProtocolIndex'), 0, 'Protocol 0 must be selected by default on startup');

  // Test interactive column resizing
  const updatedWidths = sandbox.window.setColumnWidths({ sidebarWidth: 260, listWidth: 540 });
  assert.equal(updatedWidths.sidebarWidth, 260);
  assert.equal(updatedWidths.listWidth, 540);
  assert.equal(sandbox.document.documentElement.style._props['--sidebar-width'], '260px');
  assert.equal(sandbox.document.documentElement.style._props['--list-width'], '540px');

  const resetWidths = sandbox.window.resetColumnWidths();
  assert.equal(resetWidths.sidebarWidth, 232);
  assert.equal(resetWidths.listWidth, 460);

  const nextIdx = runExpr('navigateProtocolList(1)');
  assert.equal(nextIdx, 1, 'navigateProtocolList(1) (J / ArrowDown) must advance to protocol 1');
  assert.equal(runExpr('currentDrawerIndex'), 1, 'Cockpit right column must display protocol 1');

  const prevIdx = runExpr('navigateProtocolList(-1)');
  assert.equal(prevIdx, 0, 'navigateProtocolList(-1) (K / ArrowUp) must return to protocol 0');

  // Test 1, 2, 3 power copy actions
  runExpr('triggerPowerCopy(1)');
  assert.equal(elements.toastMsg.textContent, '✅ Snippet completo copiado com sucesso!');

  runExpr('triggerPowerCopy(2)');
  assert.equal(elements.toastMsg.textContent, '✅ Conduta copiada com sucesso!');

  runExpr('triggerPowerCopy(3)');
  assert.equal(elements.toastMsg.textContent, '✅ Receita copiada com sucesso!');

  // Test Modo Consulta vs Modo Treino
  runExpr("setWorkstationMode('treino')");
  assert.equal(runExpr('workstationMode'), 'treino');
  assert.equal(runExpr('currentDrawerTab'), 'interactive', 'Treino mode must switch PEP protocol to interactive tab');

  runExpr("setWorkstationMode('consulta')");
  assert.equal(runExpr('workstationMode'), 'consulta');
  assert.equal(runExpr('currentDrawerTab'), 'pep', 'Consulta mode must switch PEP protocol back to full snippet tab');

  // Test (?) Shortcuts modal
  runExpr('openShortcutsModal()');
  assert.equal(elements.shortcutsOverlay.classList.contains('open'), true, 'openShortcutsModal must open shortcuts modal');
  assert.equal(elements.shortcutsOverlay.classList.contains('open'), true);
  runExpr('closeShortcutsModal()');
  assert.equal(elements.shortcutsOverlay.classList.contains('open'), false, 'closeShortcutsModal must close shortcuts modal');
});

test('Preceptor V2.0 Audit: All 19 Clinical Skills cards upgraded in 05_Habilidades_Clinicas, snippets_hab.json, and index.html', () => {
  const { runExpr } = extractScriptAndRun();
  const allData = Array.from<any>(runExpr('allData'));
  const habItems = allData.filter((d: any) => d.mod_id === 'hab');
  assert.equal(habItems.length, 19, 'Must have all 19 Clinical Skills cards in index.html');

  const habJsonPath = path.resolve(process.cwd(), 'snippets/snippets_hab.json');
  const habJson = JSON.parse(fs.readFileSync(habJsonPath, 'utf8'));
  assert.equal(habJson.length, 19, 'snippets_hab.json must have 19 cards');

  for (const item of habItems) {
    assert.ok(item.trigger && item.trigger.startsWith(';hab-'), `Card ${item.id} must have a ;hab-* trigger`);
    assert.ok(item.anchor && item.anchor.length > 20, `Card ${item.id} must have a V2.0 anchor sequence`);
    assert.ok(item.pre_porta && item.pre_porta.includes('1. O QUE NÃO ESQUECER'), `Card ${item.id} pre_porta must include V2.0 Preceptor structure`);
    assert.ok(item.pre_porta.includes('COMO REGISTRAR NO PRONTUÁRIO'), `Card ${item.id} pre_porta must include ready-to-copy clinical record`);
    assert.ok(Array.isArray(item.checklist_sections) && item.checklist_sections.length >= 3, `Card ${item.id} must have structured checklist sections`);
    const hasV2Section = item.checklist_sections.some((s: any) => s.title.includes('Upgrade Preceptor V2.0'));
    assert.equal(hasV2Section, true, `Card ${item.id} must include Upgrade Preceptor V2.0 checklist section`);
    assert.ok(Array.isArray(item.pitfalls) && item.pitfalls.length >= 4, `Card ${item.id} must have Red Flags + Pitfalls populated`);

    // Verify corresponding markdown file on disk
    const mdFull = path.resolve(process.cwd(), item.path);
    const mdText = fs.readFileSync(mdFull, 'utf8');
    assert.ok(mdText.includes('## 🎯 1. O QUE NÃO ESQUECER'), `${item.path} must have V2.0 section 1`);
    assert.ok(mdText.includes('## 🧠 2. MNEMÔNICO / REGRA DE OURO'), `${item.path} must have V2.0 section 2`);
    assert.ok(mdText.includes('## 🛠️ 3. COREOGRAFIA / PASSO A PASSO TÉCNICO'), `${item.path} must have V2.0 section 3`);
    assert.ok(mdText.includes('## 🚨 4. RED FLAGS'), `${item.path} must have V2.0 section 4`);
    assert.ok(mdText.includes('## 📝 5. COMO REGISTRAR NO PRONTUÁRIO'), `${item.path} must have V2.0 section 5`);
    assert.ok(mdText.includes('## ⚠️ 6. ARMADILHAS DO INTERNO'), `${item.path} must have V2.0 section 6`);
    assert.ok(mdText.includes('## ✅ 7. CHECKLIST PÓS-ATENDIMENTO'), `${item.path} must have V2.0 section 7`);
  }
});

test('Padrão Ouro PEP v2.0: All 74 PEP protocols (15 GO + 42 UPA + 7 Enfermaria + 10 Pediatria) have bipartite Conduta, Diretriz/Guia, and 49 Outpatient Receitas', () => {
  const { runExpr } = extractScriptAndRun();
  const allData = Array.from<any>(runExpr('allData'));
  const pepItems = allData.filter((d: any) => d.mod_id !== 'hab');
  assert.equal(pepItems.length, 74, 'Must have all 74 PEP protocols in index.html');

  const goItems = pepItems.filter((d: any) => d.mod_id === 'go');
  const upaItems = pepItems.filter((d: any) => d.mod_id === 'upa');
  const enfItems = pepItems.filter((d: any) => d.mod_id === 'enf');
  const pedItems = pepItems.filter((d: any) => d.mod_id === 'ped');

  assert.equal(goItems.length, 15, 'Must have 15 GO protocols');
  assert.equal(upaItems.length, 42, 'Must have 42 UPA protocols');
  assert.equal(enfItems.length, 7, 'Must have 7 Enfermaria protocols');
  assert.equal(pedItems.length, 10, 'Must have 10 Pediatria protocols');

  for (const item of pepItems) {
    assert.equal(item.has_split, true, `PEP protocol ${item.id} (${item.trigger}) must have bipartite # PLANO / CONDUTA split`);
    assert.ok(item.conduta_body && item.conduta_body.length > 250, `PEP protocol ${item.id} must have complete conduta_body`);
    assert.equal(item.has_guia, true, `PEP protocol ${item.id} (${item.trigger}) must have Guia/Diretriz populated`);
    assert.ok(item.guia_body && item.guia_body.length > 400, `PEP protocol ${item.id} must have substantive guia_body`);
  }

  // All 10 Pediatria protocols must have weight-based outpatient/discharge Receitas
  for (const item of pedItems) {
    assert.equal(item.has_receita, true, `Pediatria protocol ${item.id} (${item.trigger}) must have Receita Domiciliar / Alta`);
    assert.ok(item.receita_body && item.receita_body.length > 250, `Pediatria protocol ${item.id} must have complete receita_body`);
  }

  const totalReceitas = pepItems.filter((d: any) => d.has_receita && d.receita_body.length > 250).length;
  assert.ok(totalReceitas >= 49, `Expected at least 49 PEP protocols with complete Receita Domiciliar / Alta, found ${totalReceitas}`);
});

test('Personalizar v2.0 Engine: Balanced brackets, zero DD/MM/AAAA choice splits, and clean choice groups across all 74 PEP protocols', () => {
  const { runExpr } = extractScriptAndRun();
  const allData = Array.from<any>(runExpr('allData'));
  const pepItems = allData.filter((d: any) => d.mod_id !== 'hab');

  // Verify DD/MM/AAAA and DD/MM are never split into choices
  const dateFullChoices = Array.from<string>(runExpr("splitTopLevelChoices('DD/MM/AAAA')"));
  assert.deepEqual(dateFullChoices, ['DD/MM/AAAA'], 'DD/MM/AAAA must never be split into DD, MM, AAAA pills');

  const dateShortChoices = Array.from<string>(runExpr("splitTopLevelChoices('DD/MM')"));
  assert.deepEqual(dateShortChoices, ['DD/MM'], 'DD/MM must never be split into DD, MM pills');

  // Verify nested brackets inside options are kept intact by parseBalancedBrackets + splitTopLevelChoices
  const usgChoices = Array.from<string>(
    runExpr("splitTopLevelChoices('Solicitada hoje / Realizada em [DD/MM] com CCN de [ ] mm = IG USG: [ ]s[ ]d')")
  );
  assert.deepEqual(usgChoices, [
    'Solicitada hoje',
    'Realizada em [DD/MM] com CCN de [ ] mm = IG USG: [ ]s[ ]d'
  ]);

  // Verify every bracket across all 74 PEP protocols parses cleanly with zero DD/MM/AAAA or '...' pills
  for (const item of pepItems) {
    const lines = String(item.pep_body).split('\n');
    for (const line of lines) {
      const escaped = JSON.stringify(line);
      const tokens = Array.from<any>(runExpr(`parseBalancedBrackets(${escaped})`));
      for (const tok of tokens) {
        if (tok.type === 'bracket') {
          const choices = Array.from<string>(runExpr(`splitTopLevelChoices(${JSON.stringify(tok.inner)})`));
          if (choices.length > 1) {
            for (const ch of choices) {
              assert.notEqual(ch, 'DD', `Protocol ${item.id} must not produce a 'DD' choice pill in line: ${line}`);
              assert.notEqual(ch, 'MM', `Protocol ${item.id} must not produce a 'MM' choice pill in line: ${line}`);
              assert.notEqual(ch, 'AAAA', `Protocol ${item.id} must not produce an 'AAAA' choice pill in line: ${line}`);
              assert.notEqual(ch, '...', `Protocol ${item.id} must not produce a '...' choice pill in line: ${line}`);
            }
          }
        }
      }
    }
  }
});

test('Editorial Diretrizes & Raciocínio Clínico: Formatted HTML renderer and structured "Por Quê" sections across all 74 PEP protocols', () => {
  assert.ok(htmlContent.includes('id="drawerGuiaPanel"'), 'Must include dedicated #drawerGuiaPanel for formatted Diretrizes');
  assert.ok(htmlContent.includes('class="guia-section-card'), 'Must define .guia-section-card editorial styling');

  const { runExpr } = extractScriptAndRun();
  const allData = Array.from<any>(runExpr('allData'));
  const pepItems = allData.filter((d: any) => d.mod_id !== 'hab');

  // Verify inline formatter converts bold, code pills, and LaTeX clinical symbols cleanly
  const formatted = String(runExpr("formatGuiaInlineHtml('Diluir `$MgSO_4$` **4 g** $\\\\rightarrow$ `100 mL/h`')"));
  assert.ok(formatted.includes('<code class="guia-inline-code">MgSO₄</code>'), 'Must format inline code and MgSO4 symbol');
  assert.ok(formatted.includes('<strong class="guia-strong">4 g</strong>'), 'Must format bold text');
  assert.ok(formatted.includes('→'), 'Must convert LaTeX rightarrow to →');

  // Verify all 74 PEP protocols have multi-section structured Diretrizes explaining "Por Que"
  for (const item of pepItems) {
    assert.ok(item.guia_body.includes('### '), `Protocol ${item.id} must have structured ### sections in guia_body`);
    assert.ok(
      item.guia_body.includes('Por Que') || item.guia_body.includes('Por quê') || item.guia_body.includes('Por que'),
      `Protocol ${item.id} must explain clinical rationale ("Por Que") in guia_body`
    );
    assert.equal(item.guia_body.includes('```mermaid'), false, `Protocol ${item.id} must not contain raw mermaid code in guia_body`);
    assert.equal(item.guia_body.includes('[!IMPORTANT]'), false, `Protocol ${item.id} must not contain raw GitHub callout syntax in guia_body`);
  }
});

test('Personalizar v3.0 & Modular Architecture: Sub-inputs restored, 49 Receitas unified in pep_body, weight-based dose helper, and /src modules', () => {
  // 1. Verify modular /src architecture files exist
  const requiredModules = [
    'src/styles/cockpit.css',
    'src/data/clinical_data.ts',
    'src/engine/personalizar.ts',
    'src/engine/diretrizes.ts',
    'src/engine/search.ts',
    'src/engine/workstation.ts'
  ];
  for (const relPath of requiredModules) {
    const full = path.resolve(process.cwd(), relPath);
    assert.equal(fs.existsSync(full), true, `Modular file ${relPath} must exist`);
  }

  const { sandbox, runExpr } = extractScriptAndRun();
  const allData = Array.from<any>(runExpr('allData'));
  const pepItems = allData.filter((d: any) => d.mod_id !== 'hab');

  // 2. Verify zero stripped choice brackets ([Nega /], [Ausente //10 min], or choice options ending with ':')
  for (const item of pepItems) {
    assert.equal(item.pep_body.includes('[Nega /]'), false, `Protocol ${item.id} must not have stripped [Nega /]`);
    assert.equal(item.pep_body.includes('//10 min]'), false, `Protocol ${item.id} must not have stripped //10 min]`);
    const lines = String(item.pep_body).split('\n');
    for (const line of lines) {
      const tokens = Array.from<any>(runExpr(`parseBalancedBrackets(${JSON.stringify(line)})`));
      for (const tok of tokens) {
        if (tok.type === 'bracket') {
          const choices = Array.from<string>(runExpr(`splitTopLevelChoices(${JSON.stringify(tok.inner)})`));
          if (choices.length > 1) {
            for (const ch of choices) {
              assert.equal(ch.trim().endsWith(':'), false, `Choice option "${ch}" in protocol ${item.id} must include an inline [ ] sub-input after colon`);
            }
          }
        }
      }
    }
  }

  // 3. Verify all 49 protocols with has_receita: true have their prescription unified inside pep_body
  const receitaItems = pepItems.filter((d: any) => d.has_receita);
  assert.ok(receitaItems.length >= 49, 'Must have at least 49 protocols with has_receita: true');
  for (const item of receitaItems) {
    assert.ok(
      /PRESCRIÇÃO DOMICILIAR|PRESCRIÇÃO DE ALTA|RECEITA DE ALTA|PRESCRIÇÃO MÉDICA AMBULATORIAL/i.test(item.pep_body),
      `Protocol ${item.id} (${item.title}) with has_receita: true must include its prescription section inside pep_body for Personalizar customization`
    );
  }

  // 4. Verify inline weight-based dose calculator helper in Personalizar v3.0
  const doses12kg = sandbox.window.computeWeightBasedDoses(12);
  assert.ok(doses12kg, 'computeWeightBasedDoses(12) must return calculated doses');
  assert.equal(doses12kg.dipironaGotas, 10, '12 kg Dipirona gotas (500mg/mL) must be 10 gotas');
  assert.equal(doses12kg.dipironaMg, 240, '12 kg Dipirona mg (20 mg/kg) must be 240 mg');
  assert.equal(doses12kg.paracetamolGotas, 12, '12 kg Paracetamol gotas (200mg/mL) must be 12 gotas');
  assert.equal(doses12kg.ibuprofenoGotas100, 12, '12 kg Ibuprofeno 100mg/mL must be 12 gotas');
  assert.equal(doses12kg.amoxi50Ml8h, '4,0', '12 kg Amoxicilina 50mg/kg/dia (250mg/5mL) must be 4,0 mL de 8/8h');
  assert.equal(doses12kg.amoxi90Ml12h, '6,8', '12 kg Amoxicilina 90mg/kg/dia (400mg/5mL) must be 6,8 mL de 12/12h');
  assert.equal(doses12kg.prednisolonaMlDia, '4,0', '12 kg Prednisolona 1mg/kg/dia (3mg/mL) must be 4,0 mL/dia');
  assert.equal(typeof sandbox.window.focusNextEmptyInteractiveInput, 'function', 'focusNextEmptyInteractiveInput must be exposed on window');
});



test('Compositor Modular de Prescrição: Carrinho de Prescrição em 1 Clique (#tabCartBtn, #btnAddToCart, #drawerCartPanel)', () => {
  const html = fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf-8');
  assert.ok(html.includes('id="btnAddToCart"'), 'Must include #btnAddToCart button in drawer footer');
  assert.ok(html.includes('id="tabCartBtn"'), 'Must include #tabCartBtn tab in drawer tabs');
  assert.ok(html.includes('id="drawerCartPanel"'), 'Must include #drawerCartPanel dedicated UI panel');
  assert.ok(html.includes('function addCustomItemToCart'), 'Must define addCustomItemToCart function in JS');
  assert.ok(html.includes('function copyPrescriptionCart'), 'Must define copyPrescriptionCart function in JS');
});
