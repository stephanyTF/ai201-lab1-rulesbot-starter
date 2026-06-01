# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Each chunk will be formatted as a labeled block. The header mentions the game, followed by the chunk text, with a delimter " ----". This delimter is the Markdown separator that LLMs handle well. I won't include the distance score since the chunks should already be ranked in the order and including the score may distract the LLM from the text. 

```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
Answer using only the rule text provided in the context section. Do not draw on outside knowledge or fill in gaps from what you know about board games.

Begin every answer with: "According to the rules of <game_name>..." or "Based on <game_name>'s rules..."

Quote the relevant rule text directly, then explain it in plain language.

If the context only partially addresses the question, state what the rules do say and explicitly note what is not covered.




```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
At the end of each answer, always cite the source of the answer following this example: "According to the Monopoly rules, to get out of Jail you must either pay a $50 fine before rolling on either of your next two turns, use a Get Out of Jail Free card, or roll doubles. [Source: Monopoly_Rules.txt]"
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
If the answer is not in the provided text at all, respond with: "The provided rules do not cover this question."
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
I'll remove the low-relevance chunks because I don't want to risk providing the LLM with poor quality context and misinform the user. It's better to admit lacking knowledge rather than confidently providing wrong information and weakening trust. 

Some of the tradeoffs for the different methods:

1. Filtering Low-relevant chunks by cutting off at a distance threshold or removing entirely may risk removing a chunk that actually contains the right rule.

2. Passing all the chunks in will risk diluting the correct response with less meaningful text that doesn't answer the user's query in the end.


```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
The system message should have behavioral instructions (how to answer, what format to use, how to handle missing info). For the user message, it should be structured with the retrieved chunks as context plus the original query. An example would be: "Here are the relevant rules: [chunks]. Based on these, answer: [query]."

```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: How to give clues in the game?
Response: "The  rules do not cover this question  in question as they seem to pertain to two different games: Clue and Codenames..."
Correctly grounded? Yes
Cited the right game? Not really
```

**One thing you changed from your original spec after seeing the actual output:**

```
I added to the spec a case where the user's query is ambiguous such as not specifying a game. By asking the user to clarify the question, the RulesBot could produce a more meaningful and helpful output. However, the RulesBot, doesn't ask the user to clarify the question but instead tries to explain the rules of the different games whose chunks have the least distance scores. The system prompt may need to be structured better to allow the RolesBot to have the flexibilty to ask for clarification rather than being limited to answering with what its given. 
```
