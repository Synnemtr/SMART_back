# SMART 2024 (backend)

![Insalogo](Images/logo-insa_0.png)

Students: Alexis Bruneau, Axel Maillot, Synne Moe Trettenes

### Abstract
This is the backend for the SMART-project at INSA Lyon there the objective is to create game-elements for different HEXAD-player types as well as an algorithm that is going to introduce game-elements to a user based on their main HEXAD-12 type as well as their motivation-score using the SDI.

## Description 
This is the app from the project __Adaptive and Privacy-Aware Persuasive Strategy for behavior change (APAPS)__ team DRIM, funded by [LIRIS laboratory](https://liris.cnrs.fr/), [INSA Lyon](https://www.insa-lyon.fr/) and partner [University of Passau](https://www.uni-passau.de/en/).

[Link to frontend](https://github.com/Synnemtr/SMART_front/blob/main/)

## Project Goal
The main aim of this project is to develop another branch of the already ongoing app-development of the APAPS-project. For this sub-branch, the team will focus on the gamification aspect of the APAPS-project. How should the game-elements be created and stored? In which way should users (with their player-type), game-elements and algorithm be connected? This will include creating user HEXAD-12 types as well as give users motivation scores based in the SDI (Ryan and Deci 2000) and HEXAD-12 (Krath et al. 2023) theory. The main objective of this project will be to create and implement an algorithm to choose the correct game element for the specific user based in HEXAD-12 player type. This algorithm should also be able to evolve over time, as the user’s motivation might change, or the HEXAD-12 type can become a different one, while the user uses the app. In order to create this algorithm, there also has to be created several game-elements for the different existing HEXAD-types; socialises, free spirits, achievers, philanthropists, players, and disruptors Krath et al. 2023. Data collected by Felix B  ̈OLZ (PhD at the University of Passau) mostly through a seminar called ”Data collection and processing on sustainable and healthy food” can also be used to test the implementation of the algorithm on different users. This seminar is part of the course catalogue of the Faculty of Computer Science and Mathematics of Passau1. The data has been gathered online using a web application. The  goal is to create an algorithm/ a recommender system that determined what game element to introduce to a user based on collaborative filtering with user-user similatiry. The purpose of the System: The recommender system is designed to suggest game elements to users based on their interests and similarities with other users. It uses collaborative filtering to find users with similar preferences and suggest items accordingly.Ratings are given explicit and is provided by users on a scale (e.g., 1 to 5 stars). How do you determine which users are similar to one another? 
Cosine Similarity: Cosine similarity is a measure of similarity between two vectors. It is calculated as the cosine of the angle between them. For two users, the similarity is calculated based on their ratings for common items. Similarity Matrix: A matrix where the rows and columns represent user IDs, and the values are the cosine similarity between users. Sorting Recommendations: Sort recommendations by predicted rating in descending order to recommend the most fitting element. Fallback for New Users: If the user has no ratings, generate random recommendations based on their HEXAD-12 type.

## Requirements
Python 3.6 or higher \
Django 2.2 or higher \
Django Rest Framework 3.11 or higher \
PostgreSQL 12.2 or higher
Docker

### Installation
1. Clone the repository
2. Install the requirements
3. Run the server
4. Go to http://localhost:8000/doc/ to see the documentation
5. Enjoy!

### Launch the application for the first time with Docker
1. Run ```docker compose up``` at the root of the repository.
2. You should have 2 Docker containers running: sustain-dev-db (Postgres container) and sustain-dev-api (API container).
3. Then, open a new command prompt and execute ```docker exec -it sustain-dev-api sh``` to acces to a Shell for the API container.
4. Within this Shell, execute the two following commands:
    ```python3 manage.py migrate``` (for M1 chips on mac)

    ```python manage.py migrate```

    ```python manage.py createsuperuser``` -> you will prompted a username and password to create a super user for the application.
5. The backend should now work properly.

## Material
This is the material for the HEXAD-12 types, and how we determine which user gets which player-type.
### How to answer the questions
Each score is from 1 to 7
- 1: Strongly disagree
- 2: Disagree
- 3: Somewhat disagree
- 4: Neutral
- 5: Somewhat agree
- 6: Agree
- 7: Strongly agree
#### Hexad Question
__Philanthropist__ \
Q1. Rewards are a great way to motivate me \
Q2. It is important to me to follow my own path \
__Socializer__ \
Q3. It makes me happy if I am able to help others \
Q4. I dislike following rules \
__Free Spirit__ \
Q5. I see myself as a rebel \
Q6. I like to be in control of my own destiny \
__Achiever__ \
Q7. I like mastering difficult tasks \
Q8. I enjoy emerging victorious out of difficult circumstances \
__Disruptor__ \
Q9. The well-being of others is important to me \
Q10. I enjoy group activities \
__Player__ \
Q11. Being independent is important to me \
Q12. I like being part of a team

- POST request to `api/v1/gamification-profiles/questions/` with body:
```json
{
    "data": [
        {"question_id": 1, "score": 5},
        {"question_id": 2, "score": 5},
        {"question_id": 3, "score": 5},
        {"question_id": 4, "score": 5},
        {"question_id": 5, "score": 5},
        {"question_id": 6, "score": 6},
        {"question_id": 7, "score": 5},
        {"question_id": 8, "score": 5},
        {"question_id": 9, "score": 5},
        {"question_id": 10, "score": 5},
        {"question_id": 11, "score": 5},
        {"question_id": 12, "score": 5}
    ]
}
```

- GET request to `api/v1/gamification-profiles/profiles/?profile_id=1` with parameter `profile_id`. The sample result is:
```json
[
    {
        "name": "Philanthropist",
        "description": "Philanthropists are people who engage in philanthropy; that is, they donate their time, money, and/or reputation to charitable causes. Philanthropy is a combination of two Greek words, philos, meaning love, and anthropos, meaning human beings, thus philanthropy is giving love for humanity.",
        "score": 10
    },
    {
        "name": "Socializer",
        "description": "Socializers are people who engage in socialization; that is, they interact with other people. Socialization is a combination of two Greek words, social, meaning companionship, and ization, meaning the process of making. Thus, socialization is the process of making companionship.",
        "score": 10
    },
    {
        "name": "Free Spirit",
        "description": "Free Spirits are people who engage in free spirit; that is, they are free from society. Free spirit is a combination of two Greek words, free, meaning freedom, and spirit, meaning soul, thus free spirit is the freedom of the soul.",
        "score": 10
    },
    {
        "name": "Achiever",
        "description": "Achievers are people who engage in achievement; that is, they accomplish goals. Achievement is a combination of two Greek words, achieve, meaning to accomplish, and ment, meaning the result of, thus achievement is the result of accomplishing.",
        "score": 10
    },
    {
        "name": "Disruptor",
        "description": "Disruptors are people who engage in disruption; that is, they interrupt the normal course. Disruption is a combination of two Greek words, dis, meaning not, and rupt, meaning break, thus disruption is the act of not breaking.",
        "score": 10
    },
    {
        "name": "Player",
        "description": "Players are people who engage in play; that is, they have fun. Play is a combination of two Greek words, ple, meaning pleasure, and ay, meaning the act of, thus play is the act of pleasure.",
        "score": 10
    }
]
```
