# Protocolo de Atendimento: Constatação de Óbito Hospitalar & Preenchimento da Declaração de Óbito (DO)
**Categoria:** Declaração de Óbito e Cuidados  
**Atalho Recomendado:** `;obito-do`

---

## 📋 Snippet para Prontuário Eletrônico (PEP)

```text
###### CONSTATAÇÃO DE ÓBITO HOSPITALAR & REGISTRO MÉDICO-LEGAL ######
# IDENTIFICAÇÃO & CRONOLOGIA DO ÓBITO:
- Paciente: [Nome completo], [Idade] anos | Sexo: [Masculino / Feminino] | DN: [DD/MM/AAAA]
- Prontuário / Registro: [ ] | Setor / Leito: [ ]
- Data e Horário Exato da Constatação do Óbito: [DD/MM/AAAA] às [HH:MM]

# OBJETIVO (EXAME FÍSICO CONFIRMATÓRIO DE MORTE CLÍNICA):
Chamado(a) ao leito às [HH:MM] pela equipe de enfermagem por parada cardiorrespiratória / ausência de sinais vitais. Ao exame físico dirigido à beira do leito, constato:
1. Nível de Consciência & Estímulo Central: Paciente irresponsivo(a) ao chamado verbal e ao estímulo álgico central (Escala de Coma de Glasgow = 3), com atonia muscular generalizada.
2. Reflexos de Tronco Encefálico: Pupilas em midríase paralítica bilateral, fixas e arreativas ao estímulo fotomotor direto e consensual; reflexo corneopalpebral abolido bilateralmente.
3. Aparelho Respiratório: Ausência absoluta de movimentos respiratórios toracoabdominais (apneia completa) e silêncio auscultatório pulmonar bilateral por mais de 1 minuto ininterrupto.
4. Aparelho Cardiovascular: Ausência de pulsos arteriais centrais (carotídeos e femorais) à palpação e ausência completa de bulhas cardíacas à ausculta precordial prolongada (> 1 minuto).
5. Monitorização Eletrocardiográfica: [Assistolia confirmada no protocolo da linha reta em 2 derivações com ganho máximo e cabos checados / Paciente em cuidados paliativos exclusivos de fim de vida sem indicação de manobras invasivas de RCP].

# AVALIAÇÃO MÉDICO-LEGAL DA NATUREZA DO ÓBITO:
- Classificação Legal da Morte:
  * [Morte de Causa Natural com Assistência Médica Hospitalar — Diagnóstico conhecido; Declaração de Óbito (DO) emitida pelo médico assistente/plantonista].
  * [Morte Violenta ou Suspeita de Causa Externa (Acidente, queda da própria altura com fratura, trauma, intoxicação exógena, agressão ou suicídio) — NÃO emitida DO no hospital; acionado Instituto Médico Legal (IML)].
  * [Morte de Causa Natural de Etiologia Indeterminada sem diagnóstico definido — Corpo encaminhado ao Serviço de Verificação de Óbito (SVO)].

# PLANO / CONDUTA:

>> CADEIA CAUSAL REGISTRADA NA DECLARAÇÃO DE ÓBITO (CAMPO 40 — PARTE I E II):
- PARTE I (Cadeia Causal Direta — da causa terminal na linha A até a causa básica na última linha):
  * Linha a (Causa Imediata / Terminal): [ex: Choque séptico refratário / Insuficiência respiratória aguda hipoxêmica / Tamponamento cardíaco] — Tempo aproximado: [ ] [horas / dias].
  * Linha b (Devido a / Causa Intermediária): [ex: Pneumonia bacteriana nosocomial / Tromboembolismo pulmonar maciço / Infarto agudo do miocárdio] — Tempo aproximado: [ dias].
  * Linha c (Devido a / Causa Intermediária): [Não se aplica / Causa: [ ]] — Tempo aproximado: [ ].
  * Linha d (Causa Básica Fundamental — doença que iniciou a cadeia): [ex: Doença Pulmonar Obstrutiva Crônica grave / Neoplasia maligna de cólon metastática / Aterosclerose coronariana hipertensiva] — Tempo aproximado: [ ] [meses / anos].
- PARTE II (Outras condições mórbidas preexistentes que contribuíram, mas não entraram na cadeia direta):
  * [ex: Diabetes Mellitus tipo 2, Doença Renal Crônica estágio 4, Fibrilação Atrial crônica].

>> CONDUTA PÓS-ÓBITO & ACOLHIMENTO FAMILIAR (PROTOCOLO SPIKES):
1. Declarado o óbito às [HH:MM] e registrado em prontuário eletrônico.
2. Realizada comunicação presencial da má notícia em ambiente privativo, com linguagem clara e postura empática (Protocolo SPIKES), ao familiar responsável: [Nome do familiar] (Grau de parentesco: [ ]).
3. Esclarecidas todas as dúvidas da família quanto à evolução clínica e entregues as orientações documentais junto ao Serviço Social / Secretaria do setor.
4. Autorizada a retirada de dispositivos invasivos (exceto se encaminhamento ao IML, onde dispositivos devem ser mantidos in situ) e preparo digno do corpo pela equipe de enfermagem.
```

