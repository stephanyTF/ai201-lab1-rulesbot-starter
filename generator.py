from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return "The provided rules do not cover this question."

    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(f"Game: {chunk['game']}\n{chunk['text']}")
    context = "\n----\n".join(context_blocks)

    system_prompt = (
        "If the query or user's question is ambiguous such as not specifying a game, ask the user to state which game they are asking about.\n\n"
        "Answer using only the rule text provided in the context section. "
        "Do not draw on outside knowledge or fill in gaps from what you know about board games.\n\n"
        "Begin every answer with: \"According to the rules of <game_name>...\" or \"Based on <game_name>'s rules...\"\n\n"
        "Quote the relevant rule text directly, then explain it in plain language.\n\n"
        "If the context only partially addresses the question, state what the rules do say and explicitly note what is not covered.\n\n"
        "If the answer is not in the provided text at all, respond with: \"The provided rules do not cover this question.\"\n\n"
        "At the end of each answer, always cite the source using the format: [Source: <filename>]"
    )

    user_message = f"Here are the relevant rules:\n\n{context}\n\n----\n\nBased on these rules, answer: {query}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
