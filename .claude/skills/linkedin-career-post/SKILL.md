---
name: linkedin-career-post
description: Gera e (opcionalmente) publica um post de posicionamento executivo no LinkedIn para Álvaro Felisberto (FP&A / Strategic Finance), seguindo o ELITE EXECUTIVE BRANDING System v6.0 — distribuição de portfólio, memória estratégica (sem repetir tema), filtros de altitude executiva e os 15 deliverables. Use quando o usuário pedir para criar/agendar/publicar um post de carreira no LinkedIn, ou quando disparada por uma Routine agendada. Modos de entrega: draft-email (Gmail, funciona já), linkedin-api (requer token) e print.
---

# LinkedIn Career Post — ELITE EXECUTIVE BRANDING v6.0

Gera UM post de posicionamento executivo por execução, otimizado para **avanço de
carreira** (empregabilidade, senioridade percebida, potencial salarial), não para
engajamento. Escrito para o perfil de **Álvaro Felisberto, CFP®**.

## Passo a passo (siga em ordem)

### 1. Carregue o contexto
- Leia `references/scope.md` (persona, distribuição de conteúdo, filtros, deliverables).
- Leia `references/profile.md` (fatos do perfil + **guardrails de honestidade** — nunca
  inflar senioridade, nunca dizer "5 anos de FP&A", sempre enquadrar a troca de área e o
  job-hopping como progressão deliberada).

### 2. Escolha a categoria e evite repetição
Rode:
```
python3 scripts/rotation.py --next
```
Isso retorna JSON com: `category` (A–F) que está mais atrás da meta de distribuição, o
`type_name`, e `avoid_themes` (temas dos últimos posts — NÃO repita nenhum deles).

Se o usuário pediu um tema específico, respeite o tema, mas ainda registre na memória.

### 3. Gere o post no escopo
Produza o conteúdo seguindo `scope.md` para a categoria escolhida. Antes de finalizar,
passe pelos 3 filtros obrigatórios (ROI de carreira, executor-vs-decisor, proposta
R$25k+). Se falhar em qualquer um, reescreva.

Monte um JSON com TODOS os 15 deliverables (post_principal, comentario_1, comentario_2,
titulo_invisivel, ats_keywords, competencias, reputation_score, career_roi_score,
prob_recruiters, prob_headhunters, prob_cfos, senioridade, cargo_associado, gap_fechado,
sugestao_imagem). Salve em `scratch/last_post.json`.

### 4. Entregue (escolha o modo)
Leia a variável de ambiente `LINKEDIN_POST_MODE` (default: `draft-email`).

- **`draft-email`** (funciona hoje, zero risco): crie um rascunho no Gmail via a ferramenta
  `mcp__Gmail__create_draft` para `alvarofelisbertojr@gmail.com`, assunto
  `[LinkedIn Draft] <titulo_invisivel>`, corpo = post_principal + os 2 comentários +
  bloco de ATS keywords + sugestão de imagem. O usuário revisa e posta com 1 toque.
- **`linkedin-api`** (requer `LINKEDIN_ACCESS_TOKEN` no ambiente): rode
  `python3 scripts/post_linkedin.py --text-file scratch/commentary.txt --first-comment-file scratch/comment1.txt`
  (escreva o texto do post em `scratch/commentary.txt` e o comentário #1 em
  `scratch/comment1.txt` antes). Faça `--dry-run` primeiro se o usuário quiser conferir.
- **`print`**: apenas mostre o post final no chat.

### 5. Registre na memória estratégica
Rode:
```
python3 scripts/rotation.py --record --category <A-F> --theme "<tema curto>" \
  --keywords "kw1,kw2,kw3" --seniority "<senioridade sinalizada>" --gap "<gap fechado>"
```
Mantém histórico dos últimos 100, evita repetição e sobe a sofisticação com o tempo.

## Regras
- Português brasileiro, tom executivo, sóbrio. Sem emoji excessivo, sem hashtag-spam
  (máx. 3 hashtags relevantes).
- NUNCA invente números do perfil do Álvaro. Se um número reforçaria o post e não está em
  `profile.md`, deixe um placeholder `[confirmar: ...]` e avise o usuário.
- Um post por execução. Nunca publique sem o modo estar explicitamente em `linkedin-api`.
