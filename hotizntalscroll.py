from tkinter import *
from random import randint, choice

root = Tk()
root.geometry("1000x600")
root.title("Horizontal Scrollable Labels")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)

spacing_Frame=Frame(root,width=100,height=100)
main_frame = Frame(root, bg="#FF0000",height=40)
secondry_frame= Frame(root,bg="red")
# Create main frame


main_frame.pack(expand=True, padx=10, pady=10,anchor="n")
# spacing_Frame.grid(row=0,column=1,sticky="nsew")
# main_frame.grid(row=1,column=1,sticky="nsew")
# secondry_frame.grid(row=2,column=1,rowspan=1000,sticky="nsew")
# Create a canvas
canvas = Canvas(main_frame, width=1000, height=40)

# Create horizontal scrollbar
scrollbar = Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
scrollbar.pack(side='bottom', fill='x')

# Configure canvas
canvas.configure(xscrollcommand=scrollbar.set)
canvas.pack(expand=True, fill='both')

# Create frame inside canvas to hold labels
inner_frame = Frame(canvas)
inner_frame.rowconfigure(0,weight=1)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

# Add some sample labels
sample_texts = [f"Label {i}" for i in range(1, 21)]
labels = []

for i, text in enumerate(sample_texts):
    mm=randint(5,30)
    inner_frame.columnconfigure(i,weight=mm)
    label = Label(inner_frame,width= mm,
                        background= choice(["#D1263D","#61D126","#44D126","#D19B26","#264ED1"]),
                        height=2, text=mm)
    # label.pack(side="right")
    label.grid(column=mm,row=0)
    labels.append(label)

# Update scroll region after adding labels
inner_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox('all'))

def on_mousewheel(event):
# Shift + MouseWheel for horizontal scrolling
    if event.state == 1:  # Shift is being held
        canvas.xview_scroll(int(-1 * (event.delta / 220)), 'units')
    else:
        canvas.xview_scroll(int(-1 * (event.delta / 220)), 'units')
# Bind mouse wheel for horizontal scrolling
canvas.bind('<MouseWheel>', on_mousewheel)
canvas.bind('<Shift-MouseWheel>', on_mousewheel)



root.mainloop()