import random

SOFT_QUOTES = [
    "Small steps still count.",
    "You don’t need to solve everything today.",
    "Clarity grows when pressure reduces.",
    "Progress can be quiet.",
    "Be patient with your mind—it's working hard.",
]

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
            "What are the two options you’re weighing, and what are you trying to protect in each?",
            "What would a 'good enough' outcome look like (not perfect)?",
        ]
    prompts += [
        "Which value matters most here (peace, growth, stability, self-respect, something else)?",
        "What is one small step that gives clarity without fully committing?",
    ]

    quote = random.choice(SOFT_QUOTES) if show_quote else None
    return summary, prompts[:6], quote
