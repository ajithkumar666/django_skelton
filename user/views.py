from django.http.response import JsonResponse
from django.views import View
from rest_framework.decorators import api_view
import fire
import subprocess
import json

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
            command = [
                "torchrun",
                "--nproc_per_node", "1",
                "/home/ubuntu/llama/Llama2ChatModel/chat_completion.py",
                "--ckpt_dir","/home/ubuntu/llama/Llama2ChatModel/llama-2-7b-chat/",
                "--tokenizer_path", "/home/ubuntu/llama/Llama2ChatModel/tokenizer.model",
                "--max_seq_len", "512",
                "--max_batch_size", "8",
                "--prompt", "Newtons laws"
            ]

            # Run the command
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Print the output and error, if any
            print("Output:\n")
            #print("Error:\n", result.stderr)
            print("--------------------\n")
            res = result.stdout.strip()
            res=res.split("ImmiResult:")[1].strip()

            resd:dict={}
            resd["content"]=res

            print(resd)
            return JsonResponse(resd)