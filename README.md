# hugging_face_downloader

### Work In Progress

I don't expect anyone to use this, but if it's helpful or it sucks, let me know :)

The models downloaded this way can be converted with Llama.cpp for easy use with LangChain and other local llm solutions.

## Summary
A tool used to download LLama models from Hugging Face for local use.

## Usage

Download the hf_downloader script and put it anywhere that works for you.

Run the script and specify the name of the model you want to download:

```python
  python ./hf_downloader.py tokyotech-llm/Swallow-7b-hf
```

You can specify multiple models at once if you want to download multple models

```python
  python ./hf_downloader.py tokyotech-llm/Swallow-7b-hf tokyotech-llm/Swallow-70b-hf 
```

Currently if you specify no model, the tokyotech-llm/Swallow-7b-hf will be downloaded so be careful!

You can also edit the script list that contains the models to add multiple if you don't want to c&p a bunch into the command line - pick your poison.

## Ouput Location

Files will all be output to ```scriptDIR/models/modelName``` eg:

```/Users/username/Documents/projects/models/Swallow-7b-hf```

