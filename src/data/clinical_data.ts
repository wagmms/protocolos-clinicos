// ============================================================================
// REPOSITÓRIO TIPADO DOS 93 CARTÕES CLÍNICOS (74 PEP + 19 HABILIDADES)
// ============================================================================

export interface ChecklistItem {
  id: string;
  text: string;
}

export interface ChecklistSection {
  title: string;
  items: ChecklistItem[];
}

export interface PitfallItem {
  title: string;
  detail: string;
}

export interface ClinicalProtocolItem {
  id: string;
  mod_id: 'go' | 'upa' | 'enf' | 'ped' | 'hab';
  module_name: string;
  badge: string;
  title: string;
  trigger: string;
  all_triggers: string[];
  category: string;
  path: string;
  pep_body?: string;
  has_split?: boolean;
  evolucao_body?: string;
  conduta_body?: string;
  has_receita?: boolean;
  receita_body?: string;
  has_guia?: boolean;
  guia_body?: string;
  time_goal?: string;
  hab_category?: string;
  anchor?: string;
  pre_porta?: string;
  checklist_sections?: ChecklistSection[];
  pitfalls?: PitfallItem[];
  pitfalls_raw?: string;
  tags_sintomas?: string[];
  symptom_priority?: number;
}

export const MODULE_COUNTS = {
  total: 93,
  pep: 74,
  go: 15,
  upa: 42,
  enf: 7,
  ped: 10,
  hab: 19
} as const;