---

## 🎯 Diretrizes & Raciocínio Clínico (O Porquê das Condutas)

### 🧠 1. Por Que a Declaração de Óbito (DO) Segue uma Cadeia Fisiopatológica de Baixo para Cima? (Rigor Médico-Legal CFM)
- **A função epidemiológica e jurídica da Declaração de Óbito (Resolução CFM nº 1.779/2005 e Manual do Ministério da Saúde):** A DO não é apenas um documento burocrático para sepultamento; ela é a fonte primária das estatísticas vitais de mortalidade do país. Na **Parte I (Linhas a, b, c, d)**, a leitura cronológica e fisiopatológica ocorre de baixo para cima: a **Causa Básica (última linha preenchida)** iniciou o processo mórbido que produziu as **Causas Intermediárias**, culminando na **Causa Imediata (Linha a)**.
- **Por que "Parada Cardiorrespiratória (PCR)" e "Falência de Múltiplos Órgãos" NUNCA podem ser a causa básica:** A PCR é o mecanismo terminal pelo qual 100% dos seres humanos falecem — colocá-la na DO equivale a escrever *"morreu porque parou de viver"*. Da mesma forma, *"Insuficiência Respiratória"* ou *"Choque"* na linha A exigem obrigatoriamente que as linhas abaixo especifiquem qual doença etiológica os provocou.

### 💊 2. Por Que a Queda da Própria Altura no Idoso Proíbe o Médico do Hospital de Assinar a DO?
- **A regra jurídica inviolável da Causa Externa (Mesmo Tardia):** Sempre que o evento inicial que desencadeou a cadeia de eventos até a morte for um agente externo (físico, químico, mecânico, térmico ou violento), a morte é classificada juridicamente como **Morte por Causa Externa / Não Natural**, independentemente de quantos dias, semanas ou meses o paciente permaneceu internado no hospital.
- **O exemplo clássico de prova e de plantão:** Um idoso de 82 anos tropeça no tapete de casa (queda da própria altura), fratura o fêmur, interna, opera com sucesso, mas no 14º DPO desenvolve pneumonia aspirativa, evolui para choque séptico e vai a óbito na UTI. Porque a pneumonia e o choque séptico decorreram da imobilização/internação gerada pela fratura traumática, **a Causa Básica é a queda acidental (Causa Externa)**. Assinar a DO no hospital neste caso configura infração ético-legal; o corpo deve ser obrigatoriamente encaminhado ao **Instituto Médico Legal (IML)** mantendo tubos, drenos e cateteres *in situ*.

### 🧭 3. Fluxo Decisório de Competência para Emissão da DO (Hospital vs SVO vs IML)
| Cenário Clínico do Óbito | Quem Deve Emitir a Declaração de Óbito (DO)? | Conduta Prática do Plantonista |
| :--- | :--- | :--- |
| **1. Morte Natural com Diagnóstico Conhecido** (Paciente internado ou em pronto-socorro sob cuidados médicos por doença clínica definida) | **Médico Assistente ou Plantonista do Hospital** (obrigação ética e legal). | Preencher as 3 vias da DO com cadeia causal completa (Parte I e II), sem rasuras, e entregar via amarela à família. |
| **2. Morte Violenta ou Suspeita de Causa Externa** (Acidente de trânsito, queda da própria altura com fratura, agressão, PAF/FAB, intoxicação exógena, queimadura, suicídio, suspeita de negligência) | **Instituto Médico Legal (IML)** — Perito Médico Legista após necropsia forense. | **NÃO emitir a DO no hospital.** Manter dispositivos invasivos no corpo, registrar o óbito no prontuário e acionar Polícia Civil / IML via Serviço Social. |
| **3. Morte Natural de Causa Indeterminada** (Morte súbita sem causa clínica elucidada, já afastada qualquer hipótese de trauma ou violência) | **Serviço de Verificação de Óbito (SVO)** (ou médico do serviço público/plantonista se o município não possuir SVO). | Preencher guia de encaminhamento detalhada para o SVO após confirmar ausência total de sinais de violência externa. |
