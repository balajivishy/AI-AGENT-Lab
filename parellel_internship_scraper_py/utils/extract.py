def extract_features(job):

    text = job["title"].lower()

    skills = []
    category = "unknown"

    # 🔹 Skill detection
    if "python" in text:
        skills.append("Python")
    if "sql" in text:
        skills.append("SQL")
    if "machine learning" in text or "ml" in text:
        skills.append("Machine Learning")
    if "excel" in text:
        skills.append("Excel")
    if "java" in text:
        skills.append("Java")
    if "c++" in text:
        skills.append("C++")
    if "react" in text:
        skills.append("React")
    if "node" in text:
        skills.append("Node")

    # 🔹 Category detection
    if "data" in text or "ml" in text:
        category = "Data/ML"
    elif "backend" in text:
        category = "Backend"
    elif "frontend" in text:
        category = "Frontend"

    return {
        "skills": skills,
        "category": category
    }