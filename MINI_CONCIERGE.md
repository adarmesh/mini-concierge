# Mini Concierge

Evening pet project: a small clone of the MSC Concierge Cloud graph, built to learn how this repo works.
Build it in a scratch directory outside the repo, not inside it.

## Pinned versions

Match the repo, because the current web docs target newer APIs.

| Package | Version |
|---|---|
| langgraph | 0.2.76 |
| langfuse | 2.60.9 |
| langchain-core | 0.3.75 |
| langchain-openai | 0.3.32 |

Version differences to know about:

- Langfuse v3 imports the handler from `langfuse.langchain`. This repo uses v2: `langfuse.callback`.
- Newer LangGraph docs use `InMemorySaver`. This repo uses `MemorySaver`.
- Context7 library ID for matching LangGraph docs: `/langchain-ai/langgraph/0.2.74`.

## Steps

| Step | Build | Repo file to read first |
|---|---|---|
| 1 | `MultiAgentState` (TypedDict with `messages`, `entry_agent`). Entry node classifies the intent and sets `entry_agent` to `primary` or `dining`. | `backend/graph/graph.py` |
| 2 | `route_to_main_agents` conditional edge, returning `state["entry_agent"]`. Two agent nodes (`bind_tools`) share one `ToolNode` holding the union of their tools. | `backend/graph/graph_utils.py:34-42`, `backend/graph/graph.py:75-86` |
| 3 | `route_from_main_agents`: tool calls go to `tools`, which loops back to the agent. Otherwise go to an `ending_tasks` node (a stub summarizer). | `backend/graph/graph.py` |
| 4 | `MemorySaver` checkpointer. Invoke twice with the same `thread_id` and check that state persists. | `backend/graph/graph.py:37` |
| 5 | Langfuse `CallbackHandler` passed in `config={"callbacks": [...]}`. Read the trace tree. | `backend/client/clients_factory.py` |
| 6 | Load the prompt from an `.md` file with a `{chatbot_name}` placeholder. | `backend/repository/filesystem_prompts_repository.py` |
| 7 | Optional: a 5-case JSON dataset, run before and after a prompt change. | `backend/tests/conversation/docs/README.md` |

## References

- [Build a multi-source knowledge base with routing](https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base)
- [Interrupts, with a tool-node loop example](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Memory / checkpointers](https://docs.langchain.com/oss/javascript/langgraph/add-memory)
- [StateGraph reference](https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
- [Langfuse LangChain & LangGraph tracing](https://langfuse.com/integrations/frameworks/langchain)
- [Langfuse LangGraph cookbook](https://langfuse.com/guides/cookbook/integration_langgraph)
- [Langfuse Python v2 → v3 upgrade path](https://langfuse.com/docs/observability/sdk/python/upgrade-path)
