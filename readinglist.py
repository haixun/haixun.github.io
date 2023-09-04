import json

with open('readinglist.json', 'r') as file:
    data = json.load(file)

with open('readinglist.markdown', 'w') as publicReadingList, open('myreadinglist.markdown', 'w') as personalReadingList:
    publicReadingList.write(f"# Reading List\n\n")
    personalReadingList.write(f"# Reading List\n\n")

    for week, articles in data.items():
        publicReadingList.write(f"### Week of {week}\n\n")
        personalReadingList.write(f"### Week of {week}\n\n")
        for article in articles:
            publicReadingList.write(f"* [{article['title']}]({article['url']}), {article['source']}\n")
            personalReadingList.write(f"* [{article['title']}]({article['url']}) [[local]({article['local']})], {article['source']}\n")
        publicReadingList.write(f"\n")
        personalReadingList.write(f"\n")
