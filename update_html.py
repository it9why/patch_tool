import re

with open('index.html', 'r') as f:
    content = f.read()

# Current string for the type and dependency form-groups (with nested div)
current_type_dep = '''                    <div class="form-group">
                    <div class="form-group">
                        <label for="activityType">Type</label>
                        <input type="text" id="activityType" list="typeOptions" placeholder="e.g., Development">
                        <datalist id="typeOptions">
                            <option value="Development">
                            <option value="Design">
                            <option value="Meeting">
                            <option value="Testing">
                            <option value="Documentation">
                            <option value="Other">
                        </datalist>
                    </div>
                        <label for="dependency">Dependency (Optional)</label>
                        <select id="dependencies">
                            <option value="">None</option>
                        </select>
                    </div>'''

new_type_dep = '''                    <div class="form-group">
                        <label for="activityType">Type</label>
                        <input type="text" id="activityType" list="typeOptions" placeholder="e.g., Development">
                        <datalist id="typeOptions">
                            <option value="Development">
                            <option value="Design">
                            <option value="Meeting">
                            <option value="Testing">
                            <option value="Documentation">
                            <option value="Other">
                        </datalist>
                    </div>
                    <div class="form-group">
                        <label for="dependency">Dependency (Optional)</label>
                        <select id="dependencies">
                            <option value="">None</option>
                        </select>
                    </div>'''

# Replace the nested structure with two separate form-groups
content = content.replace(current_type_dep, new_type_dep)

# Now, the dependency form-group and add button form-group
current_dep_add = '''                    <div class="form-group">
                        <label for="dependency">Dependency (Optional)</label>
                        <select id="dependencies">
                            <option value="">None</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="addActivity">&nbsp;</label>
                        <button id="addActivity" class="btn-primary" type="button"><i class="fas fa-plus"></i> Add Activity</button>
                    </div>'''

new_dep_add = '''                    <div class="form-group">
                        <label for="dependency">Dependency (Optional)</label>
                        <select id="dependencies">
                            <option value="">None</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="allowNonWorkingDays">Allow on non‑working days</label>
                        <select id="allowNonWorkingDays">
                            <option value="false">No (default)</option>
                            <option value="true">Yes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="addActivity">&nbsp;</label>
                        <button id="addActivity" class="btn-primary" type="button"><i class="fas fa-plus"></i> Add Activity</button>
                    </div>'''

content = content.replace(current_dep_add, new_dep_add)

with open('index.html', 'w') as f:
    f.write(content)

print("Updated index.html")
