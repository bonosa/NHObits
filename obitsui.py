import threading
from tkinter import Tk, Text, Button, Radiobutton, IntVar, Label, Scrollbar, Frame, END
from obits import scrape_obituaries  # Ensure obits.py is correctly set up

def fetch_and_display_obituaries(next_page=False):
    def scrape_and_update():
        current_page = page_var.get()
        if next_page:
            current_page += 1  # Increment page if next_page is True
        
        mode = 'page_by_page' if mode_var.get() == 1 else 'all_at_once'
        file_path = "pagebypageplus.txt" if mode == 'page_by_page' else "allatonce.txt"
        
        # Fetch data
        names = scrape_obituaries("https://www.newsherald.com/obituaries", mode, current_page, 3 if mode == 'all_at_once' else 1)
        print(f"Names fetched from page {current_page}: {names}")  # Debugging print
        
        # Write names to file
        with open(file_path, "a" if mode == 'page_by_page' else "w") as file:
            for name in names:
                file.write(name + '\n')
        
        # Update UI
        text_area.delete('1.0', END)
        text_area.insert(END, '\n'.join(names))
        
        # Update page_var only in 'page_by_page' mode
        if mode == 'page_by_page' and names:
            page_var.set(current_page)
            print(f"Moving to page {current_page + 1}")
        
        loading_label.config(text="")  # Clear loading message

    loading_label.config(text="Loading... Please wait.")
    threading.Thread(target=scrape_and_update, daemon=True).start()

def go_to_next_page():
    """Fetch the next page of obituaries for 'Page by Page' mode."""
    if mode_var.get() == 1:
        fetch_and_display_obituaries(next_page=True)

def update_next_page_button_visibility():
    """Show or hide the 'Next Page' button based on the selected mode."""
    if mode_var.get() == 1:
        next_page_button.pack(side='bottom', pady=5)
    else:
        next_page_button.pack_forget()

root = Tk()
root.title("Obituary Scraper")
frame = Frame(root)
frame.pack(padx=10, pady=10)

mode_var = IntVar(value=1)  # Default to 'Page by Page' mode
page_var = IntVar(value=1)  # Start from the first page

# Mode selection
Radiobutton(frame, text="Page by Page", variable=mode_var, value=1, command=update_next_page_button_visibility).pack(anchor='w')
Radiobutton(frame, text="All at Once", variable=mode_var, value=2, command=update_next_page_button_visibility).pack(anchor='w')

# Fetch button
Button(frame, text="Fetch Obituaries", command=lambda: fetch_and_display_obituaries()).pack(pady=10)

# Next Page button, visibility managed by mode selection
next_page_button = Button(frame, text="Next Page", command=go_to_next_page)

# Initial setup for button visibility based on mode
update_next_page_button_visibility()

# UI Elements for displaying fetched names and loading status
loading_label = Label(frame, text="")
loading_label.pack()

text_area = Text(frame, height=15, width=50)
scrollbar = Scrollbar(frame, orient='vertical', command=text_area.yview)
text_area.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')
text_area.pack(side='left', fill='both', expand=True)

root.mainloop()
