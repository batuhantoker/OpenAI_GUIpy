import tkinter as tk
import openai

def generate_response():
    # Get the model, API key, and prompt
    model = model_var.get()
    api_key = api_key_entry.get()
    prompt = prompt_entry.get()

    # Set the API key
    openai.api_key = api_key

    # Generate a response
    completions = openai.Completion.create(engine=model, prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.5)
    message = completions.choices[0].text

    # Display the response
    response_label.config(text=message)

# Create the window
window = tk.Tk()
window.title("OpenAI GUI")

# Create a frame for the model selection
model_frame = tk.Frame(window)
model_frame.pack()

# Create a label for the model selection
model_label = tk.Label(model_frame, text="Select a model:")
model_label.pack(side="left")

# Create a variable to store the selected model
model_var = tk.StringVar(value="text-davinci-002")

# Create a dropdown menu for the model selection
model_menu = tk.OptionMenu(model_frame, model_var, "text-davinci-002", "davinci", "curie")
model_menu.pack(side="left")

# Create a frame for the API key entry
api_key_frame = tk.Frame(window)
api_key_frame.pack()

# Create a label for the API key entry
api_key_label = tk.Label(api_key_frame, text="Enter API key:")
api_key_label.pack(side="left")

# Create an entry for the API key
api_key_entry = tk.Entry(api_key_frame)
api_key_entry.pack(side="left")

# Create a frame for the prompt entry
prompt_frame = tk.Frame(window)
prompt_frame.pack()

# Create a label for the prompt entry
prompt_label = tk.Label(prompt_frame, text="Enter prompt:")
prompt_label.pack(side="left")

# Create an entry for the prompt
prompt_entry = tk.Entry(prompt_frame)
prompt_entry.pack(side="left")

# Create a button to generate the response
generate_button = tk.Button(window, text="Generate Response", command=generate_response)
generate_button.pack()

# Create a label to display the response
response_label = tk.Label(window, text="")
response_label.pack()

# Run the window loop
window.mainloop()
