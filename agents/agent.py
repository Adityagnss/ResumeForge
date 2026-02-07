"""
Agent module - Exposes the root agent for ADK discovery.
"""

# Import and expose the root agent
from agents.unibot import unibot

# ADK looks for root_agent in this module
root_agent = unibot
