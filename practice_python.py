class Person:
    def set_name(self, name_list):
        # Sets the first, middle and last name from a list
        if len(name_list) == 3: # If all names are provided
            self.first_name,self.middle_name,self.last_name = name_list
        elif len(name_list) == 2: # If fist and last name are provided 
            self.first_name,self.last_name = name_list
            self.middle_name = ""
        else:
            raise ValueError("Error => Name without last name is not accepted")

    def get_full_name(self):
         # Return fullname include middle name if provided
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
    
class Student(Person):
    def set_graduation_year(self, year):
        # Sets the graduation year
        self.graduation_year = year

student = Student()

#Test cases
   
# Case 1: First and Last names are provided
student.set_name(["Jubair","Kibria"]) 
student.set_graduation_year(2008) # Sets graduation year
print(student.get_full_name(),"was the class of",student.graduation_year)
    
# Case 2: All three names are provided
student.set_name(["Jubair","Bin","Kibria"])
print(student.get_full_name(),"was the class of",student.graduation_year)
    
# Case 3: Only one name is provided
student.set_name(["Jubair"]) # Sets all names using a list