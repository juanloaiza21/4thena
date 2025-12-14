import google.generativeai as genai
from app.core.config import settings
import json
import random

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.model = None

    async def generate_whatsapp_messages(self, count: int = 5) -> list:
        """
        Generate random WhatsApp-style messages using Gemini.
        Simulates a Yuno customer asking about payment integration.
        """
        if not self.model:
            # Fallback messages if no API key
            return self._generate_fallback_messages(count)

        prompt = f"""Hello, please act as a client for Yuno. Your goal is to set up a payment integration for Colombia and Mexico that handles credit cards and PSE, along with risk management. Adopt the persona of a client who needs this implementation.

Generate {count} WhatsApp messages in English (professional but friendly tone) that a client would send to their Yuno account executive inquiring about the integration. All messages MUST be in English. Each message MUST include a reference to the client's company name (can be a fictional company name like "TechFlow", "PayMaster", "QuickBuy", "NovaPay", etc.). IMPORTANT: Do NOT use placeholders like "[Yuno Account Executive Name]" or any bracketed text. Just refer to "Yuno" as the company directly.

Return ONLY a valid JSON array with this exact format:
[
  {{"text": "message content here"}}
]
Card payment integration

PSE integration (Note: PSE is specific to Colombia; if the audience is international, you might use "Bank transfer integration")
- Risk and fraud management
    - "Do you have a specific SDK for React Native to handle credit card tokenization?"
    - "Does your API support recurring billing and subscription models for Visa and Mastercard?"
    - "How do you handle PCI DSS compliance? Do we need to host the payment form ourselves?"
    - "Can we implement one-click payments using saved cards with your current API?"
- Implementation timelines
    - "How does the PSE redirection flow work within your checkout process?"
    - "Do we need a separate contract with ACH Colombia, or do you act as the aggregator for PSE?"
    - "Is the notification of a successful PSE payment real-time, or is there a delay?"
    - "Can we customize the look and feel of the bank selection interface?"
- Costs and fees
    - "What are the costs associated with the integration?"
    - "Are there any hidden fees or additional charges?"
    - "Do we need to pay for the sandbox environment?"
- Technical support
    - "What is the response time for support?"
    - "Do we need to pay for the sandbox environment?"
    - "Do we need to pay for the sandbox environment?"
- Name of the company requiring the implementation
Only return the JSON array, nothing else."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean up response
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            messages = json.loads(text.strip())
            return [msg.get("text", "") for msg in messages]
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._generate_fallback_messages(count)

    def _generate_fallback_messages(self, count: int) -> list:
        """Fallback messages when Gemini is not available."""
        fallback = [
            "Hello, I am interested in integrating Yuno’s payment solutions for operations in Colombia and Mexico.",
            "What is the estimated timeline for a full PSE integration?",
            "Which card networks do you support in Mexico? Does that include Visa, Mastercard, and Amex?",
            "We also require robust risk management. Do you offer a built-in fraud prevention engine?",
            "Could you detail your transaction fees and pricing structure?",
            "Do you provide a Sandbox environment for development and testing?",
            "Is your technical support team available in Spanish?",
            "Does your platform support recurring payments and subscription billing?",
            "What compliance documentation is required to begin the onboarding process?",
            "Do you offer a RESTful API and Webhooks for real-time notifications?"
        ]
        return random.sample(fallback, min(count, len(fallback)))

gemini_service = GeminiService()
