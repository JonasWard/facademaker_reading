class IAmAClass:
    def print_me(self):
        print(str(type(self).__name__) )

if __name__ == "__main__":
    IAmAClass().print_me()