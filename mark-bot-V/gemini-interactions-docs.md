# The Interactions API

**The Interactions API is now generally available. We recommend using this API for access to all the latest features and models.**

The Interactions API is the best way to build with Gemini models and agents. As of June 2026, it is Generally Available and recommended for all new projects. While it is now considered legacy, the original generateContent API remains fully supported.

## Why use the Interactions API?

- **Universal interface for all applications**: Designed as the standard interface for every use case, including single-turn text generation, multimodal understanding, structured outputs, tool orchestration, and agentic workflows.
- **Single API for models and agents**: One unified endpoint and pattern for calling standard Gemini models as well as specialized agents directly (such as Deep Research and custom managed agents).
- **New capabilities out of the box**: Features like optional server-side conversation state using **`previous_interaction_id`**, observable execution steps for debugging and UI rendering, and background execution for long-running tasks using **`background=true`**.
- **Lower cost with higher cache hit rates**: When using multi-turn conversations, optional server-side state management enables more efficient context caching across turns, reducing token costs.
- **Where new features launch**: Going forward, all new models, multimodal capabilities, tools, and agentic features will launch on the Interactions API.

By default, the Interactions API stores requests so you can leverage the server-side state management features by using **`previous_interaction_id`**. You can opt into stateless behavior by setting **`store=false`**. See the data retention section for details.

## Get started

- **Set up your coding agent**: Connect to the Gemini Docs MCP and install the `gemini-interactions-api` skill to give your assistant direct access to the latest developer docs and best practices. For detailed steps, see the *Set up your coding agent guide*.
- **Migrate from `generateContent`**: If you have an existing integration, follow the *Migration guide* to transition to the Interactions API.
- **Get started**: Follow the steps in the *Interactions API Get started guide*.

## Feature guides

Explore the specific capabilities of the Interactions API through these guides. You can use the toggle on these pages to switch between `generateContent` and Interactions API:

- Text generation
- Image generation
- Image understanding
- Audio understanding
- Video understanding
- Document processing
- Function calling
- Structured output
- Deep Research Agent
- Flex inference
- Priority inference

## How the Interactions API works

The Interactions API centers around a core resource: the **Interaction**. An **Interaction** represents a complete turn in a conversation or task. It acts as a session record, containing the entire history of an interaction as a chronological sequence of execution steps. These steps include model thoughts, server-side or client-side tool calls and results (like **`function_call`** and **`function_result`**), and the final **`model_output`**. The stored resource (retrieved via **`interactions.get`**) also includes **`user_input`** steps for full context, though the **`interactions.create`** response only returns model-generated steps.

When you make a call to **`interactions.create`**, you are creating a new **Interaction** resource.

## Server-side state management

You can use the `id` of a completed interaction in a subsequent call using the **`previous_interaction_id`** parameter to continue the conversation. The server uses this ID to retrieve the conversation history, saving you from having to resend the entire chat history.

The **`previous_interaction_id`** parameter preserves only the conversation history (inputs and outputs). The other parameters are interaction-scoped and apply only to the specific interaction you are currently generating:

- **`tools`**
- **`system_instruction`**
- **`generation_config`** (including `thinking_level`, `temperature`, etc.)

This means you must re-specify these parameters in each new interaction if you want them to apply. This server-side state management is optional; you can also operate in stateless mode by sending the full conversation history in each request.

## Data storage and retention

By default, the API stores all **Interaction** objects (**`store=true`**) in order to simplify use of server-side state management features (with **`previous_interaction_id`**), background execution (using **`background=true`**) and observability purposes.

- **Paid tier**: The system retains interactions for 55 days.
- **Free tier**: The system retains interactions for 1 day.

If you don't want this, you can set **`store=false`** in your request. This control is separate from state management; you can opt out of storage for any interaction. However, note that **`store=false`** is incompatible with background execution and prevents using **`previous_interaction_id`** for subsequent turns.

For **Paid Tier** projects, you can configure the retention window in AI Studio to automatically mark logs for deletion from project storage after 7, 14, 28, or 55 days. A shorter retention may affect retrieval of past conversations.

