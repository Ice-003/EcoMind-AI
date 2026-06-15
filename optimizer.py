import json
import tiktoken
from groq import Groq
from settings import get_setting

# Use standard tiktoken encoding for generic token estimation
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    """Estimates the number of tokens in a text."""
    if not text:
        return 0
    return len(enc.encode(text))

def optimize_prompt(original_prompt, mode):
    """
    Calls Groq API to optimize the prompt and returns a dict with:
    - optimized_prompt
    - efficiency_score (1-100)
    - suggestions (list of strings)
    - tokens_used (completion tokens)
    """
    api_key = get_setting('groq_api_key')
    if not api_key:
        raise ValueError("Groq API key is missing. Please configure it in Settings.")
        
    client = Groq(api_key=api_key)
    
    mode_instructions = {
        "Concise": "Make the prompt as short as possible while retaining the core intent. Remove all fluff.",
        "Balanced": "Improve clarity and structure while reducing unnecessary words. Maintain a polite and professional tone.",
        "Maximum Efficiency": "Format the prompt perfectly for an LLM (e.g., using delimiters, clear structured constraints). Strip all conversational filler (e.g., 'please', 'can you')."
    }
    
    system_prompt = f"""You are an expert AI Prompt Engineer and Sustainability Consultant.
Your goal is to optimize the user's prompt to be more token-efficient while maintaining or improving its effectiveness.

Mode selected: {mode}
Instruction for mode: {mode_instructions.get(mode, mode_instructions['Balanced'])}

Output your response strictly as a JSON object with the following keys:
- "optimized_prompt": The new, highly efficient prompt.
- "efficiency_score": An integer from 1-100 indicating how much better this is than the original (100 being perfect).
- "suggestions": A list of short strings explaining what you changed and why.

Do not output any markdown formatting like ```json or anything outside the JSON object."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": original_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        usage = response.usage
        
        parsed_result = json.loads(result_content)
        
        # We need the token count of the optimized prompt. 
        # We can estimate it directly to be consistent with how we measured the original.
        optimized_prompt_text = parsed_result.get("optimized_prompt", "")
        optimized_tokens = count_tokens(optimized_prompt_text)
        
        return {
            "optimized_prompt": optimized_prompt_text,
            "efficiency_score": parsed_result.get("efficiency_score", 85),
            "suggestions": parsed_result.get("suggestions", []),
            "optimized_tokens": optimized_tokens
        }
        
    except Exception as e:
        raise Exception(f"Failed to optimize prompt: {str(e)}")
