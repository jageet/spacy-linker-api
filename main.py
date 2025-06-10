from fastapi import FastAPI
from pydantic import BaseModel
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class TextRequest(BaseModel):
    text: str

@app.post("/link-locations")
def link_locations(req: TextRequest):
    text = req.text
    doc = nlp(text)

    # Only use GPE entities (e.g., cities, countries)
    gpe_ents = [ent for ent in doc.ents if ent.label_ == "GPE"]

    # Track already replaced spans to avoid nesting
    spans_to_replace = []

    for ent in gpe_ents:
        spans_to_replace.append((ent.start_char, ent.end_char, ent.text))

    # Sort by start position descending to avoid offset shifting
    spans_to_replace.sort(reverse=True, key=lambda x: x[0])

    for start, end, val in spans_to_replace:
        # Replace only the original span
        text = text[:start] + f"[{val}]()" + text[end:]

    return {"linked_text": text}
