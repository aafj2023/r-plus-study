# R+ Study — Próximos passos / Handoff

App de estudos para a prova de residência (R+) da Giulia. Single-file (`index.html`),
HTML/CSS/JS puro + Chart.js + Dexie + Firebase. PWA instalável e offline.

## 🔗 Endereços
- **App no ar:** https://aafj2023.github.io/r-plus-study/
- **Código (GitHub):** https://github.com/aafj2023/r-plus-study
- **Pasta no PC:** `C:\Users\giuli\OneDrive\Área de Trabalho\r-plus-study\` (o app é o `index.html`)
- **Firebase (login + sync):** projeto `doctor-calendar-c4c6f` em https://console.firebase.google.com
- **Usuário GitHub:** `aafj2023`

## ▶️ Como retomar depois
1. Abrir uma nova conversa do Claude Code **nesta mesma pasta** (Área de Trabalho).
2. Dizer: "vamos continuar o R+ Study" + o que quer fazer.
3. O Claude lê a memória do projeto e já sabe a arquitetura, repo, site e Firebase.

## ✅ O que o app já faz (estado atual)
- **Login obrigatório com Google** (tela de entrada) + **sincronização na nuvem** (Firestore) entre aparelhos.
- **PWA:** instalável na tela inicial e funciona **offline**.
- **Início (dashboard):** saudação com o nome ("Bom dia, [nome]"), avatar/perfil com logout,
  missão do dia, e visão **realizado × planejado** por horizonte: **hoje, esta semana, este mês,
  mês que vem (projeção) e até a prova** — com pílulas de status (no ritmo / atrás / adiantada) e o que fazer.
- **Aulas e Questões:** contadores rápidos (+1/+2/...), metas semanais/mensais ajustáveis.
- **Aulas detalhadas:** registrar aula (disciplina, número, duração, obs) — coexiste com os contadores.
- **Revisão espaçada (SRS):** D+1/D+7/D+15/D+30 baseada em questões; **reconstrução retroativa**
  por disciplina que distribui o backlog sem sobrecarregar (teto diário ajustável).
- **Stats:** progresso do curso, constância/streaks, heatmap de atividade, mapa por disciplina,
  gráficos, e os mesmos indicadores realizado × planejado do Início.
- **Backup:** exportar/importar tudo em um arquivo (⚙ Plano).
- **Detalhes de qualidade:** datas em horário local (sem virada às 21h), status coerente entre telas.

## 💡 Ideias para as próximas rodadas (backlog)
- [ ] Conectar a revisão ao contador de questões (ao marcar "✓ Fiz", somar ~8 questões no total).
- [ ] Resumo semanal de revisões / "fechamento da semana" com celebração.
- [ ] Total de aulas **por disciplina** (% e faltantes reais por matéria no mapa do curso).
- [ ] Lembretes locais (notificação) para revisar.
- [ ] Publicar na **Google Play** (empacotar o PWA via PWABuilder — taxa única US$ 25 da conta dev).
- [ ] Editar/ajustar metas mensais; metas por disciplina.

## 🛠️ Para quem for mexer no código (referência técnica)
- **Publicar mudança:** editar `index.html` → `git add` → `git commit` → `git push`.
  O GitHub Pages republica sozinho em ~1 min. Forçar atualização no navegador: **Ctrl+Shift+R**.
- **Testar localmente:** há um servidor estático em `..\.claude\serve.ps1` (porta 8137), usado com o preview do Claude. Não vai no repositório.
- **Arquivos do PWA:** `manifest.webmanifest`, `sw.js`, `icon-192/512/180.png`.
  Ao mudar libs em cache, subir a versão do cache em `sw.js` (`CACHE = 'rplus-vN'`).
- **Login (só a pessoa faz, se as sessões expirarem):** `gh auth login` (GitHub) e console do Firebase.

> Tudo está commitado e publicado. Nada se perde entre sessões.