You can delete stored interactions at any time using the **`delete`** method programmatically, which requires the interaction ID. You can also view and manage stored interactions logs, including deletion from project storage, in AI Studio.

After the retention period expires, your data will be deleted automatically.

Interactions objects are processed according to the terms.

## View interactions in AI Studio

The API stores Interactions API requests executed with **`store=true`** for projects on the Paid Tier. You can view them directly from the **Logs** page in Google AI Studio. See the *Logs guide* for more.

## Best practices

- **Cache hit rate**: Implicit caching is supported in both stateful and stateless modes (see Quickstart). Using **`previous_interaction_id`** (stateful) to continue conversations allows the system to more easily utilize implicit caching for the conversation history, which improves performance and reduces costs.
- **Mixing interactions**: You have the flexibility to mix and match Agent and Model interactions within a conversation. For example, you can use a specialized agent, like the Deep Research agent, for initial data collection, and then use a standard Gemini model for follow-up tasks such as summarizing or reformatting, linking these steps with the **`previous_interaction_id`**.

## Supported models & agents

| Model Name | Type | Model ID |
|---|---|---|
| Gemini 3.5 Flash | Model | `gemini-3.5-flash` |
| Gemini 3.1 Pro Preview | Model | `gemini-3.1-pro-preview` |
| Gemini 3.1 Flash-Lite | Model | `gemini-3.1-flash-lite` |
| Gemini 3 Flash Preview | Model | `gemini-3-flash-preview` |
| Gemini 2.5 Pro | Model | `gemini-2.5-pro` |
| Gemini 2.5 Flash | Model | `gemini-2.5-flash` |
| Gemini 2.5 Flash-lite | Model | `gemini-2.5-flash-lite` |
| Gemini 3 Pro Image | Model | `gemini-3-pro-image` |
| Gemini 3.1 Flash Image | Model | `gemini-3.1-flash-image` |
| Gemini 3.1 Flash TTS Preview | Model | `gemini-3.1-flash-tts-preview` |
| Gemma 4 31B IT | Model | `gemma-4-31b-it` |
| Gemma 4 26B MoE IT | Model | `gemma-4-26b-a4b-it` |
| Lyria 3 Clip Preview | Model | `lyria-3-clip-preview` |
| Lyria 3 Pro Preview | Model | `lyria-3-pro-preview` |
| Deep Research Preview | Agent | `deep-research-preview-04-2026` |
| Deep Research Preview | Agent | `deep-research-max-preview-04-2026` |
| Antigravity Preview | Agent | `antigravity-preview-05-2026` |

### SDKs

You can use latest version of the Google GenAI SDKs in order to access Interactions API.

On Python, this is **`google-genai`** package from **2.3.0** version onwards.

## Limitations

- **Remote MCP**: Gemini 3 does not support remote MCP, this is coming soon.
- **Multi-turn model compatibility**: When mixing different models in a conversation (either stateful or stateless), subsequent models must support the output modalities of the previous models as input. For example, if you generate an image using `gemini-3.1-flash-image`, you cannot continue that conversation with a model that doesn't accept image inputs (such as a text-only model or a music-generation model like Lyria).

The following features are supported by the `generateContent` API but are not yet available in the Interactions API:

- **Video metadata**: The `video_metadata` field, used to set clipping intervals and custom frame rates for video understanding.
- **Batch API**
- **Automatic function calling (Python)**
- **Explicit caching**: Note that server-side implicit caching is available in the Interactions API via **`previous_interaction_id`**.
- **Safety settings**: Custom safety settings are not supported in the Interactions API.

---

## Getting started

> **Note**: This version of the page covers the Interactions API.

This guide gets you started with the Gemini API using the Interactions API. You'll make your first API call in under a minute and explore text generation, multimodal understanding, image generation, structured output, tools, function calling, agents, and background execution.

Using a coding agent? Install the skill so your agent stays current with Interactions API patterns:

```bash
npx skills add google-gemini/gemini-skills --skill gemini-interactions-api
```

The Interactions API is available through the Python and JavaScript SDKs, as well as through REST.

### 1. Get an API key

