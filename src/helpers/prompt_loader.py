import yaml

def load_prompt(path: str, **kwargs) -> str:
    """
    Reads a YAML prompt file and formats it using the provided variables.
    """
    with open(path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)

    template = prompt_data["template"]
    return template.format(**kwargs)
