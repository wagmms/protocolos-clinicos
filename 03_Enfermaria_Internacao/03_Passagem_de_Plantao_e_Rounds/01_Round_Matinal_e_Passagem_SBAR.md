# Protocolo de Atendimento: Round Matinal e Passagem de Plantão (Formato SBAR)
**Categoria:** Passagem de Plantão e Rounds  
**Atalho Recomendado:** `;sbar-round`

---

## 📋 Snippet para Prontuário Eletrônico (PEP)

```text
###### PASSAGEM DE PLANTÃO & ROUND MULTIDISCIPLINAR (PROTOCOLO SBAR) ######
# 1. [S] SITUATION (MANCHETE EXECUTIVA DO LEITO):
- Leito: [ ] | Paciente: [Nome], [Idade] anos | Equipe: [Clínica Médica / Cirurgia Geral / Terapia Intensiva]
- Tempo de Internação: [ ]º DIH ([Não cirúrgico / [ ]º DPO de [ ]])
- Diagnóstico Principal Ativo: [ ]
- Antimicrobiano em Curso: [Sem antibiótico / Em uso de [ ] — D[ ] de [ ] dias (início em [DD/MM])]
- Status de Gravidade / Código de Cuidado: [Estável em enfermaria / Vigilância aproximada (semi-intensivo) / Cuidados paliativos proporcionais definidos]

# 2. [B] BACKGROUND (CONTEXTO CLÍNICO & HISTÓRICO ESSENCIAL):
- Motivo da Admissão: Internado(a) em [DD/MM/AAAA] por quadro de [ ].
- Comorbidades de Base: [Hígido(a) / HAS / DM2 / IC (FE [ ]%) / DRC estágio [ ] / DPOC / Cirrose / Neoplasia: [ ]].
- Intervenções Relevantes Realizadas na Internação: [Tratamento clínico exclusivo / Procedimento cirúrgico: [ ]/ Toracocentese / Paracentese / EDA / Transfusão].
- Alergias Medicamentosas: [Nega alergias / Alérgico(a) a: [ ]].

# 3. [A] ASSESSMENT (AVALIAÇÃO DAS ÚLTIMAS 24H, EXAME & LABORATÓRIO):
- Evolução nas Últimas 24h: [Estável, sem intercorrências no plantão / Apresentou pico febril de [ ] °C / Apresentou dessaturação para [ ]% / Episódio de hipotensão ou dor aguda].
- Sinais Vitais Atuais: PA: [ ]x[ ] mmHg | FC: [ ] bpm | FR: [ ] irpm | SpO2: [ ]% ([em ar ambiente / sob O2 a [ ] L/min]) | Tax máx 24h: [ ] °C.
- Balanço Hídrico & Diurese (24h): Diurese: [ ] mL ([ ] mL/kg/h) | BH 24h: [Neutro / Positivo em +[ ] mL / Negativo em -[ ] mL].
- Achados Físicos Positivos do Dia: [Lúcido(a), eupneico(a), abdome flácido e indolor, extremidades bem perfundidas / Alteração relevante: [ ]].
- Dispositivos Ativos: [Acesso periférico em [MSD / MSE] D[ ] / CVC em [ ] D[ ] / SVD / SNE / Dreno [ ] com débito de [ ] mL/24h].
- Exames Laboratoriais e Culturas Recentes:
  * Hb: [ ] | Leuco: [ ] (Bast: [ ]%) | Plaq: [ ] | PCR: [ ] | Cr: [ ] | Ur: [ ] | Na: [ ] | K: [ ].
  * Culturas / Imagem: [Sem pendências / Aguardando hemocultura/urocultura colhida em [DD/MM] / Imagem: [ ]].

# PLANO / CONDUTA:

>> 4. [R] RECOMMENDATION (METAS DO DIA & PENDÊNCIAS COM CRITÉRIO DE AÇÃO):
1. Metas Terapêuticas Definidas no Round:
   - Dieta & Hidratação: [Manter dieta oral / Progredir dieta / Suspender soroterapia basal].
   - Antimicrobiano: [Manter D / Transicionar para via oral hoje / Suspender antibiótico hoje].
   - Dispositivos: [Retirar SVD hoje / Sacar acesso venoso / Sacar dreno cirúrgico / Manter dispositivos].
2. Pendências Objetivas para o Plantonista (Formato "Se X → Fazer Y"):
   - Pendência 1 (Laboratório): Checar resultado de [Eletrólitos / Hb / Função renal / Cultura] às [HH:MM] -> [Se K < 3,5 mEq/L, repor KCl; se Hb < 7,0 g/dL, transfundir 1 CH; se normal, manter conduta].
   - Pendência 2 (Imagem / Parecer): Cobrar realização/laudo de [TC / USG / Parecer da [ ]] -> [Conduta conforme achado: [ ]].
   - Pendência 3 (Vigilância Clínica): Reavaliar [padrão respiratório / pressão arterial / diurese] às [HH:MM].
3. Previsão de Alta Hospitalar: [Programada alta para (hoje / amanhã / em 48h) após conclusão de metas].
```

---

## 🎯 Diretrizes & Raciocínio Clínico (O Porquê das Condutas)

### 🧠 1. Por Que Estruturamos a Passagem de Plantão no Método SBAR? (Fisiopatologia & Segurança do Paciente)
- **Por que falhas de comunicação na troca de turno são a principal causa de eventos sentinela:** Estudos da *Joint Commission* e da OMS demonstram que até **70% dos erros médicos graves em pacientes internados** resultam de falhas de comunicação durante a passagem de plantão (*handoff*). Passagens narrativas desestruturadas omitem o código de gravidade, esquecem doses de antibiótico e deixam pendências vagas ("ver exames à tarde") sem plano de contingência.
- **Por que a Regra dos 60–90 Segundos transforma o Round Matinal:** O cérebro humano retém informações acionáveis quando apresentadas em sequência previsível: **Quem é o paciente e por que está aqui (`S`), o que tem de base (`B`), como passou as últimas 24h (`A`) e o que precisa ser decidido agora (`R`)**.

### 💊 2. Por Que Toda Pendência Deve Ter "Dono, Horário e Gatilho de Ação (Se X → Fazer Y)"?
- **Por que "checar laboratório" é uma pendência perigosa:** Quando o médico diarista passa para o plantonista noturno apenas *"checar o controle de sódio e hemoglobina das 18h"*, o plantonista que não conhece a história basal do paciente não sabe se `Hb = 7,8 g/dL` é uma queda aguda de `11,0 g/dL` ou o basal crônico do paciente.
- **O padrão de ouro de segurança (*Contingency Planning*):** Toda pendência deve ser transferida com o gatilho terapêutico explícito: *"Colhemos Hb às 16h por suspeita de melena; o basal de manhã era 9,2 g/dL. Se vier `< 7,5 g/dL` ou tiver taquicardia, transfundir 1 concentrado de hemácias e acionar endoscopia"*.

### 🧭 3. Estrutura Prática dos 4 Tempos do SBAR no Round de Enfermaria
| Etapa SBAR | Tempo Alvo | O Que Incluir Obrigatoriamente | O Que NUNCA Fazer no Round |
| :--- | :---: | :--- | :--- |
| **1. Situation (S)** | **15 seg** | Leito, nome, idade, DIH/DPO, diagnóstico principal e dia do antibiótico (`D_`). | Começar contando a história da emergência de 10 dias atrás sem dizer qual é o diagnóstico atual. |
| **2. Background (B)** | **15 seg** | Comorbidades-chave, motivo da internação, cirurgias realizadas e alergias. | Ler lista de 15 medicamentos de uso contínuo sem relevância para a decisão aguda do dia. |
| **3. Assessment (A)** | **30 seg** | Intercorrências das 24h, curva térmica, balanço hídrico, exame dirigido, dispositivos e curvas de PCR/Leuco/Cr. | Ler todos os valores normais do laboratório sem destacar a tendência (ex: *"PCR caiu de 180 para 42"*). |
| **4. Recommendation (R)** | **20 seg** | Metas do dia (dieta, *switch* oral, retirada de sondas) e pendências no formato **"Se X → Fazer Y"**. | Sair do leito sem definir se a sonda vesical/acesso venoso permanece e qual é o critério exato para a alta. |
