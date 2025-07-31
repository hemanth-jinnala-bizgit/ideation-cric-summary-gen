# test_tools.py
from cricket_api_tools import ScorecardTool, MatchInfoTool, HighlightsTool, CommentaryTool
from pydantic import ValidationError

# Replace with a real Match ID
match_id = "105778"  # Example match

# Instantiate tools
scorecard_tool = ScorecardTool()
match_info_tool = MatchInfoTool()
highlights_tool = HighlightsTool()
commentary_tool = CommentaryTool()

# Test each tool
print("🧪 Testing Cricket Tools...\n")

print("📋 Match Info:\n")
print(match_info_tool.run(match_id=match_id))

print("\n🏏 Scorecard:\n")
print(scorecard_tool.run(match_id=match_id))

print("\n⚡ Highlights:\n")
print(highlights_tool.run(match_id=match_id))

print("\n🎤 Commentary:\n")
print(commentary_tool.run(match_id=match_id))
