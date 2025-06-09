from fastapi import FastAPI
from pydantic import BaseModel
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class TextRequest(BaseModel):
    text: str

@app.post("/link-locations")
def link_locations(req: TextRequest):
    doc = nlp(req.text)
    ents = [ent for ent in doc.ents if ent.label_ == "GPE"]

    # Sort by start index descending to avoid messing up offsets when replacing
    ents = sorted(ents, key=lambda x: x.start_char, reverse=True)

    text = req.text
    for ent in ents:
        start = ent.start_char
        end = ent.end_char
        mention = text[start:end]
        # Only wrap the original text (not already-wrapped)
        text = text[:start] + f"[{mention}]()" + text[end:]

    return {"linked_text": text}
