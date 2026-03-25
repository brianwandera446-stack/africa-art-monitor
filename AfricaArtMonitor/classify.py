"""
AFRICA ART CLASSIFIER — Artist Focused
Detects news about African artists (continent + diaspora)
"""

import re
from dataclasses import dataclass
from typing import Optional

# Africa terms (continent + diaspora focus)
AFRICA_GEOGRAPHIC = [
    "africa", "african", "kenya", "kenyan", "nigeria", "nigerian", 
    "ghana", "ghanaian", "south africa", "nairobi", "lagos"
]

ALL_AFRICA_TERMS = AFRICA_GEOGRAPHIC

# ARTIST-FOCUSED subjects
SUBJECTS = {
    "artists": {
        "keywords": ["artist", "painter", "sculptor", "photographer", "born in", "based in"],
        "signals": ["dies", "death", "wins", "awarded", "controversy", "record price"],
        "reject": ["new body of work", "group show"],
    }
}

@dataclass
class ClassificationResult:
    title: str
    relevant: bool
    subject: Optional[str]
    tier: str
    reason: str

def normalise(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def contains_phrase(text, phrase):
    escaped = re.escape(phrase)
    pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return bool(re.search(pattern, text))

def classify(title: str, description: str = "") -> ClassificationResult:
    text = normalise(f"{title} {description}")
    
    # Check Africa relevance
    africa_match = next((t for t in ALL_AFRICA_TERMS if contains_phrase(text, t)), None)
    if not africa_match:
        return ClassificationResult(title=title, relevant=False, subject=None, tier="B", reason="no Africa term")
    
    # Check artist keywords
    artist_keywords = next((k for k in SUBJECTS["artists"]["keywords"] if contains_phrase(text, k)), None)
    artist_signals = sum(1 for s in SUBJECTS["artists"]["signals"] if contains_phrase(text, s))
    
    if artist_keywords and (artist_signals > 0 or "artist" in text):
        tier = "A" if artist_signals > 0 else "B"
        return ClassificationResult(
            title=title, 
            relevant=True, 
            subject="artists", 
            tier=tier, 
            reason=f"africa='{africa_match}' artist='{artist_keywords}' signals={artist_signals}"
        )
    
    return ClassificationResult(title=title, relevant=True, subject=None, tier="B", reason=f"africa='{africa_match}' no artist match")

if __name__ == "__main__":
    print("Africa Art Classifier loaded successfully!")
