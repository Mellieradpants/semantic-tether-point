import re


def normalize_text(text: str):
    # Remove section prefixes like "Section 3:"
    return re.sub(r"^\s*Section\s+\d+:\s*", "", text, flags=re.IGNORECASE)


def empty_parse():
    return {
        "what": {
            "claim": None,
            "action": None,
            "conditions": []
        },
        "who": {
            "actors": [],
            "responsibleParty": None,
            "decisionAuthority": None
        },
        "where": {
            "system": None,
            "jurisdiction": None,
            "controllingEntity": None
        },
        "when": {
            "timing": None,
            "triggers": [],
            "deadlines": [],
            "sequence": []
        },
        "why": {
            "statedReason": None,
            "reasonActionAlignment": None
        },
        "how": {
            "mechanism": None,
            "implementation": [],
            "enforcement": None
        }
    }


def extract_conditions(text: str):
    patterns = [r"\bif\b[^.;,]*", r"\bwhen\b[^.;,]*", r"\bunless\b[^.;,]*", r"\bexcept\b[^.;,]*", r"\bunder\b[^.;,]*"]
    return [m.group(0).strip() for p in patterns for m in re.finditer(p, text, re.IGNORECASE)]


def extract_deadlines(text: str):
    pattern = r"\bwithin\s+\d+\s+(day|days|week|weeks|month|months|year|years)\b"
    return [m.group(0).strip() for m in re.finditer(pattern, text, re.IGNORECASE)]


def extract_triggers(text: str):
    patterns = [r"\bif\b[^.;,]*", r"\bwhen\b[^.;,]*", r"\bupon\b[^.;,]*"]
    return [m.group(0).strip() for p in patterns for m in re.finditer(p, text, re.IGNORECASE)]


def extract_sequence(text: str):
    patterns = [r"\bbefore\b[^.;,]*", r"\bafter\b[^.;,]*", r"\bthen\b[^.;,]*"]
    return [m.group(0).strip() for p in patterns for m in re.finditer(p, text, re.IGNORECASE)]


def extract_reason(text: str):
    match = re.search(r"\bbecause\b[^.;,]*|\bdue to\b[^.;,]*|\bin order to\b[^.;,]*", text, re.IGNORECASE)
    return match.group(0).strip() if match else None


def extract_mechanism(text: str):
    # IMPORTANT: removed "under"
    match = re.search(r"\bby\b[^.;,]*|\bthrough\b[^.;,]*|\bvia\b[^.;,]*|\busing\b[^.;,]*", text, re.IGNORECASE)
    return match.group(0).strip() if match else None


def extract_enforcement(text: str):
    match = re.search(r"\bpenalty\b[^.;,]*|\bviolation\b[^.;,]*|\bfailure to comply\b[^.;,]*", text, re.IGNORECASE)
    return match.group(0).strip() if match else None


def extract_actor_action(text: str):
    pattern = r"^\s*([A-Z][A-Za-z0-9_\-/ ]+?)\s+(must|shall|may|cannot|required to)\b"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        actor = match.group(1).strip()
        modal = match.group(2).strip()
        action = text[match.end(2):].strip(" .;:")

        return {
            "actors": [actor],
            "responsibleParty": actor,
            "decisionAuthority": actor if modal.lower() == "may" else None,
            "action": action if action else None,
            "modal": modal.lower()
        }

    return {"actors": [], "responsibleParty": None, "decisionAuthority": None, "action": None, "modal": None}


def analyze_anchor(anchor: dict):
    raw_text = anchor["text"]
    text = normalize_text(raw_text)

    parse = empty_parse()
    actor_action = extract_actor_action(text)

    parse["what"]["claim"] = raw_text
    parse["what"]["action"] = actor_action["action"]
    parse["what"]["conditions"] = extract_conditions(text)

    parse["who"]["actors"] = actor_action["actors"]
    parse["who"]["responsibleParty"] = actor_action["responsibleParty"]
    parse["who"]["decisionAuthority"] = actor_action["decisionAuthority"]

    parse["when"]["deadlines"] = extract_deadlines(text)
    parse["when"]["triggers"] = extract_triggers(text)
    parse["when"]["sequence"] = extract_sequence(text)

    parse["why"]["statedReason"] = extract_reason(text)

    parse["how"]["mechanism"] = extract_mechanism(text)
    parse["how"]["enforcement"] = extract_enforcement(text)

    return parse


def contains_precision_claim(text: str):
    if re.search(r"\b\d+(\.\d+)?%\b", text):
        return True

    if re.search(r"\b\d{2,}\b", text):
        if not re.search(r"\b(day|days|month|months|year|years|annually)\b", text.lower()):
            return True

    return False


def review_parse_output(parse: dict, tether_anchor: dict):
    missing_signals = []
    control_flags = []

    claim = parse["what"]["claim"]
    action = parse["what"]["action"]
    actors = parse["who"]["actors"]
    authority = parse["who"]["decisionAuthority"]
    enforcement = parse["how"]["enforcement"]
    modal = tether_anchor.get("matchedSignals", [])

    if action and not actors:
        missing_signals.append("missing_actor")

    # ONLY require authority for permission cases
    if "permission" in modal and not authority:
        missing_signals.append("missing_decision_authority")

    if "obligation" in modal and not enforcement:
        missing_signals.append("missing_enforcement")

    if contains_precision_claim(claim or ""):
        control_flags.append("precision_claim_present")
        if tether_anchor.get("type") == "text_span":
            control_flags.append("precision_claim_without_source_path")

    return {
        "missingSignals": missing_signals,
        "controlFlags": control_flags,
        "driftDetected": False,
        "status": "ok"
    }
