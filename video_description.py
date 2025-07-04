import ollama
import textwrap

class YouTubeMetaGenerator:
    def __init__(self):
        self.system_prompt = textwrap.dedent("""
            You are an expert in generating SEO-optimized and viral-ready metadata for YouTube Shorts.

            All videos involve ranking viral clips on a specific topic (e.g., funniest dogs, best fails, etc.).

            Based on the given base title, respond **only** with:

            Title: <the improved title, max 100 characters, MUST include #shorts and keep the structure of "Ranking the...">

            Description: <a 100–200 word description with relevant keywords and hashtags>

            Tags: <a single string of comma-separated tags, total characters must not exceed 500, no bullet points, no list format>

            Your response **must be formatted exactly as shown**, with no extra commentary, no markdown, and no explanation. Only output the three fields exactly as labeled.
        """)

    def prompt_creation(self, title):
        return [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': f'Base Title: {title}'}
        ]

    def run_model(self, title, model='llama3'):
        prompt = self.prompt_creation(title)
        response = ollama.chat(model=model, messages=prompt)
        return response['message']['content']
