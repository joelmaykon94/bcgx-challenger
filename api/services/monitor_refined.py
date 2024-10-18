class FeedbackSystem:
    def __init__(self):
        self.feedback_data = []

    def collect_feedback(self, question, response, correctness):
        feedback = {
            "question": question,
            "response": response,
            "correctness": correctness
        }
        self.feedback_data.append(feedback)

    def analyze_feedback(self):
        correct_responses = [f for f in self.feedback_data if f['correctness']]
        incorrect_responses = [f for f in self.feedback_data if not f['correctness']]
        print(f"Total de respostas corretas: {len(correct_responses)}")
        print(f"Total de respostas incorretas: {len(incorrect_responses)}")

# Exemplo de uso do sistema de feedback
feedback_system = FeedbackSystem()
feedback_system.collect_feedback("O que é SAI?", "SAI é uma técnica...", True)
feedback_system.collect_feedback("Qual o impacto?", "O impacto é...", False)
feedback_system.analyze_feedback()
