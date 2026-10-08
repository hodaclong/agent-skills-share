# OpenAI API adapter for design tasks

Use this reference only when the design task needs an OpenAI API request. It defines the boundary between design decisions and provider configuration; it is not a place to store credentials.

## Configuration

Read configuration from the runtime environment or the user's explicitly approved temporary configuration:

```bash
OPENAI_API_KEY=<runtime secret; never commit or save>
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_IMAGE_MODEL=<model supported by the configured endpoint>
OPENAI_TEXT_MODEL=<model supported by the configured endpoint>
```

If the user later supplies a custom API link, use it only for the current approved task. Do not copy it into this file or any project artifact. If the link includes a key or token, ask the user to rotate it and provide the endpoint without the secret.

## Routing

1. Decide whether the request needs image generation, image editing, text-only design reasoning, or a local deterministic composition.
2. Load the relevant design reference from `ak-design` and collect the exact copy, brand constraints, dimensions, input-image roles, and output path.
3. Use the configured OpenAI image model only when the endpoint and model are known to support the requested operation.
4. For reference images, label each input as `reference`, `edit target`, or `supporting insert`; preserve logos and other identity-critical assets unless the user asks for a redesign.
5. Keep exact text out of the image-generation prompt when rendering accuracy is important. Generate the visual base first, then add verified copy/logo/icon overlays with a deterministic local composition step.
6. Inspect the final raster asset for text accuracy, logo integrity, contrast, dimensions, and accidental watermarks before delivery.

## Safety and privacy

- Never print, log, embed, or return `OPENAI_API_KEY` or an authorization header.
- Do not upload customer data, private brand files, credentials, or unapproved personal images to an external endpoint.
- Ask for explicit confirmation before sending a local image to a new external destination when the user has not already named that destination.
- Treat a successful HTTP response as provider delivery only; verify the downloaded image and the final workspace artifact separately.
- Do not claim that an image uses a real resort/product photo unless the source asset was actually supplied and verified.

## Generic request contract

Use the endpoint's current official contract. Do not invent provider-specific fields when the custom endpoint documentation is not available. The request context should include:

- `purpose`: design task and channel
- `size`: exact output dimensions or aspect ratio
- `prompt`: visual direction, composition, palette, and avoid list
- `input_images`: local paths and roles, if supported
- `text`: exact copy to preserve in the deterministic overlay step
- `output`: workspace destination and format

For errors, redact the response body before reporting it. Report the HTTP status, a short safe error category, and the next missing configuration; never expose provider bodies that may contain secrets or personal data.
