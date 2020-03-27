import unittest
import users
import pandas as pd

#Testy uzywaja skroconych danych z podanego pliku
class TestUsers(unittest.TestCase):
    example_users = [
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  },
  {
    "id": 2,
    "name": "Ervin Howell",
    "username": "Antonette",
    "email": "Shanna@melissa.tv",
    "address": {
      "street": "Victor Plains",
      "suite": "Suite 879",
      "city": "Wisokyburgh",
      "zipcode": "90566-7771",
      "geo": {
        "lat": "-43.9509",
        "lng": "-34.4618"
      }
    },
    "phone": "010-692-6593 x09125",
    "website": "anastasia.net",
    "company": {
      "name": "Deckow-Crist",
      "catchPhrase": "Proactive didactic contingency",
      "bs": "synergize scalable supply-chains"
    }
  }]

    example_posts = [
        {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
        },
        {
            "userId": 2,
            "id": 15,
            "title": "eveniet quod temporibus",
            "body": "reprehenderit quos placeat\nvelit minima officia dolores impedit repudiandae molestiae nam\nvoluptas recusandae quis delectus\nofficiis harum fugiat vitae"
        }
    ]

    df_posts = pd.DataFrame(example_posts).set_index('userId')
    df_users = pd.DataFrame(example_users).set_index('id')
    df = df_posts.merge(df_users, left_index=True, right_index=True)

    def testCount(self):
        counts = users.count_posts(self.df)
        self.assertTrue(('Bret napisal(a) 1 postow' in counts) & ('Antonette napisal(a) 1 postow' in counts))

    def testDuplicates(self):
        self.assertEqual(users.find_duplicates(self.df), [])

    def testDistances(self):
        df = users.find_neighbours(self.df_users)
        self.assertTrue(((df['user_id'] == 1.0) & (df['neighbour_id'] == 2.0) & (df['distance'] == 115.802)).any())


if __name__ == '__main__':
    unittest.main()