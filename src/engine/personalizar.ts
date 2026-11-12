// ============================================================================
// MOTOR INTERATIVO PEP v3.0 (Personalizar com Sub-Inputs, Cache de Sessão,
// Opções Exclusivas de Receita, Cálculo Ponderal Inline, Nägele e IMC)
// ============================================================================

export interface BracketToken {
  type: 'text' | 'bracket';
  raw: string;
  inner?: string;
}

export interface WeightDoseSummary {
  weightKg: number;
  dipironaAllowed: boolean;
  dipironaGotas: number;
  dipironaMlSolucao: string;
  dipironaMg: number;
  paracetamolGotas: number;
  paracetamolMg: number;
  ibuprofenoAllowed: boolean;
  ibuprofenoGotas100: number;
  ibuprofenoGotas50: number;
  ibuprofenoMg: number;
  ondansetronaMg: string;
  ondansetronaMlEv: string;
  amoxi50Ml8h: string;
  amoxi90Ml12h: string;
  prednisolonaMlDia: string;
  prednisolonaMgDia: number;
  dexametasonaCrupeMg: string;
  midazolamImEvMg: string;
}

export function parseBalancedBrackets(str: string): BracketToken[] {
  const tokens: BracketToken[] = [];
  let i = 0;
  let textStart = 0;
  const n = str.length;

  while (i < n) {
    if (str[i] === '[') {
      let depth = 1;
      let j = i + 1;
      while (j < n && depth > 0) {
        if (str[j] === '[') depth++;
        else if (str[j] === ']') depth--;
        j++;
      }
      if (depth === 0) {
        if (i > textStart) {
          tokens.push({ type: 'text', raw: str.slice(textStart, i) });
        }
        const rawBracket = str.slice(i, j);
        const inner = str.slice(i + 1, j - 1);
        tokens.push({ type: 'bracket', raw: rawBracket, inner });
        i = j;
        textStart = i;
        continue;
      }
    }
    i++;
  }
  if (textStart < n) {
    tokens.push({ type: 'text', raw: str.slice(textStart) });
  }
  return tokens;
}

export function splitTopLevelChoices(inner: string): string[] {
  const trimmed = inner.trim();
  if (/^(?:DD\/MM\/AAAA|DD\/MM|MM\/AAAA|HH:MM)$/i.test(trimmed)) {
    return [trimmed];
  }
  if (/^(?:SE\s+|Se\s+|Opcional\b|OPÇÃO\s+|MODALIDADE\s+|1ª\s*ESCOLHA|2ª\s*ESCOLHA|OU\s+|Escolha\s+|NÃO\s+PRESCREVER|CONTRAINDICAD)/i.test(trimmed)) {
    return [trimmed];
  }

  const parts: string[] = [];
  let bDepth = 0;
  let pDepth = 0;
  let curStart = 0;
  const n = inner.length;

  for (let i = 0; i < n; i++) {
    const ch = inner[i];
    if (ch === '[') bDepth++;
    else if (ch === ']' && bDepth > 0) bDepth--;
    else if (ch === '(') pDepth++;
    else if (ch === ')' && pDepth > 0) pDepth--;

    if (bDepth === 0 && pDepth === 0) {
      if (inner.slice(i, i + 3) === ' / ' || inner.slice(i, i + 3) === ' | ') {
        parts.push(inner.slice(curStart, i).trim());
        curStart = i + 3;
        i += 2;
      }
    }
  }
  parts.push(inner.slice(curStart).trim());

  const filtered = parts.filter(Boolean);
  if (filtered.length > 1) return filtered;

  if (/^[a-zA-ZÀ-ÿ]{4,}\/[a-zA-ZÀ-ÿ]{4,}$/.test(trimmed)) {
    return trimmed.split('/');
  }

  return [trimmed];
}

