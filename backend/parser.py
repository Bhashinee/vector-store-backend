from unstructured.partition.auto import partition
from unstructured.documents.elements import ElementType, CheckBox

def parse_content(file):
    elements = partition(file=file)
    parsed_text_output = convert_elements_to_markdown(elements=elements)

    # return parsed_text_output
    return parsed_text_output

def convert_elements_to_markdown(elements):
    markdown = []
    
    for element in elements:
        element_type = element.category  # Using category instead of type since that's what's used in the classes
        
        # Headers and Titles
        if element_type in [ElementType.TITLE]:
            markdown.append(f"# {element.text}")

        # Subheadings
        if element_type in [ElementType.HEADLINE, ElementType.SUB_HEADLINE, 
                          ElementType.SECTION_HEADER, ElementType.FIELD_NAME]:
            markdown.append(f"## {element.text}")
            
        # Narrative Content
        elif element_type in [ElementType.NARRATIVE_TEXT, ElementType.TEXT, ElementType.PARAGRAPH,
                            ElementType.ABSTRACT, ElementType.THREADING, ElementType.FORM,
                            ElementType.VALUE, ElementType.COMPOSITE_ELEMENT]:
            markdown.append(f"{element.text}\n")
            
        # List Items
        elif element_type in [ElementType.LIST_ITEM, ElementType.BULLETED_TEXT, 
                            ElementType.LIST_ITEM_OTHER]:
            markdown.append(f"- {element.text}")
            
        # Tables
        elif element_type == ElementType.TABLE:
            if element.metadata.text_as_html:
                # Could add HTML-to-Markdown table conversion here if needed
                markdown.append(f"```html\n{element.metadata.text_as_html}\n```")
            else:
                markdown.append(f"```\n{element.text}\n```")
                
        # Images and Figures
        elif element_type in [ElementType.IMAGE, ElementType.PICTURE, ElementType.FIGURE]:
            if element.metadata.image_path:
                markdown.append(f"![Image]({element.metadata.image_path})")
            elif element.metadata.image_base64:
                markdown.append(f"![Image](data:{element.metadata.image_mime_type};base64,{element.metadata.image_base64})")
            else:
                markdown.append(f"![Image]({element.text})")
                
        # Captions
        elif element_type in [ElementType.FIGURE_CAPTION, ElementType.CAPTION]:
            markdown.append(f"*{element.text}*")
            
        # Headers and Footers
        elif element_type in [ElementType.HEADER, ElementType.PAGE_HEADER]:
            markdown.append(f"**{element.text}**")
        elif element_type in [ElementType.FOOTER, ElementType.PAGE_FOOTER, ElementType.FOOTNOTE]:
            markdown.append(f"_{element.text}_")
            
        # Special Formatting
        elif element_type == ElementType.CODE_SNIPPET:
            markdown.append(f"```code\n{element.text}\n```")
            
        elif element_type == ElementType.FORMULA:
            markdown.append(f"$${element.text}$$")
            
        # Contact Information
        elif element_type == ElementType.ADDRESS:
            markdown.append(f"[{element.text}]")
        elif element_type == ElementType.EMAIL_ADDRESS:
            markdown.append(f"<{element.text}>")
            
        # Form Key-Values
        elif element_type == ElementType.FORM_KEYS_VALUES:
            if element.metadata.key_value_pairs:
                for pair in element.metadata.key_value_pairs:
                    key_text = pair['key']['text']
                    value_text = pair['value']['text'] if pair['value'] else ""
                    markdown.append(f"**{key_text}:** {value_text}")
            else:
                markdown.append(f"{element.text}\n")
                
        # Structural Elements
        elif element_type == ElementType.PAGE_BREAK:
            markdown.append("---")
        elif element_type == ElementType.PAGE_NUMBER:
            markdown.append(f"[Page {element.text}]")
            
        # Checkboxes
        elif isinstance(element, CheckBox):
            marker = "[x]" if element.checked else "[ ]"
            markdown.append(f"{marker} {element.text}")
            
        # Default case for UncategorizedText and others
        else:
            markdown.append(f"{element.text}\n")
            
    return "\n".join(markdown)
