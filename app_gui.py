import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import time
import random

model = tf.keras.models.load_model("keras_model.h5")

with open("labels.txt", "r") as f:
    labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]

cancer_classes = [0, 1, 3, 7]

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)

def is_valid_skin_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.asarray(img, dtype=np.float32) / 255.0
        mean_pixel = np.mean(img_array)
        return 0.25 < mean_pixel < 0.85
    except:
        return False

def diagnose_skin_cancer(image_path):
    img_data = preprocess_image(image_path)
    prediction = model.predict(img_data)[0]
    max_index = np.argmax(prediction)
    confidence = prediction[max_index] * 100
    predicted_label = labels[max_index]

    if confidence < 70:
        return f"⚠️ Result uncertain. Try a clearer image.\nTop Prediction: {predicted_label} ({confidence:.2f}%)"
    elif max_index in cancer_classes:
        return f"🔴 Yes, cancer detected!\nType: {predicted_label} ({confidence:.2f}%)"
    else:
        return f"🟢 No cancer detected.\nPrediction: {predicted_label} ({confidence:.2f}%)"

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        global selected_image_path
        selected_image_path = file_path
        img = Image.open(file_path).resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        result_label.config(text="Image uploaded. Click 'Check Cancer' to diagnose.")

def check_cancer():
    if not selected_image_path:
        messagebox.showwarning("Warning", "Please upload an image first.")
        return

    if not is_valid_skin_image(selected_image_path):
        messagebox.showerror("Invalid Image", "⚠️ Please upload a proper skin lesion image.")
        result_label.config(text="❌ Invalid image. Please try again with a skin photo.")
        return

    result_label.config(text="🔍 Diagnosing...")
    root.update()
    time.sleep(1.5)

    result_text = diagnose_skin_cancer(selected_image_path)
    messagebox.showinfo("Diagnosis Result", result_text)
    result_label.config(text=result_text)

root = tk.Tk()
root.title("Skin Cancer Detection")
root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.bind("<Escape>", lambda event: root.destroy())

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0, bg="#1e1e2f")
canvas.pack(fill="both", expand=True)

particles = []
num_particles = 80
for _ in range(num_particles):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    r = random.randint(1, 3)
    dx = random.uniform(-0.7, 0.7)
    dy = random.uniform(-0.7, 0.7)
    p = {'id': canvas.create_oval(x - r, y - r, x + r, y + r, fill="#00ffd5", outline=""), 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'r': r}
    particles.append(p)

def animate_particles():
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        if p['x'] > screen_width: p['x'] = 0
        if p['x'] < 0: p['x'] = screen_width
        if p['y'] > screen_height: p['y'] = 0
        if p['y'] < 0: p['y'] = screen_height
        canvas.coords(p['id'], p['x'] - p['r'], p['y'] - p['r'], p['x'] + p['r'], p['y'] + p['r'])

    root.after(20, animate_particles)

animate_particles()

main_frame = tk.Frame(canvas, bg="#1e1e2f")

main_frame.place(relx=0.5, rely=0.5, anchor="center")

selected_image_path = None

title_label = tk.Label(main_frame, text="🩺 Skin Cancer Detection", font=("Helvetica", 32, "bold"), bg="#1e1e2f", fg="#00ffd5")
title_label.pack(pady=30)

upload_btn = tk.Button(main_frame, text="📁 Upload Image", command=upload_image, bg="#00ffd5", fg="#1e1e2f",
                       font=("Arial", 20, "bold"), padx=30, pady=15, bd=0, activebackground="#00c9aa", cursor="hand2")
upload_btn.pack(pady=20)

check_btn = tk.Button(main_frame, text="🧪 Check Cancer", command=check_cancer, bg="#ff3c6f", fg="#ffffff",
                      font=("Arial", 20, "bold"), padx=30, pady=15, bd=0, activebackground="#e0315e", cursor="hand2")
check_btn.pack(pady=10)

image_frame = tk.Frame(main_frame, bg="#f0f0f0", bd=2, relief="ridge")
image_frame.pack(pady=30)

image_label = tk.Label(image_frame, bg="#f0f0f0")
image_label.pack()

result_label = tk.Label(main_frame, text="", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="#00ff88", wraplength=800, justify="center")
result_label.pack(pady=30)

footer = tk.Label(root, text="Made by Tahir & Ghufran ❤️ in Python", font=("Arial", 12), bg="#1e1e2f", fg="#888")
footer.place(relx=0.5, rely=0.97, anchor="center")

root.mainloop()