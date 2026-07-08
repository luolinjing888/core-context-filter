# Core Context Handoff Schema

Use this schema when the receiving workflow needs consistent fields.

## Markdown Fields

- `source_title`
- `source_url`
- `source_author`
- `source_date`
- `source_type`
- `receiving_agent`
- `target_task`
- `core_context`
- `execution_implications`
- `reference_map`
- `discarded_or_deferred`
- `uncertainty_follow_up`

## JSON Shape

```json
{
  "source": {
    "title": "",
    "url": "",
    "author": "",
    "date": "",
    "type": ""
  },
  "handoff": {
    "receiving_agent": "",
    "target_task": "",
    "core_context": [],
    "execution_implications": [],
    "reference_map": [
      {
        "core_point": "",
        "source_reference": "",
        "why_it_matters": ""
      }
    ],
    "discarded_or_deferred": {
      "deferred": [],
      "dropped": []
    },
    "uncertainty_follow_up": []
  }
}
```

## Quality Checklist

- Can the receiving agent execute without reading the full source?
- Are all high-impact claims traceable?
- Are source assumptions marked?
- Is irrelevant persuasion or filler removed?
- Does the packet preserve enough reference information to revisit the raw material later?
