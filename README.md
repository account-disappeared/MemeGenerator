# 😹Meme Generator
###### A side project by a bored High School Freshman🏫

---

### How to use it

1. choose whether to upload your own image or use a template(prefered)
2. If you choose to use a template, everytime you hit the "Refresh Meme Template" button, you will get a new image
3. Enter a prompt for the AI (Example: When I go back to school on Monday)
4. Choose the style of the meme caption (Witty, Sarcastic, Wholesome or Dark Humor)
5. Generate a caption and download

---

### How to run it

#### Website (no actual function)🕸️
If you go [here](https://meme-generator-1009835531129.us-central1.run.app/).
You can check out the GUI and the meme templates, you cannot generate a meme caption as the LLM is not running

#### Local Python🐍
when you have set up your LLM

Run:

`Streamlit run meme.py`

when you are in a python virtual enviroment

#### Local Docker🐋
when you have set up your LLM

Build the docker image and run from the docker engine


---

### How it works
The whole app is done using 3 main libraries:
* Streamlit for GUI
* Pillow for text overlay
* Huggingface Endpoint for LLM calls
* TinyDB for storing Meme templates

---

### Roadmap
 - [x] BETTER Prompts
 - [ ] use FastAPI to make a backend for LLM calls
 - [ ] Integrate with my [RAG chatbot](https://github.com/account-disappeared/RAG-Chatbot)
 - [ ] change UI language
 - [ ] support different language fonts
 - [ ] rewrite frontend using React
---

Changelog📃

#### 0.1 -- ***Initial Release: 2025/4/18***
- Includes all basic functions as described above
- Only supports English characters.

#### 0.2 --***Operation LLM: 2025/5/17***
- Improved existing prompts: `generate_captions_upload(prompt, style)` and ` generate_captions(prompt, style, template_url)` for better direction following and better results
