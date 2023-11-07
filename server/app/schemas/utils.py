def to_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )
