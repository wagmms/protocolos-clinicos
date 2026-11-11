# 🩺 Sistema Protocolar de Atendimento Médico & Snippets para PEP

Biblioteca médica estruturada, defensiva e padronizada para atendimento clínico, registros em Prontuário Eletrônico do Paciente (PEP: MV, Tasy, Vivver, e-SUS) e discussão de casos em rounds.

**Total de Modelos Prontos:** 81 protocolos de alta performance com negativas médico-legais, receitas estruturadas com doses ponderais (mg/kg e gotas/kg), bundles de segurança (FAST HUG BID) e condutas de bolso.

---

## ⚡ Como Usar no Dia a Dia

### Método 1: Cockpit Web Offline (1 Clique para Copiar)
Abra no navegador o arquivo [`painel_rapido_snippets.html`](painel_rapido_snippets.html):
- **5 Abas de navegação:** Todas as especialidades, Ginecologia & Obstetrícia, UPA Adulto, Enfermaria & Internação ou Pediatria & Puericultura.
- **Filtros rápidos:** Filtragem instantânea por subcategoria clínica (ex: Puericultura, IVAS, Desidratação, Emergências, SOAP).
- **Busca ultra-rápida:** Digite por sintoma, doença, atalho (ex: `;ped-doses`, `;bva`, `;crupe`, `;fasthug`, `;sca`) ou exame.
- **Botões dedicados:** "Copiar PEP" e "Copiar Receita" para transferir diretamente à área de transferência sem formatar nada.
- Funciona 100% offline em qualquer dispositivo (Desktop, notebook do plantão, tablet ou smartphone).

