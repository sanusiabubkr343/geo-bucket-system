import re
from difflib import SequenceMatcher
from typing import List, Optional, Set

# ===== CONFIGURABLE PARAMETERS =====
COMMON_SUFFIXES: Set[str] = {
    # Property/development types
    'estate', 'phase', 'layout', 'area', 'zone', 'district',
    'quarters', 'village', 'town', 'city', 'metropolis',
    'suburb', 'extension', 'sector', 'block', 'ward', 'precinct',
    'compound', 'community', 'settlement', 'housing',

    # Directional/positional
    'north', 'south', 'east', 'west', 'central',
    'upper', 'lower', 'inner', 'outer', 'middle',
    'new', 'old',

    # Road/street types
    'street', 'road', 'avenue', 'boulevard', 'drive', 'lane',
    'way', 'close', 'crescent', 'circle', 'court', 'place',
    'highway', 'expressway', 'motorway', 'freeway',

    # Administrative divisions
    'local', 'government', 'lga', 'state', 'federal',
    'municipal', 'council', 'borough', 'county', 'parish',

    # Nigerian-specific suffixes
    'lekki', 'ikeja', 'victoria', 'island', 'mainland',
    'apapa', 'surulere', 'yaba', 'ajah', 'ikoyi',

    # Numbered suffixes
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    'first', 'second', 'third', 'fourth', 'fifth',
    'sixth', 'seventh', 'eighth', 'ninth', 'tenth',

    # General location markers
    'junction', 'roundabout', 'crossing', 'intersection',
    'corner', 'end', 'side', 'front', 'back', 'center', 'centre',

    # Building/complex types
    'plaza', 'mall', 'market', 'complex', 'center', 'centre',
    'building', 'towers', 'heights', 'gardens', 'park',
    'resort', 'hotel', 'motel', 'inn',

    # Transportation hubs
    'airport', 'station', 'terminal', 'depot', 'garage',
    'parking', 'bus', 'train', 'railway',

    # Natural features
    'river', 'hill', 'mountain', 'valley', 'lake', 'sea',
    'beach', 'coast', 'shore', 'forest', 'wood', 'field',

    # Religious/educational
    'church', 'mosque', 'temple', 'cathedral', 'school',
    'college', 'university', 'academy', 'institute',

    # Commercial/industrial
    'industrial', 'commercial', 'business', 'trade',
    'market', 'shop', 'store', 'mall', 'plaza'
}

OBVIOUS_STOP_WORDS: Set[str] = {
    # Articles and pronouns
    'a', 'an', 'the', 'some', 'any', 'all', 'every', 'each',
    'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her',
    'its', 'our', 'their',

    # Prepositions
    'in', 'on', 'at', 'by', 'for', 'to', 'from', 'with', 'via',
    'of', 'about', 'above', 'below', 'under', 'over', 'between',
    'among', 'through', 'across', 'around', 'along', 'beside',
    'near', 'opposite', 'beyond', 'within', 'without', 'into',
    'onto', 'upon', 'inside', 'outside',

    # Conjunctions
    'and', 'or', 'but', 'nor', 'so', 'yet', 'either', 'neither',
    'both', 'whether', 'although', 'though', 'even', 'if', 'unless',
    'since', 'until', 'when', 'while', 'before', 'after', 'because',

    # Adverbs and intensifiers
    'very', 'quite', 'rather', 'somewhat', 'just', 'only', 'merely',
    'simply', 'also', 'too', 'as', 'well', 'here', 'there', 'where',
    'when', 'why', 'how', 'once', 'twice', 'thrice'
}




# ===== UTILITY FUNCTIONS =====
def _clean_text(text: str) -> str:
    """Clean and normalize text"""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return re.sub(r'[^\w\s,]', '', text)


def _calculate_word_frequencies(locations: List[str]) -> dict:
    """Calculate word frequencies from known locations"""
    word_freq = {}
    for loc in locations:
        for word in re.findall(r'\w+', loc.lower()):
            word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq


def _should_skip_word(
        word: str,
        part_index: int,
        word_freq: dict,
        total_locations: int,
        remove_common_suffixes: bool,
        frequency_threshold: float = 0.3
) -> bool:
    """Determine if a word should be skipped based on various criteria"""
    # Skip common words across locations
    if word_freq and word in word_freq:
        frequency = word_freq[word] / total_locations
        if frequency > frequency_threshold:
            return True

    # Skip common suffixes in non-first parts
    if remove_common_suffixes and part_index > 0:
        if word in COMMON_SUFFIXES:
            return True

    # Skip obvious stop words
    if word in OBVIOUS_STOP_WORDS:
        return True

    return False


def _get_fallback_name(name: str) -> str:
    """Get fallback name when no normalized parts are found"""
    words = re.findall(r'\w+', name)
    if not words:
        return name

    # Return the longest word as it's often the most distinctive
    try:
        return max(words, key=len)
    except ValueError:
        return words[0] if words else name


# ===== MAIN FUNCTION =====
def normalize_location_name(
        name: str,
        known_locations: Optional[List[str]] = None,
        remove_common_suffixes: bool = True
) -> str:
    """
    Smart location normalization that learns from context

    Args:
        name: Location name to normalize
        known_locations: List of other locations in the system for context
        remove_common_suffixes: Whether to remove common location suffixes
    """
    # Clean input
    cleaned_name = _clean_text(name)

    # Split by commas for hierarchical parsing
    parts = [p.strip() for p in cleaned_name.split(',') if p.strip()]
    if not parts:
        return _get_fallback_name(cleaned_name)

    # Calculate word frequencies if we have known locations
    word_freq = {}
    total_locations = 0
    if known_locations:
        word_freq = _calculate_word_frequencies(known_locations)
        total_locations = len(known_locations)

    # Process each part
    normalized_parts = []

    for i, part in enumerate(parts):
        words = part.split()
        filtered_words = []

        for word in words:
            if not _should_skip_word(
                    word=word,
                    part_index=i,
                    word_freq=word_freq,
                    total_locations=total_locations,
                    remove_common_suffixes=remove_common_suffixes
            ):
                filtered_words.append(word)

        if filtered_words:
            normalized_parts.append(' '.join(filtered_words))

    # Handle case where no normalized parts were found
    if not normalized_parts:
        return _get_fallback_name(cleaned_name)

    # Return appropriate format
    if len(normalized_parts) > 1:
        return ', '.join(normalized_parts)
    return normalized_parts[0]


# ===== ALIASES AND HELPER FUNCTIONS =====


def similarity(a: str, b: str) -> float:
    """Calculate string similarity ratio (case-insensitive)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# ===== CONFIGURATION UTILITIES =====
def add_custom_suffixes(new_suffixes: Set[str]) -> None:
    """Add custom suffixes to the common suffixes list"""
    COMMON_SUFFIXES.update(new_suffixes)


def add_custom_stop_words(new_stop_words: Set[str]) -> None:
    """Add custom stop words to the obvious stop words list"""
    OBVIOUS_STOP_WORDS.update(new_stop_words)


def get_all_suffixes() -> Set[str]:
    """Get all configured suffixes"""
    return COMMON_SUFFIXES.copy()


def get_all_stop_words() -> Set[str]:
    """Get all configured stop words"""
    return OBVIOUS_STOP_WORDS.copy()