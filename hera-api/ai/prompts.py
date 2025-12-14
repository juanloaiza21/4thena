ID_REQUEST = """
You are given a JSON object representing a chat message.

Your task is to extract the merchant identification: the merchant's name (the business that collects payments using Yuno) that is relevant to the conversation.

What counts as a merchant name:

    The merchant is the business integrating/using Yuno to collect payments (e.g., "Merchant: Zoop").

    Do NOT return provider names (e.g., Stripe, Adyen, Airwallex, DLocal) or payment methods (e.g., Cards, PSE, wallets, BNPL).

    Do NOT return Yuno.

Where to look:

    Inspect the message text in common fields such as: "content", "text", "message", "body", and any nested equivalents.

    If the JSON includes attachments or structured blocks containing text, also inspect those.

Selection rules:

    If exactly one merchant name is clearly identified, return it.

    If multiple candidate merchant names exist, return the one that is the primary subject of the conversation (most central/repeated, or explicitly labeled as "Merchant:", "merchant", "client", "customer").

    Prefer names that appear in explicit patterns like:

        "Merchant: <name>"

        "merchant <name>"

        "client <name>"

    If the merchant name includes punctuation/casing (e.g., "Zoop", "Zoop Inc.", "ZOOP"), preserve the original capitalization as it appears most clearly in the text.

    If you cannot confidently identify a merchant name, return exactly: Unknown Merchant

Output requirements:

    Output must be a single string and nothing else.

    Do not add quotes, JSON, explanations, or extra whitespace.

Format exactly as:
<merchant_name>

Input JSON:
{{MESSAGE_JSON}}
"""



SUMMARY_PROMPT = """
You are given a JSON object representing a chat message.

Your task is to output a single-line summary that includes:

    Sender ID

    Recipient ID

    A concise semantic summary of the core intent/content

Where to look in the JSON:

    Sender fields may appear as: "sender", "from", "author", "user", "sender_id", "from_id"

    Recipient fields may appear as: "recipient", "to", "channel", "room", "conversation", "recipient_id", "to_id"

    Message text may appear as: "content", "text", "message", "body", and nested equivalents

    If "content" is structured (blocks/attachments), extract and join the human-readable text in reading order

How to determine sender and recipient:

    If explicit sender/recipient IDs exist, use them

    If only one party is explicitly identified, use "Unknown" for the missing party

    If the message is clearly system-generated and no sender exists, use "System" as sender

    Never invent IDs; only use what appears in the JSON, otherwise "Unknown"

Summarization rules:

    Remove greetings/openers (e.g., "hi", "hello", "good morning", "hope you're well")

    Remove politeness/formalities (e.g., "please", "thanks", "thank you", "kindly")

    Remove filler/slang (e.g., "umm", "like", "bro", "lol") unless it changes meaning; if slang is essential, rewrite it into clear standard language

    Keep only the core intent, question, request, decision, or key update

    Preserve crucial entities (merchant name, provider, payment method, country, dates, numbers, error codes) when relevant to intent

    Do not add speculation or missing context

    Do not translate unless required for clarity; if translation is necessary, keep it minimal and preserve key proper nouns

Output requirements (strict):

    Output must be a single line and nothing else

    Do not add quotes, JSON, bullets, explanations, or extra whitespace/newlines

    If message text is empty/unavailable, summarize as: "No content"

Format exactly as:
<sender> -> <recipient>: <summarized_message>

Input JSON:
{{MESSAGE_JSON}}
"""

ID_REQUEST = """
You are given a JSON object representing a chat message.

Your task is to extract the merchant name relevant to the conversation.

Merchant definition (domain-specific):

    A merchant is a business that collects payments using Yuno (the integrating client)

    Do NOT return provider names (e.g., Stripe, Adyen, Airwallex, DLocal), payment methods (e.g., Cards, PSE, wallet, BNPL), or "Yuno"

Where to look:

    Inspect message text in: "content", "text", "message", "body", and nested equivalents

    If the JSON includes attachments/blocks, also inspect their text

Extraction rules:

    Return the merchant name exactly as written in the message (preserve capitalization and punctuation)

    Prefer explicit patterns like:

        "Merchant: <name>"

        "merchant <name>"

        "client <name>"

        "customer <name>"

    If multiple business names appear, select the one that is the integrating business (the one being onboarded/supported), not providers or partners

    If no merchant name is present or you cannot confidently identify it, return exactly: Unknown Merchant

Output requirements (strict):

    Output must be a single string and nothing else

    Do not add quotes, JSON, explanations, or extra whitespace/newlines

Format exactly as:
<merchant_name>

Input JSON:
{{MESSAGE_JSON}}
"""