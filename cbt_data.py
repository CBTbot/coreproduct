# CBT Data Module
# Contains distortion phrases and CBT responses

from typing import Dict, List

DISTORTION_PHASES: Dict[str, List[str]] = {
    "catastrophizing": [
        "this is going to ruin everything", "I'll never recover from this",
        "it's all falling apart", "I'm doomed", "this will end terribly"
    ],
    "overgeneralization": [
        "I always screw things up", "nothing ever works out for me",
        "everything I do fails", "no one ever listens to me", "it's always my fault"
    ],
    "mind reading": [
        "they think I'm stupid", "everyone's laughing at me",
        "they don't like me", "he must be annoyed with me", "they think I'm a loser"
    ],
    "fortune telling": [
        "I know this will go wrong", "it's going to be a disaster",
        "they're going to reject me", "this will end badly", "nobody will show up"
    ],
    "emotional reasoning": [
        "I feel like a failure, so I must be one",
        "it feels hopeless, so it is",
        "I feel anxious, so something bad is going to happen",
        "if I feel this way, it must be true"
    ],
    "personalization": [
        "this happened because of me", "it's my fault they're upset",
        "I should have done more", "if I were better, this wouldn't have happened"
    ],
    "labeling": [
        "I'm such a loser", "he's a jerk", "I'm an idiot",
        "they're all selfish", "I'm broken"
    ],
    "should statements": [
        "I should be better at this", "they should know what I need",
        "I shouldn't feel this way", "I have to succeed", "I must always be in control"
    ]
}

CBT_RESPONSES: Dict[str, str] = {
    "catastrophizing": "It sounds like you're imagining the worst-case scenario. What are some more realistic outcomes that could happen?",
    "overgeneralization": "Are you basing this on one experience, or is there evidence it always happens? What might be an exception to this thought?",
    "mind reading": "How do you know what they're thinking? Could there be another explanation for their behavior?",
    "fortune telling": "Is there real evidence this will happen, or is this a prediction? What might go right instead?",
    "emotional reasoning": "Just because you feel it doesn't mean it's true. Can you separate the feeling from the facts?",
    "personalization": "Are you taking responsibility for something that isn't entirely in your control? Who else might be involved?",
    "labeling": "Instead of labeling yourself, what specific behavior are you unhappy with? What would you say to a friend in your shoes?",
    "should statements": "Are these 'shoulds' helping or hurting you? Can you reframe this thought in a kinder, more flexible way?"
}
