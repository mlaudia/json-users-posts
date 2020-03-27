import json
from math import sqrt
from urllib.request import urlopen
import pandas as pd

# liczy liczbę postów napisanych przez użytkowników
# zwraca listę stringów postaci "{username} napisal(a) {count} postow"
def count_posts(df):
    counts = df['username'].value_counts()
    strings = []

    for username, count in counts.items():
        strings.append(f"{username} napisal(a) {count} postow")

    return strings

# Szuka duplikatów wśród tytułów postów
# Zwraca listę tytułów powtarzających się
def find_duplicates(df):
    duplicates = df[df.duplicated(['title'])]
    duplicate_list = duplicates['title'].values.tolist()
    return list(dict.fromkeys(duplicate_list))

# Dla wszystkich użytkowników o kolejnych userId znajduje innego, który jest jego najbliższym sąsiadem
# Zwraca DataFrame o kolumnach: user_id, neighbour_id, distance
def find_neighbours(df_users):
    lngs = df_users.address.apply(lambda x: x.get('geo').get('lng'))
    lats = df_users.address.apply(lambda x: x.get('geo').get('lat'))
    coords = pd.concat([lngs, lats], axis=1, keys=['long', 'lat'])
    distances = pd.DataFrame({"user_id":[], "neighbour_id":[], "distance":[]})

    for user_id in range(1, len(df_users.index)):
        long1 = float(lngs[user_id])
        lat1 = float(lats[user_id])
        dist = 1000000
        neighbour = 0
        for index, row in coords.iterrows():
            if index != user_id:
                temp = distance(long1, float(row['long']), lat1, float(row['lat']))
                if temp < dist:
                    dist = round(temp, 3)
                    neighbour = index

        distances = distances.append({"user_id":user_id, "neighbour_id":neighbour, "distance":dist}, ignore_index=True)

    return distances

#oblicza dystans pomiędzy dwoma punktami o danych współrzędnych
def distance(long1, long2, lat1, lat2):
    return sqrt((long2 - long1) ** 2 + (lat2 - lat1) ** 2)


posts_url = 'https://jsonplaceholder.typicode.com/posts'
users_url = 'https://jsonplaceholder.typicode.com/users'

posts = json.loads(urlopen(posts_url).read())
users = json.loads(urlopen(users_url).read())

df_posts = pd.DataFrame(posts).set_index('userId')
df_users = pd.DataFrame(users).set_index('id')
df = df_posts.merge(df_users, left_index=True, right_index=True)

print(count_posts(df))
print(find_duplicates(df))
print(find_neighbours(df_users))