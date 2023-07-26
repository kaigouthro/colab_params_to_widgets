import re

def convert_to_widget_code(text):
    matches = re.findall(r"(\w+)\s*=\s*(.*?)\s*#@param(?:\s*(.+))?$", text, re.MULTILINE)
    code = ""
    for match in matches:
        param_name = match[0]
        param_value = match[1]
        param_config = match[2]
        widget_type = re.search('type:\\s*"(\w+)"', param_config)
        if widget_type:
            widget_type = widget_type.group(1)
            if widget_type == "raw":
                code += f"{param_name} = {param_value} # CHECKTHIS\n"
            elif widget_type == "string":
                code += f"{param_name} = widgets.Text(value='{param_value}', description='{param_name}')\n"
            elif widget_type == "number":
                #split float and int
                if param_value.is_integer():
                    code += f"{param_name} = widgets.IntText(value={param_value}, description='{param_name}')\n"
                else:
                    code += f"{param_name} = widgets.FloatText(value={param_value}, description='{param_name}')\n"
            elif widget_type == "slider":
                min_value = re.search("min:(.*?),", param_config)
                max_value = re.search("max:(.*?),", param_config)
                step_value = re.search("step:(.*?)}", param_config)
                code += f"{param_name} = widgets.FloatSlider(value={param_value}, min={min_value}, max={max_value}, step={step_value}, description='{param_name}')\n"
            elif widget_type == "integer":
                code += f"{param_name} = widgets.IntText(value={param_value}, description='{param_name}')\n"
            elif widget_type == "boolean":
                code += f"{param_name} = widgets.Checkbox(value={param_value}, description='{param_name}')\n"
            elif widget_type == "date":
                code += f"{param_name} = widgets.DatePicker(value='{param_value}', description='{param_name}')\n"
            else:
                code += f"# Widget type not supported: {widget_type}\n"
        else:
            if param_config:
                param_config = re.match(r"(\[.*\])", param_config).group(1)
                # add for cases where no widget type is specified, but an array of options is given
                if param_config.startswith("[") and param_config.endswith("]"):
                    options = param_config[1:-1]
                    options = options.split(",")
                    options = [option.strip() for option in options]
                    options = [option.strip('"') for option in options]
                    code += f"{param_name} = widgets.Dropdown(options={options}, value='{param_value}', description='{param_name}')\n"
            else:
                code += f"\n# Widget configuration not supported: {param_config}\n"
                code += f"{param_name} = '{param_value}'  # No widget configuration\n\n"

    return code



# test

TEXT = """
# @title String fields
text              = 'value'       #@param {type:"string"}
dropdown          = '1st option'  #@param ["1st option", "2nd option", "3rd option"]
text_and_dropdown = 'value'       #@param ["1st option", "2nd option", "3rd option"] {allow-input: true}
"""

WIDGET_CODE = convert_to_widget_code(TEXT)

print(WIDGET_CODE)
