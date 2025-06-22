import re
from collections import Counter

def estrai_frequenza_attributi(path_file):
  

    with open(path_file, "r", encoding="utf-8") as f:
        log_text = f.read()
    

    where_clauses = re.findall(
        r"WHERE\s+(.*?)\s+GROUP BY", log_text, flags=re.IGNORECASE | re.DOTALL
    )
    
    attribute_counter = Counter()
  
    sql_keywords = {"BETWEEN", "AND", "OR", "NOT", "ELSE", "END", "CASE", "AS"}

    for clause in where_clauses:
      
        conditions = re.split(r"\s+AND\s+", clause, flags=re.IGNORECASE)
        for cond in conditions:
        
            tokens = re.findall(r"\b[A-Z_]+\b", cond)
            for token in tokens:
               
                if token.upper() not in sql_keywords and not token.isdigit():
                    attribute_counter[token] += 1
    
    return attribute_counter

if __name__ == "__main__":

    percorso_log = "queries.txt"
    
    frequenze = estrai_frequenza_attributi(percorso_log)
    print("Frequenza degli attributi nelle clausole WHERE:")
    for attr, freq in frequenze.most_common():
        print(f"{attr}: {freq}")
