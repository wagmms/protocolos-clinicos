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
  // Verify 3-column resizable grid CSS & anti-slop clinical palette
  assert.ok(htmlContent.includes('grid-template-columns: var(--sidebar-width, 232px) 6px var(--list-width, 460px) 6px minmax(360px, 1fr)'), 'Must define 3 resizable desktop columns with draggable splitters');
  assert.ok(htmlContent.includes('id="resizerSidebar"'), 'Must include #resizerSidebar drag splitter');
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
  runExpr('closeShortcutsModal()');
  assert.equal(elements.shortcutsOverlay.classList.contains('open'), false, 'closeShortcutsModal must close shortcuts modal');
});
