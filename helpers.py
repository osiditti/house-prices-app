def usd(value):
    """Formats value as USD."""
    return "${:,.0f}".format(value)