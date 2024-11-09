import threading # this line is used to Imports Python’s threading module,which allows the creation and management of threads.
import tkinter as tk # this line is Imports Tkinter, a Python library for creating graphical user interfaces

BUFFER_SIZE = 10 # the buffer storeage size is set to 10
buffer = [None] * BUFFER_SIZE # this line  Initializes a list of None values
in_index = 0 # this line which will keep track of the next position where the producer should insert an item.
out_index = 0 # this line which will keep track of the next position where the consumer should remove an item.
x = 0 # It increments each time a new item is produced, helping to generate unique item values.
# the below 3 are the semaphore variables
mutex = threading.Semaphore(1)     # A binary semaphore initialized to 1, acting as a mutual exclusion (mutex) lock to ensure only one thread accesses the buffer at a time.
full = threading.Semaphore(0)      #  A counting semaphore to track the number of filled slots in the buffer. Initially set to 0 because the buffer is empty at the start.
empty = threading.Semaphore(BUFFER_SIZE)  # Counting semaphore to track empty slots

# Function to produce an item and add it to the buffer
def producer():
    global in_index, x

    if empty.acquire(blocking=False):  # Try to acquire empty slot
        mutex.acquire()  # Enter critical section

        x += 1
        buffer[in_index] = x
        log_text(f"Producer produces item {x}")
        in_index = (in_index + 1) % BUFFER_SIZE

        mutex.release()  # Exit critical section
        full.release()   # Signal that there is a new full slot
    else:
        log_text("Buffer is full! Cannot produce.")

# Function to consume an item and remove it from the buffer
def consumer():
    global out_index

    if full.acquire(blocking=False):  # Try to acquire full slot
        mutex.acquire()  # Enter critical section

        item = buffer[out_index]
        log_text(f"Consumer consumes item {item}")
        buffer[out_index] = None  # Clear the buffer slot
        out_index = (out_index + 1) % BUFFER_SIZE

        mutex.release()  # Exit critical section
        empty.release()  # Signal that there is a new empty slot
    else:
        log_text("Buffer is empty! Cannot consume.")

# Function to update the log area in the GUI
def log_text(text):
    log_area.insert(tk.END, text + "\n")
    log_area.see(tk.END)

# Function to handle the producer button click
def producer_button_click():
    threading.Thread(target=producer).start()

# Function to handle the consumer button click
def consumer_button_click():
    threading.Thread(target=consumer).start()

# Function to handle the exit button click
def exit_button_click():
    root.quit()
    root.destroy()

# Initialize the GUI
root = tk.Tk()
root.title("Producer-Consumer Problem")
root.geometry("400x400")

# Add buttons and log area to the GUI
producer_button = tk.Button(root, text="Produce", command=producer_button_click)
producer_button.pack(pady=10)

consumer_button = tk.Button(root, text="Consume", command=consumer_button_click)
consumer_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_button_click)
exit_button.pack(pady=10)

log_label = tk.Label(root, text="Buffer Log:")
log_label.pack()

log_area = tk.Text(root, height=15, width=40)
log_area.pack(pady=10)

# Run the main GUI loop
root.mainloop()