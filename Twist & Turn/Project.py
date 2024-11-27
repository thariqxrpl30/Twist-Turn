import tkinter as tk
from tkinter import messagebox
import math
import time
import pygame   # Tambahkan ini untuk suara
import os  

#Fungsi Tambah
def tambah():
    """Tambahkan nama ke list."""
    new_name = entry.get().strip()
    if new_name:
        names.append(new_name)
        listbox.insert(tk.END, new_name)
        entry.delete(0, tk.END)
        draw_wheel()
        panah()

#Fungsi Hapus
def hapus():
    """Hapus nama yang dipilih dari list dan perbarui roda."""
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        names.pop(index)
        listbox.delete(index)
        draw_wheel()
        panah()

#Fungsi Reset
def resets():
    """Reset daftar nama."""
    names.clear()
    listbox.delete(0, tk.END)
    draw_wheel()
    panah()

#Fungsi Suara saat Menang
pygame.mixer.init()
def play_sound():
    sound_file = os.path.join(os.path.dirname(__file__), "Terompet.mp3")
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

#Roda Berputar
def spin_wheel():
    """Putar roda dengan animasi selama sekitar 9 detik, terlepas dari jumlah elemen."""
    global current_angle

    total_duration = 9 
    spins = 100 

    # Kecepatan awal animasi
    speed = total_duration / (spins ** 1.5)  
    angle_per_step = 15  

    for i in range(spins):
        current_angle = (current_angle + angle_per_step) % 360 
        draw_wheel()
        panah()
        root.update()
        
        time.sleep(speed)
        speed *= 1.02  

    # Menghitung pemenang berdasarkan posisi panah
    if len(names) > 0:
        sector_size = 360 / len(names)
        adjusted_angle = (360 - current_angle) % 360
        index = int(adjusted_angle / sector_size)
        if index >= len(names):
            index = 0

        final_choice = names.pop(index)  # Hapus pemenang dari daftar
        listbox.delete(index)  # Hapus pemenang dari Listbox
        
        # Mainkan suara saat pemenang muncul
        play_sound()
        messagebox.showinfo("You got a choice!", f"Pilihan untukmu adalah:\n\n{final_choice}")

    draw_wheel()
    panah()

#Gambar Roda
def draw_wheel():
    """Gambar roda dan bagiannya di Canvas."""
    canvas.delete("all")
    num_names = len(names)
    
    center_x = 200  
    center_y = 200  
    radius_outer = 150  
    
    #Warna Roda jika belum ada data sama sekali
    if num_names == 0:
        canvas.create_oval(
            center_x - radius_outer, center_y - radius_outer,
            center_x + radius_outer, center_y + radius_outer,
            fill="silver" #Silver
            , outline="white"
        )
        return

    angle_per_sector = 360 / num_names
    start_angle = current_angle

    # Tambahkan lingkaran luar sebagai border
    canvas.create_oval(
        center_x - radius_outer, center_y - radius_outer,
        center_x + radius_outer, center_y + radius_outer,
        outline="white", width=2
    )

    #Warna Roda jika hanya ada 1 data
    if num_names == 1:
        canvas.create_oval(50, 50, 350, 350, fill="#F9B7FF" #Pink
                           , outline="white", width=2)
        canvas.create_text(center_x, center_y, 
                           text=names[0], 
                           fill="Black",    #Warna Tulisan pada Lingkaran
                           font=("Arial", 16, "bold"))
        return

    for i, name in enumerate(names):
        end_angle = start_angle + angle_per_sector

        # Gambar sektor
        canvas.create_arc(
            center_x - radius_outer, center_y - radius_outer,
            center_x + radius_outer, center_y + radius_outer,
            start=start_angle,
            extent=angle_per_sector,
            fill=colors[i % len(colors)],
            outline="white",
            tags="wheel"
        )

        text_angle = math.radians((start_angle + end_angle) / 2)
        text_radius = radius_outer * 0.7
        x = center_x + text_radius * math.cos(text_angle)
        y = center_y - text_radius * math.sin(text_angle)

        rotation = (start_angle + angle_per_sector / 2) + 90
        if 90 <= rotation <= 270:
            rotation += 180

        canvas.create_text(
            x, y,
            text=name,
            fill="Black",   #Warna Tulisan Pada Lingkaran
            font=("Arial", 12, "bold"),
            angle=rotation,
            tags="wheel"
        )

        start_angle = end_angle

