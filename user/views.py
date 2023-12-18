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
            res: dict = {}
            raw_data: dict = dict(request.data)
            print(raw_data)
            prompt:str = raw_data['prompt']
            if len(prompt) == 0:
                print("Please enter your prompt")
                res["message"]="Please enter your prompt"
                res["status"]=False
                return JsonResponse(res)
            command = [
                "torchrun",
                "--nproc_per_node", "1",
                "/home/ubuntu/llama/Llama2ChatModel/chat_completion.py",
                "--ckpt_dir","/home/ubuntu/llama/Llama2ChatModel/llama-2-7b-chat/",
                "--tokenizer_path", "/home/ubuntu/llama/Llama2ChatModel/tokenizer.model",
                "--max_seq_len", "512",
                "--max_batch_size", "8",
                "--prompt", prompt
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
            resd["status"]=True

            print(resd)
            return JsonResponse(resd)

    @api_view(["POST"])
    def mistrial(request):
        if request.method == "POST":
            res: dict = {}
            raw_data: dict = dict(request.data)
            print(raw_data)
            prompt:str = raw_data['prompt']
            if len(prompt) == 0:
                print("Please enter your prompt")
                res["message"]="Please enter your prompt"
                res["status"]=False
                return JsonResponse(res)
            from transformers import AutoModelForCausalLM, AutoTokenizer
            device = "cpu" # the device to load the model onto
            model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
            tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

            messages = [
            {"role": "user", "content": str(prompt)}
            ]

            encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

            model_inputs = encodeds.to(device)
            model.to(device)

            generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
            decoded = tokenizer.batch_decode(generated_ids)
            result = "ImmiResult:"+decoded[0].strip()
            result=result.split("ImmiResult:")[1].strip()
            resd:dict={}
            resd["content"]=result
            resd["status"]=True
            return JsonResponse(resd)
