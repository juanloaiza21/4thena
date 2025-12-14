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
        Generate WhatsApp conversation messages including both client inquiries and Yuno responses.
        """
        if not self.model:
            return self._generate_fallback_whatsapp_conversation(count)

        prompt = f"""Generate a WhatsApp conversation between potential clients and Yuno (a payment integration company).
        
Generate {count} messages total. Mix of client inquiries AND Yuno responses. About 60% should be client messages, 40% should be Yuno responses.

Topics to cover:
- Payment integration for Colombia and Mexico
- Credit card processing, PSE (Colombian bank transfers)
- Risk management and fraud prevention
- API capabilities, webhooks, sandbox environment
- Pricing and implementation timelines

Return ONLY a valid JSON array with this exact format:
[
  {{"text": "message content", "is_yuno": false}},
  {{"text": "response from Yuno", "is_yuno": true}}
]

Rules:
- All messages MUST be in English
- Casual but professional WhatsApp tone
- Client messages should include their company name (use fictional names like TechFlow, PayMaster, QuickBuy, NovaPay)
- Yuno responses should be helpful and friendly
- Do NOT use placeholders like [Name] or bracketed text
- Make it feel like a real WhatsApp chat thread

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
            return messages
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._generate_fallback_whatsapp_conversation(count)

    def _generate_fallback_whatsapp_conversation(self, count: int) -> list:
        """Fallback WhatsApp conversation when Gemini is not available."""
        fallback = [
            {"text": "Hey! This is Mike from TechFlow. We need to integrate payments for our Colombia launch. Can you help?", "is_yuno": False},
            {"text": "Hi Mike! Absolutely, we'd love to help TechFlow. We have full support for Colombia including PSE and card payments. What's your timeline?", "is_yuno": True},
            {"text": "Hi there, Sarah from PayMaster here. Quick question - do you guys support fraud prevention out of the box?", "is_yuno": False},
            {"text": "Hey Sarah! Yes, our platform includes real-time fraud detection and customizable risk rules. Want me to send you the docs?", "is_yuno": True},
            {"text": "QuickBuy team here. How long does a typical integration take?", "is_yuno": False},
            {"text": "Usually 2-4 weeks depending on complexity. We give you sandbox access right away so you can start testing immediately!", "is_yuno": True},
            {"text": "NovaPay checking in. Do you have webhooks for transaction updates?", "is_yuno": False},
            {"text": "Yep! Full webhook support for all events - payments, refunds, chargebacks. Real-time notifications.", "is_yuno": True},
            {"text": "Hey, FinTech Solutions here. What about PCI compliance?", "is_yuno": False},
            {"text": "We're PCI DSS Level 1 certified. With our tokenization, you won't need to handle card data directly. Makes compliance much easier for you!", "is_yuno": True},
        ]
        return random.sample(fallback, min(count, len(fallback)))

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

    async def generate_linkedin_conversation(self, count: int = 5) -> list:
        """
        Generate LinkedIn conversation messages including both client inquiries and Yuno responses.
        """
        if not self.model:
            return self._generate_fallback_linkedin_conversation(count)

        prompt = f"""Generate a LinkedIn conversation between potential clients and Yuno (a payment integration company).
        
Generate {count} messages total. Mix of client inquiries AND Yuno responses. About 60% should be client messages, 40% should be Yuno responses.

Topics to cover:
- Payment integration for Colombia and Mexico
- Credit card processing, PSE (Colombian bank transfers)
- Risk management and fraud prevention
- API capabilities, webhooks, sandbox environment
- Pricing and implementation timelines

Return ONLY a valid JSON array with this exact format:
[
  {{"text": "message content", "is_yuno": false}},
  {{"text": "response from Yuno", "is_yuno": true}}
]

Rules:
- All messages MUST be in English
- Professional LinkedIn tone
- Client messages should include their company name (use fictional names like TechFlow, PayMaster, QuickBuy, NovaPay)
- Yuno responses should be helpful and professional
- Do NOT use placeholders like [Name] or bracketed text
- Make it feel like a real conversation thread

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
            return messages
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._generate_fallback_linkedin_conversation(count)

    def _generate_fallback_linkedin_conversation(self, count: int) -> list:
        """Fallback LinkedIn conversation when Gemini is not available."""
        fallback = [
            {"text": "Hi! I'm the CTO at TechFlow. We're exploring payment solutions for our expansion to Latin America. Does Yuno support both Colombia and Mexico?", "is_yuno": False},
            {"text": "Hello! Yes, Yuno provides comprehensive payment solutions across Latin America, including Colombia and Mexico. We support local payment methods like PSE in Colombia and OXXO in Mexico, alongside international card processing.", "is_yuno": True},
            {"text": "That's great to hear. At PayMaster, we're particularly interested in your fraud prevention capabilities. Can you tell me more?", "is_yuno": False},
            {"text": "Absolutely! Our risk management platform includes real-time fraud detection, customizable rules, and machine learning models. We can reduce chargeback rates significantly.", "is_yuno": True},
            {"text": "QuickBuy here. What's the typical integration timeline for a full implementation?", "is_yuno": False},
            {"text": "Most integrations can be completed within 2-4 weeks depending on complexity. We provide sandbox access immediately and dedicated technical support throughout.", "is_yuno": True},
            {"text": "Hi from NovaPay! Do you offer webhooks for real-time transaction notifications?", "is_yuno": False},
            {"text": "Yes! We have a robust webhook system for all transaction events. You'll receive real-time notifications for payments, refunds, and chargebacks.", "is_yuno": True},
            {"text": "I'm from FinTech Solutions. What about PCI DSS compliance? Do we need to handle card data ourselves?", "is_yuno": False},
            {"text": "We're fully PCI DSS Level 1 compliant. With our hosted checkout and tokenization services, you won't need to handle raw card data, simplifying your compliance requirements.", "is_yuno": True},
        ]
        return random.sample(fallback, min(count, len(fallback)))

gemini_service = GeminiService()
