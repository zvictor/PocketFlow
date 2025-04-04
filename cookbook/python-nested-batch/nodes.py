import os
from brainyflow import Node

class LoadGrades(Node):
    """Node that loads grades from a student's file."""
    
    async def prep(self, shared):
        """Get file path from parameters."""
        class_name = self.params["class"]
        student_file = self.params["student"]
        return os.path.join("school", class_name, student_file)
    
    async def exec(self, file_path):
        """Load and parse grades from file."""
        with open(file_path, 'r') as f:
            # Each line is a grade
            grades = [float(line.strip()) for line in f]
        return grades
    
    async def post(self, shared, prep_res, grades):
        """Store grades in shared store."""
        shared["grades"] = grades
        return "calculate"

class CalculateAverage(Node):
    """Node that calculates average grade."""
    
    async def prep(self, shared):
        """Get grades from shared store."""
        return shared["grades"]
    
    async def exec(self, grades):
        """Calculate average."""
        return sum(grades) / len(grades)
    
    async def post(self, shared, prep_res, average):
        """Store and print result."""
        # Store in results dictionary
        if "results" not in shared:
            shared["results"] = {}
        
        class_name = self.params["class"]
        student = self.params["student"]
        
        if class_name not in shared["results"]:
            shared["results"][class_name] = {}
            
        shared["results"][class_name][student] = average
        
        # Print individual result
        print(f"- {student}: Average = {average:.1f}")
        return "default" 