from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class TextInput(BaseModel):
    text: str

@app.post("/link-locations")
def link_locations(input: TextInput):
    text = input.text
    doc = nlp(text)
    locations = set(ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"])
    sorted_locations = sorted(locations, key=len, reverse=True)

    for loc in sorted_locations:
        pattern = r"\b" + re.escape(loc) + r"\b"
        text = re.sub(pattern, f"[{loc}]()", text)

    return {"linked_text": text}