To use the Gemini API, you need to have an **API key** to authenticate your requests, enforce security limits, and track usage to your account.

- Google AI Studio automatically creates a project and API key for new users. You can copy it from the API keys page.
- If you need a new key, click **Create API key** in AI Studio and follow the dialog to add a new key-project pair.

**Create a Gemini API Key**

Set your key as an environment variable:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

#### Upgrade to the paid tier

Upgrading to the paid tier increases your rate limits and requires setting up Cloud Billing.

- Click **Set up billing** on the AI Studio API keys or Projects pages.
- Follow the Cloud Billing dialog to create or link a billing account, add a payment method, and prepay a minimum of $10 (or currency equivalent) in paid credits.
- View your API usage in Google AI Studio under **Dashboard > Usage**.
- See the Billing page for more information.

### 2. Install the SDK and make your first call

Install the SDK and generate text with a single API call.

**Python**

Install the SDK:
```bash
pip install -U google-genai
```

Initialize the client and make a request:
```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain how AI works in a few words"
)
print(interaction.output_text)
```

Response:
```json
{
  "id": "v1_ChdpQUFvYXI...",
  "status": "completed",
  "usage": {
    "total_tokens": 197,
    "total_input_tokens": 8,
    "total_output_tokens": 12
  },
  "created": "2026-06-09T12:01:25Z",
  "steps": [
    {
      "type": "thought",
      "signature": "EvEFCu4FAQw..."
    },
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "AI learns patterns from data, then uses those patterns to make predictions or decisions on new data."
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```

When using REST, the API returns the full Interaction resource containing metadata, usage statistics, and the step-by-step history of the turn.

While the SDKs expose the full response, they also provide convenience properties like **`interaction.output_text`** and **`interaction.output_image`** to access final outputs directly. Learn more about the response structure in the Interactions overview or read the text generation guide for details on system instructions and generation config.

### 3. Stream the response

For more fluid interactions, stream the response as it's generated. Each **`step.delta`** event delivers a chunk of text you can display immediately.

**Python**

```python
from google import genai

client = genai.Client()

stream = client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain how AI works",
    stream=True
)
for event in stream:
    print(event)
```

When streaming, the server responds with a stream of server-sent events (SSE). Each event includes a type and JSON data.

Response:
```
event: interaction.created
data: {"interaction":{"id":"v1_Chd...","status":"in_progress","model":"gemini-3.5-flash"},"event_type":"interaction.created"}

event: step.start
data: {"index":0,"step":{"type":"thought"},"event_type":"step.start"}

event: step.delta
data: {"index":0,"delta":{"signature":"EvEFCu4F...","type":"thought_signature"},"event_type":"step.delta"}

event: step.stop
data: {"index":0,"event_type":"step.stop"}

event: step.start
data: {"index":1,"step":{"type":"model_output"},"event_type":"step.start"}

event: step.delta
data: {"index":1,"delta":{"text":"AI ","type":"text"},"event_type":"step.delta"}

event: step.delta
data: {"index":1,"delta":{"text":"works ","type":"text"},"event_type":"step.delta"}

event: step.stop
data: {"index":1,"event_type":"step.stop"}

event: interaction.completed
data: {"interaction":{"id":"v1_Chd...","status":"completed","usage":{"total_tokens":197}},"event_type":"interaction.completed"}
```
For a detailed look at handling streaming events and delta types, see the *streaming interactions guide*.

### 4. Multi-turn conversations

The Interactions API supports multi-turn conversations with two approaches:

- **Stateful (recommended)**: Continue a conversation on the server using **`previous_interaction_id`**. Ideal for most chat and agentic workflows where you want the server to manage history and optimize caching.
- **Stateless**: Manage the conversation history on the client by passing all previous turns (including intermediate model thought and tool steps) in each request.

#### Stateful (recommended)

Chain interactions by passing **`previous_interaction_id`**. The server manages the full conversation history for you.

**Python**

```python
from google import genai

client = genai.Client()

# Server-side state (recommended)
interaction1 = client.interactions.create(
    model="gemini-3.5-flash",
    input="I have 2 dogs in my house.",
)
print("Response 1:", interaction1.output_text)

interaction2 = client.interactions.create(
    model="gemini-3.5-flash",
    input="How many paws are in my house?",
    previous_interaction_id=interaction1.id,
)
print("Response 2:", interaction2.output_text)
```

