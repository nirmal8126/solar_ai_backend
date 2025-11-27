def detect_utility_from_address(address: str | None) -> str | None:
    if not address:
        return None

    a = address.lower()

    if "delhi" in a:
        return "BSES / TPDDL"
    if "mumbai" in a:
        return "Tata Power / Adani (Mumbai)"
    if "bangalore" in a or "bengaluru" in a:
        return "BESCOM"
    if "ahmedabad" in a:
        return "Torrent Power"
    if "surat" in a:
        return "DGVCL"
    if "jaipur" in a:
        return "JVVNL"

    # fallback
    return None
