from datetime import datetime
import os
import random
from typing import List
import openai
from openai import AsyncOpenAI
import json
import asyncio
import traceback


from app.schemas.email import (
    Email,
    EmailImportant,
    EmailSummary,
    EmailMetadata,
    Todo,
    EmailResponse,
    TodoList,
)

client = AsyncOpenAI(api_key=(os.getenv("OPENAI_API_KEY")), max_retries=3)
semaphore = asyncio.Semaphore(5)


async def send_email_metadata(emails: list[Email]):
    email_dicts = [email.model_dump() for email in emails]
    for email_dict in email_dicts:
        email_dict["created"] = email_dict["created"].isoformat()

    print(f"Length of incoming emails: {len(emails)}")

    system_prompt = """
You are an AI Assitant designed to help a user manage their email inbox. 
The user has asked you to let them know which emails may be important and which ones are spam.
The user is a business professional working in the tech field and importance is only regarding work related emails.
Only provide response for emails that are considered important or spam.
Each email should only have 1 entry in the response.
Rank each email by priority, ensuring that no two emails have the same priority rating.
Return the data as a JSON object and ensure that the response is valid JSON.
The id in the returned JSON MUST MATCH the id of the email you are referring to. This is EXTREMELY IMPORTANT.
The format of the JSON object is as follows:
{
    "emails": [
        {
            "id": "string",
            "is_important": "boolean",
            "is_spam": "boolean",
            "important_reason": "string",
            "spam_reason": "string",
            "priority_rating": "number"
        }
    ]
}
""".strip()
    try:
        response = await client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(email_dicts)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        # Assuming the content is a JSON string that represents a dictionary
        content_dict = json.loads(content)
        return [EmailImportant(**email) for email in content_dict["emails"]]

    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response.__dict__)


async def summarize_email(email: Email):
    async with semaphore:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant who assists users with their email inbox. Please summarize emails and include names of people if possible. The body of the email is in the content field.",
            },
            {
                "role": "user",
                "content": f"Summarize the following email: {email}",
            },
        ]
        response = None

        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            content = response.choices[0].message.content
            print(f"context: {content}")
            # Assuming the content is a JSON string that represents a dictionary
            print(f"response: {response}")

            if response:
                print(f"GPT Summary: {response.choices[0].message.content}")
                return EmailSummary(
                    id=email.id,
                    summary=response.choices[0].message.content,
                )
            else:
                return None
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        finally:
            # This will always be executed, even if an exception is thrown
            semaphore.release()


async def summarize_emails(emails: List[Email]):
    # Create a list of tasks for each email
    tasks = [summarize_email(email) for email in emails]

    # Run the tasks concurrently and gather the results
    email_summaries = await asyncio.gather(*tasks)

    return email_summaries


async def summarize_single_email(email: Email):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who assists users with their email inbox. Please summarize emails and include names of people if possible. The body of the email is in the content field. Please return the response in JSON format. With the summary having a 'summary' key. The summary must be a string.",
        },
        {
            "role": "user",
            "content": f"Summarize the following email: {email}",
        },
    ]
    try:
        response = await client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        content_dict = json.loads(content)
        print(f"context: {content}")
        # Assuming the content is a JSON string that represents a dictionary
        print(f"response: {response}")
        if response:
            return EmailSummary(
                id=email.id,
                summary=content_dict["summary"],
            )
        else:
            return None
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)


async def create_todo_list(emails: List[Email]):
    system_prompt = """
    You are an intelligent AI assistant designed to help users manage their priorities by creating a todo list.
    Using the emails provided, create a todo list for the user. Feel free to change the priority rating of the emails if you think it is necessary.
    Please sort the todo list by most urgent and import to least urgent and important.
    The todolist should be in the context of a business professional working in the tech field.
    Please return the todo list as a json object. Please make sure that the response is valid json.
    The format should be:
        {
            "todo": [
                {
                    "task": string,
                    "priorit": number
                }
            ]
        }
    """.strip()
    email_dicts = [email.dict() for email in emails]
    for email_dict in email_dicts:
        email_dict["created"] = (
            email_dict["created"].isoformat()
            if isinstance(email_dict["created"], datetime)
            else email_dict["created"]
        )
    print("Sending todo info to openai")
    try:
        response = await client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(email_dicts)},
            ],
            response_format={"type": "json_object"},
        )
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        # Assuming the content is a JSON string that represents a dictionary

    content = response.choices[0].message.content
    todo_list = TodoList.parse_raw(content)
    return todo_list


async def suggestResponse(email: Email):
    prompt = """
    You are an intelligent AI assistant with the ability to respond to emails. All responses should be business professional.
    You will be given an email and you must respond to it.
    The response should also be in JSON format and have a 'response' key and it must be a string.
    """.strip()
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": email.model_dump_json(exclude_unset=True),
        },
    ]
    try:
        response = await client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        content_dict = json.loads(content)
        print(f"context: {content}")
        # Assuming the content is a JSON string that represents a dictionary
        print(f"response: {response}")
        if response:
            return EmailResponse(
                id=email.id,
                response=content_dict["response"],
            )
        else:
            return None
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
