# Prompt — Request Workbench Capture Back History

Use this prompt when re-entering a Workbench and asking chat to summarize what has already been captured.

## Prompt

I am re-entering an active Workbench.

Before summarizing current state, Capture Back history, or next steps, first ask me to upload the latest file matching:

```text
outputs/history/repo_history_for_llm_*.md
```

If I have not generated it yet, tell me to run:

```bash
make pack
```

Then ask me to upload the newest history file from:

```text
outputs/history/
```

Use the uploaded history file as the source of truth.

Do not rely on conversation memory if the uploaded repo history says otherwise.

After I upload the history file, summarize:

- recent Capture Back history;
- cards added or changed;
- Capture Back manifests;
- LI rules added or changed;
- docs added or changed;
- prompts added or changed;
- notes and lessons captured;
- generated assets captured;
- current open decisions or risks;
- what this Workbench now knows;
- what should govern the next step.

If the uploaded history appears stale or incomplete, say so and ask for a newer `repo_history_for_llm_*.md` or the latest repo pack.

## Short version

Ask for the latest:

```text
outputs/history/repo_history_for_llm_*.md
```

Use it as source of truth. Summarize Workbench Capture Back history and current state from that file.
