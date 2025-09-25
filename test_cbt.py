#!/usr/bin/env python3
"""
Basic tests for CBT Chatbot functionality.
Run with: python test_cbt.py
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cbt_detector import CBTAnalyzer, detect_distortions_with_cbt
from cbt_data import DISTORTION_PHASES, CBT_RESPONSES
from config import config


def test_exact_match_detection():
    """Test exact phrase matching."""
    analyzer = CBTAnalyzer()
    result = analyzer.detect_distortions("this is going to ruin everything")

    # Find the exact match for catastrophizing
    exact_matches = [r for r in result if r["method"] == "exact" and r["type"] == "catastrophizing"]

    assert len(exact_matches) == 1, f"Expected exactly 1 exact match for catastrophizing, got {len(exact_matches)}"
    assert exact_matches[0]["match"] == "this is going to ruin everything", f"Match text doesn't match input"
    print("✅ Exact match detection test passed")


def test_similarity_match_detection():
    """Test similarity-based matching."""
    analyzer = CBTAnalyzer()
    result = analyzer.detect_distortions("I feel like a complete failure")

    # Should find emotional reasoning and possibly others
    distortion_types = [r["type"] for r in result]
    assert "emotional reasoning" in distortion_types, f"Expected 'emotional reasoning' in {distortion_types}"

    # Check that similarity method is used
    methods = [r["method"] for r in result]
    similarity_methods = [m for m in methods if m.startswith("similarity")]
    assert len(similarity_methods) > 0, f"Expected at least one similarity method, got {methods}"
    print("✅ Similarity match detection test passed")


def test_sentiment_analysis():
    """Test sentiment analysis functionality."""
    analyzer = CBTAnalyzer()

    # Test positive sentiment
    positive_result = analyzer.analyze_sentiment("I feel so happy and excited!")
    assert positive_result is not None, "Sentiment analysis should be available"
    assert positive_result["sentiment"] == "positive", f"Expected positive sentiment, got {positive_result['sentiment']}"
    assert positive_result["polarity"] > 0, f"Expected positive polarity, got {positive_result['polarity']}"

    # Test negative sentiment
    negative_result = analyzer.analyze_sentiment("I feel terrible and sad")
    assert negative_result["sentiment"] == "negative", f"Expected negative sentiment, got {negative_result['sentiment']}"
    assert negative_result["polarity"] < 0, f"Expected negative polarity, got {negative_result['polarity']}"

    print("✅ Sentiment analysis test passed")


def test_input_validation():
    """Test input validation and error handling."""
    analyzer = CBTAnalyzer()

    # Test empty input
    result = analyzer.detect_distortions("")
    assert result == [], f"Expected empty result for empty input, got {result}"

    # Test very short input
    result = analyzer.detect_distortions("hi")
    assert result == [], f"Expected empty result for short input, got {result}"

    # Test non-string input
    result = analyzer.detect_distortions(123)
    assert result == [], f"Expected empty result for non-string input, got {result}"

    print("✅ Input validation test passed")


def test_configuration():
    """Test configuration loading."""
    assert config.similarity_threshold == 0.85, f"Expected threshold 0.85, got {config.similarity_threshold}"
    assert config.min_text_length == 3, f"Expected min length 3, got {config.min_text_length}"
    assert config.model_name == "en_core_web_md", f"Expected model 'en_core_web_md', got {config.model_name}"
    print("✅ Configuration test passed")


def test_data_integrity():
    """Test that distortion data is properly structured."""
    assert len(DISTORTION_PHASES) == 8, f"Expected 8 distortion types, got {len(DISTORTION_PHASES)}"
    assert len(CBT_RESPONSES) == 8, f"Expected 8 CBT responses, got {len(CBT_RESPONSES)}"

    # Check that all distortion types have responses
    for distortion_type in DISTORTION_PHASES.keys():
        assert distortion_type in CBT_RESPONSES, f"Missing response for distortion type: {distortion_type}"

    print("✅ Data integrity test passed")


def run_all_tests():
    """Run all tests and report results."""
    print("🧪 Running CBT Chatbot Tests...\n")

    tests = [
        test_configuration,
        test_data_integrity,
        test_input_validation,
        test_exact_match_detection,
        test_similarity_match_detection,
        test_sentiment_analysis,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("💥 Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
