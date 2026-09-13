import os
from dotenv import load_dotenv
from google.adk.agents import Agent

from my_agent.tools.search import google_search
from my_agent.tools.problem_scorer import score_problem
from my_agent.tools.ranker import rank_problems
from my_agent.tools.facebook_tool import open_facebook

# Load environment variables from .env file
load_dotenv()

root_agent = Agent(
    name="business_problem_agent",
    model="gemini-3.1-flash-lite",
    instruction="""
You are a Business Opportunity Research Agent.

If the user asks you to open Facebook, simply use the `open_facebook` tool.

Otherwise, follow this workflow strictly for business research:
1. Search for real user problems using `google_search`.
2. Extract distinct problems from the evidence.
3. For every problem, provide evidence for each scoring dimension.
4. Use `score_problem` to calculate the deterministic score.
5. Never invent evidence.
6. If evidence is weak or unavailable, explicitly say so.
7. Collect scored problems.
8. Use `rank_problems` to rank them.
9. Return:
   - Top 3 opportunities
   - Total score
   - Priority
   - Key supporting evidence
   - Main weakness / uncertainty
   - Suggested next validation step

Do not manually calculate totals.
Always use `score_problem`.
Do not manually rank opportunities.
Always use `rank_problems`.
""",
    tools=[
        google_search,
        score_problem,
        rank_problems,
        open_facebook,
    ],
)
