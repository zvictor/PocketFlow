from pocketflow import Node, BatchNode
from utils import call_llm
import yaml

class GenerateOutline(Node):
    def prep(self, shared):
        return shared["topic"]
    
    def exec(self, topic):
        prompt = f"""
Create a simple outline for an article about {topic}.
Include at most 3 main sections (no subsections).

Output the sections in YAML format as shown below:

```yaml
sections:
    - First section 
    - Second section
    - Third section
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        structured_result = yaml.safe_load(yaml_str)
        return structured_result
    
    def post(self, shared, prep_res, exec_res):
        # Store the structured data
        shared["outline_yaml"] = exec_res
        
        # Extract sections
        sections = exec_res["sections"]
        shared["sections"] = sections
        
        # Format for display
        formatted_outline = "\n".join([f"{i+1}. {section}" for i, section in enumerate(sections)])
        shared["outline"] = formatted_outline
        
        # Display the results
        print("\n===== OUTLINE (YAML) =====\n")
        print(yaml.dump(exec_res, default_flow_style=False))
        print("\n===== PARSED OUTLINE =====\n")
        print(formatted_outline)
        print("\n=========================\n")
        
        print(f"Parsed {len(sections)} sections: {sections}")
            
        return "default"

class WriteSimpleContent(BatchNode):
    def prep(self, shared):
        # Return the list of sections to process
        return shared.get("sections", [])
    
    def exec(self, section):
        prompt = f"""
Write a short paragraph (MAXIMUM 100 WORDS) about this section:

{section}

Requirements:
- Explain the idea in simple, easy-to-understand terms
- Use everyday language, avoiding jargon
- Keep it very concise (no more than 100 words)
- Include one brief example or analogy
"""
        return section, call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res_list):
        # Create a dictionary of section: content
        section_contents = {}
        all_content = []
        
        for section, content in exec_res_list:
            section_contents[section] = content
            all_content.append(f"## {section}\n\n{content}\n")
        
        shared["section_contents"] = section_contents
        
        # Combine all content into a single draft
        shared["draft"] = "\n".join(all_content)
        
        print("\n===== SECTION CONTENTS =====\n")
        for section, content in section_contents.items():
            print(f"--- {section} ---")
            print(content)
            print()
        print("===========================\n")
        
        return "default"

class ApplyStyle(Node):
    def prep(self, shared):
        """
        Get the draft from shared data
        """
        return shared["draft"]
    
    def exec(self, draft):
        """
        Apply a specific style to the article
        """
        prompt = f"""
        Rewrite the following draft in a conversational, engaging style:
        
        {draft}
        
        Make it:
        - Conversational and warm in tone
        - Include rhetorical questions that engage the reader
        - Add analogies and metaphors where appropriate
        - Include a strong opening and conclusion
        """
        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        """
        Store the final article in shared data
        """
        shared["final_article"] = exec_res
        print("\n===== FINAL ARTICLE =====\n")
        print(exec_res)
        print("\n========================\n")
        return "default" 