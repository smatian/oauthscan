

from openai import OpenAI
import os



def detectBadStuff(image_url):
    client = OpenAI(api_key=os.environ['openaikey'])

    response = client.chat.completions.create(
        #temperature = 0.99,
        #frequency_penalty = 0.73,
        #presence_penalty = 0.91,
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": os.environ['openaiprompt']},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300
    )

    # Analyze the response to determine if it contains "yes"
    print(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == "__main__":
    test = detectBadStuff("https://www.shutterstock.com/shutterstock/videos/1093313969/thumb/10.jpg?ip=x480")
    print(test)


