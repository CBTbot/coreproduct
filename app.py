#CBT Bot
#consider adding something like SpaCY for some natural language processing
#i'll look up the documentation later on that in order to figure out what i need to do
#next 
import random
import math
import spacy
from spacy.matcher import PhraseMatcher


nlp = spacy.load("en_core_web_sm")


#some cognitive distortion patterns 

# Load model with word vectors for similarity
nlp = spacy.load("en_core_web_md")

# Your distortion phrase dictionary
distortion_phrases = {
    "catastrophizing": [
        "this is going to ruin everything",
        "I’ll never recover from this",
        "it’s all falling apart",
        "I’m doomed",
        "this will end terribly"
    ],
    "overgeneralization": [
        "I always screw things up",
        "nothing ever works out for me",
        "everything I do fails",
        "no one ever listens to me",
        "it’s always my fault"
    ],
    "mind reading": [
        "they think I’m stupid",
        "everyone’s laughing at me",
        "they don’t like me",
        "he must be annoyed with me",
        "they think I’m a loser"
    ],
    # Add more distortions here as needed...
}

# Set up PhraseMatcher
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for label, phrases in distortion_phrases.items():
    patterns = [nlp.make_doc(phrase) for phrase in phrases]
    phrase_matcher.add(label.upper(), patterns)

# Unified detection function
def detect_distortions(text, similarity_threshold=0.85):
    doc = nlp(text)
    results = []

    # --- Exact Phrase Matching ---
    matches = phrase_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        results.append({
            "type": label.lower(),
            "match": span.text,
            "method": "exact"
        })

    # --- Fuzzy Similarity Matching ---
    for label, phrases in distortion_phrases.items():
        for phrase in phrases:
            phrase_doc = nlp(phrase)
            sim = doc.similarity(phrase_doc)
            if sim >= similarity_threshold:
                results.append({
                    "type": label,
                    "match": phrase,
                    "method": f"similarity ({sim:.2f})"
                })

    return results




cbt_responses = {
    "catastrophizing": "It sounds like you're imagining the worst-case scenario. What are some more realistic outcomes that could happen?",
    "overgeneralization": "Are you basing this on one experience, or is there evidence it always happens? What might be an exception to this thought?",
    "all-or-nothing thinking": "Are things really all bad, or is there some middle ground? What would a more balanced view look like?",
    "mind reading": "How do you know what they’re thinking? Could there be another explanation for their behavior?",
    "fortune telling": "Is there real evidence this will happen, or is this a prediction? What might go right instead?",
    "emotional reasoning": "Just because you feel it doesn’t mean it’s true. Can you separate the feeling from the facts?",
    "personalization": "Are you taking responsibility for something that isn’t entirely in your control? Who else might be involved?",
    "labeling": "Instead of labeling yourself, what specific behavior are you unhappy with? What would you say to a friend in your shoes?",
    "should statements": "Are these 'shoulds' helping or hurting you? Can you reframe this thought in a kinder, more flexible way?"
}

def detect_distortions_with_cbt(text, similarity_threshold=0.85):
    doc = nlp(text)
    results = []

    matches = phrase_matcher(doc)
    seen_types = set()

    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id].lower()
        seen_types.add(label)
        results.append({
            "type": label,
            "match": span.text,
            "method": "exact",
            "cbt_response": cbt_responses.get(label)
        })

    for label, phrases in distortion_phrases.items():
        if label in seen_types:
            continue  # Skip if already matched exactly
        for phrase in phrases:
            phrase_doc = nlp(phrase)
            sim = doc.similarity(phrase_doc)
            if sim >= similarity_threshold:
                results.append({
                    "type": label,
                    "match": phrase,
                    "method": f"similarity ({sim:.2f})",
                    "cbt_response": cbt_responses.get(label)
                })
                seen_types.add(label)
                break  # Avoid multiple matches for the same distortion

    return results

#distortions = {
    #'All-or-nothing thinking': 'You see things in black-and-white terms, without acknowledging the gray areas in between.',
   # 'Overgeneralization': 'You view a single negative event as a never-ending pattern of defeat.',
   # 'Mental filter': 'You focus on the negative aspects of a situation, ignoring the positive.',
    #'Disqualifying the positive': 'You reject positive experiences by insisting they don\’t count.',
   # 'Jumping to conclusions': 'You make negative interpretations without actual evidence.',
  #  'Catastrophizing': 'You expect the worst possible outcome or view a situation as far worse than it really is.',
  #  'Emotional reasoning': 'You assume your negative emotions reflect objective reality.',
  #  'Should statements': 'You criticize yourself or others with “shoulds,” “oughts,” or “musts.”',
  #  'Labeling and mislabeling': 'You assign global negative labels to yourself or others based on a single event.',
  #  'Personalization': 'You believe you are responsible for events outside your control.'
#}

#initial chatbot greeting
#def greet():
    # print("Hello! I'm your CBT Assistant. Let's work together to challenge negative thoughts.")
     #print("I can help you recognize thinking patterns and offer suggestions.")
    # print("Type 'exit' anytime to end the chat.\n")

#Asking for user's automatic thoughts 
#def get_thought():
   # thought = input("can you tell me about a negative thought you've been having recently?")
    #if thought.lower == 'exit':
       # return None
    #return thought

#Identifying cognitive distortions 
#def cognitive_distortion(thought):
    #identified_distortions = []
    #for distorion, explanation in distortions.items():
       # if distorion.lower() in thought.lower():
           # identified_distortions.append((distorion , explanation))
   ## return identified_distortions

# Identifying cognitive distortions
#def identify_distortion(thought):
    #identified_distortions = []
   # for distortion, explanation in distortions.items():
        #if distortion.lower() in thought.lower():
            #identified_distortions.append((distortion, explanation))
    #return identified_distortions


#Challenge negative thoughts 
#def challenge_thoughts(distortions):
   # print("Let's examine your thought and challenge it!\n")
    #for distortion, explanation in distortions:
       # print(f"Distortion {distortion}\n Explanation {explanation}")
    #new_thought = input("\n What's a more balanced way of looking at this?")
    #return new_thought

#def cbt_chatbot():
   # greet()

    #while True:
        #thought = get_thought()
        #if not thought:
            #print("Goodbye!")
            #break
       # distortions_found = identify_distortion(thought)

        #if distortions_found:
           # print("\n It seems like your thought may contain some cognitive distortions.")
            #new_thought = challenge_thoughts(distortions_found)
            #print(f'\nYour new thought: {new_thought}')
        #else:
            #print(f'\nIt seems like your thought is more netural. Keep it up!')

        #cont = input("\nWould like you talk about another thought? (Yes/No) ")

        #if cont.lower() != 'yes':
            #print('Goodbye!')
           # break  



#if __name__ == "__main__":
    #cbt_chatbot()
    