export function computeWeightBasedDoses(weightKg: number): WeightDoseSummary | null {
  if (!Number.isFinite(weightKg) || weightKg < 2 || weightKg > 150) return null;

  // Dipirona (ANVISA/SBP: contraindicada em < 3 meses ou < 5 kg; dose 15-25 mg/kg/dose, média 20 mg/kg)
  const dipironaAllowed = weightKg >= 5;
  const dipironaMg = Math.min(1000, Math.round(weightKg * 20));
  const dipironaGotas = Math.min(40, Math.round(weightKg * 0.8));
  const dipironaMlSolucao = Math.min(20, (weightKg * 20) / 50).toFixed(1).replace('.', ',');

  // Paracetamol 200 mg/mL (SBP/AAP: 10-15 mg/kg/dose; 1 gota ≈ 13-15 mg => 1 gota/kg, máx 50 gotas = 750 mg)
  const paracetamolMg = Math.min(750, Math.round(weightKg * 13));
  const paracetamolGotas = Math.min(50, Math.round(weightKg * 1));

  // Ibuprofeno (SBP/AAP: evitar em < 6 meses / < 7 kg; dose 10 mg/kg/dose 8/8h, máx 400 mg/dose)
  const ibuprofenoAllowed = weightKg >= 7;
  const ibuprofenoMg = Math.min(400, Math.round(weightKg * 10));
  const ibuprofenoGotas100 = Math.min(40, Math.round(weightKg * 1));
  const ibuprofenoGotas50 = Math.min(80, Math.round(weightKg * 2));

  // Ondansetrona (SBP/OMS/PALS: 0,15 mg/kg/dose, máx 8 mg)
  const ondaMgVal = Math.min(8, weightKg * 0.15);
  const ondansetronaMg = ondaMgVal.toFixed(1).replace('.', ',');
  const ondansetronaMlEv = (ondaMgVal / 2).toFixed(1).replace('.', ',');

  // Amoxicilina 50 mg/kg/dia dividida de 8/8h na suspensão de 250 mg/5 mL (50 mg/mL) => peso / 3 mL por dose (teto 10 mL = 500 mg/dose)
  const amoxi50Ml8h = Math.min(10, weightKg / 3).toFixed(1).replace('.', ',');
  // Amoxicilina 90 mg/kg/dia dividida de 12/12h na suspensão de 400 mg/5 mL (80 mg/mL) => (peso * 90 / 160) mL por dose (teto suspensão 12,5 mL = 1.000 mg/dose)
  const amoxi90Ml12h = Math.min(12.5, (weightKg * 90) / 160).toFixed(1).replace('.', ',');

  // Prednisolona 1 mg/kg/dia na solução de 3 mg/mL => peso / 3 mL 1x/dia (teto pediátrico GINA/SBP: 40 mg/dia = 13,3 mL/dia)
  const prednisolonaMgDia = Math.min(40, Math.round(weightKg * 1));
  const prednisolonaMlDia = Math.min(13.3, weightKg / 3).toFixed(1).replace('.', ',');

  // Dexametasona Crupe (0,15 a 0,6 mg/kg dose única, máx 10 mg) e Midazolam Crise Convulsiva (0,2 mg/kg IM/EV, máx 10 mg)
  const dexametasonaCrupeMg = Math.min(10, weightKg * 0.6).toFixed(1).replace('.', ',');
  const midazolamImEvMg = Math.min(10, weightKg * 0.2).toFixed(1).replace('.', ',');

  return {
    weightKg,
    dipironaAllowed,
    dipironaGotas,
    dipironaMlSolucao,
    dipironaMg,
    paracetamolGotas,
    paracetamolMg,
    ibuprofenoAllowed,
    ibuprofenoGotas100,
    ibuprofenoGotas50,
    ibuprofenoMg,
    ondansetronaMg,
    ondansetronaMlEv,
    amoxi50Ml8h,
    amoxi90Ml12h,
    prednisolonaMlDia,
    prednisolonaMgDia,
    dexametasonaCrupeMg,
    midazolamImEvMg
  };
}

