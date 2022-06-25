import pandas as pd
from elasticsearch_dsl import Search, connections
from elasticsearch import Elasticsearch


class Data:
    def __init__(self, data_path):
        self.data_path = data_path
        self.dataset = pd.read_csv(self.data_path)
        self.es = Elasticsearch(hosts=["localhost:9200"])

    def getSpecificHotelReviews(self, hotel_name):
        hotels = self.dataset[(self.dataset["Categories"] == 'Hotels')]
        specific_hotel = hotels[(hotels["Name"] == hotel_name)]
        reviews = specific_hotel['ReviewsText']
        return reviews

    def getUniqueHotelNames(self):
        hotels = self.dataset[(self.dataset["Categories"] == 'Hotels')]
        hotel_names = hotels["Name"].unique().tolist()
        return hotel_names

    def preprocessData(self):
        self.dataset = self.dataset.rename(index=str, columns={'reviews.date': 'ReviewsDate',
                                                               'reviews.dateAdded': 'ReviewsDateAdded',
                                                               'reviews.doRecommend': 'ReviewsRecommend',
                                                               'reviews.id': 'ReviewsId',
                                                               'reviews.rating': 'ReviewsRating',
                                                               'reviews.text': 'ReviewsText',
                                                               'reviews.title': 'ReviewsTitle',
                                                               'reviews.userCity': 'ReviewsUserCity',
                                                               'reviews.username': 'ReviewsUsername',
                                                               'reviews.userProvince': 'ReviewsUserProvince',
                                                               'categories': 'Categories',
                                                               'name': 'Name'})

        self.dataset.drop(['ReviewsUserProvince', 'ReviewsRecommend', 'ReviewsUserCity', 'ReviewsId'], axis=1,
                          inplace=True)
        self.dataset.dropna()

    def indexDataToElastic(self):
        self.es.indices.create(index='hotels_docs', ignore=400)
        processed_data = self.dataset.dropna()
        hotels = processed_data[processed_data["Categories"] == 'Hotels']
        unique_hotels = hotels['Name'].unique().tolist()
        doc_id = 1
        for hotel_name in unique_hotels:
            specific_hotel = hotels[hotels['Name'] == hotel_name]
            address = specific_hotel['address'].unique()[0]
            category = specific_hotel['Categories'].unique()[0]
            city = specific_hotel['city'].unique()[0]
            province = specific_hotel['province'].unique()[0]
            latitude = str(specific_hotel['latitude'].unique()[0])
            longitude = str(specific_hotel['longitude'].unique()[0])
            postal_code = str(specific_hotel['postalCode'].unique()[0])

            reviews_info = specific_hotel[
                ['ReviewsUsername', 'ReviewsDate', 'ReviewsDateAdded', 'ReviewsText', 'ReviewsRating']].applymap(
                str)

            review_date = pd.to_datetime(reviews_info['ReviewsDate']).tolist()
            review_date_added = pd.to_datetime(reviews_info['ReviewsDateAdded']).tolist()
            review_rate = reviews_info['ReviewsRating'].tolist()
            reviews_username = reviews_info['ReviewsUsername'].tolist()
            reviews_text = reviews_info['ReviewsText'].tolist()

            hotel = {
                'hotel name': hotel_name,
                'address': address,
                'city': city,
                'province': province,
                'category': category,
                'postal_code': postal_code,
                'latitude': latitude,
                'longitude': longitude,
                'review_info':
                    {
                        "reviews_username": reviews_username,
                        "review_rate": review_rate,
                        "reviews_text": reviews_text,
                        "review_date": review_date,
                        "review_date_added": review_date_added

                    }

            }

            self.es.index(index="hotels_docs", id=str(doc_id), document=hotel)
            doc_id += 1

    def getHotelById(self, doc_id):
        hotel_doc = self.es.get(index="hotels_docs", id=doc_id)
        return hotel_doc

    def getAllHotelsDoc(self):
        hotels_docs = self.es.search(
            index="hotels_docs",
            body={
                "query": {
                    "match_all": {}
                }
            }
        )
        return hotels_docs

    def getHotelByName(self, name):
        hotel_doc = self.es.search(
            index="hotels_docs",
            body={
                "query": {
                    "match": {
                        'hotel name': name
                    }
                }
            }
        )
        return hotel_doc
