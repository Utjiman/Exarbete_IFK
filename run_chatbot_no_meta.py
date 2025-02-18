from chatbot_no_meta import ask_lm_studio

if __name__ == "__main__":
    print("🔵 IFK Göteborg Chatbot - Ställ en fråga!")
    while True:
        user_input = input("Du: ")
        if user_input.lower() in ["exit", "quit", "avsluta"]:
            print("🔵 Avslutar chatten...")
            break

        answer = ask_lm_studio(user_input)
        print(f"Bot: {answer}\n")
