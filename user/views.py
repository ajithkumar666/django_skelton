from typing import Optional
from django.http.response import JsonResponse
from django.views import View
from rest_framework.decorators import api_view
import os
from llama import Llama
import fire


# Create your views here.
class UserView(View):
    
    @api_view(["POST"])
    def test(request):
        if request.method == "POST":
            res: dict = {}
            res["message"] = "This is a test API"
            res["status"] = True
            return JsonResponse(res)

    @api_view(["POST"])
    def llama(request):
        if request.method == "POST":
            raw_data: dict = dict(request.data)
            print(raw_data)
            res: dict = {}
            res["content"] = fire.Fire(Llama22().main)
            res["status"] = True
            print(res)
            return JsonResponse(res)

class Llama22():
    def main(
        ckpt_dir: str = "/home/ubuntu/llama/Llama2ChatModel/llama-2-7b-chat/",
        tokenizer_path: str = "/home/ubuntu/llama/Llama2ChatModel/tokenizer.model",
        temperature: float = 0.6,
        top_p: float = 0.9,
        max_seq_len: int = 512,
        max_batch_size: int = 8,
        max_gen_len: Optional[int] = None,
        prompt: str = "Newtons laws",
    ):
        generator = Llama.build(
            ckpt_dir=ckpt_dir,
            tokenizer_path=tokenizer_path,
            max_seq_len=max_seq_len,
            max_batch_size=max_batch_size,
        )
        res: dict = {}

        if len(prompt) == 0:
            res["message"] = "Prompt is empty"
            res["status"] = False
            return res
        else:
            # print("Prompt is : ",prompt)
            pass

        dialogs = [
            [{"role": "user", "content": prompt}],
        ]
        results = generator.chat_completion(
            dialogs,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )

        for dialog, result in zip(dialogs, results):
            res["content"] = result["generation"]["content"]
            res["status"] = True
        return res