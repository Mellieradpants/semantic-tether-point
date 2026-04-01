import re


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
    conditions = []
    patterns = [
        r"\bif\b[^.;,]*",
        r"\bwhen\b[^.;,]*",
        r"\bunless\b[^.;,]*",
        r"\bexcept\b[^.;,]*",
        r"\bunder\b[^.;,]*"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        conditions.extend([m.strip() for m in matches if m.strip()])

    return conditions


def extract_deadlines(text: str):
    patterns = [
        r"\bwithin\s+\d+\s+(day|days|week|weeks|month|months|year|years)\b",
        r"\bby\s+[A-Z][a-z]+\s+\d{1,2},?\s+\d{4}\b",
        r"\bby\s+\d{4}-\d{2}-\d{2}\b",
        r"\bby\s+\d{1,2}:\d{2}\b",
        r"\bwithin\s+\d+\s+business\s+days\b"
    ]

    deadlines = []
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            full_matches = re.finditer(pattern, text, flags=re.IGNORECASE)
            deadlines.extend([m.group(0).strip() for m in full_matches])

    return deadlines


def extract_triggers(text: str):
    triggers = []
    patterns = [
        r"\bif\b[^.;,]*",
        r"\bwhen\b[^.;,]*",
        r"\bupon\b[^.;,]*",
        r"\bafter\b[^.;,]*",
        r"\bbefore\b[^.;,]*"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        triggers.extend([m.strip() for m in matches if m.strip()])

    return triggers


def extract_sequence(text: str):
    sequence = []
    patterns = [
        r"\bbefore\b[^.;,]*",
        r"\bafter\b[^.;,]*",
        r"\bthen\b[^.;,]*",
        r"\bfollowing\b[^.;,]*"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        sequence.extend([m.strip() for m in matches if m.strip()])

    return sequence


def extract_reason(text: str):
    patterns = [
        r"\bbecause\b[^.;,]*",
        r"\bdue to\b[^.;,]*",
        r"\bin order to\b[^.;,]*"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def extract_mechanism(text: str):
    patterns = [
        r"\bby\b[^.;,]*",
        r"\bthrough\b[^.;,]*",
        r"\bvia\b[^.;,]*",
        r"\busing\b[^.;,]*",
        r"\bpursuant to\b[^.;,]*",
        r"\bunder\b[^.;,]*"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def extract_enforcement(text: str):
    patterns = [
        r"\bsubject to\b[^.;,]*",
        r"\bpenalty\b[^.;,]*",
        r"\bpenalties\b[^.;,]*",
        r"\bviolation\b[^.;,]*",
        r"\bviolations\b[^.;,]*",
        r"\bfailure to comply\b[^.;,]*",
        r"\benforced\b[^.;,]*"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def extract_actor_action(text: str):
    actor_patterns = [
        r"^\s*([A-Z][A-Za-z0-9_\-/ ]+?)\s+(must|shall|may|cannot|required to)\b",
        r"^\s*(The\s+[A-Z][A-Za-z0-9_\-/ ]+?)\s+(must|shall|may|cannot|required to)\b",
    ]

    for pattern in actor_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            actor = match.group(1).strip()
            modal = match.group(2).strip()
            action_start = match.end(2)
            action_text = text[action_start:].strip(" .;:")
            return {
                "actors": [actor],
                "responsibleParty": actor,
                "action": action_text if action_text else None,
                "modal": modal
            }

    return {
        "actors": [],
        "responsibleParty": None,
        "action": None,
        "modal": None
    }


def analyze_anchor(anchor: dict):
    text = anchor["text"]
    parse = empty_parse()

    actor_action = extract_actor_action(text)

    parse["what"]["claim"] = text
    parse["what"]["action"] = actor_action["action"]
    parse["what"]["conditions"] = extract_conditions(text)

    parse["who"]["actors"] = actor_action["actors"]
    parse["who"]["responsibleParty"] = actor_action["responsibleParty"]

    parse["when"]["deadlines"] = extract_deadlines(text)
    parse["when"]["triggers"] = extract_triggers(text)
    parse["when"]["sequence"] = extract_sequence(text)

    if anchor.get("type") == "timestamp":
        parse["when"]["timing"] = text

    parse["why"]["statedReason"] = extract_reason(text)

    parse["how"]["mechanism"] = extract_mechanism(text)
    parse["how"]["enforcement"] = extract_enforcement(text)

    return parse


def contains_precision_claim(text: str):
    return bool(re.search(r"\b\d+(\.\d+)?%?\b", text))


def review_parse_output(parse: dict, tether_anchor: dict):
    missing_signals = []
    control_flags = []
    drift_detected = False
    status = "ok"

    claim = parse["what"]["claim"]
    action = parse["what"]["action"]
    actors = parse["who"]["actors"]
    authority = parse["who"]["decisionAuthority"]
    triggers = parse["when"]["triggers"]
    enforcement = parse["how"]["enforcement"]

    if not claim:
        missing_signals.append("missing_claim")
        status = "blocked"

    if action and not actors:
        missing_signals.append("missing_actor")

    if action and not authority:
        missing_signals.append("missing_decision_authority")

    if tether_anchor.get("matchedSignals") and "obligation" in tether_anchor["matchedSignals"]:
        if not enforcement:
            missing_signals.append("missing_enforcement")

    conditional_language_present = bool(re.search(r"\bif\b|\bwhen\b|\bupon\b|\bunless\b", claim or "", flags=re.IGNORECASE))
    if conditional_language_present and not triggers:
        missing_signals.append("missing_trigger_conditions")

    if contains_precision_claim(claim or ""):
        control_flags.append("precision_claim_present")
        if tether_anchor.get("type") == "text_span":
            control_flags.append("precision_claim_without_source_path")

    return {
        "missingSignals": missing_signals,
        "controlFlags": control_flags,
        "driftDetected": drift_detected,
        "status": status
    }