Response:
```json
{
  "id": "v2_Chd...",
  "status": "completed",
  "usage": {
    "total_tokens": 240,
    "total_input_tokens": 60,
    "total_output_tokens": 20
  },
  "steps": [
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "There are 8 paws in your house. 2 dogs \u00d7 4 paws = 8 paws."
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash"
}
```
The second interaction returns a complete response object that includes only the new steps, but is grounded in the previous turn's context. Learn more about maintaining state in the *multi-turn conversations guide*, or explore stateless mode for client-side history management.

### 5. Multimodal understanding

Gemini models understand images, audio, video, and documents natively. Pass media alongside text in a single request.

**Python**

```python
import base64
from google import genai

client = genai.Client()

# Load a local image
with open("sample.jpg", "rb") as f:
    image_bytes = f.read()
image_b64 = base64.b64encode(image_bytes).decode("utf-8")

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "Compare this local image and this remote audio file."},
        {
            "type": "image",
            "data": image_b64,
            "mime_type": "image/jpeg"
        },
        {
            "type": "audio",
            "uri": "https://storage.googleapis.com/generativeai-downloads/data/sample.mp3",
            "mime_type": "audio/mp3"
        }
    ]
)
print(interaction.output_text)
```

Response:
```json
{
  "id": "v1_Chd...",
  "status": "completed",
  "usage": {
    "total_tokens": 300
  },
  "steps": [
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "The local image displays a pipe organ while the remote audio file is a sample MP3 clip..."
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```
Explore how to pass images, video, and audio files in the *image understanding guide*.

**hearing** - Audio understanding

Transcribe, summarize, or answer questions about audio files.

**videocam** - Video understanding

Analyze video content, locate events, and describe actions.

**description** - Document processing

Extract information from PDFs and other document formats.

### 6. Multimodal generation

Gemini can generate images natively using the Nano Banana image models.

**Python**

```python
import base64
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="Generate an image of a futuristic city skyline at sunset",
)

with open("generated_image.png", "wb") as f:
    f.write(base64.b64decode(interaction.output_image.data))
```

Response:
```json
{
  "id": "v1_Chd...",
  "status": "completed",
  "steps": [
    {
      "type": "model_output",
      "content": [
        {
          "type": "image",
          "data": "BASE64_ENCODED_IMAGE",
          "mime_type": "image/png"
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.1-flash-image",
}
```
When the model generates an image, it returns the base64-encoded image data in a step within the `steps` array, as well as via the **`output_image`** convenience property. Check out the *image generation guide* to learn about aspect ratios, image editing, and references.

**record_voice_over** - Speech generation

Generate expressive, multi-speaker speech with Gemini 3.1 Flash TTS.

**music_note** - Music generation

Create clips and full-length songs with Lyria 3.

### 7. Use structured output

Configure the model to return JSON that matches a schema you define. Structured output works with **Pydantic** (Python) and **Zod** (JavaScript).

**Python**

```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Recipe(BaseModel):
    recipe_name: str = Field(description="Name of the recipe.")
    ingredients: List[str] = Field(description="List of ingredients.")
    prep_time_minutes: Optional[int] = Field(description="Prep time in minutes.")

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Give me a recipe for banana bread",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Recipe.model_json_schema()
    },
)

recipe = Recipe.model_validate_json(interaction.output_text)
print(recipe)
```

Response:
```json
{
  "id": "v1_Chd...",
  "status": "completed",
  "steps": [
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "{\n  \"recipe_name\": \"Classic Banana Bread\",\n  \"ingredients\": [\n    \"3 ripe bananas, mashed\",\n    \"1/3 cup melted butter\",\n    \"3/4 cup sugar\",\n    \"1 egg, beaten\",\n    \"1 teaspoon vanilla extract\",\n    \"1 teaspoon baking soda\",\n    \"Pinch of salt\",\n    \"1.5 cups all-purpose flour\"\n  ],\n  \"prep_time_minutes\": 15\n}"
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```
The output text block contains a valid JSON string conforming exactly to the requested schema. To learn how to define more complex structures and recursive schemas, see the *structured output guide*.

