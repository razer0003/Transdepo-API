# Multi-Agent AI Prototype

## Overview

A modular system for processing human requests through multi-step AI agents:

1. **Feeder**: Converts human language to a structured prompt.
2. **Interpreter**: Converts to compact Gibbertext and selects the right department.
3. **Departments**: Specialized AIs process requests based on department.

## How it Works

- Send a POST to `/process` with `{ "request": "Book me a flight from NYC to LA on July 10th." }`
- Returns the Gibbertext, department, and the response.

## Setup

1. `pip install -r requirements.txt`
2. Add `.env` file with your `OPENAI_API_KEY`.
3. Run: `uvicorn main:app --reload`

## Example

Request:
```json
{ "request": "Tell me a joke." }
```

Response:
```json
{
  "gibbertext": "act:joke;obj:random",
  "department": "joke",
  "result": "Why did the chicken cross the road? ..."
}
```