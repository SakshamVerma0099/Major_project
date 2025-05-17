import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from PIL import Image, ImageTk
import base64
import os

def run_image_analysis_ui(api_key, image_path):
    openai.api_key = api_key
    base64_image = None

    root = tk.Tk()
    root.title("Aerial Image Analyzer")
    root.geometry("800x700")
    root.configure(bg="#f0f4f7")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image path does not exist: {image_path}")

    try:
        img = Image.open(image_path)
        img.thumbnail((500, 500))
        tk_img = ImageTk.PhotoImage(img)

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to load image:\n{e}")

    # --- Functions ---
    def analyze_image():
        prompt = prompt_entry.get()
        if not prompt.strip():
            prompt = "Today we are examining our fileds for and kind of crop desease if you spot any kind of desease please explain the problem and give solution if possible "

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            result = response["choices"][0]["message"]["content"]
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)
            output_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"API call failed:\n{e}")

    # --- UI Layout ---
    tk.Label(root, text="Aerial Image Analysis", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=10)

    control_frame = tk.Frame(root, bg="#f0f4f7")
    control_frame.pack(pady=5)

    tk.Label(control_frame, text="Prompt : today we are searching desease in crops ", bg="#f0f4f7").pack()
    prompt_entry = tk.Entry(control_frame, width=70)
    prompt_entry.pack(pady=5)
    prompt_entry.insert(0, "today we are searching desease in crops")

    ttk.Button(control_frame, text="Analyze Image", command=analyze_image).pack(pady=5)

    image_frame = tk.Frame(root, bg="#f0f4f7")
    image_frame.pack(pady=10)

    image_label = tk.Label(image_frame, image=tk_img)
    image_label.image = tk_img
    image_label.pack()

    tk.Label(root, text="Image Explanation", font=("Helvetica", 14, "bold"), bg="#f0f4f7").pack(pady=5)
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15, font=("Helvetica", 11))
    output_text.pack(pady=10)
    output_text.config(state=tk.DISABLED)

    root.mainloop()


# --- Run the tool ---
if __name__ == "__main__":
    run_image_analysis_ui(
        api_key="sk-proj-NM2Ztmed",  
        image_path=r"C:\Users\ASUS\Downloads\Screenshot 2025-05-06 234248.png"
    )
