import os
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool


def validate_newsletter(output):
    lines = output.raw.splitlines()
    if (
        len(lines) != 5
        or lines[0] != "Tech in 5 lines"
        or any(
            not lines[index].startswith(f"{index}. ")
            or not lines[index][3:].strip()
            for index in range(1, 4)
        )
        or not lines[4].startswith("Why it matters: ")
        or not lines[4][len("Why it matters: ") :].strip()
        or any(not line.strip() for line in lines)
    ):
        return (
            False,
            "Use exactly five nonempty lines: 'Tech in 5 lines', three lines "
            "numbered 1. through 3., and a 'Why it matters: ' line. No other text.",
        )
    return True, output.raw


def main():
    missing = [
        name for name in ("OPENAI_API_KEY", "SERPER_API_KEY") if not os.getenv(name)
    ]
    if missing:
        raise SystemExit(f"Set the following environment variables: {', '.join(missing)}")

    today = datetime.now().astimezone().strftime("%Y-%m-%d")
    model = os.getenv("MODEL") or "gpt-4o-mini"
    search = SerperDevTool()
    researcher = Agent(
        role="Technology News Researcher",
        goal="Find the three most important current technology news stories.",
        backstory=(
            "You are a meticulous technology reporter who searches the web, "
            "checks publication dates and relies on credible sources."
        ),
        tools=[search],
        llm=model,
        allow_delegation=False,
        verbose=True,
    )
    writer = Agent(
        role="Technology Newsletter Writer",
        goal="Turn researched news into a concise, accurate newsletter.",
        backstory=(
            "You are an editor who writes clearly from supplied reporting, "
            "without adding unverified facts."
        ),
        tools=[],
        llm=model,
        allow_delegation=False,
        verbose=True,
    )
    find = Task(
        description=(
            f"Search the web for the top three distinct technology news stories "
            f"for today, {today} (local date). Prioritize significance and "
            "recent reporting, and check publication dates. For each story provide "
            "its headline, a factual one-sentence summary, publication date, "
            "source name and source URL. Do not invent stories, dates or URLs; "
            "if you cannot verify three current stories, say so explicitly."
        ),
        expected_output=(
            "A numbered list of three distinct verified stories, each with a "
            "headline, one-sentence summary, publication date, source name and "
            "source URL; explicitly identify any missing verified stories."
        ),
        agent=researcher,
    )
    write = Task(
        description=(
            "Write a newsletter using only the Researcher's supplied results. "
            "Do not search, invent facts, or fill gaps with unverified stories. "
            "If a story is missing, use its numbered line to say it could not "
            "be verified. Include no preamble, blank lines, or Markdown fences."
        ),
        expected_output=(
            "Exactly five nonempty lines: line 1 is 'Tech in 5 lines'; lines "
            "2-4 begin '1. ', '2. ', and '3. ' respectively and each summarize "
            "one story; line 5 begins 'Why it matters: ' and explains the "
            "overall significance in one sentence."
        ),
        agent=writer,
        context=[find],
        guardrail=validate_newsletter,
    )
    crew = Crew(
        agents=[researcher, writer],
        tasks=[find, write],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    valid, message = validate_newsletter(result)
    if not valid:
        raise SystemExit(f"Newsletter formatting failed: {message}")
    print(result.raw)


if __name__ == "__main__":
    main()
