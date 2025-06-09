# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import spacy

nlp = spacy.load("en_core_web_sm")

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/link-locations")
def link_locations(req: TextRequest):
    doc = nlp(req.text)
    result = req.text
    # Replace locations with markdown hyperlinks
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geographic locations
            result = result.replace(ent.text, f"[{ent.text}]()")
    return {"linked_text": result}
