import pandas as pd
import unicodedata

# I Prefer OOP to FP
class Statistic:
    def __init__(self, file):
        self.data = pd.read_excel(file)
        self.subject_list = ["Math", "English", "Reading", "History", "Science"]

    def show_data(self):
        return self.data
    
    # lower text and strip out -> find a relative word
    def normalize(self, text):
        text = text.lower().strip()
        text = unicodedata.normalize("NFD",text)
        return "".join(
            char for char in text
        )


    def process_query(self, query):
        query = self.normalize(query)
        
        # Switch - case (basic rule-based)
        if "male" in query and ("gender" in query):
            gender = self.data["Gender"].astype(str).apply(self.normalize)
            return gender[gender == "male"]
        
        if "female" in query and ("gender" in query):
            gender = self.data["Gender"].astype(str).apply(self.normalize)
            return gender[gender == "female"]
        
        if "highest" in query:
            # Search the subject like a pointer
            subject = next(
                (word for word in self.subject_list if word.lower() in query),
            None
            )

            if subject is not None:
                highest_index = self.data[subject].idxmax()
            else:
                highest_index = self.data["GPA"].idxmax()
            
            return self.data.loc[[highest_index]]
        
        if "lowest" in query:
            # Search the subject like a pointer
            subject = next(
                (word for word in self.subject_list if word.lower() in query),
            None
            )

            if subject is not None:
                highest_index = self.data[subject].idxmin()
            else:
                highest_index = self.data["GPA"].idxmin()
            
            return self.data.loc[[highest_index]]

