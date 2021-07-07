import aiosqlite, asyncio
import itertools
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE = "questions.db"


@app.post("/question")
async def route_questions():

    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        resp = []
        for number, question in enumerate(request.json):
            this_resp = {
                "Number": number + 1,
                "Answer": None,
            }
            print(f"Question number {question['Number']}: ")
            print(f"Question: {question['Content']}")
            answer_fromdb = await db.execute(
                "SELECT QuestionAnswer FROM Questions WHERE QuestionContent=:q_content",
                {"q_content": question["Content"]},
            )
            row = await answer_fromdb.fetchone()
            for option in question["Options"]:
                # show all options and answers
                # print(
                #     f"Option {option['OptionKey']}: {option['OptionContent']}", end=" "
                # )
                if option["OptionContent"] == row[0]:
                    print(
                        f"Ans : Option {option['OptionKey']}: {option['OptionContent']}"
                    )
                    # print("Correct Answer")
                    this_resp["Answer"] = option["OptionKey"]

            resp.append(this_resp)

        return json.dumps(resp)
        # return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True)
