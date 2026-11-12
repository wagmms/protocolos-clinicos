// ============================================================================
// RENDERIZADOR EDITORIAL DE DIRETRIZES & RACIOCÍNIO CLÍNICO ("POR QUÊ")
// ============================================================================

export function escapeHtml(str: unknown): string {
  return String(str == null ? '' : str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function formatGuiaInlineHtml(rawStr: unknown): string {
  let s = String(rawStr == null ? '' : rawStr);
  s = s
    .replace(/\$\\rightarrow\$/g, '→')
    .replace(/\$\\leftarrow\$/g, '←')
    .replace(/\$\\ge\$/g, '≥')
    .replace(/\$\\le\$/g, '≤')
    .replace(/\$\\pm\$/g, '±')
    .replace(/\$\\times\$/g, '×')
    .replace(/\$\\beta\$/g, 'β')
    .replace(/\$\\alpha\$/g, 'α')
    .replace(/\$\\gamma\$/g, 'γ')
    .replace(/\$MgSO_4\$/g, 'MgSO₄')
    .replace(/\$PGE_2\$/g, 'PGE₂')
    .replace(/\$PGI_2\$/g, 'PGI₂')
    .replace(/\$Fe\^\{2\+\}\$/g, 'Fe²⁺')
    .replace(/\$Fe\^\{3\+\}\$/g, 'Fe³⁺')
    .replace(/\$O_2\$/g, 'O₂')
    .replace(/\$CO_2\$/g, 'CO₂')
    .replace(/\$10\^5\$/g, '10⁵')
    .replace(/\$([^$]+)\$/g, '$1');

  const codeTokens: string[] = [];
  s = s.replace(/`([^`]+)`/g, (_, codeContent) => {
    const idx = codeTokens.length;
    codeTokens.push(`<code class="guia-inline-code">${escapeHtml(codeContent)}</code>`);
    return `\u0000CODE_${idx}\u0000`;
  });

  s = escapeHtml(s);
  s = s.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong class="guia-strong"><em class="guia-em">$1</em></strong>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong class="guia-strong">$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em class="guia-em">$1</em>');
  s = s.replace(/\u0000CODE_(\d+)\u0000/g, (_, idx) => codeTokens[Number(idx)] || '');
  return s;
}

export function classifyGuiaSectionTheme(title: string): { cls: string; tag: string } {
  const t = String(title || '').toLowerCase();
  if (t.includes('proibid') || t.includes('não ') || t.includes('nao ') || t.includes('armadilha') || t.includes('trava') || t.includes('erro') || t.includes('🚫')) {
    return { cls: 'theme-danger', tag: 'Segurança & Travas' };
  }
  if (t.includes('prescrev') || t.includes('farmacolog') || t.includes('antibiót') || t.includes('antibiot') || t.includes('uterotôn') || t.includes('magnésio') || t.includes('suplement') || t.includes('💊') || t.includes('💉')) {
    return { cls: 'theme-pharma', tag: 'Farmacologia & Doses' };
  }
  if (t.includes('tabela') || t.includes('critério') || t.includes('criterio') || t.includes('checklist') || t.includes('cronograma') || t.includes('classifica') || t.includes('interpreta') || t.includes('🧭') || t.includes('🪡') || t.includes('📐')) {
    return { cls: 'theme-criteria', tag: 'Critérios & Decisão' };
  }
  return { cls: 'theme-why', tag: 'Fisiopatologia & Porquê' };
}
