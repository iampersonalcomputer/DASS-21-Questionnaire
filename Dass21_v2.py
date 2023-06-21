# 1 Declare database
import sqlite3

def administer_questionnaire():
    questions = [
        ("Stress", "Saya dapati diri saya sukar ditenteramkan.\n"), #1
        ("Anxiety", "Saya sedar mulut saya terasa kering.\n"), #2
        ("Depression", "Saya tidak dapat mengalami perasaan positif sama sekali.\n"), #3
        ("Anxiety", "Saya mengalami kesukaran bernafas (contohnya pernafasan yang laju, tercungap-cungap walaupun tidak melakukan senaman fizikal).\n"), #4
        ("Depression", "Saya sukar untuk mendapatkan semangat bagi melakukan sesuatu perkara.\n"), #5
        ("Stress", "Saya cenderung untuk bertindak keterlaluan dalam sesuatu keadaan.\n"), #6
        ("Anxiety", "Saya rasa menggeletar (contohnya pada tangan).\n"), #7
        ("Stress", "Saya rasa saya menggunakan banyak tenaga dalam keadaan cemas.\n"), #8
        ("Anxiety", "Saya bimbang keadaan di mana saya mungkin menjadi panik dan melakukan perkara yang membodohkan diri.\n"), #9
        ("Depression", "Saya rasa saya tidak mempunyai apa-apa untuk diharapkan.\n"), #10
        ("Stress", "Saya dapati diri saya semakin gelisah.\n"), #11
        ("Stress", "Saya rasa sukar untuk relaks.\n"), #12
        ("Depression", "Saya rasa sedih dan murung.\n"), #13
        ("Stress", "Saya tidak dapat menahan sabar dengan perkara yang menghalang saya meneruskan apa yang saya lakukan.\n"), #14
        ("Anxiety", "Saya rasa hampir-hampir menjadi panik/cemas.\n"), #15
        ("Depression", "Saya tidak bersemangat dengan apa jua yang saya lakukan.\n"), #16
        ("Depression", "Saya rasa tidak begitu berharga sebagai seorang individu.\n"), #17
        ("Stress", "Saya rasa saya mudah tersentuh.\n"), #18
        ("Anxiety", "Saya sedar tindakbalas jantung saya walaupun tidak melakukan aktiviti fizikal (contohnya kadar denyutan jantung bertambah, atau denyutan jantung berkurangan).\n"), #19
        ("Anxiety", "Saya berasa takut tanpa sebab yang munasabah.\n"), #20
        ("Depression", "Saya rasa hidup ini tidak bermakna.\n") #21
    ]

    responses = [[], [], []]

    print("\nSila baca setiap kenyataan di bawah dan kadarkan jawapan anda bagi menggambarkan keadaan anda sepanjang minggu yang lalu.\n"
          "Tiada jawapan yang betul atau salah. Jangan mengambil masa yang terlalu lama untuk menjawab mana-mana kenyataan.\n"
          "\nSkala kadar adalah seperti berikut:\n"
          "      0 = Tidak langsung menggambarkan keadaan saya.\n"
          "      1 = Sedikit atau jarang-jarang menggambarkan keadaan saya.\n"
          "      2 = Banyak atau kerapkali menggambarkan keadaan saya.\n"
          "      3 = Sangat banyak atau sangat kerap menggambarkan keadaan saya.\n")

    for i, (category, question) in enumerate(questions):
        response = input(f"{i+1}. {question} ")

        while not response.isdigit() or int(response) not in range(4):
            print("Jawapan tidak sah. Sila masukkan nombor antara 0 dan 3 sahaja. Terima kasih.")
            response = input(f"{i+1}. {question} ")

        for j in range(3):
            if category.lower() == ["depression", "anxiety", "stress"][j]:
                responses[j].append(int(response))

    return responses

def calculate_scores(responses):
    scores = []

    for i in range(3):
        score = sum(responses[i][j] for j in range(len(responses[i])))
        scores.append(score)

    return scores

def interpret_scores(scores):
    categories = ["Depression", "Anxiety", "Stress"]

    severity_ranges = {
        "Depression": [
            (0, 4, "Normal"),
            (5, 6, "Mild"),
            (7, 10, "Moderate"),
            (11, 13, "Severe"),
            (14, 21, "Extremely Severe")
        ],
        "Anxiety": [
            (0, 3, "Normal"),
            (4, 5, "Mild"),
            (6, 7, "Moderate"),
            (8, 9, "Severe"),
            (10, 21, "Extremely Severe")
        ],
        "Stress": [
            (0, 7, "Normal"),
            (8, 9, "Mild"),
            (10, 12, "Moderate"),
            (13, 16, "Severe"),
            (17, 21, "Extremely Severe")
        ]
    }

    for i in range(3):
        category = categories[i]
        score = scores[i]

        severity = ""
        for lower, upper, range_name in severity_ranges[category]:
            if lower <= score <= upper:
                severity = range_name
                break

        print(f"\n{category} score: {score} ({severity})")

def save_responses_to_database(name, id, responses, scores):
    conn = sqlite3.connect('questionnaire.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (name TEXT, id TEXT, depression_score INTEGER, anxiety_score INTEGER, stress_score INTEGER)''')

    c.execute("INSERT INTO responses VALUES (?, ?, ?, ?, ?)",
              (name, id, scores[0], scores[1], scores[2]))

    conn.commit()
    conn.close()

def main():
    print("\nDASS-21 Questionnaire")

    Name = input("\nSila masukkan nama penuh anda: ")
    ID_number = input("Sila masukkan No. Kad Pengenalan anda: ")

    while True:
        responses = administer_questionnaire()
        scores = calculate_scores(responses)
        interpret_scores(scores)

        save_responses_to_database(Name, ID_number, responses, scores)

        retake = input("\nAdakah anda mahu menjawab questionnaire ini semula? (Y/N):\n")
        if retake.lower() != "y":
            print("\nTerima kasih kerana menjawab soal selidik kami!")
            print("Program dihentikan.")
            break

if __name__ == "__main__":
    main()