### 8. Use tools

Ground the model's response in real-time information with Google Search. The API automatically searches, processes results, and returns citations.

**Python**

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Who won the euro 2024?",
    tools=[{"type": "google_search"}]
)

print(interaction.output_text)

# Print citations
for step in interaction.steps:
    if step.type == "model_output":
        for content_block in step.content:
            if content_block.type == "text" and content_block.annotations:
                print("\nCitations:")
                for annotation in content_block.annotations:
                    if annotation.type == "url_citation":
                        print(f"  [{annotation.title}]({annotation.url})")
```

Response:
```json
{
  "id": "v1_Chd...",
  "status": "completed",
  "steps": [
    {
      "type": "thought",
      "signature": "EvEFCu4F..."
    },
    {
      "type": "google_search_call",
      "arguments": {
        "queries": ["UEFA Euro 2024 winner"]
      }
    },
    {
      "type": "google_search_result",
      "call_id": "search_001",
      "result": [
        {
          "search_suggestions": "<!-- HTML and CSS search widget -->"
        }
      ]
    },
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "Spain won Euro 2024, defeating England 2-1 in the final.",
          "annotations": [
            {
              "type": "url_citation",
              "url": "https://www.uefa.com/euro2024",
              "title": "uefa.com",
              "start_index": 0,
              "end_index": 56
            }
          ]
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```
The search steps are detailed within the interaction history, and the final output includes inline citations pointing to web sources.

You can learn how to extract search citations in the *Google Search grounding guide*, or see how to combine multiple tools in the *tool combination guide*.

**code** - Code execution

Run Python code in a secure sandboxed Borg environment.

**link** - URL context

Pass public web URLs directly to ground responses in webpage content.

**search** - File search

Index and search across uploaded documents and media files.

**map** - Google Maps

Ground responses in real-world geospatial and location data.

**computer** - Computer use

Browser automation and screen interaction.

### 9. Call your own functions

Function calling lets you connect the model to your code. You declare a function's name and parameters, the model decides when to call it and returns structured arguments, and you execute it locally and send the result back.

#### Stateful (recommended)

**Python**

```python
import json
from google import genai

client = genai.Client()

weather_tool = {
    "type": "function",
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

available_functions = {
    "get_current_temperature": lambda location: {
        "location": location, "temperature": "22", "unit": "celsius"
    },
}

user_input = "What is the temperature in London?"
previous_id = None

while True:
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=user_input,
        tools=[weather_tool],
        previous_interaction_id=previous_id,
    )

    function_results = []
    for step in interaction.steps:
        if step.type == "function_call":
            result = available_functions[step.name](**step.arguments)
            print(f"Called {step.name}({step.arguments}) → {result}")
            function_results.append({
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            })

    if not function_results:
        break

    user_input = function_results
    previous_id = interaction.id

print(interaction.output_text)
```

Response:

During **Turn 1**, the model returns a response with status `requires_action` and the `function_call` step:

```json
{
  "id": "v1_Chd...",
  "status": "requires_action",
  "steps": [
    {
      "type": "function_call",
      "id": "call_abc123",
      "name": "get_current_temperature",
      "arguments": {
        "location": "London"
      }
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash"
}
```

After you run the function locally and submit the result (**Turn 2**), the final completed interaction returns:

```json
{
  "id": "v1_Chd...",
  "status": "completed",
  "steps": [
    {
      "type": "function_call",
      "id": "call_abc123",
      "name": "get_current_temperature",
      "arguments": {
        "location": "London"
      }
    },
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "The temperature in London is currently 22°C."
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```
For advanced features like parallel function calling or function choice modes, see the *function calling guide*.

### 10. Run a managed agent

Managed agents run in a remote sandbox with access to tools like code execution and file management. Pass an agent instead of a model and set `environment="remote"`.

**Python**

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Write a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt. Then read the file and print its contents.",
    environment="remote",
)
print(f"Environment: {interaction.environment_id}")
print(interaction.output_text)
```

You can also define and save custom agents with your own instructions, skills, and data sources.

**rocket_launch** - Quickstart

Make your first agent call, stream responses, and build a custom agent.

**smart_toy** - Antigravity Agent

Capabilities, tools, multimodal input, and pricing for the default agent.

**experiment** - Agents in AI Studio

Visual playground for prototyping agents without writing code.

### 11. Run tasks in the background

Set **`background=True`** to run long tasks asynchronously. Poll for results with **`interactions.get()`**. For more details, see the *Background execution guide*.

**Python**

```python
import time
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Write a detailed analysis of the impact of artificial intelligence on modern healthcare.",
    background=True,
)
print(f"Started background task: {interaction.id}")
print(f"Status: {interaction.status}")

# Poll for completion
while True:
    result = client.interactions.get(interaction.id)
    print(f"Status: {result.status}")
    if result.status == "completed":
        print(f"\nResult:\n{result.output_text}")
        break
    elif result.status == "failed":
        print(f"Failed: {result.error}")
        break
    time.sleep(5)
```

Response:

The initial response returns immediately with status `in_progress`:

```json
{
  "id": "v1_abc123",
  "status": "in_progress",
  "object": "interaction",
  "model": "gemini-3.5-flash"
}
```

Once the background task is fully executed, checking the interaction state returns:

```json
{
  "id": "v1_abc123",
  "status": "completed",
  "steps": [
    {
      "type": "model_output",
      "content": [
        {
          "type": "text",
          "text": "Artificial intelligence has transformed modern healthcare in several..."
        }
      ]
    }
  ],
  "object": "interaction",
  "model": "gemini-3.5-flash",
}
```
Read about running models and agents asynchronously in the *background execution guide*.

---

# Image understanding

Gemini models are built to be multimodal from the ground up, unlocking a wide range of image processing and computer vision tasks including but not limited to image captioning, classification, and visual question answering without having to train specialized ML models.

In addition to their general multimodal capabilities, Gemini models offer enhanced accuracy for specific use cases like object detection and segmentation, through additional training.

### Passing images to Gemini

You can provide images as input to Gemini using several methods:

- **Passing image using URL**: Ideal for publicly accessible images.
- **Passing inline image data**: For base64-encoded image data.
- **Uploading images using the File API**: Recommended for larger files or for reusing images across multiple requests.

### Passing image using URL

You can upload an image using the Files API and pass it in the request.

```python
from google import genai

client = genai.Client()

uploaded_file = client.files.upload(file="path/to/organ.jpg")

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "Caption this image."},
        {
            "type": "image",
            "uri": uploaded_file.uri,
            "mime_type": uploaded_file.mime_type
        }
    ]
)
print(interaction.output_text)
```

### Passing inline image data

You can provide image data as base64-encoded strings.

```python
import base64
from google import genai

with open('path/to/small-sample.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "Caption this image."},
        {
            "type": "image",
            "data": base64.b64encode(image_bytes).decode('utf-8'),
            "mime_type": "image/jpeg"
        }
    ]
)
print(interaction.output_text)
```
> **Note**: Inline image data limits your total request size (text prompts, system instructions, and inline bytes) to 20MB. For larger requests, upload image files using the File API.

### Uploading images using the File API

For large files or to be able to use the same image file repeatedly, use the Files API. See the Files API guide.

```python
from google import genai

client = genai.Client()

my_file = client.files.upload(file="path/to/sample.jpg")

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "Caption this image."},
        {
            "type": "image",
            "uri": my_file.uri,
            "mime_type": my_file.mime_type
        }
    ]
)
print(interaction.output_text)
```

### Prompting with multiple images

You can provide multiple images in a single prompt by including multiple image objects in the `input` array.

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "What is different between these two images?"},
        {
            "type": "image",
            "uri": "https://example.com/image1.jpg",
            "mime_type": "image/jpeg"
        },
        {
            "type": "image",
            "uri": "https://example.com/image2.jpg",
            "mime_type": "image/jpeg"
        }
    ]
)
print(interaction.output_text)
```