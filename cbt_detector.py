# CBT Detector Module
# Core logic for detecting cognitive distortions

import spacy
import logging
from spacy.matcher import PhraseMatcher
from typing import List, Dict, Optional, Tuple, Union
from cbt_data import DISTORTION_PHASES, CBT_RESPONSES
from config import config

# Check if spacytextblob is available
try:
    from spacytextblob import spacytextblob
    SPACYTEXTBLOB_AVAILABLE = True
except ImportError:
    SPACYTEXTBLOB_AVAILABLE = False
    logging.warning("spacytextblob not available. Sentiment analysis will be disabled.")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CBTAnalyzer:
    # Class variable to track spacytextblob availability
    _sentiment_available = SPACYTEXTBLOB_AVAILABLE

    def __init__(self, model_name: str = None, similarity_threshold: float = None):
        self.model_name = model_name or config.model_name
        self.similarity_threshold = similarity_threshold or config.similarity_threshold
        self.distortion_phrases = DISTORTION_PHASES
        self.cbt_responses = CBT_RESPONSES

        # Initialize spaCy model with error handling
        self.nlp = self._load_spacy_model()
        self.phrase_matcher = self._setup_phrase_matcher()

        # Add sentiment analysis pipeline if available
        if self._sentiment_available:
            try:
                self.nlp.add_pipe('spacytextblob')
                logger.info("Sentiment analysis pipeline added successfully")
            except Exception as e:
                logger.warning(f"Failed to add sentiment analysis pipeline: {e}")
                self._sentiment_available = False

        # Cache for processed phrases to avoid re-processing
        self._phrase_docs_cache = {}

        # Pre-process all distortion phrases for faster similarity comparison
        self._preprocess_phrase_docs()

    def _load_spacy_model(self) -> spacy.Language:
        """Load spaCy model with proper error handling."""
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
            return nlp
        except OSError as e:
            logger.error(f"Failed to load spaCy model '{self.model_name}': {e}")
            logger.info("Please install the model with: python -m spacy download en_core_web_md")
            raise RuntimeError(f"spaCy model '{self.model_name}' not found. Please install it first.") from e

    def _setup_phrase_matcher(self) -> PhraseMatcher:
        """Set up PhraseMatcher for exact phrase detection."""
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        for label, phrases in self.distortion_phrases.items():
            patterns = [self.nlp.make_doc(phrase) for phrase in phrases]
            matcher.add(label.upper(), patterns)
        return matcher

    def _preprocess_phrase_docs(self) -> None:
        """Pre-process all distortion phrases into spaCy docs for faster comparison."""
        logger.debug("Pre-processing distortion phrases for faster similarity matching")
        for label, phrases in self.distortion_phrases.items():
            self._phrase_docs_cache[label] = [self.nlp(phrase) for phrase in phrases]
        logger.debug(f"Pre-processed {len(self._phrase_docs_cache)} distortion types")

    def _find_best_similarity_match(self, doc: spacy.tokens.Doc, label: str, threshold: float) -> Optional[Dict[str, str]]:
        """Find the best similarity match for a given distortion type using pre-processed docs."""
        best_match = None
        best_sim = 0.0

        # Use pre-processed docs from cache for better performance
        for phrase_doc, phrase in zip(self._phrase_docs_cache[label], self.distortion_phrases[label]):
            sim = doc.similarity(phrase_doc)
            if sim >= threshold and sim > best_sim:
                best_match = {
                    "type": label,
                    "match": phrase,
                    "method": f"similarity ({sim:.2f})",
                    "cbt_response": self.cbt_responses.get(label)
                }
                best_sim = sim

        return best_match

    def analyze_sentiment(self, text: str) -> Optional[Dict[str, Union[str, float]]]:
        """
        Analyze the sentiment of the input text.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with polarity, subjectivity, and sentiment classification, or None if unavailable
        """
        if not self._sentiment_available:
            return None

        try:
            doc = self.nlp(text)
            return {
                "polarity": doc._.blob.polarity,
                "subjectivity": doc._.blob.subjectivity,
                "sentiment": "positive" if doc._.blob.polarity > 0.1 else "negative" if doc._.blob.polarity < -0.1 else "neutral"
            }
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return None

    def detect_distortions(self, text: str) -> List[Dict[str, str]]:
        """
        Detect cognitive distortions in text using both exact matching and similarity.

        Args:
            text: Input text to analyze

        Returns:
            List of detected distortions with metadata
        """
        # Input validation
        if not isinstance(text, str):
            logger.warning(f"Invalid input type: expected str, got {type(text)}")
            return []

        text = text.strip()
        if len(text) < config.min_text_length:
            logger.debug(f"Text too short for analysis: {len(text)} characters")
            return []

        try:
            logger.debug(f"Processing text: '{text[:50]}...'")
            doc = self.nlp(text)
            results = []
            seen_types = set()

            # Check exact matches first
            matches = self.phrase_matcher(doc)
            for match_id, start, end in matches:
                label = self.nlp.vocab.strings[match_id].lower()
                if label not in seen_types:
                    seen_types.add(label)
                    results.append({
                        "type": label,
                        "match": doc[start:end].text,
                        "method": "exact",
                        "cbt_response": self.cbt_responses.get(label)
                    })
                    logger.debug(f"Found exact match for distortion: {label}")

            # Only check similarity for unseen distortion types
            remaining_types = set(self.distortion_phrases.keys()) - seen_types
            for label in remaining_types:
                best_match = self._find_best_similarity_match(doc, label, self.similarity_threshold)
                if best_match:
                    results.append(best_match)
                    seen_types.add(label)
                    logger.debug(f"Found similarity match for distortion: {label}")

            logger.info(f"Detected {len(results)} distortions in text")
            return results

        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return []


def detect_distortions_with_cbt(text: str, similarity_threshold: float = 0.85) -> List[Dict[str, str]]:
    """
    Convenience function for detecting distortions.
    Creates a new analyzer instance each time.
    """
    analyzer = CBTAnalyzer(similarity_threshold=similarity_threshold)
    return analyzer.detect_distortions(text)
