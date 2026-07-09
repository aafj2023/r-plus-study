# linkedin-career-post — Setup

Skill de posicionamento executivo no LinkedIn (ELITE EXECUTIVE BRANDING v6.0).
Gera 1 post por execução no escopo de carreira de Álvaro Felisberto (FP&A / Strategic
Finance), com memória estratégica (sem repetir tema) e os 15 deliverables.

## Modos de entrega (`LINKEDIN_POST_MODE`)

| Modo | O que faz | Requisitos |
|------|-----------|-----------|
| `draft-email` (default) | Cria um rascunho no Gmail com o post pronto pra revisar e postar | Conector Gmail ativo (já disponível) |
| `linkedin-api` | Publica direto no LinkedIn via API oficial | `LINKEDIN_ACCESS_TOKEN` no ambiente |
| `print` | Só mostra o post no chat | — |

⚠️ **Não existe automação não-oficial.** O modo `linkedin-api` usa exclusivamente a API
pública do LinkedIn. Bots que logam pela sua conta violam os Termos e podem restringir o
perfil — este skill não faz isso.

## Como obter o `LINKEDIN_ACCESS_TOKEN` (uma vez)

1. Crie um app em https://developer.linkedin.com/ (associe a uma Company Page sua).
2. Em **Products**, solicite **"Share on LinkedIn"** e **"Sign In with LinkedIn using OpenID Connect"**.
3. Escopos necessários: `openid`, `profile`, `w_member_social`.
4. Rode o fluxo OAuth 3-legged (Authorization Code) e troque o code por um access token.
   - O token de membro dura ~60 dias; renove quando expirar.
5. Exporte no ambiente: `export LINKEDIN_ACCESS_TOKEN="..."`

Teste sem publicar:
```
python3 scripts/post_linkedin.py --text-file post.txt --dry-run
```

## Agendamento (postar sozinho, ex.: ter/qui às 9h)

Use uma **Routine** do Claude Code que dispara este skill numa sessão nova a cada firing.
Peça ao Claude: *"crie um trigger cron `0 9 * * 2,4` que roda o skill linkedin-career-post
em sessão nova"*. Combine com `LINKEDIN_POST_MODE=linkedin-api` para publicar automático,
ou deixe em `draft-email` para receber o rascunho e aprovar antes.

## Arquivos
- `SKILL.md` — instruções que o Claude segue ao ser invocado.
- `references/scope.md` — escopo v6.0 (persona, distribuição, filtros, deliverables).
- `references/profile.md` — fatos do perfil + guardrails de honestidade.
- `scripts/rotation.py` — memória estratégica e escolha de categoria.
- `scripts/post_linkedin.py` — publicação via API oficial.
- `memory/history.json` — histórico dos últimos 100 posts.