#Gambar Panah
def panah():
    arrow_size = 20
    arrow_base = 15
    arrow_x = 350  
    arrow_y = 200  

    points = [
        arrow_x, arrow_y,
        arrow_x + arrow_base, arrow_y - arrow_size,
        arrow_x + arrow_base, arrow_y + arrow_size,
    ]
    
    canvas.create_polygon(
        points,
        fill="#9F000F", #Warna Panah
        outline="black",
        width=2,
        tags="indicator"
    )

# Inisialisasi GUI
root = tk.Tk()
root.title("Twist & Turn")
root.geometry("500x700")
root.config(bg="Black") #Warna Latar GUI

canvas = tk.Canvas(root, width=400, height=400, highlightthickness=0, 
                   bg="Black" #Warna Latar Canvas
                   )
canvas.pack(pady=10)

frame = tk.Frame(root, 
                 bg="Black" #Warna Latar Tempat Tombol
                 )
frame.pack(pady=10)

listbox_label = tk.Label(root, text="Daftar Nama:", bg="Black", #Warna Latar 
                         fg="white", font=("Arial", 12))
listbox_label.pack()

listbox = tk.Listbox(root, width=30, height=10, bg="#DADBDD"  #Warna Latar Tempat List
                     , fg="black", relief=tk.SOLID, bd=1)
listbox.pack(pady=10)

entry = tk.Entry(frame, bg="white", #Warna Latar Tempat Input
                 justify="center", font=("Arial", 12))
entry.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, ipady=5)

names = []
current_angle = 0

#Warna Setiap Sektor Lingkaran
colors = ["#F9B7FF", "#EDE6D6", "#E0B0FF", "#9E7BFF", "#822EFF", "#736AFF", "#D291BC", 
          "#D462FF", "#FF77FF", "#FF69B4", "#FFB2D0", "#F8B88B", "#F75D59", "#FF8674", 
          "#FFA07A", "#8A865D", "#E9AB17", "#BCB88A", "#FBB117", "#FFDAB9", 
          "#64E986", "#A0D6B4", "#F8B88B"]

                        #Warna Cadangan
#FF0000 red
#FFFF00 yellow
#0000FF blue
#00FF00 lime
#FF00FF magenta
#FFFFFF white
#513B1C milk chocolate

frame.columnconfigure(0, weight=1, uniform="group1")
frame.columnconfigure(1, weight=1, uniform="group1")
frame.columnconfigure(2, weight=1, uniform="group1")
frame.columnconfigure(3, weight=1, uniform="group1")

#Tombol Tambah
add_button = tk.Button(frame, text="Tambahkan", command=tambah, bg="green", fg="black"  #Warna Tulisan pada Tombol
                       , font=("Arial", 12), width=12, height=1)
add_button.grid(row=0, column=1, padx=10, pady=5)

#Tombol Delete
delete_button = tk.Button(frame, text="Hapus", command=hapus, bg="orange", fg="black"   #Warna Tulisan pada Tombol
                          , font=("Arial", 12), width=12, height=1)
delete_button.grid(row=0, column=2, padx=10, pady=5)

#Tombol Reset
reset_button = tk.Button(frame, text="Reset", command=resets, bg="red", fg="black"  #Warna Tulisan pada Tombol
                         , font=("Arial", 12), width=12, height=1)
reset_button.grid(row=0, column=3, padx=10, pady=5)

#Tombol Spin
spin_button = tk.Button(frame, text="Spin!", command=spin_wheel, bg="#ADD8E6", fg="black"   #Warna Tulisan pada Tombol
                        , font=("Arial", 12), width=12, height=1)
spin_button.grid(row=0, column=4, padx=10, pady=5)

draw_wheel()

root.mainloop()