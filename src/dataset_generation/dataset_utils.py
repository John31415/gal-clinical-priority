from collections import defaultdict
import csv
import json
from src.utils.load_json import load_json

disease_mapping = defaultdict(set)
drug_mapping = defaultdict(set)
with open("dataset/disease2drug.csv", mode="r", encoding="utf8") as file:
    for row in csv.DictReader(file):
        disease = row["disease"].strip()
        raw_drug = row["drug"]
        drugs = [d.strip() for d in raw_drug.split("/")]
        for drug in drugs:
            disease_mapping[disease].add(drug)
            drug_mapping[drug].add(disease)


def drug2disease():
    result = [
        {"drug": drug, "disease": sorted(list(diseases))}
        for drug, diseases in drug_mapping.items()
    ]
    result.sort(key=lambda x: len(x["disease"]), reverse=True)
    with open("dataset/drug2disease.json", mode="w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)


# drug2disease()

with open("dataset/drug2disease.json", "r", encoding="utf-8") as f:
    drug2disease_data = json.load(f)


def get_top_diseases(top_n: int = 10) -> list[str]:
    top_diseases = list(
        set(
            [
                disease
                for item in drug2disease_data[:top_n]
                for disease in item["disease"]
            ]
        )
    )
    return top_diseases


def disease2drug(disease: str, top_n: int = 5) -> list[str]:
    drugs = list(disease_mapping[disease])
    drugs.sort(key=lambda x: len(drug_mapping[x]), reverse=True)
    return drugs[:top_n]


def text_json_to_dict(text: str) -> dict:
    return json.loads(text)


def text2json(dict: dict, path: str) -> None:
    data = load_json(path=path)
    data.append(dict)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