### Método 2: Atalhos Automáticos de Teclado (Espanso)
Se você utiliza o **[Espanso](https://espanso.org/)**:
- **Compilado Geral (81 modelos):** [`snippets/espanso_completo.yml`](snippets/espanso_completo.yml)
- **Pediatria & Puericultura:** [`snippets/ped_espanso.yml`](snippets/ped_espanso.yml)
- **Enfermaria & Internação:** [`snippets/enf_espanso.yml`](snippets/enf_espanso.yml)
- **Pronto Atendimento / UPA:** [`snippets/upa_espanso.yml`](snippets/upa_espanso.yml)
- **Ginecologia & Obstetrícia:** [`snippets/go_espanso.yml`](snippets/go_espanso.yml)
- Basta copiar o arquivo desejado para a pasta de correspondências (`~/.config/espanso/match/` no Linux ou `%APPDATA%\espanso\match\` no Windows).
- Ao digitar o atalho (ex: `;ped-doses`, `;bva` ou `;fasthug`) em qualquer campo de texto ou prontuário, o texto se expande instantaneamente.

### Método 3: Extensões de Navegador (Text Blaze, ProKeys, etc.)
- Arquivos JSON prontos para importação:
  * [`snippets/snippets_todos.json`](snippets/snippets_todos.json) (Todos os 81 modelos)
  * [`snippets/snippets_ped.json`](snippets/snippets_ped.json) (11 modelos de Pediatria)
  * [`snippets/snippets_enf.json`](snippets/snippets_enf.json) (10 modelos de Enfermaria)
  * [`snippets/snippets_upa.json`](snippets/snippets_upa.json) (37 modelos de UPA)
  * [`snippets/snippets_go.json`](snippets/snippets_go.json) (23 modelos de GO)

---

## 📋 Tabela Mestra: Pediatria & Puericultura (11 Modelos)

| Atalho | Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- | :--- |
| `;ped-ficha` | Ficha Mestra Universal de Pediatria (Pronto Atendimento & Ambulatório) | Ficha Mestra e Triagem | [`00_Ficha_Mestra_Universal_Pediatrica.md`](04_Pediatria_Puericultura/01_Ficha_Mestra_e_Triagem/00_Ficha_Mestra_Universal_Pediatrica.md) |
| `;puericultura` | Consulta de Puericultura & Marcos do DNPM (0 a 24 Meses) | Puericultura e Ambulatorio | [`01_Consulta_Puericultura_Marcos_DNPM.md`](04_Pediatria_Puericultura/02_Puericultura_e_Ambulatorio/01_Consulta_Puericultura_Marcos_DNPM.md) |
| `;ped-resfriado` | Resfriado Comum & Rinofaringite Aguda Pediátrica | Respiratorio e IVAS | [`01_Resfriado_Comum_e_Obstrucao_Nasal.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/01_Resfriado_Comum_e_Obstrucao_Nasal.md) |
| `;bva` | Bronquiolite Viral Aguda (BVA) no Lactente | Respiratorio e IVAS | [`02_Bronquiolite_Viral_Aguda_BVA.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/02_Bronquiolite_Viral_Aguda_BVA.md) |
| `;crupe` | Laringite Aguda & Crupe Viral (Laringotraqueobronquite) | Respiratorio e IVAS | [`03_Laringite_Estridulosa_Crupe_Viral.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/03_Laringite_Estridulosa_Crupe_Viral.md) |
| `;ped-otite` | Otite Média Aguda (OMA) Pediátrica | Respiratorio e IVAS | [`04_Otite_Media_Aguda_Pediatrica.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/04_Otite_Media_Aguda_Pediatrica.md) |
| `;ped-pneumonia` | Pneumonia Adquirida na Comunidade (PAC) Pediátrica | Respiratorio e IVAS | [`05_Pneumonia_Adquirida_na_Comunidade_PAC.md`](04_Pediatria_Puericultura/03_Respiratorio_e_IVAS/05_Pneumonia_Adquirida_na_Comunidade_PAC.md) |
| `;ped-desidratacao` | Gastroenterite Aguda (GECA) & Planos de Desidratação da OMS | Gastrointestinal e Desidratacao | [`01_GECA_e_Planos_Desidratacao_OMS.md`](04_Pediatria_Puericultura/04_Gastrointestinal_e_Desidratacao/01_GECA_e_Planos_Desidratacao_OMS.md) |
| `;ped-febre` | Febre sem Foco & Manejo do Lactente Febril | Febre e Infeccoes Sistemicas | [`01_Febre_sem_Foco_e_Lactente_Febril.md`](04_Pediatria_Puericultura/05_Febre_e_Infeccoes_Sistemicas/01_Febre_sem_Foco_e_Lactente_Febril.md) |
| `;convulsao-febril` | Crise Convulsiva Febril na Infância | Febre e Infeccoes Sistemicas | [`02_Crise_Convulsiva_Febril.md`](04_Pediatria_Puericultura/05_Febre_e_Infeccoes_Sistemicas/02_Crise_Convulsiva_Febril.md) |
| `;ped-doses` | Guia Mestre de Doses Ponderais & Conversões em Pediatria | Guia Doses Ponderais Calculadora | [`01_Guia_Mestre_Doses_Ponderais_Pediatricas.md`](04_Pediatria_Puericultura/06_Guia_Doses_Ponderais_Calculadora/01_Guia_Mestre_Doses_Ponderais_Pediatricas.md) |

---

## 📋 Tabela Mestra: Enfermaria & Internação Hospitalar (10 Modelos)

| Atalho | Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- | :--- |
| `;enf-adm-clin` | Admissão em Enfermaria de Clínica Médica | Admissao e Avaliacao Inicial | [`01_Admissao_Clinica_Medica.md`](03_Enfermaria_Internacao/01_Admissao_e_Avaliacao_Inicial/01_Admissao_Clinica_Medica.md) |
| `;enf-adm-cir` | Admissão Cirúrgica (Pré e Pós-Operatório em Leito) | Admissao e Avaliacao Inicial | [`02_Admissao_Cirurgica_Pre_e_Pos.md`](03_Enfermaria_Internacao/01_Admissao_e_Avaliacao_Inicial/02_Admissao_Cirurgica_Pre_e_Pos.md) |
| `;enf-evo-clin` | Evolução Diária SOAP - Clínica Médica | Evolucao Diaria SOAP | [`01_Evolucao_SOAP_Clinica_Medica.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/01_Evolucao_SOAP_Clinica_Medica.md) |
| `;enf-evo-po` | Evolução Diária SOAP - Pós-Operatório Cirúrgico | Evolucao Diaria SOAP | [`02_Evolucao_SOAP_Pos_Operatorio.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/02_Evolucao_SOAP_Pos_Operatorio.md) |
| `;fasthug` | Checklist de Metas Diárias - Bundle FAST HUG BID | Evolucao Diaria SOAP | [`03_Checklist_Metas_FAST_HUG_BID.md`](03_Enfermaria_Internacao/02_Evolucao_Diaria_SOAP/03_Checklist_Metas_FAST_HUG_BID.md) |
| `;sbar-round` | Round Matinal e Passagem de Plantão (Formato SBAR) | Passagem de Plantao e Rounds | [`01_Round_Matinal_e_Passagem_SBAR.md`](03_Enfermaria_Internacao/03_Passagem_de_Plantao_e_Rounds/01_Round_Matinal_e_Passagem_SBAR.md) |
| `;pi-hosp` | Parecer de Interconsulta Médica Hospitalar (PI) | Interconsultas e Pareceres | [`01_Parecer_Interconsulta_PI_Hospitalar.md`](03_Enfermaria_Internacao/04_Interconsultas_e_Pareceres/01_Parecer_Interconsulta_PI_Hospitalar.md) |
| `;alta-clin` | Sumário de Alta Hospitalar - Clínica Médica | Altas e Desospitalizacao | [`01_Sumario_de_Alta_Clinica_Medica.md`](03_Enfermaria_Internacao/05_Altas_e_Desospitalizacao/01_Sumario_de_Alta_Clinica_Medica.md) |
| `;alta-cir` | Sumário de Alta Hospitalar - Cirurgia Geral & Especialidades | Altas e Desospitalizacao | [`02_Sumario_de_Alta_Cirurgica.md`](03_Enfermaria_Internacao/05_Altas_e_Desospitalizacao/02_Sumario_de_Alta_Cirurgica.md) |
| `;obito-do` | Constatação de Óbito Hospitalar & Preenchimento da Declaração de Óbito (DO) | Declaracao de Obito e Cuidados | [`01_Constatacao_de_Obito_e_Checklist_DO.md`](03_Enfermaria_Internacao/06_Declaracao_de_Obito_e_Cuidados/01_Constatacao_de_Obito_e_Checklist_DO.md) |

---

## 📋 Tabela Mestra: Pronto Atendimento / UPA Adulto (37 Modelos)

| Atalho | Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- | :--- |
| `;upa-ficha` | Ficha Mestra Universal de Pronto Atendimento (UPA / Pronto-Socorro) | Triagem e Ficha Mestra | [`00_Ficha_Mestra_Universal_UPA.md`](02_Pronto_Atendimento_UPA/01_Triagem_e_Ficha_Mestra/00_Ficha_Mestra_Universal_UPA.md) |
| `;resfriado` | Atendimento de Pronto Atendimento - Resfriado Comum e Rinofaringite Aguda | Infeccoes e Vias Aereas | [`01_Resfriado_e_Rinofaringite.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/01_Resfriado_e_Rinofaringite.md) |
| `;amigdalite` | Atendimento de Pronto Atendimento - Faringoamigdalite Aguda | Infeccoes e Vias Aereas | [`02_Faringoamigdalite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/02_Faringoamigdalite_Aguda.md) |
| `;otite` | Atendimento de Pronto Atendimento - Otite Média Aguda (OMA) | Infeccoes e Vias Aereas | [`03_Otite_Media_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/03_Otite_Media_Aguda.md) |
| `;sinusite` | Atendimento de Pronto Atendimento - Rinossinusite Aguda Bacteriana | Infeccoes e Vias Aereas | [`04_Sinusite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/04_Sinusite_Aguda.md) |
| `;pneumonia` | Atendimento de Pronto Atendimento - Pneumonia Adquirida na Comunidade (PAC) | Infeccoes e Vias Aereas | [`05_Pneumonia_PAC.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/05_Pneumonia_PAC.md) |
| `;conjuntivite` | Atendimento de Pronto Atendimento - Conjuntivite Aguda (Viral vs Bacteriana) | Infeccoes e Vias Aereas | [`06_Conjuntivite_Aguda.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/06_Conjuntivite_Aguda.md) |
| `;dengue` | Atendimento de Pronto Atendimento - Dengue e Arboviroses (Classificação MS) | Infeccoes e Vias Aereas | [`07_Dengue_e_Arboviroses.md`](02_Pronto_Atendimento_UPA/02_Infeccoes_e_Vias_Aereas/07_Dengue_e_Arboviroses.md) |
| `;geca` | Atendimento de Pronto Atendimento - Gastroenterite Aguda (GECA) e Desidratação | Gastrointestinal e Abdominal | [`01_GECA_Gastroenterite.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/01_GECA_Gastroenterite.md) |
| `;drge` | Atendimento de Pronto Atendimento - Dispepsia Aguda e DRGE | Gastrointestinal e Abdominal | [`02_Dispepsia_e_DRGE.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/02_Dispepsia_e_DRGE.md) |
| `;abdome-agudo` | Atendimento de Pronto Atendimento - Dor Abdominal Aguda e Abdome Agudo Cirúrgico | Gastrointestinal e Abdominal | [`03_Dor_Abdominal_e_Suspeita_Cirurgica.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/03_Dor_Abdominal_e_Suspeita_Cirurgica.md) |
| `;hda` | Atendimento de Pronto Atendimento - Hemorragia Digestiva Alta (HDA) | Gastrointestinal e Abdominal | [`04_Hemorragia_Digestiva_Alta_HDA.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/04_Hemorragia_Digestiva_Alta_HDA.md) |
| `;hemorroida` | Atendimento de Pronto Atendimento - Hemorroida (Trombose) e Fissura Anal | Gastrointestinal e Abdominal | [`05_Hemorroida_e_Fissura_Anal.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/05_Hemorroida_e_Fissura_Anal.md) |
| `;parasitose` | Atendimento de Pronto Atendimento - Parasitoses Intestinais e Verminoses | Gastrointestinal e Abdominal | [`06_Parasitose_Intestinal.md`](02_Pronto_Atendimento_UPA/03_Gastrointestinal_e_Abdominal/06_Parasitose_Intestinal.md) |
| `;sca` | Atendimento de Pronto Atendimento - Dor Torácica Aguda e SCA (Protocolo de 10 Minutos) | Cardiovascular e Respiratorio | [`01_Dor_Toracica_e_SCA.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/01_Dor_Toracica_e_SCA.md) |
| `;has-crise` | Atendimento de Pronto Atendimento - Crise Hipertensiva (Urgência vs Emergência vs Pseudocrise) | Cardiovascular e Respiratorio | [`02_Crise_Hipertensiva.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/02_Crise_Hipertensiva.md) |
| `;asma` | Atendimento de Pronto Atendimento - Asma Aguda e Crise de Broncoespasmo | Cardiovascular e Respiratorio | [`03_Asma_e_Broncoespasmo.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/03_Asma_e_Broncoespasmo.md) |
| `;dpoc` | Atendimento de Pronto Atendimento - DPOC Exacerbado | Cardiovascular e Respiratorio | [`04_DPOC_Exacerbado.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/04_DPOC_Exacerbado.md) |
| `;eap` | Atendimento de Pronto Atendimento - Edema Agudo de Pulmão (EAP) e ICAD | Cardiovascular e Respiratorio | [`05_Insuficiencia_Cardiaca_e_EAP.md`](02_Pronto_Atendimento_UPA/04_Cardiovascular_e_Respiratorio/05_Insuficiencia_Cardiaca_e_EAP.md) |
| `;cefaleia` | Atendimento de Pronto Atendimento - Cefaleia Aguda e Red Flags (SNOOP10) | Neurologia e Saude Mental | [`01_Cefaleia_Aguda_e_Red_Flags.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/01_Cefaleia_Aguda_e_Red_Flags.md) |
| `;vertigem` | Atendimento de Pronto Atendimento - Vertigem Aguda e Labirintite (Protocolo HINTS) | Neurologia e Saude Mental | [`02_Vertigem_e_Labirintite.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/02_Vertigem_e_Labirintite.md) |
| `;convulsao` | Atendimento de Pronto Atendimento - Crise Convulsiva e Estado de Mal Epiléptico | Neurologia e Saude Mental | [`03_Crise_Convulsiva.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/03_Crise_Convulsiva.md) |
| `;ansiedade` | Atendimento de Pronto Atendimento - Crise de Ansiedade e Transtorno de Pânico | Neurologia e Saude Mental | [`04_Crise_de_Ansiedade_Panico.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/04_Crise_de_Ansiedade_Panico.md) |
| `;surto` | Atendimento de Pronto Atendimento - Agitação Psicomotora e Surto Psiquiátrico | Neurologia e Saude Mental | [`05_Agitacao_Psicomotora_e_Surto.md`](02_Pronto_Atendimento_UPA/05_Neurologia_e_Saude_Mental/05_Agitacao_Psicomotora_e_Surto.md) |
| `;itu` | Atendimento de Pronto Atendimento - Infecção do Trato Urinário (Cistite vs Pielonefrite) | Nefrologia Urologia e Dermatologia | [`01_ITU_Cistite_e_Pielonefrite.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/01_ITU_Cistite_e_Pielonefrite.md) |
| `;colica-renal` | Atendimento de Pronto Atendimento - Nefrolitíase e Cólica Renal Aguda | Nefrologia Urologia e Dermatologia | [`02_Nefrolitiase_Colica_Renal.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/02_Nefrolitiase_Colica_Renal.md) |
| `;uretrite` | Atendimento de Pronto Atendimento - Uretrite Aguda Masculina e ISTs | Nefrologia Urologia e Dermatologia | [`03_Uretrite_DST_Masculina.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/03_Uretrite_DST_Masculina.md) |
| `;lombalgia` | Atendimento de Pronto Atendimento - Lombalgia Mecânica e Lombociatalgia | Nefrologia Urologia e Dermatologia | [`04_Lombalgia_e_Lombociatalgia.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/04_Lombalgia_e_Lombociatalgia.md) |
| `;alergia` | Atendimento de Pronto Atendimento - Reação Alérgica, Urticária e Anafilaxia | Nefrologia Urologia e Dermatologia | [`05_Crise_Alergica_e_Urticaria.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/05_Crise_Alergica_e_Urticaria.md) |
| `;celulite` | Atendimento de Pronto Atendimento - Erisipela, Celulite e Drenagem de Abscesso | Nefrologia Urologia e Dermatologia | [`06_Celulite_Erisipela_e_Abscesso.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/06_Celulite_Erisipela_e_Abscesso.md) |
| `;zoster` | Atendimento de Pronto Atendimento - Herpes Zoster e Neuralgia Aguda | Nefrologia Urologia e Dermatologia | [`07_Herpes_Zoster.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/07_Herpes_Zoster.md) |
| `;escabiose` | Atendimento de Pronto Atendimento - Escabiose (Sarna Humana) | Nefrologia Urologia e Dermatologia | [`08_Escabiose_Sarna.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/08_Escabiose_Sarna.md) |
| `;gota` | Atendimento de Pronto Atendimento - Crise Aguda de Gota (Podagra) e Artrite Gotosa | Nefrologia Urologia e Dermatologia | [`09_Artrite_Gotosa_Gota.md`](02_Pronto_Atendimento_UPA/06_Nefrologia_Urologia_e_Dermatologia/09_Artrite_Gotosa_Gota.md) |
| `;cad` | Atendimento de Pronto Atendimento - Cetoacidose Diabética (CAD) e EHH | Emergencias Graves e Procedimentos | [`01_Cetoacidose_Diabetica_e_EHH.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/01_Cetoacidose_Diabetica_e_EHH.md) |
| `;intoxicacao` | Atendimento de Pronto Atendimento - Intoxicações Exógenas e Intoxicação Alcoólica Aguda | Emergencias Graves e Procedimentos | [`02_Intoxicacao_Exogena_e_Alcoolica.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/02_Intoxicacao_Exogena_e_Alcoolica.md) |
| `;sri` | Atendimento de Pronto Atendimento - Sequência Rápida de Intubação (SRI / IOT) | Emergencias Graves e Procedimentos | [`03_Sequencia_Rapida_de_Intubacao_SRI.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/03_Sequencia_Rapida_de_Intubacao_SRI.md) |
| `;pcr` | Parada Cardiorrespiratória (PCR) Adulto & Cuidados Pós-RCE | Emergencias Graves e Procedimentos | [`04_Parada_Cardiorrespiratoria_PCR.md`](02_Pronto_Atendimento_UPA/07_Emergencias_Graves_e_Procedimentos/04_Parada_Cardiorrespiratoria_PCR.md) |

---

## 📋 Tabela Mestra: Ginecologia & Obstetrícia (23 Modelos)

| Atalho | Protocolo Clínico | Área / Subcategoria | Arquivo |
| :--- | :--- | :--- | :--- |
| `;puerp-adm` | Admissão em Enfermaria de Puerpério | Enfermaria Puerperio | [`01_Puerperio_Admissao.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/01_Puerperio_Admissao.md) |
| `;puerp-evo` | Evolução Diária em Enfermaria de Puerpério | Enfermaria Puerperio | [`02_Puerperio_Evolucao_Diaria.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/02_Puerperio_Evolucao_Diaria.md) |
| `;puerp-alta-pn` | Relatório de Alta de Puerpério - Parto Normal | Enfermaria Puerperio | [`03_Puerperio_Alta_Parto_Normal.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/03_Puerperio_Alta_Parto_Normal.md) |
| `;puerp-alta-pc` | Relatório de Alta de Puerpério - Cesariana | Enfermaria Puerperio | [`04_Puerperio_Alta_Cesarea.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/04_Puerperio_Alta_Cesarea.md) |
| `;round-puerp` | Script de Passagem de Caso / Round de Puerpério | Enfermaria Puerperio | [`05_Puerperio_Round_Passagem_de_Caso.md`](01_Ginecologia_Obstetricia/01_Enfermaria_Puerperio/05_Puerperio_Round_Passagem_de_Caso.md) |
| `;pn-1cons` | Ambulatório de Pré-Natal - Primeira Consulta | Ambulatorio GO | [`01_Pre_Natal_Primeira_Consulta.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/01_Pre_Natal_Primeira_Consulta.md) |
| `;pn-ret` | Ambulatório de Pré-Natal - Consulta Subsequente (Retorno) | Ambulatorio GO | [`02_Pre_Natal_Consulta_Subsequente.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/02_Pre_Natal_Consulta_Subsequente.md) |
| `;gin-amb` | Ambulatório de Ginecologia Geral - Consulta de Rotina e Queixas | Ambulatorio GO | [`03_Ginecologia_Geral_Consulta.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/03_Ginecologia_Geral_Consulta.md) |
| `;pi-gin` | Parecer de Interconsulta - Ginecologia (PI) | Ambulatorio GO | [`04_Ginecologia_Interconsulta_PI.md`](01_Ginecologia_Obstetricia/02_Ambulatorio_GO/04_Ginecologia_Interconsulta_PI.md) |
| `;implanon-ins` | Procedimento Ambulatorial - Inserção de Implanon (Etonogestrel 68 mg) | Procedimentos Ambulatoriais | [`01_Procedimento_Insercao_Implanon.md`](01_Ginecologia_Obstetricia/03_Procedimentos_Ambulatoriais/01_Procedimento_Insercao_Implanon.md) |
| `;implanon-troca` | Procedimento Ambulatorial - Retirada e Troca de Implanon | Procedimentos Ambulatoriais | [`02_Procedimento_Troca_Implanon.md`](01_Ginecologia_Obstetricia/03_Procedimentos_Ambulatoriais/02_Procedimento_Troca_Implanon.md) |
| `;diu-amb` | Procedimento Ambulatorial - Inserção de DIU (Cobre ou Hormonal) | Procedimentos Ambulatoriais | [`03_Procedimento_Insercao_DIU_Ambulatorial.md`](01_Ginecologia_Obstetricia/03_Procedimentos_Ambulatoriais/03_Procedimento_Insercao_DIU_Ambulatorial.md) |
| `;pc-cef` | Descrição Cirúrgica - Cesariana (Polo Cefálico) | Centro Obstetrico Cirurgias | [`01_Cirurgia_Cesarea_Cefalica.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/01_Cirurgia_Cesarea_Cefalica.md) |
| `;pc-pelv` | Descrição Cirúrgica - Cesariana (Apresentação Pélvica) | Centro Obstetrico Cirurgias | [`02_Cirurgia_Cesarea_Pelvico.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/02_Cirurgia_Cesarea_Pelvico.md) |
| `;pc-diu-lt` | Descrição Cirúrgica - Cesariana com DIU Transcesárea ou Laqueadura Tubárea (Pomeroy) | Centro Obstetrico Cirurgias | [`03_Cirurgia_Cesarea_com_DIU_ou_Laqueadura.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/03_Cirurgia_Cesarea_com_DIU_ou_Laqueadura.md) |
| `;pn-eutocico` | Descrição de Parto Normal Eutócico (Espontâneo) | Centro Obstetrico Cirurgias | [`04_Parto_Normal_Eutocico.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/04_Parto_Normal_Eutocico.md) |
| `;pn-instrumentado` | Descrição de Parto Normal Instrumentado - Vácuo Extrator e Fórceps (Simpson) | Centro Obstetrico Cirurgias | [`05_Parto_Normal_Instrumentado_Vacuo_e_Forceps.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/05_Parto_Normal_Instrumentado_Vacuo_e_Forceps.md) |
| `;perineorrafia` | Revisão de Canal de Parto e Perineorrafia (Lacerações e Episiotomia) | Centro Obstetrico Cirurgias | [`06_Revisao_Canal_e_Sutura_Laceracao_Episiotomia.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/06_Revisao_Canal_e_Sutura_Laceracao_Episiotomia.md) |
| `;srpa-pc` | Reavaliação Pós-Cesariana em SRPA (Sala de Recuperação Pós-Anestésica) | Centro Obstetrico Cirurgias | [`07_Reavaliacao_Pos_Cesarea_SRPA.md`](01_Ginecologia_Obstetricia/04_Centro_Obstetrico_Cirurgias/07_Reavaliacao_Pos_Cesarea_SRPA.md) |
| `;amiu` | Procedimento Cirúrgico - AMIU (Aspiração Manual Intrauterina) | Esvaziamento Uterino | [`01_Procedimento_AMIU.md`](01_Ginecologia_Obstetricia/05_Esvaziamento_Uterino/01_Procedimento_AMIU.md) |
| `;curetagem` | Procedimento Cirúrgico - Curetagem Uterina Evacuatória | Esvaziamento Uterino | [`02_Procedimento_Curetagem_Uterina.md`](01_Ginecologia_Obstetricia/05_Esvaziamento_Uterino/02_Procedimento_Curetagem_Uterina.md) |
| `;hpp` | Manejo de Emergência - Hemorragia Pós-Parto (HPP) / Protocolo Código Vermelho | Emergencias GO | [`01_Emergencia_Hemorragia_Pos_Parto_HPP.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/01_Emergencia_Hemorragia_Pos_Parto_HPP.md) |
| `;pre-eclampsia` | Manejo de Emergência - Pré-Eclâmpsia Grave e Eclâmpsia | Emergencias GO | [`02_Emergencia_Pre_Eclampsia_Grave_e_Eclampsia.md`](01_Ginecologia_Obstetricia/06_Emergencias_GO/02_Emergencia_Pre_Eclampsia_Grave_e_Eclampsia.md) |

---

## 🔒 Princípios de Segurança & Blindagem Médico-Legal

1. **Rigor Ponderal Estrito na Pediatria:**
   - Todas as prescrições pediátricas trazem a dose exata por kg de peso (mg/kg/dose, gotas/kg ou mL/dose) e a dose máxima absoluta por tomada para prevenir intoxicações graves (ex: Paracetamol máx 750mg/tomada e 60mg/kg/dia).
2. **Proscrição de Iatrogenias Pediátricas Consagradas:**
   - Proibição de xaropes mucolíticos/antitussígenos e descongestionantes orais/nasais em lactentes; proibição de corticoides e broncodilatadores rotineiros na Bronquiolite Viral Aguda (BVA); proibição de Loperamida na diarreia aguda.
3. **Metas Diárias de Segurança no Leito (FAST HUG BID):**
   - Auditoria diária de dispositivos invasivos (retirar SVD e acessos desnecessários), profilaxia de TEV (Pádua/Caprini), elevação de cabeceira a 30-45°, glicemia alvo (140-180 mg/dL) e desmame racional de antibióticos e protetores gástricos.
4. **Negativas Mandatórias Obrigatórias:**
   - Checagem sistemática dos sinais cardinais de alarme por cenário clínico (afastar meningite, invaginação, abdome cirúrgico, sepse e choque).
5. **Rigores da Declaração de Óbito (CFM e MS):**
   - Preenchimento correto da cadeia causal (causa imediata na linha A até causa básica fundamental na linha D). Proibição formal de atestar morte violenta/externa no hospital (encaminhamento obrigatório ao IML).
