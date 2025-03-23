1. The OpenAI SDK enables you to build agentic AI apps in a lightweight, easy to use package with very few abstractions.
Agents SDK is the official upgrade to the experimental Swarm framework (OpenAI framework for Agents)

2. The SDK is built on 3 simple ideas
    - Agents
    - Handoffs
    - Guardrails

3. What makes SDK special? Two core principles:
    1) Enough features to be useful without overwhelming you
    2) Works perfectly out of the box, but can be customized when needed

4. We'll explore each part of the SDK, starting with Agents
    Agents are your AI workers

5. Running *`agents`* is super simple! The SDK handle all the complex work of:
    - Starting the agent
    - Letting it use tools and make decisions
    - Delivering the final answer

6. Creating an agent is super straightforward.
    You give it:
    - A name
    - Instructions
    - A model to use
    - Any tools it needs access to

7. Running agents is where the magic happens! The SDK handles all the complex work behind the scenes

8. The agent loop in how agents accomplish tasks that have multiple steps

9. The SDK let you define exactly what type of results/outputs you need:
    - Simple text response for conversational interface
    - Structured data like JSON for programmatic use
    - Rich information your app can immediately act on

10. Want to chain multiple agents together? The SDK makes this easy
    Agent SDK is perfect for building multi-agent systems.

11. For real-time experience, OpenAI has built-in Streaming!
    - Watch your agent's thinking process unfold token by token
    - Get high level updates as it makes decisions and more...

12. Tools are how agents interact with your world. Two types
    - Hosted Tools
    - Function Tools

13. *`Handoffs`* might be the best feature! Create specialized agents and let them work together

14. *`Handoffs`* are more than just routing, you can build smaller, faster models for simple tasks and more.

15. Context management comes into two flavors:
    - Local context
    - Agent context
This seperation keeps things organized while giving agents just what they need to succeed.

16. *`Guardrails`* protect your application by validating inputs before your main agent runs

17. Models in the SDK are flexible!
    - Use any openAI model
    - Mix and match different models for different agents
    - Deploy fast models for simple tasks
    - and more...

18. The SDK is python-first
    - Use familiar Python patterns and libraries.
    - and more...

19. Read to build? The Agent SDK give you production-ready AI capabilities with minimal complexity.

20. Check out the OpenAI docs to learn more about each feature.
    [Open AI docs](https://openai.github.io/openai-agents-python/)

21. For tracing and to get openAI API, below is the link
    [Platform OpenAI](https://platform.openai.com/)