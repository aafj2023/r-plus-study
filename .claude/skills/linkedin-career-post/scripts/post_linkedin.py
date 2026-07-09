#!/usr/bin/env python3
"""Publica um post (e, opcionalmente, o comentário #1) no LinkedIn via API OFICIAL.

Requer a variável de ambiente LINKEDIN_ACCESS_TOKEN, obtida via OAuth 3-legged em um app
LinkedIn com o produto "Share on LinkedIn" (escopos: openid, profile, w_member_social).

Uso:
  python3 post_linkedin.py --text-file post.txt [--first-comment-file c1.txt] [--dry-run]

Só stdlib (urllib). NÃO faz automação não-oficial: usa exclusivamente a API pública.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API = "https://api.linkedin.com"
VERSION = "202401"  # LinkedIn-Version (YYYYMM); atualize se a API pedir.


def _req(method, url, token, body=None, extra_headers=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, dict(resp.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} em {method} {url}: {e.read().decode('utf-8')}")


def get_person_urn(token):
    # /v2/userinfo (OpenID) devolve 'sub' = id do membro.
    _, _, info = _req("GET", f"{API}/v2/userinfo", token)
    sub = info.get("sub")
    if not sub:
        raise SystemExit(f"Não obtive o id do membro em /userinfo: {info}")
    return f"urn:li:person:{sub}"


def create_post(token, author, text):
    body = {
        "author": author,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    status, headers, _ = _req(
        "POST", f"{API}/rest/posts", token, body,
        extra_headers={"LinkedIn-Version": VERSION},
    )
    post_urn = headers.get("x-restli-id") or headers.get("X-RestLi-Id")
    if not post_urn:
        raise SystemExit(f"Post criado (status {status}) mas sem URN no header.")
    return post_urn


def add_comment(token, post_urn, author, text):
    url = f"{API}/v2/socialActions/{urllib.parse.quote(post_urn, safe='')}/comments"
    body = {"actor": author, "message": {"text": text}}
    _req("POST", url, token, body)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-file", required=True)
    ap.add_argument("--first-comment-file", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit("Defina LINKEDIN_ACCESS_TOKEN no ambiente (escopo w_member_social).")

    text = read_file(args.text_file)
    comment = read_file(args.first_comment_file) if args.first_comment_file else ""

    if args.dry_run:
        print("== DRY RUN — nada será publicado ==")
        print(f"[POST]\n{text}\n")
        if comment:
            print(f"[COMMENT #1]\n{comment}")
        return

    author = get_person_urn(token)
    post_urn = create_post(token, author, text)
    print(f"Publicado: {post_urn}")
    if comment:
        add_comment(token, post_urn, author, comment)
        print("Comentário #1 publicado.")


if __name__ == "__main__":
    main()
