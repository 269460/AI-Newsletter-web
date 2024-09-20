import os
from openai import AzureOpenAI

# Function to generate OpenAI completions for a given text prompt

#def generate_openai_completion(prompt):
  # message_text = [
  #   {"role": "system", "content": "This is a text to be summarized."},
  #   {"role": "user", "content": prompt}
  # ]

# Setup an AzureOpenAI client instance with specific credentials and endpoint
client = AzureOpenAI(
    azure_endpoint="https://newsletter.openai.azure.com/",
    api_key="7d06c511f9534eeda050215dd1706820",
    api_version="2024-02-15-preview"
)


def generate_summary(summary_instructions, text):
    prompt = f"{summary_instructions}\n\nText to summarize:\n{text}"
    message_text = [
        {"role": "system", "content": "You are an AI assistant tasked with summarizing technical articles."},
        {"role": "user", "content": prompt}
    ]

    # Request a completion from OpenAI's chat model
    completion = client.chat.completions.create(
        model="gpt-35-turbo",  # model = "deployment_name"
        messages=message_text,
        temperature=0.4,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Return the content of the first message in the response
    return completion.choices[0].message.content
