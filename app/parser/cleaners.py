def clean_body(text: str) -> str:
    if not text:
        return ""

    lines = text.splitlines()
    result = []

    stop_words = [
        "On ",
        ">",
        "-----Original Message-----",
    ]

    for line in lines:
        if any(line.strip().startswith(s) for s in stop_words):
            break
        result.append(line)

    return "\n".join(result).strip()
