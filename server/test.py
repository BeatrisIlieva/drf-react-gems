def first():
    print(1)
    
def second():
    def third():
        first()
    third()
    
second()