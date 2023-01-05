import tkinter as tk
import openai,urllib
import os
import requests
from PIL import Image, ImageTk
import time
timestr = time.strftime("%Y%m%d-%H")

# Create a list to store the previous prompts and responses
history = []
global i, window
i=0 # stores response number
def generate_response():
    global i, window
    # Get the model, API key, and prompt
    model = model_var.get()
    api_key = api_key_entry.get()
    prompt = prompt_entry.get()
    max_token = token_entry.get()

    # Set the API key
    openai.api_key = api_key

    # Generate a response
    # Generate a response
    if model == "image-alpha-001":
        # Generate an image
        response = openai.Image.create(
            model=model,
            prompt=prompt,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        page = requests.get(image_url)
        print(image_url)
        f_ext = os.path.splitext(image_url)[-1]
        f_name = f'img{i}.png'.format(f_ext)
        with open(timestr+f'img{i}.png', 'wb') as f:
            f.write(page.content)

        # Open the image and convert it to a PhotoImage object
        image_path = timestr+f'img{i}.png'

        r = tk.Toplevel(window)
        r.title("Generated image is saved")

        canvas = tk.Canvas(r, width=1024, height=1024)
        canvas.pack()

        my_image = tk.PhotoImage(file=image_path)
        canvas.create_image(0, 0, image=my_image, anchor=tk.NW)
        response_window.mainloop()
        # Run the window loopv
    else:
        completions = openai.Completion.create(engine=model, prompt=prompt, max_tokens=int(max_token), n=1,stop=None,temperature=0.5)
        message = completions.choices[0].text

        # Store the prompt and response in the history
        history.append((prompt, message))
        i=i+1
        # Create a new window to display the response
        response_window = tk.Tk()
        response_window.title(f"Response{i}")
        response_window.geometry("1000x500")

        # Create a frame to hold the prompt and response
        response_frame = tk.Frame(response_window)
        response_frame.pack()

        # Create a label to display the prompt
        prompt_label = tk.Label(response_frame, text='Given prompt: '+prompt+'\n Response:\n', font='Helvetica 18 bold',wraplength=400)
        prompt_label.pack(side="top")

        # Create a label to display the response
        response_label = tk.Text(response_frame)
        response_label.insert('1.0',message)
        response_label.pack(side="top")

        # Run the window loop
        response_window.mainloop()


# Create the window
window = tk.Tk()
window.title("OpenAI GUI")
window.geometry("700x350")
# Create a frame for the model selection
model_frame = tk.Frame(window)
model_frame.pack()

# Create a label for the model selection
model_label = tk.Label(model_frame, text="Select the model:", font='Helvetica 20')
model_label.pack(side="left")

# Create a variable to store the selected model
model_var = tk.StringVar(value="text-davinci-002")
models = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
    "code-davinci-002",
    "code-cushman-001",
    "image-alpha-001",
]
# Create a dropdown menu for the model selection
model_menu = tk.OptionMenu(model_frame, model_var,*models)
model_menu.pack(side="left")

# Model explanations



models_explanation = ""
j=0
for model in models:
    name, *rest, version = model.rsplit("-")
    if name == "text":
        models_explanation += f"{models[j]} - Text generation model, {rest[0]} version {version}\n"
    elif name == "code":
        models_explanation += f"{models[j]} - Code generation model, {rest[0]} version {version}\n"
    elif name == "image":
        models_explanation += f"{models[j]} - Image generation model, {rest[0]} version {version}\n"
    else:
        models_explanation += f"{models[j]} - Model with name **{name}**, {rest[0]} version {version}\n"
    j=j+1






# Create a frame for the API key entry
api_key_frame = tk.Frame(window)
api_key_frame.pack()

# Create a label for the API key entry
api_key_label = tk.Label(api_key_frame, text="Enter API key:", font='Helvetica 20')
api_key_label.pack(side="left")

# Create an entry for the API key
api_key_entry = tk.Entry(api_key_frame)
api_key_entry.pack(side="left")
api_key_entry.insert(0, "YOUR OpenAI API key")
#
# Create a frame for the max token entry
token_entry_frame = tk.Frame(window)
token_entry_frame.pack()

# Create a label for the max token entry
token_entry_label = tk.Label(token_entry_frame, text="Max token number:", font='Helvetica 20')

token_entry_label.pack(side="left")

# Create an entry for the max token
token_entry = tk.Entry(token_entry_frame)
token_entry.insert(0, "100")
token_entry.pack(side="left")

# Create a frame for the prompt entry
prompt_frame = tk.Frame(window)
prompt_frame.pack()

# Create a label for the prompt entry
prompt_label = tk.Label(prompt_frame, text="Prompt:", font='Helvetica 20')
prompt_label.pack(side="left")

# Create an entry for the prompt
prompt_entry = tk.Entry(prompt_frame,width=80)
prompt_entry.place(height=200)
prompt_entry.pack(side="left")

# Create a button to generate the response
generate_button = tk.Button(window, text="Generate Response", command=generate_response, font='Helvetica 20')
generate_button.pack()

# Create label
l = tk.Label(window, text=models_explanation)
l.config(font=("Courier", 8))
l.pack()

# Run the window loop
window.mainloop()
