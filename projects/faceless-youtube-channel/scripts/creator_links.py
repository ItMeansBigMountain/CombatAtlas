from __future__ import annotations

import os

DEFAULT_LINKS = {
    'LINKTREE_URL': 'https://linktr.ee/sosai.oyama',
    'BUY_ME_A_COFFEE_URL': 'https://buymeacoffee.com/affanfareev',
    'CASH_APP_URL': 'https://cash.app/$sosaioyama',
    'VENMO_URL': 'https://venmo.com/u/SosaiOyama',
}


def public_links() -> dict[str, str]:
    return {k: (os.getenv(k) or v).strip() for k, v in DEFAULT_LINKS.items()}


def support_block() -> str:
    links = public_links()
    return (
        "\n\nMore from me: " + links['LINKTREE_URL'] +
        "\nSupport the channel: " + links['BUY_ME_A_COFFEE_URL'] +
        "\nCash App: " + links['CASH_APP_URL'] +
        "\nVenmo: " + links['VENMO_URL']
    )
