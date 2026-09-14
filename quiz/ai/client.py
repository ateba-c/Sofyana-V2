"""
Thin LLM client used by search, classification and the editorial studio.

Provider is chosen by environment, not code:
  LLM_API_KEY    (falls back to DEEPSEEK_API_KEY, then ANTHROPIC_API_KEY)
  LLM_BASE_URL   default https://api.deepseek.com/anthropic  (DeepSeek's Anthropic-compatible endpoint)
  LLM_MODEL      default deepseek-flash   (DeepSeek maps Claude names too: sonnet/haiku→flash, opus→v4-pro)

Switching to Anthropic proper = set LLM_BASE_URL=https://api.anthropic.com and a Claude model id.
Everything degrades gracefully when no key is configured: ``is_configured()``
is False and callers should hide AI features rather than crash.
"""
import json
import re
from django.conf import settings

_client = None


def is_configured() -> bool:
    return bool(getattr(settings, 'LLM_API_KEY', ''))


def get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            timeout=getattr(settings, 'LLM_TIMEOUT', 60.0),
            max_retries=2,
        )
    return _client


def complete(system: str, user, *, max_tokens: int = 1024, temperature: float = 0.2) -> str:
    """
    One-shot completion.  ``user`` is a string or a list of Anthropic content
    blocks (so callers can pass images: see ``image_block``).
    Returns the text of the reply.
    """
    if not is_configured():
        raise RuntimeError('LLM is not configured (LLM_API_KEY missing)')
    content = user if isinstance(user, list) else [{'type': 'text', 'text': user}]
    resp = get_client().messages.create(
        model=settings.LLM_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{'role': 'user', 'content': content}],
    )
    return ''.join(block.text for block in resp.content if getattr(block, 'type', '') == 'text')


def complete_json(system: str, user, *, max_tokens: int = 2048, temperature: float = 0.1):
    """
    Like ``complete`` but the model is told to answer with JSON only and the
    reply is parsed.  Tolerates ```json fences and leading prose.
    """
    system = (system.rstrip() + '\n\nRespond with a single valid JSON value and nothing else: '
              'no prose, no markdown fences.')
    text = complete(system, user, max_tokens=max_tokens, temperature=temperature)
    return parse_json_reply(text)


def parse_json_reply(text: str):
    text = text.strip()
    fence = re.search(r'```(?:json)?\s*(.*?)```', text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Salvage the first {...} or [...] block.
    for opener, closer in (('{', '}'), ('[', ']')):
        start, end = text.find(opener), text.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError(f'LLM did not return JSON: {text[:200]!r}')


def image_block(data_b64: str, media_type: str = 'image/jpeg') -> dict:
    """Content block for a base64 image (homework photo search)."""
    return {'type': 'image', 'source': {'type': 'base64', 'media_type': media_type, 'data': data_b64}}
