# CBT Chatbot Module
# Handles the interactive chat interface

import logging
from typing import List, Dict
from cbt_detector import CBTAnalyzer

logger = logging.getLogger(__name__)


class CBTChatbot:
    def __init__(self) -> None:
        try:
            self.analyzer = CBTAnalyzer()
            logger.info("CBT Chatbot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize CBT Chatbot: {e}")
            raise

    def format_distortion_response(self, distortion: Dict[str, str]) -> str:
        """Format a single distortion detection for display."""
        response_parts = [
            f"⚠️ Detected distortion: *{distortion['type']}* ({distortion['method']})",
            f"🔍 Example phrase: \"{distortion['match']}\"",
            f"💬 CBT reflection: {distortion['cbt_response']}"
        ]
        return "\n".join(response_parts)

    def process_input(self, user_input: str) -> str:
        """Process user input and return appropriate response."""
        if user_input.lower() in ("exit", "quit"):
            return "CBT Bot: Take care! Have a good day 👋"

        results = self.analyzer.detect_distortions(user_input)
        sentiment = self.analyzer.analyze_sentiment(user_input)

        response_lines = []

        # Add sentiment analysis if available
        if sentiment:
            sentiment_emoji = "😊" if sentiment["sentiment"] == "positive" else "😔" if sentiment["sentiment"] == "negative" else "😐"
            response_lines.append(f"📊 Sentiment: {sentiment['sentiment'].title()} {sentiment_emoji} "
                                f"(Polarity: {sentiment['polarity']:.2f}, Subjectivity: {sentiment['subjectivity']:.2f})")
            response_lines.append("")

        if results:
            for r in results:
                response_lines.append(self.format_distortion_response(r))
                response_lines.append("")  # Empty line between distortions
            return "\n".join(response_lines)
        else:
            response_lines.append("✅ No distortions detected. You seem to be thinking clearly. 😊\n")
            return "\n".join(response_lines)

    def run(self) -> None:
        """Run the interactive chatbot loop."""
        print("🧠 CBT Chatbot: Let's talk. Type 'exit' to end.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                # Additional input validation
                if not user_input:
                    print("CBT Bot: Please enter some text to analyze.\n")
                    continue

                response = self.process_input(user_input)
                print(response)

                if "Take care" in response:
                    break

            except KeyboardInterrupt:
                print("\nCBT Bot: Chat interrupted. Take care! 👋")
                logger.info("Chat session interrupted by user")
                break
            except EOFError:
                print("\nCBT Bot: End of input detected. Take care! 👋")
                logger.info("Chat session ended due to EOF")
                break
            except Exception as e:
                error_msg = f"CBT Bot: Sorry, I encountered an error: {e}"
                print(error_msg)
                logger.error(f"Unexpected error in chat loop: {e}")
                continue


def start_chatbot() -> None:
    """Convenience function to start the chatbot."""
    bot = CBTChatbot()
    bot.run()
