# generator/training.py
import json
from generator.config import SYSTEM_PROMPT
from generator.cv_builder import BASE_CV

def save_training_example(job_desc, final_text, custom_prompt):
    system_used = custom_prompt if custom_prompt else SYSTEM_PROMPT

    record = {
        "messages": [
            {"role": "system", "content": system_used},
            {
                "role": "user",
                "content": f"Job Description:\n{job_desc}\n\nBase CV:\n{BASE_CV}"
            },
            {"role": "assistant", "content": final_text}
        ]
    }

    with open("data/training_data.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


    print("💾 Saved training record to training_data.jsonl")
