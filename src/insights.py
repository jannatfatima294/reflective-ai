import random

# Quotes grouped by emotional state
QUOTES_BY_STATE = {
    "Anxious / Tense": [
        "You don’t need to solve everything at once.",
        "Pressure is information, not a command.",
        "Slow down enough to hear what you actually need.",
        "It’s okay to pause without quitting.",
        "Breathe first, then decide.",
    ],
    "Heavy / Low": [
        "Rest is not a failure of discipline.",
        "You are allowed to move at a gentler pace.",
        "Low energy doesn’t mean low worth.",
        "Some days are for surviving, not excelling.",
        "Be kind to yourself today.",
    ],
    "Positive / Hopeful": [
        "Momentum grows when you trust yourself.",
        "This excitement is a signal — listen to it.",
        "Growth doesn’t have to be rushed to be real.",
        "You’re allowed to feel hopeful without overthinking it.",
        "Keep the direction, take the next step.",
    ],
    "Conflicted / Uncertain": [
        "Uncertainty is often the space before clarity.",
        "You don’t need certainty to take a small step.",
        "It’s okay to hold two truths at once.",
        "Confusion doesn’t mean you’re lost.",
        "A smaller decision can come first.",
    ],
    "Calm / Stable": [
        "Stillness can be productive.",
        "Clarity often comes when nothing is forced.",
        "This steadiness is something to protect.",
        "You don’t need to add pressure to make progress.",
        "Keep it simple, keep it steady.",
    ],
}

# Fallback quotes (if a state is missing for any reason)
SOFT_QUOTES_FALLBACK = [
    "Small steps still count.",
    "You don’t need to solve everything today.",
    "Clarity grows when pressure reduces.",
    "Progress can be quiet.",
    "Be patient with your mind—it's working hard.",
]

def pick_quote(emotional_state: str) -> str:
    quotes = QUOTES_BY_STATE.get(emotional_state)
    if quotes and len(quotes) > 0:
        return random.choice(quotes)
    return random.choice(SOFT_QUOTES_FALLBACK)

def build_output(emotional_state: str, stress_level: str, conflict_level: str, show_quote: bool):
    summary = (
        f"Text signals suggest an emotional state of **{emotional_state}**, "
        f"with **{stress_level}** cognitive load and **{conflict_level}** decision conflict."
    )

    prompts = []
    if stress_level in ["High", "Moderate"]:
        prompts += [
            "What part of this situation is draining you most (time, expectations, fear, uncertainty)?",
            "If you reduce the issue to one sentence, what is it?",
        ]
    if conflict_level in ["Medium", "High"]:
        prompts += [
            "What are the two options you’re weigh

