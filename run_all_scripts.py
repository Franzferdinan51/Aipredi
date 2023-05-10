import threading
import traceback
import requests
import subprocess
import time
from privateblockchain import PrivateBlockchain
from aipredi import fix_code
from bs4 import BeautifulSoup
import random


def train_model(stop_event, pause_event):
    epoch = 0

    while not stop_event.is_set():
        while pause_event.is_set():
            time.sleep(0.1)

        time.sleep(0.5)
        epoch += 1

        if epoch == 10:
            break

    try:
        undefined_function()
    except Exception as e:
        tb = traceback.format_exc()

        with open('error.log', 'w') as f:
            f.write(tb)

        response = input(f"An error occurred:\n\n{tb}\n\nDo you want to view the error log? (y/n)")
        if response.lower() == "y":
            subprocess.Popen(['xdg-open', 'error.log'])

    response = input("Do you want to commit the fix to the blockchain? (y/n)")
    if response.lower() == "y":
        try:
            blockchain = PrivateBlockchain()
            fixed_code = fix_code("my_file.py")
            blockchain.add_block(fixed_code)
            print("The fix has been committed to the blockchain successfully.")
        except Exception as e:
            tb = traceback.format_exc()

            with open('error.log', 'w') as f:
                f.write(tb)

            response = input(f"An error occurred while committing to the blockchain:\n\n{tb}\n\nDo you want to view the error log? (y/n)")
            if response.lower() == "y":
                subprocess.Popen(['xdg-open', 'error.log'])


def start_training():
    global stop_event, pause_event
    stop_event = threading.Event()
    pause_event = threading.Event()

    search_query = "python 'list index out of range' error fix"
    stack_overflow_results = []

    for page in range(1, 11):
        url = f"https://stackoverflow.com/search?page={page}&q={search_query}"
        try:
            webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except Exception as e:
            print(f"An error occurred while getting the webpage content: {e}")
            continue

        soup = BeautifulSoup(webpage.content, 'html.parser')

        results = soup.find_all('div', class_='question-summary search-result')

        for result in results:
            try:
                title = result.find('a', class_='question-hyperlink').get_text()
                url = f"https://stackoverflow.com{result.find('a', class_='question-hyperlink')['href']}"
                question_page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                question_soup = BeautifulSoup(question_page.content, 'html.parser')
                code_blocks = question_soup.find_all('pre', class_='lang-python')
                for code_block in code_blocks:
                    stack_overflow_results.append(code_block.get_text())
            except Exception as e:
                print(f"An error occurred while parsing the search results: {e}")
                continue

    if stack_overflow_results:
        print(f"{len(stack_overflow_results)} code fixes found.")
        fix = random.choice(stack_overflow_results)
        print(f"Using the following fix:\n\n{fix}\n\n")
        response = input("Do you want to apply this fix? (y/n)")
        if response.lower() == "y":
            with open("my_file.py", "w") as f:
                f.write(fix)
            print("The fix has been applied successfully.")
    else:
        print("No code fixes found.")
# Start training the model in a separate thread
training_thread = threading.Thread(target=train_model, args=(stop_event, pause_event))
training_thread.start()
# Wait for the user to stop or pause the training
while True:
    response = input("Enter 's' to stop training or 'p' to pause training:")
    if response.lower() == "s":
        stop_event.set()
        break
    elif response.lower() == "p":
        pause_event.set()
    else:
        print("Invalid input. Please try again.")

# Wait for the training thread to finish
training_thread.join()

print("Training complete.")


