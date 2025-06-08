import json
import random

from flask import Flask, render_template, request

app = Flask(__name__)

with open("tarot_cards_template_fixed.json", "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

def get_shuffled_deck():
    deck = []
    for name in tarot_cards:
        deck.append((name, "正位"))
        deck.append((name, "逆位"))
    random.shuffle(deck)
    return deck

def format_keywords(keywords):
    if not keywords:
        return "（這張牌沒有提供關鍵詞）"
    if len(keywords) == 1:
        return f"這張牌的關鍵在於：{keywords[0]} —— 它提醒你要留意這個面向。"
    elif len(keywords) == 2:
        return (
    f"這張牌的關鍵在於：{keywords[0]} 和 {keywords[1]} "
    f"—— 你可能正被這兩者牽動。"
        )
    elif len(keywords) == 3:
        return (
            f"這張牌的關鍵在於：{keywords[0]}、{keywords[1]}、{keywords[2]} "
            f"—— 它們共同描繪出你當下的核心議題。"
        )
    else:
        return (
        f"這張牌涵蓋了多個面向，例如：{'、'.join(keywords[:4])}……"
        f"這些都是你目前應該留意的重點。"
        )

def get_summary(spread_name):
    return {
        "單張牌": "這是一張牌的簡潔指引，" \
           "它能幫助你聚焦當下的問題核心，" \
           "提供一個明確的反思方向。",
        "三張牌": "這三張牌描繪了你過去、現在與未來的變化脈絡，" \
           "從中可以看出事情的演變方向與你可能的選擇。",
        "十字牌陣": "十字牌陣從現況、障礙、內在動力與過去經驗出發，" \
           "幫助你整體理解當下的處境與可行的結論。",
        "關係牌陣": "關係牌陣讓你更了解自己與對方的角色，"
        "以及你們之間的相處本質與潛藏問題，"
        "提供改善關係的建議。",
        "事業發展牌陣": "這個牌陣涵蓋了現況、挑戰、機會、方向與支援，\
協助你在職涯發展中做出有遠見的判斷與行動。"
    }.get(spread_name, "這個牌陣的訊息結構清晰，請依據各張牌的提示綜合評估。")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic is None:
            topic = ""
        spread_key = request.form.get("spread")
        question = request.form.get("question")

        spread_map = {
            "1": ("單張牌", 1),
            "2": ("三張牌", 3),
            "3": ("十字牌陣", 5),
            "4": ("關係牌陣", 5),
            "5": ("事業發展牌陣", 6)
        }
        spread_name, spread_count = spread_map.get(str(spread_key), ("單張牌", 1))
        deck = get_shuffled_deck()
        drawn = deck[:spread_count]

        results = []
        for card_name, position in drawn:
            data = tarot_cards[card_name][position]
            topic_key = topic + "意義"
            results.append({
                "name": card_name,
                "position": position,
                "meaning": data["整體意義"],
                "topic_meaning": data.get(topic_key, "（該主題無解釋）"),
                "keywords": format_keywords(data["關鍵詞"])
            })
        return render_template("result.html", question=question, topic=topic,
                               spread_name=spread_name, results=results,
                               summary=get_summary(spread_name))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
