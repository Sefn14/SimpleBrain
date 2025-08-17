import json
import datetime
import os

AI_AGENT = "SimpleBrain" # Name of the AI Agent
USER_INFO = "user.json" # File to store user information
memory = [] # Memory to store chat for recalling the last message

class Agent:
    def __init__(self, name):
        self.name = name

    def respond(self, input, name=""): # A predefined set of responses
        memory.append(input)
        input = input.lower()
        match(input):

            # Greetings
            case "hi" | "hello" | "hey" :
                return "Hi there, how can I help you today?"
            case "yo":
                return "Yo, how are you doing?"
            case "what's up":
                return "The sky! But how can I be of help today"

            # Questions
            case "what's your name?" | "what is your name?":
                return f"I am an AI agent called {AI_AGENT}"
            case "what is my name?" | "what's my name?":
                if name == '':
                    return "You are in guest mode"
                else:
                    return f"Your name is {name}"
            case "list of phrases":
                return """List of phrases that can be answered:
                    - Hi
                    - Hello
                    - Hey
                    - Yo
                    - What's up
                    - What is your name?
                    - What is my name?
                    - Bye
                    - Goodbye
                    - What did I say?
                    - Repeat what I said
                    [!] If you write something other than these, the program says it cannot understand you
                       """
            case "what did i say?"|"repeat what i said":
                if len(memory) < 2:
                    return "I don't have enough memory to recall your last message"
                else:
                    return f"You said '{memory[-2]}'"

            # Farewells
            case "bye" | "goodbye":
                return "Bye, I hope I was of any help!"

            # Default Case
            case _:
                return "I did not understand what you said, It does not follow the set of instructions I was given with"

    def logChat(self, input, name): # Log the chat to a .txt file
        fileName = f"{name}/chat.txt"
        with open(fileName, 'a') as file:
            file.write(input+"\n")
    def logUser(self, user):
        userInfoPath = os.path.join(user, USER_INFO)
        os.makedirs(user, exist_ok=True)
        if not os.path.exists(userInfoPath):
            data = {"name":user,"conversation":1}
            with open(userInfoPath, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            with open(userInfoPath, 'r') as file:
                data = json.load(file)
            data["conversation"] += 1
            with open(userInfoPath, 'w') as file:
                json.dump(data, file, indent=4)
    def guestChat(self):
        while True:
            userInput = input("[+] Enter text for the chat: ")
            response = self.respond(userInput)
            print(response)
            if response == "Bye, I hope I was of any help!":
                break

    def userChat(self, name):
        self.logUser(name)
        self.logChat(f"\nTime: {datetime.datetime.now().isoformat(timespec='seconds')}", name)
        while True:
            userInput = input("[+] Enter text for the chat: ")
            self.logChat("[User] "+userInput, name)
            response = self.respond(userInput, name)
            self.logChat("[SimpleBrain] "+response, name)
            print(response)
            if response == "Bye, I hope I was of any help!":
                break

    def setup(self):
        userIn = None
        name = ""
        print("""

Welcome, and thank you for using Simple Brain.
+-----------------------------------------------------------+
| ____  _                 _        ____            _        |
|/ ___|(_)_ __ ___  _ __ | | ___  | __ ) _ __ __ _(_)_ __   |
|\___ \| | '_ ` _ \| '_ \| |/ _ \ |  _ \| '__/ _` | | '_ \\  |
| ___) | | | | | | | |_) | |  __/ | |_) | | | (_| | | | | | |
||____/|_|_| |_| |_| .__/|_|\___| |____/|_|  \__,_|_|_| |_| |
|                  |_|                                      |
+-----------------------------------------------------------+

                            ~Sefn14
        """)

        print("[!]Note: Your chat will be saved in a .txt file for future review if you choose to sign up. This functionality is not available on Guest mode.")
        print("[!] Write 'List of phrases' to see all the answerable phrases")
        while userIn == None:
            try:
                userIn = int(input("[*] Input 0 for guest mode, input 1 for sign up: "))
            except ValueError:
                print("[!] Error: You did not provide an Invalid Input")
            except Exception as e:
                print(f"[!] Error: {e}")

        if userIn == 1:
            while name == "":
                name = input("[*] Enter your name: ")
            self.userChat(name)
        elif userIn == 0:
            self.guestChat()
        else:
            print("[?] Invalid Choice: Choice Unavailable")

if __name__ == "__main__":
    agent = Agent(AI_AGENT)
    agent.setup()
    
