import csv

def read_tsv_to_array(file_path):
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        for row in tsv_reader:
            data.append(row)
    return data

workshops_path = 'VLDB 2024 Workshops - List of Workshops.tsv'
papers_path = 'VLDB 2024 Workshops - All.tsv'

workshops = read_tsv_to_array(workshops_path)
papers = read_tsv_to_array(papers_path)

print("#+OPTIONS: toc:nil num:nil")
print("#+SETUPFILE: https://fniessen.github.io/org-html-themes/org/theme-bigblow.setup")

print("* VLDBW 2024")
print("** Joint Proceedings of Workshops at the 50th International Conference on Very Large Data Bases (VLDB), Guangzhou, China, 2024")
print("** VLDB 2024 Workshop Chairs")
print("*** Themis Palpanas, Philippe Bonnet")
print("** VLDB 2024 Workshop Proceeding Chair")
print("*** Haixun Wang")
print("** Accepted Workshops")
for workshop in workshops[1:]:
    print(f"*** {workshop[1]}: {workshop[0]}")
    print(f"- Workshop Chairs: {workshop[2]}")
          
for workshop in workshops[1:]:
    print("* " + workshop[1])
    print("** " + workshop[0])
    for paper in papers:
        if paper[0] == workshop[1]:
            filename = "./VLDB-Workshop-2024/" + workshop[1] + "/" + paper[4]
            print(f"*** [[{filename}][{paper[1]}]]")
            print(f"    {paper[3]}")
    print("\n")
