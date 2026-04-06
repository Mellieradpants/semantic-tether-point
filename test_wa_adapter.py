from pathlib import Path
from wa_legislature_adapter import parse_wa_legislature_xml, normalized_text_from_blocks

xml_text = Path("example-wa-response.xml").read_text(encoding="utf-8")
normalized = parse_wa_legislature_xml(xml_text)
text_output = normalized_text_from_blocks(normalized)

Path("example-wa-normalized.txt").write_text(text_output, encoding="utf-8")
print("Wrote example-wa-normalized.txt")
print(text_output)
