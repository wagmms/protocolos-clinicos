// ============================================================================
// MOTOR DE BUSCA SEMÂNTICA POR QUEIXA / SINTOMAS & FILTROS (Ctrl+K)
// ============================================================================

export function normalizeSearchText(str: unknown): string {
  return String(str || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();
}

export interface SymptomMatch {
  tag: string;
  level: number;
  isDirect: boolean;
}

export function findMatchedSymptom(
  item: { _tags_norm?: Array<{ raw: string; norm: string; isDirect: boolean }> },
  qNorm: string
): SymptomMatch | null {
  if (!qNorm || !item._tags_norm || item._tags_norm.length === 0) return null;
  let best: SymptomMatch | null = null;
  let bestScore = 0;

  for (let i = 0; i < item._tags_norm.length; i++) {
    const entry = item._tags_norm[i];
    let level = 0;
    if (entry.norm === qNorm) {
      level = 3;
    } else if (entry.norm.startsWith(qNorm) || (qNorm.length >= 4 && qNorm.startsWith(entry.norm))) {
      level = 2;
    } else if (entry.norm.includes(qNorm)) {
      level = 1;
    }
    if (level > 0) {
      const candidateScore = level * 10 + (entry.isDirect ? 5 : 0);
      if (candidateScore > bestScore) {
        bestScore = candidateScore;
        best = { tag: entry.raw, level, isDirect: entry.isDirect };
      }
    }
  }

  return best;
}
