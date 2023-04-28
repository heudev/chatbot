import json, random

def jaccard_similarity(word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def get_sensitivity():
    with open('config.json', 'r') as file:
        data = json.load(file)
        sensitivity = data['sensitivity']
        return sensitivity 

def chatbot(keyword_entered):
    response = {"similarity_ratio": 0, "keyword": None, "answers": None}
    with open("conversation.json", "r+",encoding="UTF-8") as f:
        conversations = json.load(f)
        for conversation in conversations:
            for keyword in conversation["keywords"]:
                similarity_ratio = jaccard_similarity(str(keyword_entered).lower().strip(), str(keyword).lower().strip())
                if similarity_ratio >= get_sensitivity() and similarity_ratio > response["similarity_ratio"]:
                    response["similarity_ratio"] = similarity_ratio
                    response["keyword"] = keyword
                    response["answers"] = conversation["answers"]
    if response["answers"]:
        response["answers"] = random.choice(response["answers"])
        return response["answers"]

