import os
import wget

import requests
import subprocess
import re
import sys

from tqdm import tqdm

model_links = []
model_number = ""


if len(sys.argv) < 2:
    base_links = ["tokyotech-llm/Swallow-7b-instruct-hf"] #, "tokyotech-llm/Swallow-13b-instruct-hf", "tokyotech-llm/Swallow-70b-instruct-hf"]
else:
    base_links = sys.argv[1:]


for base_link in base_links:

    print (base_link)

    base_url = f"https://huggingface.co/{base_link}"
    tree_url = base_url + "/tree/main"

    result = subprocess.run(["curl", "-s", tree_url], capture_output=True, text=True)
    html_data = result.stdout

    # model-00001-of-00003.safetensors <- model info name contains total safetensors
    pattern = r'model-00001-of-\d+\.safetensors'
    model_files = re.findall(pattern, html_data)

    # get the first entry and extract the total safetensors.
    model_total = model_files[0].split("-")[3].split('.')[0]

    # get the motel name from the link eg "https://huggingface.co/tokyotech-llm/Swallow-7b-instruct-hf"
    # -> Swallow-7b-instruct-hf
    model_name = base_link.split("/")[1]

    print ("#" * 25 + model_name + "#" * 25)

    dir = f"models/{model_name}/"

    if not os.path.exists(dir):
        os.makedirs(dir)

    #print (f"Number of models detected as: {model_total[-2:]}")

    # get the last two digits from our total, this is to ensure
    # that we get both single digit (01->09) and double digit (10+) values correctly
    print ("Discovering model files...")
    for i in range(1,int(model_total[-2:])):

        if i < 10:
            model_number = f"0{i}"
        else:
            model_number = i

        # make sure the link is valid before we add it to our list of download targets
        url = f"{base_url}/resolve/main/model-000{model_number}-of-{model_total}.safetensors?download=true"

        response = requests.head(url)

        if response.status_code == 200 or response.status_code == 302:
            model_links.append(f"{base_url}/resolve/main/model-000{model_number}-of-{model_total}.safetensors?download=true")
        else:
            #print ("End of available model links.")
            break
    
    print (f"{len(model_files)} models discovered.")
    # general static important files
    files_to_download = [
        f"{base_url}/resolve/main/config.json?download=true",
        f"{base_url}/resolve/main/generation_config.json?download=true",
        f"{base_url}/resolve/main/model.safetensors.index.json?download=true",
        f"{base_url}/resolve/main/requirements.txt?download=true",
        f"{base_url}/resolve/main/special_tokens_map.json?download=true",
        f"{base_url}/resolve/main/tokenizer.model?download=true",
        f"{base_url}/resolve/main/tokenizer_config.json?download=true",
    ]

    # add our model.safetensor files to the list of download targets
    for file in model_links:
        files_to_download.append(file)

    # download each target, using the url to extract the file name.
    for url in tqdm(files_to_download, desc="Downloading model files"):
       
       filename = os.path.basename(url).split("?")[0]
       full_path = os.path.join(dir, filename)
       
       if not os.path.exists(full_path):
            print (f"Downloading: \n{url}")
            wget.download(url, full_path)
       else:
           print (f"File {full_path} already exists.")
