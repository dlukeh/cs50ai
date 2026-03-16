# Analysis

Below are my observations from analyzing two attention heads in BERT‑base.

Attention Head Analysis


This analysis explores two attention heads from BERT‑base and describes the linguistic patterns they appear to capture. The goal is not to identify the exact internal function of each head, but to make reasonable, intuitive observations about how attention helps the model understand relationships between words.
Layer 2, Head 4 — Modifier → Noun Linking
Observation


This head consistently directs strong attention from adjectives and determiners toward the nouns they modify. In multiple sentences, descriptive words such as bright, red, tall, elegant, and the attend heavily to the noun that anchors the phrase. This suggests the head is helping the model bind modifiers to the entities they describe.
Example Sentences

    “The bright red car sped quickly down the [MASK].”

        bright → car

        red → car

        the → car

    “He admired the tall, elegant [MASK] in the garden.”

        tall → [MASK]

        elegant → [MASK]

        the → [MASK]


Interpretation

This head appears to support the model’s understanding of noun phrase structure. By linking modifiers to their nouns, the model can better interpret the meaning of the phrase as a whole and make more accurate predictions for masked tokens within those phrases.
Layer 7, Head 9 — Verb → Object / Action Structure
Observation

This head frequently shows strong attention from verbs toward their direct objects or key participants in the action. It also tends to highlight prepositions or particles that complete the meaning of the verb phrase. This suggests the head is tracking predicate–argument structure.
Example Sentences

    “The dog chased the [MASK] across the yard.”

        chased → dog

        chased → the

        chased → [MASK]

    “She placed the book on the [MASK].”

        placed → book

        placed → on

        placed → [MASK]


Interpretation

This head seems to help the model understand “who is doing what to whom.” By linking verbs to their objects and associated prepositions, the model can better infer the structure of the event being described. This is especially helpful when predicting masked tokens that depend on the action, such as objects, locations, or instruments.


Conclusion

These observations highlight how different attention heads specialize in different linguistic relationships. Some heads focus on local phrase structure (e.g., adjectives modifying nouns), while others track broader syntactic roles (e.g., verbs and their objects). Together, these specialized patterns allow the model to build a coherent representation of the sentence and make accurate predictions for masked words.

