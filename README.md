# 🩺 Sistema Protocolar de Atendimento Médico & Snippets para PEP

[![Deploy Cockpit to GitHub Pages](https://github.com/wagmms/protocolos-clinicos/actions/workflows/deploy.yml/badge.svg)](https://github.com/wagmms/protocolos-clinicos/actions/workflows/deploy.yml)
[![Cockpit Online](https://img.shields.io/badge/Cockpit_Online-Acessar_Agora-0284c7?style=flat&logo=safari&logoColor=white)](https://wagmms.github.io/protocolos-clinicos/)

🌐 **Acesse o Cockpit Online de Qualquer Lugar:** **[https://wagmms.github.io/protocolos-clinicos/](https://wagmms.github.io/protocolos-clinicos/)**

Biblioteca médica estruturada, defensiva e padronizada para atendimento clínico, registros em Prontuário Eletrônico do Paciente (PEP: MV, Tasy, Vivver, e-SUS) e discussão de casos em rounds.

**Total de Modelos Prontos:** **74 protocolos médicos de alta performance** com negativas médico-legais, receitas estruturadas, doses ponderais instantâneas, bundles de segurança (FAST HUG BID), condutas de bolso e cópia segmentada (16 protocolos arquivados em `_arquivados/`).

---

## ⚡ Como Usar no Dia a Dia

### Método 1: Cockpit Web High-End (Online & Offline)
Acesse via navegador em **[https://wagmms.github.io/protocolos-clinicos/](https://wagmms.github.io/protocolos-clinicos/)** ou abra localmente o arquivo [`index.html`](index.html) / [`painel_rapido_snippets.html`](painel_rapido_snippets.html):
- **Cópia Segmentada em 3 Níveis:** Botões dedicados para `Copiar Tudo`, `💉 Conduta` (apenas a conduta/prescrição imediata de emergência) e `💊 Receita` (receita estruturada com posologias).
- **Personalizador com Chips Interativos:** Clique nas opções `[Opção A / Opção B]` diretamente nos chips visuais na aba *"⚡ Personalizar & Chips"* para ajustar a conduta antes de copiar para o prontuário.
- **Calculadora de Doses por Peso na Topbar:** Insira o peso do paciente (`Peso: [ 70 ] kg`) e acesse instantaneamente doses calculadas de Sepse (30 mL/kg), Dengue C (10 mL/kg/h), Alteplase (0,9 mg/kg), Enoxaparina (1 mg/kg vs 0,75 mg/kg em idosos), Drogas de Intubação (SRI), Dipirona e Paracetamol gotas.
- **Command Palette Global (`Ctrl + K` ou `/`):** Pressione `Ctrl + K` em qualquer tela para abrir a busca instantânea tipo Spotlight, navegar com as setas e copiar o protocolo com `Enter` (ou abrir diretamente cartões da aba `🧠 Habilidades`).
- **Aba Dedicada `🧠 Habilidades` (19 Cartões Pré-Porta 30s — 100% Isolada dos 90 PEP):**
  - Localizada em [`05_Habilidades_Clinicas/`](05_Habilidades_Clinicas/), separada da aba `🌐 Geral`, de `snippets/snippets_todos.json` e dos arquivos Espanso (os 90 modelos de PEP não são alterados).
  - Ao abrir um cartão na aba **`🧠 Habilidades`** (ou via `Ctrl + K` marcado como `🧠 Habilidade`), o Drawer exibe 3 abas dedicadas:
    1. **`⚡ Pré-Porta 30s`:** meta de tempo, âncora mnemônica em destaque e roteiro escaneável no celular antes de entrar no atendimento.
    2. **`✅ Checklist Pós-Atendimento`:** checkboxes persistidos em `localStorage`, contador `X/Y executados` com barra de progresso, painel ao vivo **"Pontos Cegos / Itens Esquecidos"**, botão **`📋 Copiar Debriefing`** (Markdown pronto para `00_DIARIO_PONTOS_CEGOS.md`) e **`🔄 Resetar p/ Próximo Paciente`**.
    3. **`🚫 Armadilhas & Erros`:** erros críticos que falseiam o exame ou colocam o paciente em risco.
- **100% Responsivo & Offline:** Funciona no computador do plantão, notebook, tablet ou smartphone.

---

## 📋 Tabela Mestra: Pediatria & Puericultura (10 Modelos Ativos)

> *Nota: O Guia Mestre de Doses Ponderais foi arquivado na pasta `_arquivados/04_Pediatria_Puericultura/`.*

| Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- |
| Ficha Mestra Universal de Pediatria (Pronto Atendimento & Ambulatório) | Ficha Mestra e Triagem | [`00_Ficha_Mestra_Universal_Pediatrica.md`](04_Pediatria_Puericultura/01_Ficha_Mestra_e_Triagem/00_Ficha_Mestra_Universal_Pediatrica.md) |
| Consulta de Puericultura & Marcos do DNPM (0 a 24 Meses) | Puericultura e Ambulatorio | [`01_Consulta_Puericultura_Marcos_DNPM.md`](04_Pediatria_Puericultura/02_Puericultura_e_Ambulatorio/01_Consulta_Puericultura_Marcos_DNPM.md) |
| Resfriado Comum & Rinofaringite Aguda Pediátrica | Respiratorio e IVAS | [`01_Resfriado_Comum_e_Obstrucao_Nasal.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/01_Resfriado_Comum_e_Obstrucao_Nasal.md) |
| Bronquiolite Viral Aguda (BVA) no Lactente | Respiratorio e IVAS | [`02_Bronquiolite_Viral_Aguda_BVA.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/02_Bronquiolite_Viral_Aguda_BVA.md) |
| Laringite Aguda & Crupe Viral (Laringotraqueobronquite) | Respiratorio e IVAS | [`03_Laringite_Estridulosa_Crupe_Viral.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/03_Laringite_Estridulosa_Crupe_Viral.md) |
| Otite Média Aguda (OMA) Pediátrica | Respiratorio e IVAS | [`04_Otite_Media_Aguda_Pediatrica.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/04_Otite_Media_Aguda_Pediatrica.md) |
| Pneumonia Adquirida na Comunidade (PAC) Pediátrica | Respiratorio e IVAS | [`05_Pneumonia_Adquirida_na_Comunidade_PAC.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/05_Pneumonia_Adquirida_na_Comunidade_PAC.md) |
| Gastroenterite Aguda (GECA) & Planos de Desidratação da OMS | Gastrointestinal e Desidratacao | [`01_GECA_e_Planos_Desidratacao_OMS.md`](04_Pediatria_Puericultura/04_Gastrointestinal_e_Desidratacao/01_GECA_e_Planos_Desidratacao_OMS.md) |
| Febre sem Foco & Manejo do Lactente Febril | Febre e Infeccoes Sistemicas | [`01_Febre_sem_Foco_e_Lactente_Febril.md`](04_Pediatria_Puericultura/05_Febre_e_Infeccoes_Sistemicas/01_Febre_sem_Foco_e_Lactente_Febril.md) |
| Crise Convulsiva Febril na Infância | Febre e Infeccoes Sistemicas | [`02_Crise_Convulsiva_Febril.md`](04_Pediatria_Puericultura/05_Febre_e_Infeccoes_Sistemicas/02_Crise_Convulsiva_Febril.md) |

---

## 📋 Tabela Mestra: Enfermaria & Internação Hospitalar (7 Modelos Ativos)

> *Nota: 3 modelos (admissão cirúrgica pré/pós, parecer de interconsulta e sumário de alta cirúrgica) foram preservados e arquivados na pasta `_arquivados/03_Enfermaria_Internacao/`.*

| Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- |
| Admissão em Enfermaria de Clínica Médica | Admissao e Avaliacao Inicial | [`01_Admissao_Clinica_Medica.md`](03_Enfermaria_Internacao/01_Admissao_e_Avaliacao_Inicial/01_Admissao_Clinica_Medica.md) |
| Evolução Diária SOAP - Clínica Médica | Evolucao Diaria SOAP | [`01_Evolucao_SOAP_Clinica_Medica.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/01_Evolucao_SOAP_Clinica_Medica.md) |
| Evolução Diária SOAP - Pós-Operatório Cirúrgico | Evolucao Diaria SOAP | [`02_Evolucao_SOAP_Pos_Operatorio.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/02_Evolucao_SOAP_Pos_Operatorio.md) |
| Checklist de Metas Diárias - Bundle FAST HUG BID | Evolucao Diaria SOAP | [`03_Checklist_Metas_FAST_HUG_BID.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/03_Checklist_Metas_FAST_HUG_BID.md) |
| Round Matinal e Passagem de Plantão (Formato SBAR) | Passagem de Plantao e Rounds | [`01_Round_Matinal_e_Passagem_SBAR.md`](03_Enfermaria_Internacao/03_Passagem_de_Plantao_e_Rounds/01_Round_Matinal_e_Passagem_SBAR.md) |
| Sumário de Alta Hospitalar - Clínica Médica | Altas e Desospitalizacao | [`01_Sumario_de_Alta_Clinica_Medica.md`](03_Enfermaria_Internacao/05_Altas_e_Desospitalizacao/01_Sumario_de_Alta_Clinica_Medica.md) |
| Constatação de Óbito Hospitalar & Preenchimento da Declaração de Óbito (DO) | Declaracao de Obito e Cuidados | [`01_Constatacao_de_Obito_e_Checklist_DO.md`](03_Enfermaria_Internacao/06_Declaracao_de_Obito_e_Cuidados/01_Constatacao_de_Obito_e_Checklist_DO.md) |

---

## 📋 Tabela Mestra: Pronto Atendimento / UPA Adulto (42 Modelos)

| Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- |
| Ficha Mestra Universal de Pronto Atendimento (UPA / Pronto-Socorro) | Triagem e Ficha Mestra | [`00_Ficha_Mestra_Universal_UPA.md`](02_Pronto_Atendimento_UPA/01_Triagem_e_Ficha_Mestra/00_Ficha_Mestra_Universal_UPA.md) |
| Resfriado Comum e Rinofaringite Aguda | Infeccoes e Vias Aereas | [`01_Resfriado_e_Rinofaringite.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/01_Resfriado_e_Rinofaringite.md) |
| Faringoamigdalite Aguda | Infeccoes e Vias Aereas | [`02_Faringoamigdalite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/02_Faringoamigdalite_Aguda.md) |
| Otite Média Aguda (OMA) | Infeccoes e Vias Aereas | [`03_Otite_Media_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/03_Otite_Media_Aguda.md) |
| Rinossinusite Aguda Bacteriana | Infeccoes e Vias Aereas | [`04_Sinusite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/04_Sinusite_Aguda.md) |
| Pneumonia Adquirida na Comunidade (PAC) | Infeccoes e Vias Aereas | [`05_Pneumonia_PAC.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/05_Pneumonia_PAC.md) |
| Conjuntivite Aguda (Viral vs Bacteriana) | Infeccoes e Vias Aereas | [`06_Conjuntivite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/06_Conjuntivite_Aguda.md) |
| Dengue e Arboviroses (Classificação MS) | Infeccoes e Vias Aereas | [`07_Dengue_e_Arboviroses.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/07_Dengue_e_Arboviroses.md) |
| Gastroenterite Aguda (GECA) e Desidratação | Gastrointestinal e Abdominal | [`01_GECA_Gastroenterite.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/01_GECA_Gastroenterite.md) |
| Dispepsia Aguda e DRGE | Gastrointestinal e Abdominal | [`02_Dispepsia_e_DRGE.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/02_Dispepsia_e_DRGE.md) |
| Dor Abdominal Aguda e Abdome Agudo Cirúrgico | Gastrointestinal e Abdominal | [`03_Dor_Abdominal_e_Suspeita_Cirurgica.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/03_Dor_Abdominal_e_Suspeita_Cirurgica.md) |
| Hemorragia Digestiva Alta (HDA) | Gastrointestinal e Abdominal | [`04_Hemorragia_Digestiva_Alta_HDA.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/04_Hemorragia_Digestiva_Alta_HDA.md) |
| Hemorroida (Trombose) e Fissura Anal | Gastrointestinal e Abdominal | [`05_Hemorroida_e_Fissura_Anal.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/05_Hemorroida_e_Fissura_Anal.md) |
| Parasitoses Intestinais e Verminoses | Gastrointestinal e Abdominal | [`06_Parasitose_Intestinal.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/06_Parasitose_Intestinal.md) |
| Dor Torácica Aguda e SCA (Protocolo de 10 Minutos) | Cardiovascular e Respiratorio | [`01_Dor_Toracica_e_SCA.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/01_Dor_Toracica_e_SCA.md) |
| Crise Hipertensiva (Urgência vs Emergência) | Cardiovascular e Respiratorio | [`02_Crise_Hipertensiva.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/02_Crise_Hipertensiva.md) |
| Asma Aguda e Crise de Broncoespasmo | Cardiovascular e Respiratorio | [`03_Asma_e_Broncoespasmo.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/03_Asma_e_Broncoespasmo.md) |
| DPOC Exacerbado | Cardiovascular e Respiratorio | [`04_DPOC_Exacerbado.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/04_DPOC_Exacerbado.md) |
| Edema Agudo de Pulmão (EAP) e ICAD | Cardiovascular e Respiratorio | [`05_Insuficiencia_Cardiaca_e_EAP.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/05_Insuficiencia_Cardiaca_e_EAP.md) |
| Cefaleia Aguda e Red Flags (SNOOP10) | Neurologia e Saude Mental | [`01_Cefaleia_Aguda_e_Red_Flags.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/01_Cefaleia_Aguda_e_Red_Flags.md) |
| Vertigem Aguda e Labirintite (Protocolo HINTS) | Neurologia e Saude Mental | [`02_Vertigem_e_Labirintite.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/02_Vertigem_e_Labirintite.md) |
| Crise Convulsiva e Estado de Mal Epiléptico | Neurologia e Saude Mental | [`03_Crise_Convulsiva.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/03_Crise_Convulsiva.md) |
| Crise de Ansiedade e Transtorno de Pânico | Neurologia e Saude Mental | [`04_Crise_de_Ansiedade_Panico.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/04_Crise_de_Ansiedade_Panico.md) |
| Agitação Psicomotora e Surto Psiquiátrico | Neurologia e Saude Mental | [`05_Agitacao_Psicomotora_e_Surto.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/05_Agitacao_Psicomotora_e_Surto.md) |
| Infecção do Trato Urinário (Cistite vs Pielonefrite) | Nefrologia Urologia e Dermatologia | [`01_ITU_Cistite_e_Pielonefrite.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/01_ITU_Cistite_e_Pielonefrite.md) |
| Nefrolitíase e Cólica Renal Aguda | Nefrologia Urologia e Dermatologia | [`02_Nefrolitiase_Colica_Renal.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/02_Nefrolitiase_Colica_Renal.md) |
| Uretrite Aguda Masculina e ISTs | Nefrologia Urologia e Dermatologia | [`03_Uretrite_DST_Masculina.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/03_Uretrite_DST_Masculina.md) |
| Lombalgia Mecânica e Lombociatalgia | Nefrologia Urologia e Dermatologia | [`04_Lombalgia_e_Lombociatalgia.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/04_Lombalgia_e_Lombociatalgia.md) |
| Reação Alérgica, Urticária e Anafilaxia | Nefrologia Urologia e Dermatologia | [`05_Crise_Alergica_e_Urticaria.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/05_Crise_Alergica_e_Urticaria.md) |
| Erisipela, Celulite e Drenagem de Abscesso | Nefrologia Urologia e Dermatologia | [`06_Celulite_Erisipela_e_Abscesso.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/06_Celulite_Erisipela_e_Abscesso.md) |
| Herpes Zoster e Neuralgia Aguda | Nefrologia Urologia e Dermatologia | [`07_Herpes_Zoster.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/07_Herpes_Zoster.md) |
| Escabiose (Sarna Humana) | Nefrologia Urologia e Dermatologia | [`08_Escabiose_Sarna.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/08_Escabiose_Sarna.md) |
| Crise Aguda de Gota e Artrite Gotosa | Nefrologia Urologia e Dermatologia | [`09_Artrite_Gotosa_Gota.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/09_Artrite_Gotosa_Gota.md) |
| Cetoacidose Diabética (CAD) e EHH | Emergencias Graves e Procedimentos | [`01_Cetoacidose_Diabetica_e_EHH.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/01_Cetoacidose_Diabetica_e_EHH.md) |
| Intoxicações Exógenas e Intoxicação Alcoólica Aguda | Emergencias Graves e Procedimentos | [`02_Intoxicacao_Exogena_e_Alcoolica.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/02_Intoxicacao_Exogena_e_Alcoolica.md) |
| Sequência Rápida de Intubação (SRI / IOT) | Emergencias Graves e Procedimentos | [`03_Sequencia_Rapida_de_Intubacao_SRI.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/03_Sequencia_Rapida_de_Intubacao_SRI.md) |
| Parada Cardiorrespiratória (PCR) Adulto & Pós-RCE | Emergencias Graves e Procedimentos | [`04_Parada_Cardiorrespiratoria_PCR.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/04_Parada_Cardiorrespiratoria_PCR.md) |
| **Sepse e Choque Séptico (Pacote da 1ª Hora)** | Emergencias Graves e Procedimentos | [`05_Sepse_e_Choque_Septico_Pacote_1Hora.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/05_Sepse_e_Choque_Septico_Pacote_1Hora.md) |
| **AVC Agudo & AIT (Código AVC & Alteplase rt-PA)** | Emergencias Graves e Procedimentos | [`06_Acidente_Vascular_Cerebral_AVC_e_AIT.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/06_Acidente_Vascular_Cerebral_AVC_e_AIT.md) |
| **Taquiarritmias & Fibrilação Atrial (ACLS)** | Emergencias Graves e Procedimentos | [`07_Taquiarritmias_e_Fibrilacao_Atrial.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/07_Taquiarritmias_e_Fibrilacao_Atrial.md) |
| **Distúrbios Eletrolíticos Graves (HiperK & HipoNa)** | Emergencias Graves e Procedimentos | [`08_Disturbios_Eletroliticos_Hipercalemia_e_Hiponatremia.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/08_Disturbios_Eletroliticos_Hipercalemia_e_Hiponatremia.md) |
| **Pequena Cirurgia: Sutura, Profilaxia de Tétano e Raiva** | Emergencias Graves e Procedimentos | [`09_Trauma_Menor_Sutura_Tetano_e_Raiva.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/09_Trauma_Menor_Sutura_Tetano_e_Raiva.md) |

---

## 📋 Tabela Mestra: Ginecologia & Obstetrícia (15 Modelos Ativos)

> *Nota: 12 modelos cirúrgicos/específicos (admissão/altas de puerpério, parecer de interconsulta, inserção de DIU ambulatorial, cesáreas eletivas, parto instrumentado e AMIU/curetagem) foram preservados e arquivados na pasta `_arquivados/01_Ginecologia_Obstetricia/`.*

| Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- |
| Evolução Diária em Enfermaria de Puerpério | Enfermaria Puerperio | [`02_Puerperio_Evolucao_Diaria.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/02_Puerperio_Evolucao_Diaria.md) |
| Script de Passagem de Caso / Round de Puerpério | Enfermaria Puerperio | [`05_Puerperio_Round_Passagem_de_Caso.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/05_Puerperio_Round_Passagem_de_Caso.md) |
| Ambulatório de Pré-Natal - Primeira Consulta | Ambulatorio GO | [`01_Pre_Natal_Primeira_Consulta.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/01_Pre_Natal_Primeira_Consulta.md) |
| Ambulatório de Pré-Natal - Consulta Subsequente | Ambulatorio GO | [`02_Pre_Natal_Consulta_Subsequente.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/02_Pre_Natal_Consulta_Subsequente.md) |
| Ambulatório de Ginecologia Geral - Consulta de Rotina | Ambulatorio GO | [`03_Ginecologia_Geral_Consulta.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/03_Ginecologia_Geral_Consulta.md) |
| Procedimento Ambulatorial - Inserção de Implanon | Procedimentos Ambulatoriais | [`01_Procedimento_Insercao_Implanon.md`](01_Ginecologia_Obstetricia/03_Procedimentos_Ambulatoriais/01_Procedimento_Insercao_Implanon.md) |
| Procedimento Ambulatorial - Retirada e Troca de Implanon | Procedimentos Ambulatoriais | [`02_Procedimento_Troca_Implanon.md`](01_Ginecologia_Obstetricia/03_Procedimentos_Ambulatoriais/02_Procedimento_Troca_Implanon.md) |
| Descrição de Parto Normal Eutócico (Espontâneo) | Centro Obstetrico Cirurgias | [`04_Parto_Normal_Eutocico.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/04_Parto_Normal_Eutocico.md) |
| Revisão de Canal de Parto e Perineorrafia | Centro Obstetrico Cirurgias | [`06_Revisao_Canal_e_Sutura_Laceracao_Episiotomia.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/06_Revisao_Canal_e_Sutura_Laceracao_Episiotomia.md) |
| Manejo de Emergência - Hemorragia Pós-Parto (Código Vermelho) | Emergencias GO | [`01_Emergencia_Hemorragia_Pos_Parto_HPP.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/01_Emergencia_Hemorragia_Pos_Parto_HPP.md) |
| Manejo de Emergência - Pré-Eclâmpsia Grave e Eclâmpsia | Emergencias GO | [`02_Emergencia_Pre_Eclampsia_Grave_e_Eclampsia.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/02_Emergencia_Pre_Eclampsia_Grave_e_Eclampsia.md) |
| **Manejo de Emergência - Trabalho de Parto Prematuro (TPP)** | Emergencias GO | [`03_Trabalho_de_Parto_Prematuro_TPP.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/03_Trabalho_de_Parto_Prematuro_TPP.md) |
| **Manejo de Emergência - Rotura Prematura de Membranas (RPMO)** | Emergencias GO | [`04_Rotura_Prematura_de_Membranas_RPMO.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/04_Rotura_Prematura_de_Membranas_RPMO.md) |
| **Manejo de Emergência - Doença Inflamatória Pélvica (DIP)** | Emergencias GO | [`05_Doenca_Inflamatoria_Pelvica_DIP.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/05_Doenca_Inflamatoria_Pelvica_DIP.md) |
| **Infecções Puerperais: Mastite Lactacional & Endometrite** | Emergencias GO | [`06_Infeccoes_Puerperais_Mastite_e_Endometrite.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/06_Infeccoes_Puerperais_Mastite_e_Endometrite.md) |

---

## 🔒 Princípios de Segurança & Blindagem Médico-Legal

1. **Rigor Ponderal Estrito na Pediatria e Emergência:**
   - Prescrições pediátricas trazem dose exata por kg de peso (mg/kg/dose, gotas/kg ou mL/dose) e teto máximo por tomada para prevenir intoxicações graves (ex: Paracetamol máx 750mg/tomada e 60mg/kg/dia).
2. **Proscrição de Iatrogenias Consagradas:**
   - Proibição de xaropes mucolíticos/descongestionantes em lactentes; proscrição de beta-agonistas e corticoides de rotina na Bronquiolite Viral Aguda (BVA); proscrição de loperamida na diarreia aguda; proscrição de Ticagrelor na trombólise química de IAM (apenas Clopidogrel); proscrição de Amoxicilina-Clavulanato na RPMO pré-termo (risco de ECN neonatal).
3. **Metas Diárias de Segurança no Leito (FAST HUG BID):**
   - Auditoria diária de dispositivos invasivos (retirar SVD e acessos desnecessários), profilaxia de TEV (Pádua/Caprini), elevação de cabeceira a 30-45°, glicemia alvo (140-180 mg/dL) e desmame racional de antibióticos e protetores gástricos.
4. **Negativas Mandatórias Obrigatórias:**
   - Checagem sistemática dos sinais cardinais de gravidade por cenário clínico (afastar meningite, invaginação, abdome cirúrgico, sepse, choque, tamponamento, infarto e eclâmpsia).
5. **Zero Checkboxes Pré-Assinalados:**
   - Todos os checkboxes em templates copiáveis são `[ ]` em branco, exigindo validação clínica ativa pelo médico e evitando falseamento inadvertido de prontuário eletrônico.
