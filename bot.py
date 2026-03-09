import openclaw
from openclaw.vision import GeminiVision
from openclaw.core import ActionTriggers
from openclaw.handlers import ConnectivityManager


class BibiAI(openclaw.Agent):
    """
    BibiAI — AI Crypto Copilot for Binance
    Built for the Binance OpenClaw AI Contest.

    BibiAI helps users:
    - Navigate the Binance interface
    - Understand crypto concepts
    - Complete onboarding steps
    - Reduce friction during their first crypto experience
    """

    def __init__(self):

        # Load personality and rules
        super().__init__(soul_path="SOUL.md")

        # Vision reasoning engine
        self.vision_engine = GeminiVision(model="gemini-2.0-flash-exp")

        # Network resilience for unstable environments
        self.network_monitor = ConnectivityManager(mode="resilient")

    # ------------------------------------------------
    # SCREENSHOT INTERFACE GUIDANCE
    # ------------------------------------------------

    @ActionTriggers.on_image_upload
    async def analyze_interface(self, image):
        """
        Analyze screenshots of Binance interfaces
        and guide users through the next step.
        """

        print("Analyzing interface screenshot...")

        analysis = await self.vision_engine.process(
            image=image,
            task="""
            Identify important UI elements on the screen.
            Detect the next action the user should take.
            Provide clear step-by-step guidance.
            """
        )

        return {
            "action": "draw_overlay",
            "message": f"BibiAI guidance: {analysis['guidance']}",
            "confidence_score": analysis["confidence"]
        }

    # ------------------------------------------------
    # CONNECTIVITY RESILIENCE
    # ------------------------------------------------

    @ActionTriggers.on_keyword(["wifi", "internet", "slow", "network", "error"])
    async def network_support(self, user_context):
        """
        Detect network issues and provide alternative solutions.
        """

        latency = self.network_monitor.check_venue_latency()

        if latency > 1500:
            return (
                "It looks like the network connection is slow right now. "
                "Try refreshing the Binance app or switching networks if possible. "
                "If downloads are failing, I can guide you through the next steps manually."
            )

    # ------------------------------------------------
    # BEGINNER SUPPORT
    # ------------------------------------------------

    @ActionTriggers.on_keyword(["what is", "how does", "explain", "crypto"])
    async def crypto_explainer(self, user_question):
        """
        Provide beginner-friendly explanations of crypto concepts.
        """

        return (
            "I'd be happy to help explain that. "
            "Crypto can seem complicated at first, but I will break it down in simple terms."
        )

    # ------------------------------------------------
    # ONBOARDING GUIDANCE
    # ------------------------------------------------

    @ActionTriggers.on_keyword(["verify", "kyc", "deposit", "trade"])
    async def onboarding_help(self, user_context):
        """
        Guide users through Binance onboarding steps.
        """

        return (
            "Here is how you can continue:\n\n"
            "1. Open the Binance app\n"
            "2. Go to your profile section\n"
            "3. Select verification or wallet depending on your goal\n\n"
            "If you'd like, you can upload a screenshot and I will guide you visually."
        )


if __name__ == "__main__":

    # Initialize BibiAI agent
    bibi = BibiAI()

    # Run the assistant
    bibi.run(mode="production", stream=True)
