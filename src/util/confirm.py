def get_yn(prompt, default_deny=False):
    default_answer = "y"
    default_prompt = "Y/n"
    if default_deny:
        default_answer = "n"
        default_prompt = "y/N"
    final_prompt = f"{prompt} ({default_prompt}):"
    yn = ""
    final_prompt
    while yn != "y" and yn != "n":
        yn = input(final_prompt).lower()
        if yn == "":
            yn = default_answer
        if yn != "y" and yn != "n":
            print("Invalid response\n")
    print()
    return yn

def confirm(really=False):
    confirmed = get_yn("Do you want to proceed?")
    if confirmed == "n":
        return False
    if really:
        confirmed = get_yn("Are you sure?", default_deny=True)
    if confirmed == "n":
        return False
    return True