import re

from django import template

register = template.Library()

_STATUS = {
    'UNREVIEWED': ('À faire', 'bg-slate-100 text-slate-600 ring-slate-300', '#94A3B8'),
    'FLAGGED_FOR_REWORK': ('Retouche', 'bg-amber-50 text-amber-700 ring-amber-300', '#F59E0B'),
    'APPROVED': ('Validée', 'bg-emerald-50 text-emerald-700 ring-emerald-300', '#10B981'),
    'REJECTED': ('Rejetée', 'bg-rose-50 text-rose-700 ring-rose-300', '#F43F5E'),
}
_STATE = {
    'LOCKED': ('Verrouillé', '🔒', 'bg-slate-100 text-slate-600'),
    'CERTIFIED': ('Certifié', '✅', 'bg-emerald-100 text-emerald-800'),
    'DEGRADED': ('Dégradé', '⚠️', 'bg-rose-100 text-rose-700'),
}
_ACTION = {
    'created': 'Échantillon généré', 'lint_flagged': 'Signalé par le linter', 'approve': 'Approuvée',
    'rework': 'Retouche demandée', 'reject': 'Rejetée', 'reopen': 'Remise à faire', 'comment': 'Commentaire',
    'proposal_saved': 'Correction proposée', 'proposal_cleared': 'Correction annulée',
    'generator_changed': 'Générateur modifié',
}


@register.filter
def status_label(s):
    return _STATUS.get(s, (s, '', ''))[0]


@register.filter
def status_cls(s):
    return _STATUS.get(s, ('', 'bg-slate-100 text-slate-600 ring-slate-300', ''))[1]


@register.filter
def status_dot(s):
    return _STATUS.get(s, ('', '', '#94A3B8'))[2]


@register.filter
def state_label(s):
    return _STATE.get(s, (s, '', ''))[0]


@register.filter
def state_icon(s):
    return _STATE.get(s, ('', '•', ''))[1]


@register.filter
def state_cls(s):
    return _STATE.get(s, ('', '', 'bg-slate-100 text-slate-600'))[2]


@register.filter
def action_label(a):
    return _ACTION.get(a, a)


@register.filter
def plain(text):
    return re.sub(r'\*\*(.+?)\*\*', r'\1', str(text or ''))


@register.filter
def get(d, key):
    return d.get(key) if isinstance(d, dict) else None
