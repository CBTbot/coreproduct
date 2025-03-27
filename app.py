#CBT Bot
#consider adding something like SpaCY for some natural language processing
#i'll look up the documentation later on that in order to figure out what i need to do
#next 
import random
import math

#some cognitive distortion patterns 
distortions = {
    'All-or-nothing thinking': 'You see things in black-and-white terms, without acknowledging the gray areas in between.',
    'Overgeneralization': 'You view a single negative event as a never-ending pattern of defeat.',
    'Mental filter': 'You focus on the negative aspects of a situation, ignoring the positive.',
    'Disqualifying the positive': 'You reject positive experiences by insisting they don\’t count.',
    'Jumping to conclusions': 'You make negative interpretations without actual evidence.',
    'Catastrophizing': 'You expect the worst possible outcome or view a situation as far worse than it really is.',
    'Emotional reasoning': 'You assume your negative emotions reflect objective reality.',
    'Should statements': 'You criticize yourself or others with “shoulds,” “oughts,” or “musts.”',
    'Labeling and mislabeling': 'You assign global negative labels to yourself or others based on a single event.',
    'Personalization': 'You believe you are responsible for events outside your control.'
}

#initial chatbot greeting
def greet():
     print("Hello! I'm your CBT Assistant. Let's work together to challenge negative thoughts.")
     print("I can help you recognize thinking patterns and offer suggestions.")
     print("Type 'exit' anytime to end the chat.\n")

#Asking for user's automatic thoughts 
def get_thought():
    thought = input("can you tell me about a negative thought you've been having recently?")
    if thought.lower == 'exit':
        return None
    return thought

#Identifying cognitive distortions 
def cognitive_distortion(thought):
    identified_distortions = []
    for distorion, explanation in distortions.items():
        if distorion.lower() in thought.lower():
            identified_distortions.append((distorion , explanation))
    return identified_distortions

# Identifying cognitive distortions
def identify_distortion(thought):
    identified_distortions = []
    for distortion, explanation in distortions.items():
        if distortion.lower() in thought.lower():
            identified_distortions.append((distortion, explanation))
    return identified_distortions


#Challenge negative thoughts 
def challenge_thoughts(distortions):
    print("Let's examine your thought and challenge it!\n")
    for distortion, explanation in distortions:
        print(f"Distortion {distortion}\n Explanation {explanation}")
    new_thought = input("\n What's a more balanced way of looking at this?")
    return new_thought

def cbt_chatbot():
    greet()

    while True:
        thought = get_thought()
        if not thought:
            print("Goodbye!")
            break
        distortions_found = identify_distortion(thought)

        if distortions_found:
            print("\n It seems like your thought may contain some cognitive distortions.")
            new_thought = challenge_thoughts(distortions_found)
            print(f'\nYour new thought: {new_thought}')
        else:
            print(f'\nIt seems like your thought is more netural. Keep it up!')

        cont = input("\nWould like you talk about another thought? (Yes/No) ")

        if cont.lower() != 'yes':
            print('Goodbye!')
            break  



if __name__ == "__main__":
    cbt_chatbot()
    