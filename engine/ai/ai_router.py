from engine.ai.openai_client import OpenAIClient
from engine.ai.gemini_client import GeminiClient
from engine.ai.groq_client import GroqClient
from engine.ai.perplexity_client import PerplexityClient
from engine.ai.huggingface_client import HuggingFaceClient

from engine.ai.ai_validator import AIValidator
from engine.ai.ai_evaluator import AIEvaluator
from engine.ai.ai_learning_bridge import AILearningBridge


class AIRouter:


    def __init__(self):

        self.openai = OpenAIClient()
        self.gemini = GeminiClient()
        self.groq = GroqClient()
        self.perplexity = PerplexityClient()
        self.huggingface = HuggingFaceClient()

        self.validator = AIValidator()
        self.evaluator = AIEvaluator()
        self.learning = AILearningBridge()


    def run(
        self,
        task: str,
        prompt: str
    ):


        # =====================================================
        # OPENAI
        # =====================================================

        if task == "analysis":

            provider = "openai"

            response = self.openai.generate(
                prompt
            )


        # =====================================================
        # GEMINI
        # =====================================================

        elif task == "knowledge":

            provider = "gemini"

            response = self.gemini.generate(
                prompt
            )


        # =====================================================
        # GROQ
        # =====================================================

        elif task == "fast":

            provider = "groq"

            response = self.groq.generate(
                prompt
            )


        # =====================================================
        # PERPLEXITY
        # =====================================================

        elif task == "verify":

            provider = "perplexity"

            response = self.perplexity.generate(
                prompt
            )


        # =====================================================
        # HUGGING FACE
        # =====================================================

        elif task == "opensource":

            provider = "huggingface"

            response = self.huggingface.generate(
                prompt
            )


        else:

            raise Exception(
                "Unknown AI task"
            )


        # =====================================================
        # VALIDATION
        # =====================================================

        validation = self.validator.validate(
            response
        )


        verification = None

        if task == "verify":

            verification = response


        # =====================================================
        # EVALUATION
        # =====================================================

        evaluation = self.evaluator.evaluate(
            task,
            provider,
            response,
            validation,
            verification
        )


        # =====================================================
        # LEARNING
        # =====================================================

        try:

            self.learning.log_ai_result(

                task=task,

                provider=provider,

                score=
                    evaluation[
                        "score"
                    ],

                validation_status=
                    evaluation[
                        "validation_status"
                    ],

                verification=
                    evaluation[
                        "verification"
                    ]

            )

        except Exception as exc:

            print(
                "AI Learning Bridge Error:",
                exc
            )


        return {

            "provider":
                provider,

            "result":
                response,

            "evaluation":
                evaluation

        }
