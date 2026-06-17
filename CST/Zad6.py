from constraint import *

if __name__ == '__main__':
    num = int(input())

    papers = dict()

    paper_info = input()
    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        paper_info = input()

    # Define the variables
    ...
    # variabli ke bidat site papers od 1 do 10
    # Gi zemame od dict sto se pravi pri imput
    variables = list(papers.keys())

    domain = [f'T{i + 1}' for i in range(num)]

    problem = Problem(BacktrackingSolver())

    # Change this section if necessary
    problem.addVariables(variables, domain)

    # Add the constraints

    # Vo sekoj termina mozhe max 4 trudovi
    # Користиме *slots - tuple за да ги фатиме сите вредности што солверот моментално ги тестира.
    def max_4(*slots):
        # slots ќе изгледа нешто како: ('T1', 'T1', 'T2', 'T1', 'T3'...)
        # Проверуваме дали некој термин се појавува повеќе од 4 пати
        for slot in domain:
            if slots.count(slot) > 4:
                return False
        return True

    # Deka za sekoja variabla imash niza od slots sto momentalno solverot gi  testira
    problem.addConstraint(max_4, variables)

    # 2. Primer ako imme <=4 Paper ML trudovi - togash tie treba da se vo ist termin Tn
    # PRVO mora da se grupiraat vo dictary site so ist trud
    topic_to_papers = {}  #Da napravime od Paper1 : mlp vo -> {MLP: Paper1 Paper 2}
    for paper, topic in papers.items():
        if topic not in topic_to_papers:
            topic_to_papers[topic] = []
        topic_to_papers[topic].append(paper)

    for topic, topic_papers in topic_to_papers.items():
        if len(topic_papers) <= 4:
            # Ова кажува: "Сите трудови во оваа листа мора да добијат иста вредност (ист термин)"
            problem.addConstraint(AllEqualConstraint(), topic_papers)


    result = problem.getSolution()

    # Add the required print section
    # Mora da se sortiraat spored redosled
    sorted_papers = sorted(result.keys(), key=lambda x: int(x.replace('Paper', '')))

    for paper in sorted_papers:
        topic = papers[paper]
        slot = result[paper]
        print(f"{paper} ({topic}): {slot}")