# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*



---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
The 3 arguments I will pass when using  `_collection.query()` to find relevant chunks are:

1. query_texts : A list containing the queries since it's designed to take in a list even if there's only 1 query. This will let the RulesBot know what question(s) is asked and what to look for.
2. n_results: An integer representing how many relevant results to return
3. include: A list of strings that specifies what type of output to return like as "documents", "metadatas", "distances"
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
Relevant Chunk Text-
["Teams alternate turns. On each turn, the active team's Spymaster gives a clue, then the Field Operatives guess."]

Game: Codenames

Distance: .123 (Lower Cosine Score == greater Similarity)

The field "text" comes from results["documents"][0] (this is a lisit of the chunk texts), the game name comes from results["metadatas"][0], and the distance comes from results["distances"][0].

```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
I need an index of [0] to unwrap the outer list and gest results for our one query. Nesting exists, since _collection.query() takes in query_texts a as list, it can handle multiple quiries at once, therefore the return value is one inner list per query. 
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
I rather return all `n_results` to avoid fine-tuning the threshold and have more transparency in how the text chunks are scored in relevancy. 

When filtering results above a certain score, one possible tradeoff is excluding a result that's acutally relevant to the query if it's set too strictly. 

When returning all `n_results`, a tradeoff is diluting the relevant context with results that have less significance to the query.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a) If the collection is empty, it returns nothing.

(b) If the query matches no chunks well, it still returns a chunk that has the least similarity score but are still high above .7 (e.g. ~.86)

(c) When the query matches chunks from multiple games, it will return chunks from a variety of games with the least difference score.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: "What kind of clue can you give in the game?"
Top result game: Clue
Distance score: .337
Does it make sense? : No because the Clue game doesn't involve giving clues but moreso giving suggestions or accusations (whether false or true). I was expecting Codenames since the game involes a person giving clues to their team. 
```

**One thing about the query results that surprised you:**

```
The clue game being brought up as the top result surprised me because based on the game rule docs, the Clue game rules only have about 5 words that mention "clue" while the Codenames game has about 15 appearances. I wanted to test how the retrieval would perform when given a word that is shared between two games and I see that the retreival process may have given more weight to title or headers which was why the Clue game ranked higher despite not having explicit rules about giving clues. 
```
