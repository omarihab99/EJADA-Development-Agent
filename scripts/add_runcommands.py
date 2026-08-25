import os
import glob
import re

agent_files = glob.glob('.github/agents/*.agent.md') + glob.glob('non-dev-agents/*.agent.md')

for f in agent_files:
    with open(f, 'r', encoding='utf-8') as file:
        original_content = file.read()
    
    if 'tools:' not in original_content:
        # If there's no tools: block, add it after description or name.
        continue

    # Simple logic: if runCommands is already there, skip
    if 'runCommands' in original_content:
        continue

    # Find the tools: line and insert 'runCommands' into it.
    # It might be `tools: ['x', 'y']` or `tools: ["x", "y"]`
    match = re.search(r'tools:\s*\[(.*?)\]', original_content)
    if match:
        existing_tools = match.group(1)
        if existing_tools.strip():
            new_tools = f'tools: [{existing_tools}, "runCommands"]'
        else:
            new_tools = 'tools: ["runCommands"]'
        
        new_content = original_content.replace(match.group(0), new_tools)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
    else:
        # Maybe it's a multiline yaml list?
        lines = original_content.splitlines()
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith('tools:'):
                # Is it immediately followed by a list? or empty bracket?
                if '[' in line and ']' in line:
                    # Inline empty likely `tools: []` handled above, but just in case
                    new_line = line.replace(']', ', "runCommands"]')
                    new_line = new_line.replace('[,', '[')
                    new_lines[-1] = new_line
                elif len(lines) > i+1 and lines[i+1].strip().startswith('-'):
                    # Multi line
                    new_lines.append('  - "runCommands"')
                else: 
                     new_lines[-1] = line + ' ["runCommands"]'
                     
        with open(f, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_lines) + '\n')

print("Update complete.")
