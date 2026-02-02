# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

> **⚠️ Important**: This project maintains strict coding standards to ensure concept consistency and system safety. Please read the following guidelines carefully before contributing.

You can contribute in many ways:

## Coding Standards

### Terminology Guidelines (MUST READ)

This project uses a formal concept dictionary (`.concept/ontology.yml`) to ensure consistency. All contributors MUST:

1. **Use Canonical Terms Only**
   - Always use canonical terms from the glossary, never synonyms
   - Example: Use `Interpreter`, not "manager", "handler", or other synonyms
   - See [GLOSSARY.md](GLOSSARY.md) for the complete list

2. **Follow Invariant Rules**
   The following hard invariants MUST NEVER be violated:

   - **INV-STATE-001**: Interpreter state transitions are monotonic (STATE_INIT → STATE_RUNNING → STATE_STOP)
   - **INV-STATE-002**: State is automatically updated by a 3-second interval timer
   - **INV-MSG-001**: Message types must be from the enumerated set only
   - **INV-MESSAGE-001**: Message history is limited to MAX_MESSAGE_LENGTH=100
   - **INV-AUTO-001**: AutoChat triggers only when in STATE_STOP
   - **INV-STREAM-001**: StreamWrapper must support both sync and async
   - **INV-SESSION-001**: Sessions must be identified by unique UUIDs
   - **INV-SESSION-002**: Session tokens must be JWT-encoded with HS256 algorithm
   - **INV-AGENT-001**: Agents must have defined roles from the enumerated set
   - **INV-MEM-001**: Conversation memory must maintain maximum 100 messages
   - **INV-CONNECTOR-001**: Connectors must implement GuiAgentInterpreterABC interface
   - **INV-CONVERTER-001**: Converters must use MappingRule for structured transformations
   - **INV-BACKEND-001**: Backend servers must be security-restricted with allowed_paths
   - **INV-BACKEND-002**: Gradio backend must use Timer component for periodic state updates

3. **Respect AUTO Decisions**
   - Some design decisions are marked as AUTO (temporary)
   - Check `.concept/ambiguities.yml` before changing related code
   - AUTO decisions expire after 20 runs and may be revisited
   - Current AUTO decisions include:
     - **Agent**: AUTO:Agent.role:classification, AUTO:Agent.type:implementation_property
     - **Message**: AUTO:Message.structure:flat, AUTO:Message.limit:100, AUTO:Message.roles:tool_function_separation
     - **State**: AUTO:State.lifecycle:monotonic, AUTO:State.transition:auto_on_input, AUTO:State.transition:forward_only
     - **AutoChat**: AUTO:AutoChat.trigger:stop_only, AUTO:AutoChat.check:before_trigger, AUTO:AutoChat.prompt:default_continue
     - **Backend**: AUTO:Backend.primary:gradio, AUTO:Backend.deployment:security, AUTO:Backend.timer:3sec_interval
     - **Memory**: AUTO:Memory.window:k10, AUTO:Memory.limit:100, AUTO:Memory.specs:provisional, AUTO:Memory.implementation:dual_provisional
     - **Session**: AUTO:Session.jwt:algorithm_hs256
     - **Connector**: AUTO:Connector.layer:domain

4. **Introduce New Terms Properly**
   - Do NOT add new terms without review
   - Submit new terms via `.concept/term_queue.yml`
   - Provide evidence and clear definitions
   - Include code references where the term is used

5. **Term Normalization Process**
   - Before contributing, check [GLOSSARY.md](GLOSSARY.md) for canonical terms
   - Use the synonym-to-canonical mapping in GLOSSARY.md
   - Example: If you're about to use "ChatSession", use "Session" instead
   - All terminology is centrally managed in `.concept/ontology.yml`
   - Questions about terms? Check `.concept/ambiguities.yml` for pending decisions

### Code Quality Standards

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Follow Python type hints conventions
- Maintain test coverage above 80%

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/nobu007/GuiAgentLoopCore/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

GuiAgentLoopCore could always use more documentation, whether as part of the
official GuiAgentLoopCore docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/nobu007/GuiAgentLoopCore/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `GuiAgentLoopCore` for local development.

1. Fork the `GuiAgentLoopCore` repo on GitHub.
2. Clone your fork locally

    ```
    $ git clone git@github.com:your_name_here/GuiAgentLoopCore.git
    ```

3. Ensure [poetry](https://python-poetry.org/docs/) is installed.
4. Install dependencies and start your virtualenv:

    ```
    $ poetry install -E test -E doc -E dev
    ```

5. Create a branch for local development:

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions, with tox:

    ```
    $ poetry run tox
    ```

7. Commit your changes and push your branch to GitHub:

    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. **Follow Terminology Guidelines**: Ensure all code and docs use canonical terms
2. **Respect Invariants**: Verify that no hard invariants are violated
3. **Include Tests**: The pull request should include tests for invariants and new features
4. **Update Documentation**: If adding functionality, update the docs. Put your new functionality into a function with a docstring, and add the feature to the list in README.md
5. **Check Python Versions**: The pull request should work for supported Python versions. Check https://github.com/nobu007/GuiAgentLoopCore/actions and make sure that the tests pass for all supported Python versions
6. **Update GLOSSARY.md**: If introducing new terms, update `.concept/term_queue.yml` for review

## Tips

```
$ poetry run pytest tests/test_gui_agent_loop_core.py
```

To run a subset of tests.


## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in CHANGELOG.md).
Then run:

```
$ poetry run bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags
```

GitHub Actions will then deploy to PyPI if tests pass.
